"""
Simplified AI Trading Engine for Enhanced Saudi Stock Market App
User-friendly AI features with easy integration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

# Try to import ML libraries, gracefully handle if not available
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

@dataclass
class AISignal:
    """AI Trading Signal"""
    symbol: str
    company_name: str
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float  # 0.0 to 1.0
    predicted_price: float
    current_price: float
    expected_return: float  # Percentage
    risk_level: str  # 'LOW', 'MEDIUM', 'HIGH'
    reasoning: str
    timestamp: datetime

class SimpleAIEngine:
    """Simplified AI Engine for Trading Signals"""
    
    def __init__(self):
        self.signals_cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def generate_signals(self, symbols: List[str], stocks_db: Dict) -> List[AISignal]:
        """Generate AI trading signals for given symbols"""
        signals = []
        
        for symbol in symbols:
            try:
                signal = self._generate_single_signal(symbol, stocks_db)
                if signal:
                    signals.append(signal)
            except Exception as e:
                print(f"Error generating signal for {symbol}: {e}")
                continue
        
        return signals
    
    def _generate_single_signal(self, symbol: str, stocks_db: Dict) -> Optional[AISignal]:
        """Generate signal for a single stock"""
        # Check cache first
        cache_key = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        if cache_key in self.signals_cache:
            return self.signals_cache[cache_key]
        
        try:
            # Get stock info
            stock_code = symbol.replace('.SR', '')
            stock_info = stocks_db.get(stock_code, {})
            company_name = stock_info.get('name_en', 'Unknown Company')
            
            # Import yfinance here to avoid import issues
            import yfinance as yf
            
            # Fetch recent data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="3mo")
            
            if data.empty or len(data) < 20:
                return None
            
            # Generate AI signal using technical analysis
            signal = self._analyze_stock_data(data, symbol, company_name)
            
            # Cache the signal
            self.signals_cache[cache_key] = signal
            
            return signal
            
        except Exception as e:
            print(f"Error analyzing {symbol}: {e}")
            return None
    
    def _analyze_stock_data(self, data: pd.DataFrame, symbol: str, company_name: str) -> AISignal:
        """Analyze stock data and generate AI signal"""
        current_price = data['Close'].iloc[-1]
        
        # Calculate technical indicators
        # Moving averages
        sma_20 = data['Close'].rolling(20).mean().iloc[-1]
        sma_50 = data['Close'].rolling(50).mean().iloc[-1] if len(data) >= 50 else sma_20
        
        # Price momentum
        price_change_5d = (current_price / data['Close'].iloc[-6] - 1) * 100 if len(data) >= 6 else 0
        price_change_20d = (current_price / data['Close'].iloc[-21] - 1) * 100 if len(data) >= 21 else 0
        
        # Volatility
        volatility = data['Close'].pct_change().rolling(20).std().iloc[-1] * 100
        
        # Volume analysis
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]
        recent_volume = data['Volume'].iloc[-1]
        volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
        
        # RSI calculation
        rsi = self._calculate_rsi(data['Close'])
        
        # AI Decision Logic
        signal_type, confidence, reasoning = self._make_ai_decision(
            current_price, sma_20, sma_50, price_change_5d, price_change_20d,
            volatility, volume_ratio, rsi
        )
        
        # Predict price target
        if signal_type == 'BUY':
            predicted_price = current_price * (1 + 0.05 + (confidence - 0.5) * 0.1)
            expected_return = ((predicted_price / current_price) - 1) * 100
        elif signal_type == 'SELL':
            predicted_price = current_price * (1 - 0.03 - (confidence - 0.5) * 0.08)
            expected_return = ((predicted_price / current_price) - 1) * 100
        else:  # HOLD
            predicted_price = current_price * (1 + np.random.uniform(-0.02, 0.02))
            expected_return = ((predicted_price / current_price) - 1) * 100
        
        # Risk assessment
        if volatility < 5:
            risk_level = 'LOW'
        elif volatility < 15:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'
        
        return AISignal(
            symbol=symbol,
            company_name=company_name,
            signal_type=signal_type,
            confidence=confidence,
            predicted_price=predicted_price,
            current_price=current_price,
            expected_return=expected_return,
            risk_level=risk_level,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(window=period).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
        
        if loss.iloc[-1] == 0:
            return 100
        
        rs = gain.iloc[-1] / loss.iloc[-1]
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _make_ai_decision(self, current_price, sma_20, sma_50, price_change_5d, 
                         price_change_20d, volatility, volume_ratio, rsi) -> tuple:
        """AI decision making logic"""
        
        # Initialize scoring
        buy_score = 0
        sell_score = 0
        reasoning_points = []
        
        # Trend analysis
        if current_price > sma_20 > sma_50:
            buy_score += 2
            reasoning_points.append("Strong upward trend")
        elif current_price < sma_20 < sma_50:
            sell_score += 2
            reasoning_points.append("Strong downward trend")
        elif current_price > sma_20:
            buy_score += 1
            reasoning_points.append("Above short-term average")
        else:
            sell_score += 1
            reasoning_points.append("Below short-term average")
        
        # Momentum analysis
        if price_change_5d > 5:
            buy_score += 1
            reasoning_points.append("Strong recent momentum")
        elif price_change_5d < -5:
            sell_score += 1
            reasoning_points.append("Weak recent momentum")
        
        if price_change_20d > 10:
            buy_score += 1
            reasoning_points.append("Strong monthly performance")
        elif price_change_20d < -10:
            sell_score += 1
            reasoning_points.append("Weak monthly performance")
        
        # RSI analysis
        if rsi < 30:
            buy_score += 2
            reasoning_points.append("Oversold condition (RSI < 30)")
        elif rsi > 70:
            sell_score += 2
            reasoning_points.append("Overbought condition (RSI > 70)")
        elif rsi < 50:
            buy_score += 0.5
        else:
            sell_score += 0.5
        
        # Volume analysis
        if volume_ratio > 1.5:
            if buy_score > sell_score:
                buy_score += 1
                reasoning_points.append("High volume supporting trend")
            else:
                sell_score += 1
                reasoning_points.append("High volume supporting trend")
        
        # Volatility consideration
        if volatility > 20:
            # High volatility reduces confidence
            buy_score *= 0.8
            sell_score *= 0.8
            reasoning_points.append("High volatility increases risk")
        
        # Make decision
        total_score = buy_score + sell_score
        if total_score == 0:
            signal_type = 'HOLD'
            confidence = 0.5
        elif buy_score > sell_score:
            signal_type = 'BUY'
            confidence = min(0.95, 0.5 + (buy_score / (total_score * 2)) * 0.5)
        else:
            signal_type = 'SELL'
            confidence = min(0.95, 0.5 + (sell_score / (total_score * 2)) * 0.5)
        
        # If scores are close, default to HOLD
        if abs(buy_score - sell_score) < 1:
            signal_type = 'HOLD'
            confidence = 0.6
        
        reasoning = "; ".join(reasoning_points[:3])  # Top 3 reasons
        
        return signal_type, confidence, reasoning

# Global AI engine instance
ai_engine = SimpleAIEngine()

def get_ai_signals(symbols: List[str], stocks_db: Dict) -> List[AISignal]:
    """Main function to get AI signals - used by the main app"""
    return ai_engine.generate_signals(symbols, stocks_db)

# Test function
if __name__ == "__main__":
    print("🤖 Testing Simple AI Engine...")
    
    # Sample stocks database
    sample_db = {
        "2030": {"name_en": "Saudi Arabian Oil Co (Aramco)", "sector": "Energy"},
        "1120": {"name_en": "Al Rajhi Bank", "sector": "Banking"},
        "2222": {"name_en": "Saudi Aramco Base Oil Company", "sector": "Energy"}
    }
    
    # Test signals
    symbols = ["2030.SR", "1120.SR"]
    try:
        signals = get_ai_signals(symbols, sample_db)
        print(f"Generated {len(signals)} AI signals:")
        
        for signal in signals:
            print(f"\n📊 {signal.company_name} ({signal.symbol})")
            print(f"   Signal: {signal.signal_type}")
            print(f"   Confidence: {signal.confidence:.1%}")
            print(f"   Expected Return: {signal.expected_return:+.1f}%")
            print(f"   Risk Level: {signal.risk_level}")
            print(f"   Reasoning: {signal.reasoning}")
            
    except Exception as e:
        print(f"Test failed: {e}")
    
    print("✅ AI Engine test completed!")
