"""
Performance Optimizer for Saudi Stock Market App
Separates performance-critical functions for faster loading
"""

import pandas as pd
from typing import Dict, List, Optional
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import json

# Import caching
try:
    from .stock_cache import stock_cache, get_core_stocks, initialize_stock_cache
    CACHE_AVAILABLE = True
except ImportError:
    CACHE_AVAILABLE = False
    print("❌ Cache module not available")

logger = logging.getLogger(__name__)

class PerformanceOptimizer:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 60  # 1 minute cache
        
    def get_cached_data(self, key: str) -> Optional[Dict]:
        """Get cached data if still valid"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_timeout:
                return data
        return None
    
    def set_cache(self, key: str, data: Dict):
        """Set cache with timestamp"""
        self.cache[key] = (data, time.time())
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()

class FastStockFetcher:
    """Optimized stock data fetcher with minimal dependencies"""
    
    @staticmethod
    def minimal_stock_data(symbol: str) -> Optional[Dict]:
        """Get essential stock data with minimal API calls"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(f"{symbol}.SR")
            
            # Get only essential data
            hist = ticker.history(period="2d", actions=False, dividends=False, splits=False)
            
            if len(hist) < 2:
                return None
                
            current_price = hist['Close'].iloc[-1]
            previous_price = hist['Close'].iloc[-2]
            change = current_price - previous_price
            change_percent = (change / previous_price) * 100
            
            return {
                'symbol': symbol,
                'price': round(float(current_price), 2),
                'change': round(float(change), 2),
                'change_percent': round(float(change_percent), 2)
            }
        except Exception as e:
            logger.debug(f"Error fetching {symbol}: {e}")
            return None

def get_priority_stocks() -> List[str]:
    """Get priority stocks for fastest loading - now using cache"""
    if CACHE_AVAILABLE:
        try:
            cached_stocks = stock_cache.get_cached_stocks()
            if cached_stocks:
                # Return symbols from cache (limit to 12 for super fast mode)
                return [stock['symbol'] for stock in cached_stocks[:12]]
        except Exception as e:
            logger.debug(f"Cache error: {e}")
    
    # Fallback to hardcoded core symbols
    return [
        # Top liquid banks
        "1180", "1120", "1150",
        # Major energy
        "2222", "2010", "2350",
        # Key industrials  
        "1321", "2040", "2080",
        # Telecom leaders
        "7010", "7020",
        # Top performers
        "4002"
    ]

def get_fast_stocks() -> List[str]:
    """Get expanded stock list for fast mode - 25 stocks"""
    if CACHE_AVAILABLE:
        try:
            cached_stocks = stock_cache.get_cached_stocks()
            if cached_stocks:
                return [stock['symbol'] for stock in cached_stocks[:25]]
        except Exception as e:
            logger.debug(f"Cache error: {e}")
    
    # Fallback 
    priority = get_priority_stocks()
    additional = ["4001", "6001", "2090", "3080", "1202", "4020", "6050", "1182", "4180", "4191", "4270", "2130", "4160"]
    return priority + additional[:25-len(priority)]

def parallel_fetch_stocks(symbols: List[str], max_workers: int = 8) -> List[Dict]:
    """Fetch stocks in parallel with optimized threading"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all fetches
        futures = {
            executor.submit(FastStockFetcher.minimal_stock_data, symbol): symbol 
            for symbol in symbols
        }
        
        # Collect results with timeout
        for future in futures:
            try:
                result = future.result(timeout=3)  # 3 second timeout per stock
                if result:
                    results.append(result)
            except Exception as e:
                symbol = futures[future]
                logger.debug(f"Timeout/error for {symbol}: {e}")
    
    return results

def get_super_fast_summary() -> Dict:
    """Ultra-fast market summary using priority stocks only"""
    logger.info("⚡ Getting super-fast market summary...")
    
    start_time = time.time()
    
    # Get priority stocks only
    priority_symbols = get_priority_stocks()
    
    # Fetch in parallel
    stock_data = parallel_fetch_stocks(priority_symbols, max_workers=12)
    
    if not stock_data:
        return {"error": "No data available", "loading_time": 0}
    
    # Quick sort
    stock_data.sort(key=lambda x: x['change_percent'], reverse=True)
    
    end_time = time.time()
    loading_time = end_time - start_time
    
    logger.info(f"✅ Super-fast summary: {loading_time:.2f}s for {len(stock_data)} stocks")
    
    return {
        "top_gainers": stock_data[:5],
        "top_losers": stock_data[-5:][::-1],
        "total_stocks": len(stock_data),
        "loading_time": round(loading_time, 2),
        "performance_mode": "super_fast"
    }

# Global performance optimizer instance
perf_optimizer = PerformanceOptimizer()
