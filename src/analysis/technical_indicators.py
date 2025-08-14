"""
Technical analysis indicators for stock market analysis
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class TechnicalIndicators:
    """Technical analysis indicators for stock market analysis"""
    
    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Relative Strength Index (RSI)
        
        Args:
            data: Price data (typically closing prices)
            period: Period for RSI calculation
        
        Returns:
            RSI values as pandas Series
        """
        try:
            delta = data.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return pd.Series()
    
    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        
        Args:
            data: Price data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line EMA period
        
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        try:
            ema_fast = data.ewm(span=fast).mean()
            ema_slow = data.ewm(span=slow).mean()
            
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            return macd_line, signal_line, histogram
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands
        
        Args:
            data: Price data
            period: Period for moving average
            std_dev: Standard deviation multiplier
        
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        try:
            middle_band = data.rolling(window=period).mean()
            std = data.rolling(window=period).std()
            
            upper_band = middle_band + (std * std_dev)
            lower_band = middle_band - (std * std_dev)
            
            return upper_band, middle_band, lower_band
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return pd.Series(), pd.Series(), pd.Series()
    
    @staticmethod
    def sma(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Simple Moving Average (SMA)
        
        Args:
            data: Price data
            period: Period for moving average
        
        Returns:
            SMA values as pandas Series
        """
        try:
            return data.rolling(window=period).mean()
        except Exception as e:
            logger.error(f"Error calculating SMA: {e}")
            return pd.Series()
    
    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average (EMA)
        
        Args:
            data: Price data
            period: Period for moving average
        
        Returns:
            EMA values as pandas Series
        """
        try:
            return data.ewm(span=period).mean()
        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return pd.Series()
    
    @staticmethod
    def stochastic(high: pd.Series, low: pd.Series, close: pd.Series, k_period: int = 14, d_period: int = 3) -> Tuple[pd.Series, pd.Series]:
        """
        Calculate Stochastic Oscillator
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            k_period: Period for %K calculation
            d_period: Period for %D calculation
        
        Returns:
            Tuple of (%K, %D)
        """
        try:
            lowest_low = low.rolling(window=k_period).min()
            highest_high = high.rolling(window=k_period).max()
            
            k_percent = ((close - lowest_low) / (highest_high - lowest_low)) * 100
            d_percent = k_percent.rolling(window=d_period).mean()
            
            return k_percent, d_percent
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {e}")
            return pd.Series(), pd.Series()
    
    @staticmethod
    def williams_r(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Williams %R
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Period for calculation
        
        Returns:
            Williams %R values as pandas Series
        """
        try:
            highest_high = high.rolling(window=period).max()
            lowest_low = low.rolling(window=period).min()
            
            williams_r = ((highest_high - close) / (highest_high - lowest_low)) * -100
            
            return williams_r
        except Exception as e:
            logger.error(f"Error calculating Williams %R: {e}")
            return pd.Series()
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Calculate Average True Range (ATR)
        
        Args:
            high: High prices
            low: Low prices
            close: Close prices
            period: Period for calculation
        
        Returns:
            ATR values as pandas Series
        """
        try:
            prev_close = close.shift(1)
            
            tr1 = high - low
            tr2 = abs(high - prev_close)
            tr3 = abs(low - prev_close)
            
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=period).mean()
            
            return atr
        except Exception as e:
            logger.error(f"Error calculating ATR: {e}")
            return pd.Series()
