"""
🇸🇦 Saudi Exchange Integration Module
Integrates continuous data fetching with the existing trading application
"""

import json
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional
import asyncio
from continuous_data_fetcher import ContinuousSaudiExchangeFetcher, StockData
import sqlite3
import os

logger = logging.getLogger(__name__)

class SaudiExchangeDataManager:
    """
    High-level data manager that integrates continuous fetching
    with the existing trading application
    """
    
    def __init__(self, update_interval: int = 30, enable_continuous: bool = True):
        """
        Initialize the data manager
        
        Args:
            update_interval: Seconds between updates (default: 30)
            enable_continuous: Whether to enable continuous fetching
        """
        self.fetcher = ContinuousSaudiExchangeFetcher(update_interval=update_interval)
        self.enable_continuous = enable_continuous
        self.data_cache = {}
        self.last_update = None
        
        # Setup callbacks
        self.fetcher.add_callback(self._on_data_update)
        
        # Database paths
        self.main_db_path = "saudi_stocks_database.json"
        self.backup_db_path = "saudi_stocks_database_backup.json"
        
        logger.info("🚀 Saudi Exchange Data Manager initialized")
    
    def _on_data_update(self, stocks: Dict[str, StockData]):
        """Callback for continuous data updates"""
        self.data_cache = stocks
        self.last_update = datetime.now()
        
        # Update main database file
        self._update_main_database(stocks)
        
        logger.info(f"📊 Cache updated with {len(stocks)} stocks")
    
    def _update_main_database(self, stocks: Dict[str, StockData]):
        """Update the main JSON database file used by the application"""
        try:
            # Convert to the format expected by the existing application
            database_format = {}
            
            for symbol, stock in stocks.items():
                # Add .SR suffix if not present (for compatibility)
                symbol_key = f"{symbol}.SR" if not symbol.endswith('.SR') else symbol
                
                database_format[symbol_key] = {
                    "name_en": stock.name,
                    "name_ar": stock.name,  # Use English name as fallback
                    "sector": "Unknown",  # Will be populated from existing data
                    "price": stock.price,
                    "change": stock.change or 0,
                    "change_percent": stock.change_percent or 0,
                    "volume": 0,  # Not available from this source
                    "market_cap": 0,  # Not available from this source
                    "last_update": stock.timestamp.isoformat(),
                    "currency": "SAR"
                }
            
            # Merge with existing database to preserve sector information
            existing_data = self._load_existing_database()
            if existing_data:
                for symbol, stock_data in database_format.items():
                    if symbol in existing_data:
                        # Preserve existing sector and other metadata
                        stock_data["sector"] = existing_data[symbol].get("sector", "Unknown")
                        stock_data["name_ar"] = existing_data[symbol].get("name_ar", stock_data["name_en"])
            
            # Backup current database
            if os.path.exists(self.main_db_path):
                os.makedirs("backup", exist_ok=True)
                backup_filename = f"backup/saudi_stocks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                os.rename(self.main_db_path, backup_filename)
            
            # Save updated database
            with open(self.main_db_path, 'w', encoding='utf-8') as f:
                json.dump(database_format, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Updated main database with {len(database_format)} stocks")
            
        except Exception as e:
            logger.error(f"❌ Failed to update main database: {e}")
    
    def _load_existing_database(self) -> Dict:
        """Load existing database for merging"""
        try:
            if os.path.exists(self.main_db_path):
                with open(self.main_db_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"❌ Failed to load existing database: {e}")
        return {}
    
    def start(self):
        """Start the data manager"""
        if self.enable_continuous:
            self.fetcher.start_continuous_fetching()
            logger.info("✅ Continuous data fetching started")
        else:
            # Perform one-time fetch
            stocks = self.fetcher.fetch_current_data()
            if stocks:
                self._on_data_update(stocks)
    
    def stop(self):
        """Stop the data manager"""
        if self.enable_continuous:
            self.fetcher.stop_continuous_fetching()
            logger.info("🛑 Continuous data fetching stopped")
    
    def get_latest_stocks(self) -> Dict[str, Dict]:
        """
        Get latest stock data in the format expected by the trading application
        
        Returns:
            Dictionary in the format used by saudi_exchange_fetcher.py
        """
        if not self.data_cache:
            # Try to fetch fresh data
            stocks = self.fetcher.fetch_current_data()
            if stocks:
                self.data_cache = stocks
        
        # Convert to expected format
        result = {}
        for symbol, stock in self.data_cache.items():
            symbol_key = f"{symbol}.SR" if not symbol.endswith('.SR') else symbol
            result[symbol_key] = {
                "name_en": stock.name,
                "name_ar": stock.name,
                "sector": "Unknown",
                "price": stock.price,
                "change": stock.change or 0,
                "change_percent": stock.change_percent or 0,
                "volume": 0,
                "market_cap": 0,
                "last_update": stock.timestamp.isoformat(),
                "currency": "SAR"
            }
        
        return result
    
    def get_stock_by_symbol(self, symbol: str) -> Optional[Dict]:
        """Get specific stock by symbol"""
        # Remove .SR suffix for lookup
        clean_symbol = symbol.replace('.SR', '')
        
        stock = self.fetcher.get_stock(clean_symbol)
        if stock:
            return {
                "symbol": symbol,
                "name_en": stock.name,
                "name_ar": stock.name,
                "price": stock.price,
                "change": stock.change or 0,
                "change_percent": stock.change_percent or 0,
                "last_update": stock.timestamp.isoformat(),
                "currency": "SAR"
            }
        return None
    
    def get_market_summary(self) -> Dict:
        """Get market summary statistics"""
        stats = self.fetcher.get_statistics()
        
        return {
            "total_stocks": stats.get("total_stocks", 259),  # Use official count
            "gainers": stats.get("gainers_count", 0),
            "losers": stats.get("losers_count", 0),
            "unchanged": stats.get("unchanged_count", 0),
            "avg_change": stats.get("avg_change_percent", 0),
            "max_gain": stats.get("max_gain", 0),
            "max_loss": stats.get("max_loss", 0),
            "last_update": stats.get("last_update"),
            "market_status": self._get_market_status()
        }
    
    def _get_market_status(self) -> str:
        """Determine market status based on Saudi trading hours"""
        now = datetime.now()
        
        # Saudi market hours: Sunday to Thursday, 10:00 AM to 3:00 PM
        if now.weekday() in [5, 6]:  # Friday (5) and Saturday (6)
            return "closed"
        
        current_time = now.time()
        market_open = datetime.strptime("10:00", "%H:%M").time()
        market_close = datetime.strptime("15:00", "%H:%M").time()
        
        if market_open <= current_time <= market_close:
            return "open"
        else:
            return "closed"
    
    def get_top_movers(self, limit: int = 10) -> Dict:
        """Get top gainers and losers"""
        return {
            "gainers": [
                {
                    "symbol": f"{stock.symbol}.SR",
                    "name": stock.name,
                    "price": stock.price,
                    "change_percent": stock.change_percent
                }
                for stock in self.fetcher.get_top_gainers(limit)
            ],
            "losers": [
                {
                    "symbol": f"{stock.symbol}.SR",
                    "name": stock.name,
                    "price": stock.price,
                    "change_percent": stock.change_percent
                }
                for stock in self.fetcher.get_top_losers(limit)
            ]
        }
    
    def export_current_data(self, format: str = "json") -> str:
        """Export current data in various formats"""
        if format == "json":
            return self.fetcher.export_to_json()
        elif format == "csv":
            return self._export_to_csv()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_to_csv(self) -> str:
        """Export data to CSV format"""
        filename = f"saudi_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        data = []
        for symbol, stock in self.data_cache.items():
            data.append({
                'Symbol': symbol,
                'Name': stock.name,
                'Price': stock.price,
                'Change': stock.change,
                'Change%': stock.change_percent,
                'Timestamp': stock.timestamp.isoformat()
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        logger.info(f"📄 Exported {len(data)} stocks to {filename}")
        return filename
    
    def get_historical_data(self, symbol: str, days: int = 7) -> List[Dict]:
        """Get historical data for a symbol from database"""
        try:
            conn = sqlite3.connect(self.fetcher.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, price, change_value, change_percent
                FROM stock_data
                WHERE symbol = ? AND timestamp >= datetime('now', '-{} days')
                ORDER BY timestamp ASC
            '''.format(days), (symbol.replace('.SR', ''),))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'timestamp': row[0],
                    'price': row[1],
                    'change': row[2],
                    'change_percent': row[3]
                }
                for row in rows
            ]
            
        except Exception as e:
            logger.error(f"❌ Failed to get historical data: {e}")
            return []
    
    def is_data_fresh(self, max_age_minutes: int = 5) -> bool:
        """Check if cached data is fresh"""
        if not self.last_update:
            return False
        
        age = datetime.now() - self.last_update
        return age.total_seconds() < (max_age_minutes * 60)

# Global instance for easy access
_data_manager = None

def get_data_manager() -> SaudiExchangeDataManager:
    """Get the global data manager instance"""
    global _data_manager
    if _data_manager is None:
        _data_manager = SaudiExchangeDataManager()
        _data_manager.start()
    return _data_manager

def get_all_saudi_stocks() -> Dict:
    """
    Compatibility function for existing code
    Returns stock data in the expected format
    """
    manager = get_data_manager()
    return manager.get_latest_stocks()

def get_market_summary() -> Dict:
    """
    Compatibility function for existing code
    Returns market summary
    """
    manager = get_data_manager()
    return manager.get_market_summary()

def cleanup():
    """Cleanup function to stop data fetching"""
    global _data_manager
    if _data_manager:
        _data_manager.stop()
        _data_manager = None

# Register cleanup on module exit
import atexit
atexit.register(cleanup)
