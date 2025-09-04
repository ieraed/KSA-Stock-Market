"""
Core Market Data Fetcher - Optimized for Performance
Separated from main fetcher to reduce loading time
"""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional, Tuple
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_stock_price_fast(symbol: str, yahoo_suffix: str = ".SR") -> Optional[Dict]:
    """
    Fast stock price fetcher with minimal overhead
    """
    try:
        yahoo_symbol = f"{symbol}{yahoo_suffix}"
        ticker = yf.Ticker(yahoo_symbol)
        
        # Get minimal data for speed
        info = ticker.info
        hist = ticker.history(period="2d")
        
        if len(hist) < 2:
            return None
            
        current_price = hist['Close'].iloc[-1]
        previous_price = hist['Close'].iloc[-2]
        change = current_price - previous_price
        change_percent = (change / previous_price) * 100
        
        return {
            'symbol': symbol,
            'yahoo_symbol': yahoo_symbol,
            'current_price': round(current_price, 2),
            'previous_price': round(previous_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_percent, 2),
            'success': True
        }
    except Exception as e:
        logger.debug(f"Error fetching {symbol}: {e}")
        return None

def fetch_batch_prices(symbols: List[str], max_workers: int = 10) -> List[Dict]:
    """
    Fetch multiple stock prices concurrently for better performance
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_symbol = {
            executor.submit(get_stock_price_fast, symbol): symbol 
            for symbol in symbols
        }
        
        # Collect results with timeout
        for future in as_completed(future_to_symbol, timeout=30):
            try:
                result = future.result(timeout=5)
                if result and result.get('success'):
                    results.append(result)
            except Exception as e:
                symbol = future_to_symbol[future]
                logger.debug(f"Failed to fetch {symbol}: {e}")
    
    return results

def get_top_performers(stocks_data: List[Dict], count: int = 5) -> Tuple[List[Dict], List[Dict]]:
    """
    Sort stocks by performance and return top gainers/losers
    """
    # Sort by change_percent
    sorted_stocks = sorted(stocks_data, key=lambda x: x['change_percent'], reverse=True)
    
    top_gainers = sorted_stocks[:count]
    top_losers = sorted_stocks[-count:][::-1]  # Reverse to show worst first
    
    return top_gainers, top_losers

# Core stock symbols for fast loading (most liquid and important stocks)
CORE_SYMBOLS = [
    # Major Banks
    "1180", "1120", "1150", "1140", "1160",
    # Energy & Petrochemicals  
    "2222", "2010", "2350", "2020", "2310",
    # Telecom & Technology
    "7010", "7020", "4003", "4004", "4005",
    # Materials & Industrial
    "1321", "2040", "2080", "1201", "1202",
    # Healthcare & Consumer
    "4001", "4002", "6001", "6002", "6010"
]

def get_fast_market_summary() -> Dict:
    """
    Get market summary using fast method with cached stock list
    Returns REAL live data, not demo data
    """
    try:
        # Try to get cached stocks first
        from .stock_cache import get_core_stocks
        core_stocks = get_core_stocks()
        symbols = [stock['symbol'] for stock in core_stocks[:30]]  # 30 stocks for fast mode
    except ImportError:
        symbols = CORE_SYMBOLS[:30]
    
    logger.info(f"🚀 Fast market summary: Processing {len(symbols)} stocks with live data...")
    
    start_time = time.time()
    
    # Fetch live stock prices
    stock_data = fetch_batch_prices(symbols, max_workers=15)
    
    if not stock_data:
        return {
            "top_gainers": [],
            "top_losers": [],
            "error": "No live data available",
            "loading_time": time.time() - start_time,
            "performance_mode": "fast"
        }
    
    # Get top performers
    top_gainers, top_losers = get_top_performers(stock_data, count=10)
    
    end_time = time.time()
    logger.info(f"✅ Fast summary completed in {end_time - start_time:.2f} seconds")
    
    return {
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "total_stocks": len(stock_data),
        "loading_time": round(end_time - start_time, 2),
        "performance_mode": "fast",
        "success": True,  # Add success flag
        "data_source": "Live Yahoo Finance",
        "timestamp": end_time
    }
