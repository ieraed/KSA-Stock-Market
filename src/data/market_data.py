"""
Market data fetching module for Saudi stocks
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Optional, Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MarketDataFetcher:
    """Fetches market data for Saudi stocks"""
    
    def __init__(self, config):
        self.config = config
        self.saudi_stocks = {
            "2222.SR": "Saudi Aramco",
            "1120.SR": "Al Rajhi Bank", 
            "2030.SR": "SABIC",
            "4030.SR": "Riyad Bank",
            "1210.SR": "The Saudi National Bank",
            "2020.SR": "SABIC Agri-Nutrients",
            "1180.SR": "Al Rajhi Takaful",
            "2380.SR": "Petrochemical Industries Co",
            "1140.SR": "Banque Saudi Fransi",
            "4290.SR": "Al Kathiri Holding"
        }
    
    def get_stock_data(self, symbol: str, period: str = None, interval: str = None) -> Optional[pd.DataFrame]:
        """
        Fetch stock data for a given symbol
        
        Args:
            symbol: Stock symbol (e.g., "2222.SR" for Saudi Aramco)
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            period = period or self.config.default_period
            interval = interval or self.config.default_interval
            
            logger.info(f"Fetching data for {symbol} - period: {period}, interval: {interval}")
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data found for symbol {symbol}")
                return None
            
            # Clean and prepare data
            data = self._clean_data(data)
            
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_multiple_stocks_data(self, symbols: List[str], period: str = None, interval: str = None) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple stocks
        
        Args:
            symbols: List of stock symbols
            period: Data period
            interval: Data interval
        
        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        results = {}
        
        for symbol in symbols:
            data = self.get_stock_data(symbol, period, interval)
            if data is not None:
                results[symbol] = data
        
        return results
    
    def get_popular_saudi_stocks(self) -> List[str]:
        """Get list of popular Saudi stock symbols"""
        return list(self.saudi_stocks.keys())
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get basic information about a stock
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Dictionary with stock information
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Add Saudi-specific information
            if symbol in self.saudi_stocks:
                info['saudi_name'] = self.saudi_stocks[symbol]
                info['market'] = 'Tadawul'
                info['currency'] = 'SAR'
            
            return info
            
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {e}")
            return None
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare market data
        
        Args:
            data: Raw market data
        
        Returns:
            Cleaned DataFrame
        """
        # Remove any rows with NaN values
        data = data.dropna()
        
        # Ensure proper column names
        data.columns = data.columns.str.title()
        
        # Add additional calculated columns
        data['Price_Change'] = data['Close'].diff()
        data['Price_Change_Pct'] = data['Close'].pct_change() * 100
        data['High_Low_Pct'] = ((data['High'] - data['Low']) / data['Close']) * 100
        
        return data
    
    def is_market_open(self) -> bool:
        """
        Check if Saudi market is currently open
        
        Returns:
            True if market is open, False otherwise
        """
        try:
            from datetime import datetime
            import pytz
            
            # Saudi market timezone
            saudi_tz = pytz.timezone('Asia/Riyadh')
            now = datetime.now(saudi_tz)
            
            # Check if it's a trading day (Sunday to Thursday)
            if now.weekday() in [5, 6]:  # Friday, Saturday
                return False
            
            # Check trading hours (10:00 AM to 3:00 PM)
            market_open = now.replace(hour=10, minute=0, second=0, microsecond=0)
            market_close = now.replace(hour=15, minute=0, second=0, microsecond=0)
            
            return market_open <= now <= market_close
            
        except Exception as e:
            logger.error(f"Error checking market status: {e}")
            return False
