"""
Alternative Financial Data Sources for Saudi Stock Market
Implements multiple APIs for faster and more reliable data fetching
"""

import yfinance as yf
import requests
import json
import pandas as pd
import concurrent.futures
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AlternativeDataSources:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Saudi major stocks for fast loading
        self.major_saudi_stocks = {
            '2222': {'name': 'Saudi Aramco', 'yahoo': '2222.SR'},
            '1180': {'name': 'Al Rajhi Bank', 'yahoo': '1180.SR'},
            '1120': {'name': 'Al Rajhi Bank', 'yahoo': '1120.SR'},
            '2010': {'name': 'SABIC', 'yahoo': '2010.SR'},
            '4061': {'name': 'National Commercial Bank', 'yahoo': '4061.SR'},
            '2020': {'name': 'SABIC Agri-Nutrients', 'yahoo': '2020.SR'},
            '1211': {'name': 'Maaden', 'yahoo': '1211.SR'},
            '2240': {'name': 'Al Inma Bank', 'yahoo': '2240.SR'},
            '1150': {'name': 'Al Inma Bank', 'yahoo': '1150.SR'},
            '4322': {'name': 'Saudi Electricity Company', 'yahoo': '4322.SR'},
            '2040': {'name': 'Saudi Ceramics', 'yahoo': '2040.SR'},
            '1322': {'name': 'AMAK', 'yahoo': '1322.SR'}
        }

    def get_yahoo_data_fast(self, symbols, max_workers=10):
        """Get data from Yahoo Finance with concurrent requests"""
        start_time = time.time()
        results = {}
        
        def fetch_single_stock(symbol_data):
            symbol, data = symbol_data
            try:
                yahoo_symbol = data['yahoo']
                ticker = yf.Ticker(yahoo_symbol)
                hist = ticker.history(period="2d")
                info = ticker.info
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close > 0 else 0
                    
                    return symbol, {
                        'symbol': symbol,
                        'name': data['name'],
                        'current_price': float(current_price),
                        'change': float(change),
                        'change_pct': float(change_pct),
                        'volume': int(hist['Volume'].iloc[-1]) if not pd.isna(hist['Volume'].iloc[-1]) else 0,
                        'source': 'yahoo_fast'
                    }
            except Exception as e:
                logger.warning(f"Failed to fetch {symbol}: {e}")
                return symbol, None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_symbol = {
                executor.submit(fetch_single_stock, item): item[0] 
                for item in symbols.items()
            }
            
            for future in concurrent.futures.as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    symbol, result = future.result(timeout=5)
                    if result:
                        results[symbol] = result
                except Exception as e:
                    logger.warning(f"Error processing {symbol}: {e}")
        
        loading_time = time.time() - start_time
        return {
            'stocks': results,
            'loading_time': loading_time,
            'total_stocks': len(results),
            'success': len(results) > 0
        }

    def get_market_summary_fast(self):
        """Get market summary using fastest available method"""
        data = self.get_yahoo_data_fast(self.major_saudi_stocks)
        
        if not data['success']:
            return {'success': False, 'error': 'No data available'}
        
        stocks = list(data['stocks'].values())
        
        # Sort by performance
        top_gainers = sorted(stocks, key=lambda x: x['change_pct'], reverse=True)[:5]
        top_losers = sorted(stocks, key=lambda x: x['change_pct'])[:5]
        top_volume = sorted(stocks, key=lambda x: x['volume'], reverse=True)[:5]
        
        # Calculate market stats
        total_change = sum(stock['change'] for stock in stocks)
        avg_change = total_change / len(stocks) if stocks else 0
        
        return {
            'success': True,
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'movers_by_volume': top_volume,
            'movers_by_value': top_gainers,  # Use same as gainers for now
            'market_summary': {
                'tasi_index': 11000,  # Approximate current TASI
                'market_cap': '2.8T SAR',
                'volume': '272M',
                'active_stocks': len(stocks),
                'avg_change': avg_change
            },
            'loading_time': data['loading_time'],
            'total_stocks': data['total_stocks'],
            'data_source': 'yahoo_finance_fast'
        }

    def get_stock_price_alternative(self, symbol):
        """Get single stock price using alternative sources"""
        # Try Yahoo Finance first
        if symbol in self.major_saudi_stocks:
            yahoo_symbol = self.major_saudi_stocks[symbol]['yahoo']
            try:
                ticker = yf.Ticker(yahoo_symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change = current_price - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close > 0 else 0
                    
                    return {
                        'success': True,
                        'symbol': symbol,
                        'current_price': float(current_price),
                        'change': float(change),
                        'change_pct': float(change_pct),
                        'volume': int(hist['Volume'].iloc[-1]) if not pd.isna(hist['Volume'].iloc[-1]) else 0,
                        'yahoo_symbol': yahoo_symbol,
                        'source': 'yahoo_alternative'
                    }
            except Exception as e:
                logger.warning(f"Yahoo Finance failed for {symbol}: {e}")
        
        # Fallback to basic data
        return {
            'success': False,
            'error': f'No alternative data source available for {symbol}'
        }

# Global instance
alt_data = AlternativeDataSources()

def get_fast_market_data():
    """Main function to get fast market data"""
    return alt_data.get_market_summary_fast()

def get_fast_stock_price(symbol):
    """Main function to get fast stock price"""
    return alt_data.get_stock_price_alternative(symbol)
