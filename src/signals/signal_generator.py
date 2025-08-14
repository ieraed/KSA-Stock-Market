"""
Trading signal generation module
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

from ..analysis.technical_indicators import TechnicalIndicators
from ..data.market_data import MarketDataFetcher

logger = logging.getLogger(__name__)

class TradingSignal:
    """Represents a trading signal"""
    
    def __init__(self, symbol: str, signal_type: str, price: float, timestamp: datetime, 
                 confidence: float, indicators: Dict[str, Any], reason: str):
        self.symbol = symbol
        self.signal_type = signal_type  # 'BUY', 'SELL', 'HOLD'
        self.price = price
        self.timestamp = timestamp
        self.confidence = confidence  # 0.0 to 1.0
        self.indicators = indicators
        self.reason = reason
    
    def __str__(self):
        return f"{self.signal_type} {self.symbol} at {self.price:.2f} SAR (Confidence: {self.confidence:.2f}) - {self.reason}"

class SignalGenerator:
    """Generates trading signals based on technical analysis"""
    
    def __init__(self, data_fetcher, config):
        self.data_fetcher = data_fetcher
        self.config = config
        self.indicators = TechnicalIndicators()
    
    def generate_signals(self, symbol: str, timeframe: str = "1d") -> List[TradingSignal]:
        """
        Generate trading signals for a given symbol
        
        Args:
            symbol: Stock symbol
            timeframe: Data timeframe
        
        Returns:
            List of trading signals
        """
        try:
            # Fetch market data
            data = self.data_fetcher.get_stock_data(symbol, period="6mo", interval=timeframe)
            
            if data is None or data.empty:
                logger.warning(f"No data available for {symbol}")
                return []
            
            # Calculate technical indicators
            indicators_data = self._calculate_indicators(data)
            
            # Generate signals based on multiple strategies
            signals = []
            
            # RSI-based signals
            rsi_signals = self._generate_rsi_signals(symbol, data, indicators_data)
            signals.extend(rsi_signals)
            
            # MACD-based signals
            macd_signals = self._generate_macd_signals(symbol, data, indicators_data)
            signals.extend(macd_signals)
            
            # Bollinger Bands signals
            bb_signals = self._generate_bollinger_signals(symbol, data, indicators_data)
            signals.extend(bb_signals)
            
            # Moving Average signals
            ma_signals = self._generate_ma_signals(symbol, data, indicators_data)
            signals.extend(ma_signals)
            
            # Combine and filter signals
            final_signals = self._combine_signals(signals)
            
            return final_signals
            
        except Exception as e:
            logger.error(f"Error generating signals for {symbol}: {e}")
            return []
    
    def _calculate_indicators(self, data: pd.DataFrame) -> Dict[str, pd.Series]:
        """Calculate all technical indicators"""
        indicators = {}
        
        try:
            close_prices = data['Close']
            high_prices = data['High']
            low_prices = data['Low']
            
            # RSI
            indicators['rsi'] = self.indicators.rsi(close_prices, self.config.rsi_period)
            
            # MACD
            macd_line, signal_line, histogram = self.indicators.macd(
                close_prices, self.config.macd_fast, self.config.macd_slow, self.config.macd_signal
            )
            indicators['macd_line'] = macd_line
            indicators['macd_signal'] = signal_line
            indicators['macd_histogram'] = histogram
            
            # Bollinger Bands
            bb_upper, bb_middle, bb_lower = self.indicators.bollinger_bands(
                close_prices, self.config.bb_period, self.config.bb_std_dev
            )
            indicators['bb_upper'] = bb_upper
            indicators['bb_middle'] = bb_middle
            indicators['bb_lower'] = bb_lower
            
            # Moving Averages
            indicators['sma_short'] = self.indicators.sma(close_prices, self.config.sma_short)
            indicators['sma_long'] = self.indicators.sma(close_prices, self.config.sma_long)
            indicators['ema_short'] = self.indicators.ema(close_prices, self.config.sma_short)
            indicators['ema_long'] = self.indicators.ema(close_prices, self.config.sma_long)
            
            # Stochastic
            stoch_k, stoch_d = self.indicators.stochastic(high_prices, low_prices, close_prices)
            indicators['stoch_k'] = stoch_k
            indicators['stoch_d'] = stoch_d
            
            # Williams %R
            indicators['williams_r'] = self.indicators.williams_r(high_prices, low_prices, close_prices)
            
            # ATR
            indicators['atr'] = self.indicators.atr(high_prices, low_prices, close_prices)
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
        
        return indicators
    
    def _generate_rsi_signals(self, symbol: str, data: pd.DataFrame, indicators: Dict) -> List[TradingSignal]:
        """Generate signals based on RSI"""
        signals = []
        
        try:
            rsi = indicators.get('rsi')
            if rsi is None or rsi.empty:
                return signals
            
            latest_rsi = rsi.iloc[-1]
            latest_price = data['Close'].iloc[-1]
            timestamp = data.index[-1]
            
            if latest_rsi < self.config.rsi_oversold:
                # Oversold condition - potential buy signal
                confidence = min(1.0, (self.config.rsi_oversold - latest_rsi) / 10)
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type="BUY",
                    price=latest_price,
                    timestamp=timestamp,
                    confidence=confidence,
                    indicators={"rsi": latest_rsi},
                    reason=f"RSI oversold at {latest_rsi:.2f}"
                )
                signals.append(signal)
                
            elif latest_rsi > self.config.rsi_overbought:
                # Overbought condition - potential sell signal
                confidence = min(1.0, (latest_rsi - self.config.rsi_overbought) / 10)
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type="SELL",
                    price=latest_price,
                    timestamp=timestamp,
                    confidence=confidence,
                    indicators={"rsi": latest_rsi},
                    reason=f"RSI overbought at {latest_rsi:.2f}"
                )
                signals.append(signal)
                
        except Exception as e:
            logger.error(f"Error generating RSI signals: {e}")
        
        return signals
    
    def _generate_macd_signals(self, symbol: str, data: pd.DataFrame, indicators: Dict) -> List[TradingSignal]:
        """Generate signals based on MACD"""
        signals = []
        
        try:
            macd_line = indicators.get('macd_line')
            macd_signal = indicators.get('macd_signal')
            
            if macd_line is None or macd_signal is None:
                return signals
            
            # Check for MACD crossover
            if len(macd_line) >= 2 and len(macd_signal) >= 2:
                latest_macd = macd_line.iloc[-1]
                prev_macd = macd_line.iloc[-2]
                latest_signal = macd_signal.iloc[-1]
                prev_signal = macd_signal.iloc[-2]
                
                latest_price = data['Close'].iloc[-1]
                timestamp = data.index[-1]
                
                # Bullish crossover (MACD crosses above signal line)
                if prev_macd <= prev_signal and latest_macd > latest_signal:
                    confidence = 0.7
                    signal = TradingSignal(
                        symbol=symbol,
                        signal_type="BUY",
                        price=latest_price,
                        timestamp=timestamp,
                        confidence=confidence,
                        indicators={"macd": latest_macd, "macd_signal": latest_signal},
                        reason="MACD bullish crossover"
                    )
                    signals.append(signal)
                
                # Bearish crossover (MACD crosses below signal line)
                elif prev_macd >= prev_signal and latest_macd < latest_signal:
                    confidence = 0.7
                    signal = TradingSignal(
                        symbol=symbol,
                        signal_type="SELL",
                        price=latest_price,
                        timestamp=timestamp,
                        confidence=confidence,
                        indicators={"macd": latest_macd, "macd_signal": latest_signal},
                        reason="MACD bearish crossover"
                    )
                    signals.append(signal)
                    
        except Exception as e:
            logger.error(f"Error generating MACD signals: {e}")
        
        return signals
    
    def _generate_bollinger_signals(self, symbol: str, data: pd.DataFrame, indicators: Dict) -> List[TradingSignal]:
        """Generate signals based on Bollinger Bands"""
        signals = []
        
        try:
            bb_upper = indicators.get('bb_upper')
            bb_lower = indicators.get('bb_lower')
            
            if bb_upper is None or bb_lower is None:
                return signals
            
            latest_price = data['Close'].iloc[-1]
            latest_upper = bb_upper.iloc[-1]
            latest_lower = bb_lower.iloc[-1]
            timestamp = data.index[-1]
            
            # Price touching lower band - potential buy signal
            if latest_price <= latest_lower:
                confidence = 0.6
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type="BUY",
                    price=latest_price,
                    timestamp=timestamp,
                    confidence=confidence,
                    indicators={"bb_lower": latest_lower, "price": latest_price},
                    reason="Price at Bollinger lower band"
                )
                signals.append(signal)
            
            # Price touching upper band - potential sell signal
            elif latest_price >= latest_upper:
                confidence = 0.6
                signal = TradingSignal(
                    symbol=symbol,
                    signal_type="SELL",
                    price=latest_price,
                    timestamp=timestamp,
                    confidence=confidence,
                    indicators={"bb_upper": latest_upper, "price": latest_price},
                    reason="Price at Bollinger upper band"
                )
                signals.append(signal)
                
        except Exception as e:
            logger.error(f"Error generating Bollinger signals: {e}")
        
        return signals
    
    def _generate_ma_signals(self, symbol: str, data: pd.DataFrame, indicators: Dict) -> List[TradingSignal]:
        """Generate signals based on Moving Average crossovers"""
        signals = []
        
        try:
            sma_short = indicators.get('sma_short')
            sma_long = indicators.get('sma_long')
            
            if sma_short is None or sma_long is None:
                return signals
            
            if len(sma_short) >= 2 and len(sma_long) >= 2:
                latest_short = sma_short.iloc[-1]
                prev_short = sma_short.iloc[-2]
                latest_long = sma_long.iloc[-1]
                prev_long = sma_long.iloc[-2]
                
                latest_price = data['Close'].iloc[-1]
                timestamp = data.index[-1]
                
                # Golden cross (short MA crosses above long MA)
                if prev_short <= prev_long and latest_short > latest_long:
                    confidence = 0.8
                    signal = TradingSignal(
                        symbol=symbol,
                        signal_type="BUY",
                        price=latest_price,
                        timestamp=timestamp,
                        confidence=confidence,
                        indicators={"sma_short": latest_short, "sma_long": latest_long},
                        reason=f"Golden cross: SMA{self.config.sma_short} above SMA{self.config.sma_long}"
                    )
                    signals.append(signal)
                
                # Death cross (short MA crosses below long MA)
                elif prev_short >= prev_long and latest_short < latest_long:
                    confidence = 0.8
                    signal = TradingSignal(
                        symbol=symbol,
                        signal_type="SELL",
                        price=latest_price,
                        timestamp=timestamp,
                        confidence=confidence,
                        indicators={"sma_short": latest_short, "sma_long": latest_long},
                        reason=f"Death cross: SMA{self.config.sma_short} below SMA{self.config.sma_long}"
                    )
                    signals.append(signal)
                    
        except Exception as e:
            logger.error(f"Error generating MA signals: {e}")
        
        return signals
    
    def _combine_signals(self, signals: List[TradingSignal]) -> List[TradingSignal]:
        """Combine and filter signals to avoid conflicts"""
        if not signals:
            return []
        
        # Group signals by type
        buy_signals = [s for s in signals if s.signal_type == "BUY"]
        sell_signals = [s for s in signals if s.signal_type == "SELL"]
        
        final_signals = []
        
        # If we have both buy and sell signals, choose the one with higher confidence
        if buy_signals and sell_signals:
            best_buy = max(buy_signals, key=lambda x: x.confidence)
            best_sell = max(sell_signals, key=lambda x: x.confidence)
            
            if best_buy.confidence > best_sell.confidence:
                final_signals.append(best_buy)
            else:
                final_signals.append(best_sell)
        elif buy_signals:
            # Return the buy signal with highest confidence
            final_signals.append(max(buy_signals, key=lambda x: x.confidence))
        elif sell_signals:
            # Return the sell signal with highest confidence
            final_signals.append(max(sell_signals, key=lambda x: x.confidence))
        
        return final_signals
