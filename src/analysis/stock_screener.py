"""
Saudi Stock Market Screener
Comprehensive screening of all Saudi stocks with technical analysis and target prices
"""

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

logger = logging.getLogger(__name__)

class SaudiStockScreener:
    """Comprehensive screener for Saudi stock market"""
    
    def __init__(self):
        # Comprehensive list of Saudi stocks by symbol with sector classification
        self.saudi_stocks = {
            # Banks & Financial Services
            "1120": {"name": "Al Rajhi Bank", "sector": "Banks"},
            "1180": {"name": "Saudi National Bank", "sector": "Banks"},
            "1010": {"name": "Riyad Bank", "sector": "Banks"},
            "1140": {"name": "Banque Saudi Fransi", "sector": "Banks"},
            "1150": {"name": "Al Inma Bank", "sector": "Banks"},
            "1080": {"name": "Arab National Bank", "sector": "Banks"},
            "1060": {"name": "Saudi Investment Bank", "sector": "Banks"},
            "9408": {"name": "Bank AlBilad", "sector": "Banks"},
            "1030": {"name": "Alinma Bank", "sector": "Banks"},
            "1090": {"name": "Samba Financial", "sector": "Banks"},
            
            # Energy & Petrochemicals
            "2222": {"name": "Saudi Aramco", "sector": "Energy"},
            "2010": {"name": "SABIC", "sector": "Petrochemicals"},
            "2290": {"name": "YANSAB", "sector": "Petrochemicals"},
            "2330": {"name": "SIPCHEM", "sector": "Petrochemicals"},
            "2230": {"name": "Petrochemical Industries", "sector": "Petrochemicals"},
            "2082": {"name": "ACWA Power", "sector": "Energy"},
            "5110": {"name": "Saudi Electricity", "sector": "Utilities"},
            "2380": {"name": "Saudi Kayan", "sector": "Petrochemicals"},
            "2001": {"name": "Chemanol", "sector": "Petrochemicals"},
            "2110": {"name": "Saudi Steel Pipe", "sector": "Industrial"},
            "8150": {"name": "Advanced Petrochemical", "sector": "Petrochemicals"},
            "2040": {"name": "Petro Rabigh", "sector": "Petrochemicals"},
            
            # Telecommunications & Technology
            "7010": {"name": "Saudi Telecom Company", "sector": "Telecommunications"},
            "7030": {"name": "Zain KSA", "sector": "Telecommunications"},
            "7020": {"name": "Mobily", "sector": "Telecommunications"},
            "4190": {"name": "Jarir Marketing", "sector": "Technology & Electronics"},
            
            # Food & Agriculture
            "2280": {"name": "Almarai", "sector": "Food & Beverages"},
            "6010": {"name": "NADEC", "sector": "Food & Beverages"},
            "6001": {"name": "Herfy Food Services", "sector": "Food & Beverages"},
            "2050": {"name": "Savola Group", "sector": "Food & Beverages"},
            "6004": {"name": "CATRION", "sector": "Food & Beverages"},
            "6020": {"name": "Tabuk Agricultural", "sector": "Agriculture"},
            "6070": {"name": "Al Jouf Agricultural", "sector": "Agriculture"},
            "6050": {"name": "Anaam Holding", "sector": "Food & Beverages"},
            "6060": {"name": "National Agricultural Marketing", "sector": "Agriculture"},
            
            # Real Estate & Construction
            "4322": {"name": "RETAL", "sector": "Real Estate"},
            "4020": {"name": "Saudi Cement", "sector": "Materials & Construction"},
            "3060": {"name": "Yanbu Cement", "sector": "Materials & Construction"},
            "3020": {"name": "Qassim Cement", "sector": "Materials & Construction"},
            "4100": {"name": "Emaar Economic City", "sector": "Real Estate"},
            "4323": {"name": "ARESCO", "sector": "Real Estate"},
            "3040": {"name": "Aljouf Cement", "sector": "Materials & Construction"},
            "3030": {"name": "City Cement", "sector": "Materials & Construction"},
            "3080": {"name": "Northern Region Cement", "sector": "Materials & Construction"},
            
            # Healthcare & Pharmaceuticals
            "4009": {"name": "Mouwasat Medical", "sector": "Healthcare"},
            "2140": {"name": "Tihama Development", "sector": "Healthcare"},
            "4001": {"name": "SPIMACO", "sector": "Pharmaceuticals"},
            "4270": {"name": "National Medical Care", "sector": "Healthcare"},
            
            # Mining & Metals
            "1211": {"name": "Saudi Arabian Mining", "sector": "Mining"},
            
            # Industrial & Manufacturing
            "2190": {"name": "SISCO Holding", "sector": "Industrial"},
            "1832": {"name": "SAIC", "sector": "Industrial"},
            "4080": {"name": "Saudi Cable", "sector": "Industrial"},
            "1201": {"name": "Takween Advanced Industries", "sector": "Industrial"},
            "1202": {"name": "Middle East Paper", "sector": "Industrial"},
            
            # Insurance
            "8010": {"name": "SAICO", "sector": "Insurance"},
            "8020": {"name": "Mediterranean & Gulf Insurance", "sector": "Insurance"},
            "8030": {"name": "Saudi United Cooperative", "sector": "Insurance"},
            
            # Transportation & Logistics
            "4030": {"name": "Saudi Airlines Catering", "sector": "Transportation"},
            "4031": {"name": "Ground Services", "sector": "Transportation"},
            "2220": {"name": "National Shipping Company", "sector": "Transportation"},
            
            # Retail & Consumer
            "4050": {"name": "Saudi Research & Marketing", "sector": "Media & Entertainment"},
            "4200": {"name": "Al Jazeera Bank", "sector": "Banks"},
            "4250": {"name": "Kingdom Holding", "sector": "Investment & Holding"},
            "4040": {"name": "Saudi Marketing", "sector": "Consumer Services"},
            "4110": {"name": "Tihama", "sector": "Consumer Services"},
            "1203": {"name": "Al Sorayai Trading", "sector": "Consumer Services"},
            "4003": {"name": "Abdullah Al Othaim Markets", "sector": "Retail"},
            "4005": {"name": "Extra", "sector": "Retail"},
            "4006": {"name": "Fawaz Al Hokair", "sector": "Retail"},
            "4007": {"name": "Fitaihi Holding", "sector": "Retail"},
            "4280": {"name": "Arabian Centres", "sector": "Real Estate"},
            "2170": {"name": "Al Hassan Ghazi Ibrahim Shaker", "sector": "Consumer Services"}
        }
    
    def fetch_stock_data(self, symbol: str, retries: int = 2) -> Optional[Dict]:
        """Fetch comprehensive data for a single stock with retries"""
        for attempt in range(retries + 1):
            try:
                ticker_symbol = f"{symbol}.SR"
                ticker = yf.Ticker(ticker_symbol)
                
                # Get basic info
                info = ticker.info
                hist = ticker.history(period="6mo", interval="1d")
                
                if hist.empty:
                    continue
                    
                # Calculate technical indicators
                current_price = float(hist['Close'].iloc[-1])
                prev_price = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change = current_price - prev_price
                change_pct = (change / prev_price * 100) if prev_price > 0 else 0
                
                # Technical analysis
                technical_data = self._calculate_technical_indicators(hist)
                
                # Generate signals and target price
                signal_data = self._generate_stock_signal(hist, technical_data)
                
                return {
                    'symbol': symbol,
                    'company_name': info.get('longName', info.get('shortName', self.saudi_stocks.get(symbol, {}).get('name', f'Company {symbol}'))),
                    'sector': self.saudi_stocks.get(symbol, {}).get('sector', 'Other'),
                    'current_price': current_price,
                    'change': change,
                    'change_pct': change_pct,
                    'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', None),
                    'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                    'technical_indicators': technical_data,
                    'signal': signal_data['signal'],
                    'signal_strength': signal_data['strength'],
                    'target_price': signal_data['target_price'],
                    'support_level': signal_data['support'],
                    'resistance_level': signal_data['resistance'],
                    'risk_rating': signal_data['risk_rating'],
                    'last_updated': datetime.now()
                }
                
            except Exception as e:
                if attempt == retries:
                    logger.warning(f"Failed to fetch data for {symbol}: {e}")
                else:
                    time.sleep(1)  # Wait before retry
                continue
        
        return None
    
    def _calculate_technical_indicators(self, hist: pd.DataFrame) -> Dict:
        """Calculate technical indicators for stock analysis"""
        try:
            close = hist['Close']
            high = hist['High'] 
            low = hist['Low']
            volume = hist['Volume']
            
            # RSI (14-day)
            rsi = self._calculate_rsi(close, 14)
            
            # MACD
            exp1 = close.ewm(span=12).mean()
            exp2 = close.ewm(span=26).mean()
            macd = exp1 - exp2
            signal_line = macd.ewm(span=9).mean()
            
            # Bollinger Bands (20-day, 2 std)
            bb_middle = close.rolling(window=20).mean()
            bb_std = close.rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            # Moving Averages
            sma_20 = close.rolling(window=20).mean()
            sma_50 = close.rolling(window=50).mean()
            sma_200 = close.rolling(window=200).mean()
            
            # Volume indicators
            volume_ma = volume.rolling(window=20).mean()
            volume_ratio = volume.iloc[-1] / volume_ma.iloc[-1] if volume_ma.iloc[-1] > 0 else 1
            
            return {
                'rsi': rsi.iloc[-1] if not rsi.empty else 50,
                'macd': macd.iloc[-1] if not macd.empty else 0,
                'macd_signal': signal_line.iloc[-1] if not signal_line.empty else 0,
                'bb_position': ((close.iloc[-1] - bb_lower.iloc[-1]) / (bb_upper.iloc[-1] - bb_lower.iloc[-1])) * 100 if not bb_lower.empty else 50,
                'sma_20': sma_20.iloc[-1] if not sma_20.empty else close.iloc[-1],
                'sma_50': sma_50.iloc[-1] if not sma_50.empty else close.iloc[-1],
                'sma_200': sma_200.iloc[-1] if not sma_200.empty else close.iloc[-1],
                'volume_ratio': volume_ratio,
                'price_vs_sma20': ((close.iloc[-1] / sma_20.iloc[-1]) - 1) * 100 if not sma_20.empty else 0,
                'price_vs_sma50': ((close.iloc[-1] / sma_50.iloc[-1]) - 1) * 100 if not sma_50.empty else 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return {}
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI (Relative Strength Index)"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi
        except:
            return pd.Series([50] * len(prices), index=prices.index)
    
    def _generate_stock_signal(self, hist: pd.DataFrame, technical: Dict) -> Dict:
        """Generate trading signal and target price for stock"""
        try:
            current_price = hist['Close'].iloc[-1]
            high_52w = hist['High'].rolling(window=252).max().iloc[-1]
            low_52w = hist['Low'].rolling(window=252).min().iloc[-1]
            
            # Signal generation based on multiple factors
            bullish_signals = 0
            bearish_signals = 0
            
            # RSI analysis
            rsi = technical.get('rsi', 50)
            if rsi < 30:  # Oversold
                bullish_signals += 2
            elif rsi < 40:
                bullish_signals += 1
            elif rsi > 70:  # Overbought
                bearish_signals += 2
            elif rsi > 60:
                bearish_signals += 1
            
            # MACD analysis
            macd = technical.get('macd', 0)
            macd_signal = technical.get('macd_signal', 0)
            if macd > macd_signal:
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            # Moving average analysis
            price_vs_sma20 = technical.get('price_vs_sma20', 0)
            price_vs_sma50 = technical.get('price_vs_sma50', 0)
            
            if price_vs_sma20 > 2:  # Price above 20 SMA
                bullish_signals += 1
            elif price_vs_sma20 < -2:
                bearish_signals += 1
                
            if price_vs_sma50 > 0:  # Price above 50 SMA
                bullish_signals += 1
            else:
                bearish_signals += 1
            
            # Volume analysis
            volume_ratio = technical.get('volume_ratio', 1)
            if volume_ratio > 1.5:  # High volume
                if bullish_signals > bearish_signals:
                    bullish_signals += 1
                else:
                    bearish_signals += 1
            
            # Determine signal
            net_signal = bullish_signals - bearish_signals
            if net_signal >= 2:
                signal = "STRONG_BUY"
                strength = min(90, 60 + (net_signal * 5))
            elif net_signal >= 1:
                signal = "BUY"
                strength = min(75, 55 + (net_signal * 5))
            elif net_signal <= -2:
                signal = "STRONG_SELL"
                strength = max(10, 40 + (net_signal * 5))
            elif net_signal <= -1:
                signal = "SELL"
                strength = max(25, 45 + (net_signal * 5))
            else:
                signal = "HOLD"
                strength = 50
            
            # Calculate target price
            target_multiplier = 1.0
            if signal in ["STRONG_BUY", "BUY"]:
                target_multiplier = 1.05 + (strength - 50) / 1000  # 5-15% upside
            elif signal in ["STRONG_SELL", "SELL"]:
                target_multiplier = 0.95 - (50 - strength) / 1000  # 5-15% downside
            
            target_price = current_price * target_multiplier
            
            # Support and resistance levels
            support = max(low_52w, current_price * 0.85)
            resistance = min(high_52w, current_price * 1.15)
            
            # Risk rating
            volatility = hist['Close'].pct_change().std() * 100
            if volatility > 5:
                risk_rating = "HIGH"
            elif volatility > 3:
                risk_rating = "MEDIUM"
            else:
                risk_rating = "LOW"
            
            return {
                'signal': signal,
                'strength': strength,
                'target_price': round(target_price, 2),
                'support': round(support, 2),
                'resistance': round(resistance, 2),
                'risk_rating': risk_rating,
                'bullish_signals': bullish_signals,
                'bearish_signals': bearish_signals
            }
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return {
                'signal': 'HOLD',
                'strength': 50,
                'target_price': hist['Close'].iloc[-1],
                'support': hist['Low'].iloc[-1],
                'resistance': hist['High'].iloc[-1],
                'risk_rating': 'MEDIUM',
                'bullish_signals': 0,
                'bearish_signals': 0
            }
    
    def screen_all_stocks(self, max_workers: int = 10) -> pd.DataFrame:
        """Screen all Saudi stocks with parallel processing"""
        print("🔍 Starting comprehensive Saudi stock screening...")
        
        stock_data = []
        total_stocks = len(self.saudi_stocks)
        processed = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_symbol = {
                executor.submit(self.fetch_stock_data, symbol): symbol 
                for symbol in self.saudi_stocks.keys()
            }
            
            # Process results as they complete
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    result = future.result(timeout=30)
                    if result:
                        stock_data.append(result)
                    processed += 1
                    
                    if processed % 10 == 0:
                        print(f"📊 Processed {processed}/{total_stocks} stocks...")
                        
                except Exception as e:
                    logger.warning(f"Error processing {symbol}: {e}")
                    processed += 1
        
        print(f"✅ Screening complete! Analyzed {len(stock_data)} stocks.")
        
        # Convert to DataFrame
        if stock_data:
            df = pd.DataFrame(stock_data)
            return self._rank_stocks(df)
        else:
            return pd.DataFrame()
    
    def _rank_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rank stocks based on multiple criteria"""
        try:
            # Calculate composite score
            df['composite_score'] = 0
            
            # Signal strength weight (40%)
            df['composite_score'] += (df['signal_strength'] / 100) * 40
            
            # RSI score (20%) - favor oversold conditions
            rsi_scores = df['technical_indicators'].apply(lambda x: x.get('rsi', 50))
            rsi_normalized = np.where(rsi_scores < 30, 100, 
                                    np.where(rsi_scores < 50, 70, 
                                           np.where(rsi_scores < 70, 50, 20)))
            df['composite_score'] += (rsi_normalized / 100) * 20
            
            # Volume activity (15%)
            volume_scores = df['technical_indicators'].apply(lambda x: min(100, x.get('volume_ratio', 1) * 50))
            df['composite_score'] += (volume_scores / 100) * 15
            
            # Price momentum (15%) - favor stocks above moving averages
            momentum_scores = df['technical_indicators'].apply(
                lambda x: max(0, min(100, 50 + x.get('price_vs_sma20', 0) * 2))
            )
            df['composite_score'] += (momentum_scores / 100) * 15
            
            # Market cap stability (10%) - slight preference for larger caps
            if 'market_cap' in df.columns:
                market_cap_scores = np.log10(df['market_cap'].fillna(1000000)) * 10
                market_cap_normalized = np.clip(market_cap_scores, 0, 100)
                df['composite_score'] += (market_cap_normalized / 100) * 10
            
            # Sort by composite score and signal strength
            df = df.sort_values(['composite_score', 'signal_strength'], ascending=[False, False])
            
            return df
            
        except Exception as e:
            logger.error(f"Error ranking stocks: {e}")
            return df.sort_values('signal_strength', ascending=False)
    
    def get_top_picks(self, df: pd.DataFrame, top_n: int = 20) -> Dict:
        """Get top stock picks categorized by signal type"""
        if df.empty:
            return {}
        
        try:
            top_picks = {
                'strong_buys': df[df['signal'] == 'STRONG_BUY'].head(top_n),
                'buys': df[df['signal'] == 'BUY'].head(top_n),
                'top_scorers': df.head(top_n),
                'oversold_opportunities': df[
                    df['technical_indicators'].apply(lambda x: x.get('rsi', 50) < 35)
                ].head(top_n),
                'high_volume_movers': df[
                    df['technical_indicators'].apply(lambda x: x.get('volume_ratio', 1) > 2)
                ].head(top_n)
            }
            
            return top_picks
            
        except Exception as e:
            logger.error(f"Error getting top picks: {e}")
            return {'top_scorers': df.head(top_n)}
    
    def analyze_sector_performance(self, df: pd.DataFrame) -> Dict:
        """Analyze performance by sector"""
        if df.empty:
            return {}
        
        try:
            # Group by sector
            sector_analysis = {}
            
            for sector in df['sector'].unique():
                sector_stocks = df[df['sector'] == sector]
                
                if sector_stocks.empty:
                    continue
                
                # Calculate sector metrics
                total_stocks = len(sector_stocks)
                avg_change = sector_stocks['change_pct'].mean()
                avg_signal_strength = sector_stocks['signal_strength'].mean()
                avg_target_upside = ((sector_stocks['target_price'] / sector_stocks['current_price'] - 1) * 100).mean()
                
                # Count signals by type
                buy_signals = len(sector_stocks[sector_stocks['signal'].isin(['BUY', 'STRONG_BUY'])])
                sell_signals = len(sector_stocks[sector_stocks['signal'].isin(['SELL', 'STRONG_SELL'])])
                hold_signals = len(sector_stocks[sector_stocks['signal'] == 'HOLD'])
                
                # Best and worst performers
                best_performer = sector_stocks.loc[sector_stocks['change_pct'].idxmax()] if not sector_stocks.empty else None
                worst_performer = sector_stocks.loc[sector_stocks['change_pct'].idxmin()] if not sector_stocks.empty else None
                
                # Top signals
                top_signals = sector_stocks.nlargest(3, 'signal_strength')
                
                # Risk assessment
                high_risk_count = len(sector_stocks[sector_stocks['risk_rating'] == 'HIGH'])
                medium_risk_count = len(sector_stocks[sector_stocks['risk_rating'] == 'MEDIUM'])
                low_risk_count = len(sector_stocks[sector_stocks['risk_rating'] == 'LOW'])
                
                # Volume activity
                high_volume_count = len(sector_stocks[
                    sector_stocks['technical_indicators'].apply(lambda x: x.get('volume_ratio', 1) > 2)
                ])
                
                sector_analysis[sector] = {
                    'total_stocks': total_stocks,
                    'avg_change_pct': avg_change,
                    'avg_signal_strength': avg_signal_strength,
                    'avg_target_upside': avg_target_upside,
                    'buy_signals': buy_signals,
                    'sell_signals': sell_signals,
                    'hold_signals': hold_signals,
                    'buy_ratio': (buy_signals / total_stocks) * 100 if total_stocks > 0 else 0,
                    'best_performer': {
                        'symbol': best_performer['symbol'] if best_performer is not None else 'N/A',
                        'company': best_performer['company_name'] if best_performer is not None else 'N/A',
                        'change_pct': best_performer['change_pct'] if best_performer is not None else 0
                    },
                    'worst_performer': {
                        'symbol': worst_performer['symbol'] if worst_performer is not None else 'N/A',
                        'company': worst_performer['company_name'] if worst_performer is not None else 'N/A',
                        'change_pct': worst_performer['change_pct'] if worst_performer is not None else 0
                    },
                    'top_signals': top_signals,
                    'risk_distribution': {
                        'high': high_risk_count,
                        'medium': medium_risk_count,
                        'low': low_risk_count
                    },
                    'high_volume_activity': high_volume_count,
                    'sector_rating': self._calculate_sector_rating(avg_change, avg_signal_strength, buy_signals, total_stocks)
                }
            
            # Sort sectors by performance
            sorted_sectors = sorted(
                sector_analysis.items(),
                key=lambda x: (x[1]['avg_change_pct'] + x[1]['avg_signal_strength']/10),
                reverse=True
            )
            
            return {
                'sector_analysis': dict(sorted_sectors),
                'best_sector': sorted_sectors[0][0] if sorted_sectors else 'N/A',
                'worst_sector': sorted_sectors[-1][0] if sorted_sectors else 'N/A',
                'total_sectors': len(sector_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sector performance: {e}")
            return {}
    
    def _calculate_sector_rating(self, avg_change: float, avg_signal_strength: float, buy_signals: int, total_stocks: int) -> str:
        """Calculate overall sector rating"""
        try:
            # Composite score based on multiple factors
            change_score = max(0, min(100, (avg_change + 10) * 5))  # Normalize change to 0-100
            signal_score = avg_signal_strength
            buy_ratio_score = (buy_signals / total_stocks * 100) if total_stocks > 0 else 0
            
            composite_score = (change_score * 0.4) + (signal_score * 0.4) + (buy_ratio_score * 0.2)
            
            if composite_score >= 70:
                return "EXCELLENT"
            elif composite_score >= 60:
                return "GOOD"
            elif composite_score >= 50:
                return "NEUTRAL"
            elif composite_score >= 40:
                return "WEAK"
            else:
                return "POOR"
                
        except Exception:
            return "NEUTRAL"
