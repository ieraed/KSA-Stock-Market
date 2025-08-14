"""
Enhanced Tadawul Data Integration
Better integration with Saudi stock exchange data sources
"""

import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Optional, Tuple

class TadawulDataProvider:
    """Enhanced data provider for Saudi stocks with better accuracy"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Enhanced Saudi stock symbols with better mappings
        self.saudi_stocks_enhanced = {
            # Major Banks
            '1180.SR': {'name': 'Al Rajhi Bank', 'sector': 'Banks', 'tadawul_code': '1180'},
            '1120.SR': {'name': 'Riyad Bank', 'sector': 'Banks', 'tadawul_code': '1120'},
            '1030.SR': {'name': 'Samba Financial Group', 'sector': 'Banks', 'tadawul_code': '1030'},
            '1060.SR': {'name': 'Saudi British Bank', 'sector': 'Banks', 'tadawul_code': '1060'},
            
            # Energy Sector
            '2222.SR': {'name': 'Saudi Aramco', 'sector': 'Energy', 'tadawul_code': '2222'},
            '2030.SR': {'name': 'Saudi Electricity Company', 'sector': 'Energy', 'tadawul_code': '2030'},
            '2010.SR': {'name': 'Saudi Basic Industries Corporation', 'sector': 'Petrochemicals', 'tadawul_code': '2010'},
            
            # From your image - Top Gainers
            '1302.SR': {'name': 'BAWAN Company', 'sector': 'Real Estate', 'tadawul_code': '1302'},
            '1201.SR': {'name': 'Banaja for Trading', 'sector': 'Retail', 'tadawul_code': '1201'},
            '8312.SR': {'name': 'Al Sagr Insurance', 'sector': 'Insurance', 'tadawul_code': '8312'},
            '1020.SR': {'name': 'Entaj', 'sector': 'Food & Beverages', 'tadawul_code': '1020'},
            '4162.SR': {'name': 'Medgulf', 'sector': 'Healthcare', 'tadawul_code': '4162'},
            
            # From your image - Top Losers  
            '6004.SR': {'name': 'Abo Moati Company', 'sector': 'Retail', 'tadawul_code': '6004'},
            '4013.SR': {'name': 'Alhammadi Company', 'sector': 'Retail', 'tadawul_code': '4013'},
            '1321.SR': {'name': 'SRMG', 'sector': 'Media', 'tadawul_code': '1321'},
            '4003.SR': {'name': 'Cenomi Retail', 'sector': 'Retail', 'tadawul_code': '4003'},
            '4004.SR': {'name': 'Cenomi Centers', 'sector': 'Real Estate', 'tadawul_code': '4004'},
            
            # Telecommunications
            '7010.SR': {'name': 'Saudi Telecom Company', 'sector': 'Telecommunications', 'tadawul_code': '7010'},
            '7020.SR': {'name': 'Etihad Etisalat (Mobily)', 'sector': 'Telecommunications', 'tadawul_code': '7020'},
            '7030.SR': {'name': 'Zain Saudi Arabia', 'sector': 'Telecommunications', 'tadawul_code': '7030'},
            
            # Additional Major Stocks
            '2380.SR': {'name': 'Saudi Electricity Company', 'sector': 'Utilities', 'tadawul_code': '2380'},
            '1211.SR': {'name': 'Al Anwar Holdings', 'sector': 'Investment', 'tadawul_code': '1211'},
            '4290.SR': {'name': 'The Kuwaiti Danish Dairy Co.', 'sector': 'Food & Beverages', 'tadawul_code': '4290'},
        }
    
    def get_enhanced_stock_data(self, symbol: str, period: str = "1d") -> Optional[Dict]:
        """Get enhanced stock data with better accuracy"""
        try:
            # Get data from yfinance
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            info = ticker.info
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Open'].iloc[-1]
            change = current_price - previous_close
            change_pct = (change / previous_close) * 100
            
            # Get enhanced info
            stock_info = self.saudi_stocks_enhanced.get(symbol, {})
            
            return {
                'symbol': symbol,
                'tadawul_code': stock_info.get('tadawul_code', symbol.replace('.SR', '')),
                'company_name': stock_info.get('name', info.get('longName', symbol)),
                'sector': stock_info.get('sector', 'Other'),
                'current_price': float(current_price),
                'previous_close': float(previous_close),
                'change': float(change),
                'change_pct': float(change_pct),
                'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                'high': float(hist['High'].iloc[-1]),
                'low': float(hist['Low'].iloc[-1]),
                'open': float(hist['Open'].iloc[-1]),
                'market_cap': info.get('marketCap', 0),
                'timestamp': datetime.now(),
                'data_source': 'yfinance_enhanced'
            }
            
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_market_movers(self, top_n: int = 10) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Get top gainers and losers from Saudi market"""
        all_data = []
        
        print("Fetching Saudi market data...")
        
        for symbol in self.saudi_stocks_enhanced.keys():
            data = self.get_enhanced_stock_data(symbol)
            if data:
                all_data.append(data)
            time.sleep(0.1)  # Rate limiting
        
        if not all_data:
            return pd.DataFrame(), pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        
        # Sort by change percentage
        gainers = df[df['change_pct'] > 0].nlargest(top_n, 'change_pct')
        losers = df[df['change_pct'] < 0].nsmallest(top_n, 'change_pct')
        
        return gainers, losers
    
    def format_market_movers_display(self, gainers: pd.DataFrame, losers: pd.DataFrame) -> Dict:
        """Format market movers for display similar to Tadawul"""
        
        def format_stock_row(row):
            return {
                'symbol': row['tadawul_code'],
                'name': row['company_name'][:20] + '...' if len(row['company_name']) > 20 else row['company_name'],
                'price': f"{row['current_price']:.2f}",
                'change': f"{row['change']:+.2f} ({row['change_pct']:+.2f}%)",
                'change_pct': row['change_pct'],
                'sector': row['sector']
            }
        
        gainers_formatted = []
        losers_formatted = []
        
        for _, row in gainers.iterrows():
            gainers_formatted.append(format_stock_row(row))
        
        for _, row in losers.iterrows():
            losers_formatted.append(format_stock_row(row))
        
        return {
            'gainers': gainers_formatted,
            'losers': losers_formatted,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_stocks_analyzed': len(gainers) + len(losers)
        }
    
    def compare_with_tadawul_data(self) -> Dict:
        """Get market movers and compare with expected Tadawul format"""
        gainers, losers = self.get_market_movers()
        formatted_data = self.format_market_movers_display(gainers, losers)
        
        return {
            'market_movers': formatted_data,
            'data_quality': {
                'total_symbols_checked': len(self.saudi_stocks_enhanced),
                'successful_fetches': len(gainers) + len(losers),
                'data_freshness': 'Real-time via yfinance',
                'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'notes': [
                "Data source: Yahoo Finance (yfinance library)",
                "May have slight delays compared to real-time Tadawul data",
                "Symbols use .SR suffix for Yahoo Finance compatibility",
                "Consider upgrading to real-time Tadawul API for exact matching"
            ]
        }

# Example usage
if __name__ == "__main__":
    provider = TadawulDataProvider()
    result = provider.compare_with_tadawul_data()
    
    print("=== SAUDI MARKET MOVERS ===")
    print(f"Last Update: {result['data_quality']['last_update']}")
    print(f"Stocks Analyzed: {result['data_quality']['successful_fetches']}")
    
    print("\n🟢 TOP GAINERS:")
    for stock in result['market_movers']['gainers'][:5]:
        print(f"{stock['symbol']} - {stock['name']}: {stock['price']} SAR ({stock['change']})")
    
    print("\n🔴 TOP LOSERS:")
    for stock in result['market_movers']['losers'][:5]:
        print(f"{stock['symbol']} - {stock['name']}: {stock['price']} SAR ({stock['change']})")
