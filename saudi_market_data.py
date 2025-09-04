"""
Saudi Market Data Fetcher
Real-time market data from TASI that matches saudiexchange.sa
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import json
import time

def get_saudi_stock_list() -> List[str]:
    """Get list of Saudi stock symbols for yfinance (.SR suffix)"""
    
    # Major Saudi stocks that are available on Yahoo Finance with .SR suffix
    saudi_symbols = [
        # Banks
        "1120.SR", "1180.SR", "1010.SR", "1020.SR", "1030.SR", "1050.SR", 
        "1060.SR", "1080.SR", "1140.SR", "1150.SR",
        
        # Energy & Petrochemicals  
        "2222.SR", "2010.SR", "2020.SR", "2060.SR", "2090.SR", "2170.SR",
        "2210.SR", "2220.SR", "2290.SR", "2330.SR", "2350.SR", "2380.SR",
        
        # Materials & Construction
        "3020.SR", "3030.SR", "3040.SR", "3050.SR", "3060.SR", "3080.SR",
        "3090.SR", "3091.SR", "3092.SR",
        
        # Real Estate & Development
        "4020.SR", "4090.SR", "4100.SR", "4150.SR", "4220.SR", "4230.SR",
        "4250.SR", "4300.SR", "4310.SR", "4320.SR", "4321.SR", "4322.SR",
        "4323.SR", "4324.SR", "4325.SR",
        
        # Consumer & Retail
        "4001.SR", "4003.SR", "4006.SR", "4008.SR", "4050.SR", "4051.SR",
        "4160.SR", "4161.SR", "4162.SR", "4163.SR", "4164.SR", "4190.SR",
        "4191.SR", "4192.SR", "4193.SR", "4240.SR",
        
        # Healthcare
        "4002.SR", "4004.SR", "4005.SR", "4007.SR", "4009.SR", "4013.SR",
        "4017.SR", "4018.SR", "4019.SR",
        
        # Food & Agriculture
        "2050.SR", "2280.SR", "2281.SR", "2282.SR", "2283.SR", "2284.SR",
        "6001.SR", "6010.SR", "6020.SR", "6040.SR", "6050.SR", "6060.SR",
        
        # Telecom
        "7010.SR", "7020.SR", "7030.SR", "7040.SR",
        
        # Insurance
        "8010.SR", "8020.SR", "8030.SR", "8040.SR", "8050.SR", "8060.SR",
        "8070.SR", "8100.SR", "8120.SR", "8150.SR", "8160.SR", "8170.SR",
        "8180.SR", "8190.SR", "8200.SR", "8210.SR", "8230.SR", "8240.SR",
        "8250.SR", "8260.SR", "8270.SR", "8280.SR", "8300.SR", "8310.SR",
        
        # Utilities
        "2080.SR", "2081.SR", "2082.SR", "5110.SR",
        
        # Transportation
        "4030.SR", "4040.SR", "4260.SR", "4261.SR", "4262.SR", "4263.SR",
        
        # Technology
        "7200.SR", "7201.SR", "7202.SR", "7203.SR", "7204.SR",
    ]
    
    return saudi_symbols

def get_stock_name_mapping() -> Dict[str, str]:
    """Map stock symbols to company names"""
    return {
        # Banks
        "1120.SR": "AL RAJHI BANK", "1180.SR": "SNB", "1010.SR": "RIBL",
        "1020.SR": "BJAZ", "1030.SR": "SAIB", "1050.SR": "BSF",
        "1060.SR": "SAB", "1080.SR": "ANB", "1140.SR": "ALBILAD", "1150.SR": "ALINMA",
        
        # Major Companies
        "2222.SR": "SAUDI ARAMCO", "4240.SR": "CENOMI RETAIL",
        "1810.SR": "SEERA", "4003.SR": "EXTRA", "8313.SR": "RASAN",
        
        # Energy & Materials
        "2010.SR": "SABIC", "2330.SR": "ADVANCED", "2290.SR": "YANSAB", 
        "1304.SR": "ALYAMAMAH STEEL", "1833.SR": "ALMAWARID",
        
        # Technology & Services
        "4170.SR": "TECO", "4180.SR": "FITAIHI GROUP", "2350.SR": "SAUDI KAYAN",
        "4110.SR": "BATIC", "6015.SR": "AMERICANA",
        
        # Others
        "7010.SR": "STC", "2280.SR": "ALMARAI", "4190.SR": "JARIR",
        "4321.SR": "CENOMI CENTERS", "8010.SR": "TAWUNIYA"
    }

def fetch_live_market_data() -> Dict:
    """
    Fetch live market data from Yahoo Finance for Saudi stocks
    Returns data in format matching TASI website structure
    """
    
    print("🔄 Fetching live TASI market data...")
    
    saudi_symbols = get_saudi_stock_list()
    name_mapping = get_stock_name_mapping()
    
    # Fetch data for all symbols
    market_data = []
    successful_fetches = 0
    
    for symbol in saudi_symbols[:50]:  # Limit to first 50 for performance
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price data
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            previous_close = info.get('previousClose', info.get('regularMarketPreviousClose', 0))
            
            if current_price and previous_close and current_price > 0:
                change = current_price - previous_close
                change_pct = (change / previous_close) * 100
                
                # Get volume data
                volume = info.get('volume', info.get('regularMarketVolume', 0))
                market_cap = info.get('marketCap', 0)
                
                stock_data = {
                    'symbol': symbol.replace('.SR', ''),
                    'company': name_mapping.get(symbol, info.get('longName', 'Unknown')),
                    'current_price': current_price,
                    'previous_close': previous_close,
                    'change': change,
                    'change_pct': change_pct,
                    'volume': volume,
                    'market_cap': market_cap,
                    'value_traded': current_price * volume if volume else 0
                }
                
                market_data.append(stock_data)
                successful_fetches += 1
                
        except Exception as e:
            # Skip failed fetches silently to avoid spam
            continue
    
    print(f"✅ Successfully fetched data for {successful_fetches} stocks")
    
    # Create market summary with all categories matching TASI website
    if market_data:
        df = pd.DataFrame(market_data)
        
        # Sort and get top performers in each category
        top_gainers = df.nlargest(10, 'change_pct').to_dict('records')
        top_losers = df.nsmallest(10, 'change_pct').to_dict('records')
        movers_by_volume = df.nlargest(10, 'volume').to_dict('records')
        movers_by_value = df.nlargest(10, 'value_traded').to_dict('records')
        
        return {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_stocks': len(market_data),
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'movers_by_volume': movers_by_volume, 
            'movers_by_value': movers_by_value,
            'all_data': market_data
        }
    
    return {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_stocks': 0,
        'top_gainers': [],
        'top_losers': [],
        'movers_by_volume': [],
        'movers_by_value': [],
        'all_data': []
    }

def get_market_summary() -> Dict:
    """
    Main function to get market summary data
    This will be called by the enhanced app
    """
    try:
        return fetch_live_market_data()
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        
        # Return empty structure on error
        return {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_stocks': 0,
            'top_gainers': [],
            'top_losers': [],
            'movers_by_volume': [],
            'movers_by_value': [],
            'all_data': [],
            'error': str(e)
        }

if __name__ == "__main__":
    # Test the market data fetcher
    print("🧪 Testing Saudi Market Data Fetcher...")
    data = get_market_summary()
    
    print(f"\n📊 Market Summary:")
    print(f"Timestamp: {data['timestamp']}")
    print(f"Total stocks with data: {data['total_stocks']}")
    print(f"Top gainers: {len(data['top_gainers'])}")
    print(f"Top losers: {len(data['top_losers'])}")
    print(f"Volume movers: {len(data['movers_by_volume'])}")
    print(f"Value movers: {len(data['movers_by_value'])}")
    
    if data['top_gainers']:
        print(f"\n📈 Top Gainer: {data['top_gainers'][0]['symbol']} ({data['top_gainers'][0]['company']}) +{data['top_gainers'][0]['change_pct']:.2f}%")
    
    if data['top_losers']:
        print(f"📉 Top Loser: {data['top_losers'][0]['symbol']} ({data['top_losers'][0]['company']}) {data['top_losers'][0]['change_pct']:.2f}%")
