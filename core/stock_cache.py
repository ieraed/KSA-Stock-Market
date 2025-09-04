"""
Cached Stock Database for Saudi Stock Market App
Stores stock symbols, names, and basic info for fast loading
"""

import json
import os
import time
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class StockCache:
    def __init__(self, cache_file: str = "data/stock_cache.json"):
        self.cache_file = cache_file
        self.cache_timeout = 24 * 60 * 60  # 24 hours
        self.cache = self._load_cache()
        
    def _load_cache(self) -> Dict:
        """Load cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    
                # Check if cache is still valid
                if self._is_cache_valid(cache_data):
                    logger.info(f"✅ Loaded {len(cache_data.get('stocks', []))} stocks from cache")
                    return cache_data
                else:
                    logger.info("⏰ Cache expired, will refresh")
            
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
        
        return {"stocks": [], "timestamp": 0, "version": "1.0"}
    
    def _is_cache_valid(self, cache_data: Dict) -> bool:
        """Check if cache is still valid"""
        timestamp = cache_data.get('timestamp', 0)
        return (time.time() - timestamp) < self.cache_timeout
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            
            # Update timestamp
            self.cache['timestamp'] = time.time()
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            
            logger.info(f"💾 Saved {len(self.cache.get('stocks', []))} stocks to cache")
            
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def get_cached_stocks(self) -> List[Dict]:
        """Get stocks from cache"""
        return self.cache.get('stocks', [])
    
    def update_cache(self, stocks: List[Dict]):
        """Update cache with new stock data"""
        self.cache['stocks'] = stocks
        self.cache['timestamp'] = time.time()
        self._save_cache()
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """Get specific stock info from cache"""
        stocks = self.get_cached_stocks()
        for stock in stocks:
            if stock.get('symbol') == symbol:
                return stock
        return None
    
    def search_stocks(self, query: str) -> List[Dict]:
        """Search stocks by symbol or name"""
        query = query.upper()
        stocks = self.get_cached_stocks()
        results = []
        
        for stock in stocks:
            symbol = stock.get('symbol', '').upper()
            name = stock.get('name', '').upper()
            
            if query in symbol or query in name:
                results.append(stock)
        
        return results

# Pre-defined core Saudi stocks for immediate loading
CORE_SAUDI_STOCKS = [
    # Major Banks
    {"symbol": "1180", "name": "SAUDI NATIONAL BANK", "sector": "Banks"},
    {"symbol": "1120", "name": "AL RAJHI BANK", "sector": "Banks"},
    {"symbol": "1150", "name": "ALINMA BANK", "sector": "Banks"},
    {"symbol": "1140", "name": "BANK ALBILAD", "sector": "Banks"},
    {"symbol": "1160", "name": "NATIONAL COMMERCIAL BANK", "sector": "Banks"},
    
    # Energy & Petrochemicals
    {"symbol": "2222", "name": "SAUDI ARABIAN OIL COMPANY", "sector": "Energy"},
    {"symbol": "2010", "name": "SAUDI BASIC INDUSTRIES CORP", "sector": "Materials"},
    {"symbol": "2350", "name": "SAUDI KAYAN PETROCHEMICAL", "sector": "Materials"},
    {"symbol": "2020", "name": "SABIC AGRI-NUTRIENTS", "sector": "Materials"},
    {"symbol": "2310", "name": "SIBUR HOLDING", "sector": "Materials"},
    
    # Telecom & Technology
    {"symbol": "7010", "name": "SAUDI TELECOM COMPANY", "sector": "Telecommunication"},
    {"symbol": "7020", "name": "ETIHAD ETISALAT", "sector": "Telecommunication"},
    {"symbol": "4003", "name": "EXTRA", "sector": "Consumer Discretionary"},
    {"symbol": "4004", "name": "DUBAI ISLAMIC BANK", "sector": "Banks"},
    {"symbol": "4005", "name": "RIYAD BANK", "sector": "Banks"},
    
    # Materials & Industrial
    {"symbol": "1321", "name": "EAST PIPES", "sector": "Materials"},
    {"symbol": "2040", "name": "SAUDI CERAMICS", "sector": "Materials"},
    {"symbol": "2080", "name": "GASCO", "sector": "Energy"},
    {"symbol": "1201", "name": "SAUDI CEMENT", "sector": "Materials"},
    {"symbol": "1202", "name": "SOUTHERN PROVINCE CEMENT", "sector": "Materials"},
    
    # Healthcare & Consumer
    {"symbol": "4001", "name": "DALLAH HEALTHCARE", "sector": "Healthcare"},
    {"symbol": "4002", "name": "AL MOUWASAT MEDICAL SERVICES", "sector": "Healthcare"},
    {"symbol": "6001", "name": "HALWANI BROS", "sector": "Food & Beverages"},
    {"symbol": "6002", "name": "HERFY FOOD SERVICES", "sector": "Food & Beverages"},
    {"symbol": "6010", "name": "ALDREES PETROLEUM", "sector": "Energy"}
]

def get_core_stocks() -> List[Dict]:
    """Get core stocks for immediate loading"""
    return CORE_SAUDI_STOCKS.copy()

def initialize_stock_cache():
    """Initialize stock cache with core stocks if empty"""
    cache = StockCache()
    
    # If cache is empty or invalid, initialize with core stocks
    cached_stocks = cache.get_cached_stocks()
    if not cached_stocks:
        logger.info("🔄 Initializing cache with core stocks...")
        cache.update_cache(CORE_SAUDI_STOCKS)
        return CORE_SAUDI_STOCKS
    
    return cached_stocks

# Global cache instance
stock_cache = StockCache()
