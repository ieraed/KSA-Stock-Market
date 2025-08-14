"""
AI Trading Engine for Saudi Stock Market App
Advanced machine learning predictions and automated trading strategies
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

# AI/ML imports (will be installed as needed)
try:
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split, TimeSeriesSplit
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.linear_model import LinearRegression
except ImportError:
    print("Installing AI dependencies...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    from sklearn.model_selection import train_test_split, TimeSeriesSplit
    from sklearn.metrics import accuracy_score, classification_report
    from sklearn.linear_model import LinearRegression

@dataclass
class AITradingSignal:
    """Enhanced AI trading signal with machine learning predictions"""
    symbol: str
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float  # 0.0 to 1.0
    predicted_price: Optional[float]
    prediction_horizon: int  # days
    risk_score: float  # 0.0 to 1.0
    ai_features: Dict[str, float]
    timestamp: datetime
    model_version: str

class AIFeatureEngineering:
    """Advanced feature engineering for AI trading models"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.price_scaler = MinMaxScaler()
        
    def create_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create advanced technical analysis features"""
        
        # Price-based features
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
        df['volatility_5d'] = df['returns'].rolling(5).std()
        df['volatility_20d'] = df['returns'].rolling(20).std()
        
        # Moving averages and ratios
        for period in [5, 10, 20, 50, 200]:
            df[f'sma_{period}'] = df['close'].rolling(period).mean()
            df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
            df[f'price_sma_{period}_ratio'] = df['close'] / df[f'sma_{period}']
        
        # Volume features
        df['volume_sma_20'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_20']
        df['price_volume'] = df['close'] * df['volume']
        
        # Momentum indicators
        df['rsi'] = self._calculate_rsi(df['close'])
        df['macd'], df['macd_signal'] = self._calculate_macd(df['close'])
        df['bollinger_upper'], df['bollinger_lower'] = self._calculate_bollinger_bands(df['close'])
        df['bollinger_position'] = (df['close'] - df['bollinger_lower']) / (df['bollinger_upper'] - df['bollinger_lower'])
        
        # Price patterns
        df['price_change_1d'] = df['close'].pct_change(1)
        df['price_change_5d'] = df['close'].pct_change(5)
        df['price_change_20d'] = df['close'].pct_change(20)
        
        # Support/Resistance levels
        df['resistance_20d'] = df['high'].rolling(20).max()
        df['support_20d'] = df['low'].rolling(20).min()
        df['price_position'] = (df['close'] - df['support_20d']) / (df['resistance_20d'] - df['support_20d'])
        
        return df
    
    def create_market_features(self, df: pd.DataFrame, market_data: Dict) -> pd.DataFrame:
        """Create market-wide features for better predictions"""
        
        # Market sentiment features
        df['market_volatility'] = market_data.get('vix_equivalent', 0.2)
        df['market_trend'] = market_data.get('market_trend', 0.0)
        df['sector_performance'] = market_data.get('sector_performance', 0.0)
        
        # Economic indicators
        df['oil_price_change'] = market_data.get('oil_price_change', 0.0)
        df['currency_strength'] = market_data.get('sar_usd_change', 0.0)
        df['interest_rate'] = market_data.get('saudi_interest_rate', 0.05)
        
        # Calendar effects
        df['day_of_week'] = pd.to_datetime(df.index).dayofweek
        df['month'] = pd.to_datetime(df.index).month
        df['is_month_end'] = pd.to_datetime(df.index).day >= 25
        df['is_quarter_end'] = pd.to_datetime(df.index).month.isin([3, 6, 9, 12])
        
        return df
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _calculate_macd(self, prices: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD indicator"""
        ema_12 = prices.ewm(span=12).mean()
        ema_26 = prices.ewm(span=26).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9).mean()
        return macd, signal
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(period).mean()
        std = prices.rolling(period).std()
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        return upper, lower

class AITradingPredictor:
    """Advanced AI prediction engine for trading signals"""
    
    def __init__(self):
        self.models = {
            'direction': RandomForestClassifier(n_estimators=100, random_state=42),
            'price': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'volatility': LinearRegression()
        }
        self.feature_engineering = AIFeatureEngineering()
        self.is_trained = False
        self.feature_columns = []
        
    def prepare_training_data(self, df: pd.DataFrame, market_data: Dict) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare data for AI model training"""
        
        # Feature engineering
        df = self.feature_engineering.create_technical_features(df.copy())
        df = self.feature_engineering.create_market_features(df, market_data)
        
        # Create target variables
        df['future_return_5d'] = df['close'].shift(-5) / df['close'] - 1
        df['future_direction'] = (df['future_return_5d'] > 0.02).astype(int)  # 2% threshold
        df['future_volatility'] = df['returns'].shift(-5).rolling(5).std()
        
        # Select features
        feature_cols = [col for col in df.columns if col not in [
            'open', 'high', 'low', 'close', 'volume', 'symbol',
            'future_return_5d', 'future_direction', 'future_volatility'
        ]]
        
        # Clean data
        df = df.dropna()
        
        if len(df) < 100:
            raise ValueError("Insufficient data for AI training")
        
        X = df[feature_cols].values
        y_direction = df['future_direction'].values
        y_return = df['future_return_5d'].values
        
        self.feature_columns = feature_cols
        
        return X, y_direction, y_return
    
    def train_models(self, df: pd.DataFrame, market_data: Dict = None) -> Dict[str, float]:
        """Train AI models on historical data"""
        
        if market_data is None:
            market_data = self._get_default_market_data()
        
        try:
            # Prepare training data
            X, y_direction, y_return = self.prepare_training_data(df, market_data)
            
            # Split data for time series
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_dir_train, y_dir_test = y_direction[:split_idx], y_direction[split_idx:]
            y_ret_train, y_ret_test = y_return[:split_idx], y_return[split_idx:]
            
            # Train direction model
            self.models['direction'].fit(X_train, y_dir_train)
            direction_accuracy = self.models['direction'].score(X_test, y_dir_test)
            
            # Train return prediction model
            self.models['price'].fit(X_train, y_ret_train)
            return_score = self.models['price'].score(X_test, y_ret_test)
            
            # Train volatility model
            vol_mask = ~np.isnan(y_return)
            if np.sum(vol_mask) > 50:
                self.models['volatility'].fit(X[vol_mask], np.abs(y_return[vol_mask]))
            
            self.is_trained = True
            
            return {
                'direction_accuracy': direction_accuracy,
                'return_r2_score': return_score,
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
        except Exception as e:
            logging.error(f"AI model training failed: {e}")
            return {'error': str(e)}
    
    def predict_signal(self, current_data: pd.DataFrame, market_data: Dict = None) -> AITradingSignal:
        """Generate AI-powered trading signal"""
        
        if not self.is_trained:
            # Train on available data first
            self.train_models(current_data, market_data)
        
        if market_data is None:
            market_data = self._get_default_market_data()
        
        try:
            # Prepare current features
            df = self.feature_engineering.create_technical_features(current_data.copy())
            df = self.feature_engineering.create_market_features(df, market_data)
            
            # Get latest features
            latest_features = df[self.feature_columns].iloc[-1:].values
            
            # Make predictions
            direction_prob = self.models['direction'].predict_proba(latest_features)[0]
            predicted_return = self.models['price'].predict(latest_features)[0]
            
            # Determine signal
            buy_confidence = direction_prob[1] if len(direction_prob) > 1 else 0.5
            
            if buy_confidence > 0.7 and predicted_return > 0.02:
                signal_type = 'BUY'
                confidence = buy_confidence
            elif buy_confidence < 0.3 and predicted_return < -0.02:
                signal_type = 'SELL'
                confidence = 1 - buy_confidence
            else:
                signal_type = 'HOLD'
                confidence = 0.5
            
            # Calculate risk score
            volatility = df['volatility_20d'].iloc[-1] if 'volatility_20d' in df.columns else 0.2
            risk_score = min(volatility * 5, 1.0)  # Normalize to 0-1
            
            # Create AI signal
            symbol = current_data.get('symbol', 'UNKNOWN')
            current_price = current_data['close'].iloc[-1]
            predicted_price = current_price * (1 + predicted_return)
            
            return AITradingSignal(
                symbol=symbol,
                signal_type=signal_type,
                confidence=confidence,
                predicted_price=predicted_price,
                prediction_horizon=5,
                risk_score=risk_score,
                ai_features={
                    'predicted_return': predicted_return,
                    'buy_probability': buy_confidence,
                    'volatility': volatility,
                    'rsi': df['rsi'].iloc[-1] if 'rsi' in df.columns else 50
                },
                timestamp=datetime.now(),
                model_version='v1.0'
            )
            
        except Exception as e:
            logging.error(f"AI prediction failed: {e}")
            # Return neutral signal on error
            return AITradingSignal(
                symbol='ERROR',
                signal_type='HOLD',
                confidence=0.0,
                predicted_price=None,
                prediction_horizon=5,
                risk_score=1.0,
                ai_features={'error': str(e)},
                timestamp=datetime.now(),
                model_version='v1.0'
            )
    
    def _get_default_market_data(self) -> Dict:
        """Default market data when not available"""
        return {
            'vix_equivalent': 0.25,
            'market_trend': 0.0,
            'sector_performance': 0.0,
            'oil_price_change': 0.0,
            'sar_usd_change': 0.0,
            'saudi_interest_rate': 0.05
        }

class AIPortfolioOptimizer:
    """AI-powered portfolio optimization and risk management"""
    
    def __init__(self):
        self.risk_model = LinearRegression()
        
    def optimize_portfolio(self, signals: List[AITradingSignal], portfolio_value: float = 100000) -> Dict[str, Any]:
        """Optimize portfolio allocation using AI signals"""
        
        if not signals:
            return {'error': 'No signals provided'}
        
        # Filter buy signals only
        buy_signals = [s for s in signals if s.signal_type == 'BUY']
        
        if not buy_signals:
            return {'allocation': {}, 'total_confidence': 0.0, 'risk_score': 0.0}
        
        # Calculate position sizes based on confidence and risk
        total_confidence = sum(s.confidence * (1 - s.risk_score) for s in buy_signals)
        
        allocation = {}
        for signal in buy_signals:
            # Risk-adjusted weight
            weight = (signal.confidence * (1 - signal.risk_score)) / total_confidence
            position_value = portfolio_value * weight * 0.8  # 80% max allocation
            allocation[signal.symbol] = {
                'weight': weight,
                'value': position_value,
                'confidence': signal.confidence,
                'risk_score': signal.risk_score,
                'predicted_return': signal.ai_features.get('predicted_return', 0.0)
            }
        
        # Calculate portfolio metrics
        avg_risk = sum(s.risk_score for s in buy_signals) / len(buy_signals)
        avg_confidence = sum(s.confidence for s in buy_signals) / len(buy_signals)
        
        return {
            'allocation': allocation,
            'total_confidence': avg_confidence,
            'risk_score': avg_risk,
            'diversification': len(buy_signals),
            'cash_allocation': 1.0 - sum(a['weight'] for a in allocation.values()) * 0.8
        }

# Integration functions for existing app
def get_ai_enhanced_signals(portfolio_symbols: List[str], market_data_func=None) -> List[AITradingSignal]:
    """Generate AI-enhanced signals for portfolio symbols"""
    
    ai_predictor = AITradingPredictor()
    signals = []
    
    for symbol in portfolio_symbols:
        try:
            # Get historical data (this would integrate with your existing data fetcher)
            # For now, using sample data structure
            sample_data = _create_sample_stock_data(symbol)
            
            # Generate AI signal
            ai_signal = ai_predictor.predict_signal(sample_data)
            signals.append(ai_signal)
            
        except Exception as e:
            logging.error(f"Failed to generate AI signal for {symbol}: {e}")
            continue
    
    return signals

def _create_sample_stock_data(symbol: str) -> pd.DataFrame:
    """Create sample stock data for AI testing"""
    dates = pd.date_range(start='2024-01-01', end='2025-08-11', freq='D')
    n_days = len(dates)
    
    # Generate realistic price data
    np.random.seed(hash(symbol) % 2**32)
    base_price = 100
    returns = np.random.normal(0.001, 0.02, n_days)
    prices = base_price * np.exp(np.cumsum(returns))
    
    df = pd.DataFrame({
        'open': prices * (1 + np.random.normal(0, 0.01, n_days)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.015, n_days))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.015, n_days))),
        'close': prices,
        'volume': np.random.randint(100000, 1000000, n_days),
        'symbol': symbol
    }, index=dates)
    
    return df

if __name__ == "__main__":
    # Test AI trading system
    print("🤖 Testing AI Trading Engine...")
    
    # Test with sample portfolio
    test_symbols = ['2222.SR', '2030.SR', '1120.SR']  # ARAMCO, SABIC, AL RAJHI
    ai_signals = get_ai_enhanced_signals(test_symbols)
    
    print(f"\n📊 Generated {len(ai_signals)} AI signals:")
    for signal in ai_signals:
        print(f"  {signal.symbol}: {signal.signal_type} (Confidence: {signal.confidence:.2f})")
    
    # Test portfolio optimization
    optimizer = AIPortfolioOptimizer()
    portfolio_allocation = optimizer.optimize_portfolio(ai_signals)
    
    print(f"\n💼 AI Portfolio Optimization:")
    print(f"  Total Confidence: {portfolio_allocation.get('total_confidence', 0):.2f}")
    print(f"  Risk Score: {portfolio_allocation.get('risk_score', 0):.2f}")
    print(f"  Diversification: {portfolio_allocation.get('diversification', 0)} stocks")
    
    print("\n✅ AI Trading Engine Ready!")
