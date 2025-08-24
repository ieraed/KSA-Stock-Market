#!/usr/bin/env python3
"""
Quick test to verify current stock prices being used
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app functions
from apps.enhanced_saudi_app_v2 import get_stock_data, load_saudi_stocks_database

def test_key_stocks():
    """Test prices for the key stocks user mentioned"""
    
    print("🔍 Testing Current Stock Prices")
    print("=" * 50)
    
    # Load the stocks database
    stocks_db = load_saudi_stocks_database()
    print(f"📊 Loaded database with {len(stocks_db) if stocks_db else 0} stocks")
    
    # Test key stocks
    test_symbols = [
        ("4001", "A.OTHAIM MARKET"),
        ("4110", "BATIC"), 
        ("4161", "BINDAWOOD"),
        ("1010", "RIBL"),
        ("1020", "BJAZ"),
        ("1080", "ANB")
    ]
    
    print("\n📈 Current Prices:")
    print("-" * 70)
    print(f"{'Symbol':<8} {'Company':<20} {'Price':<10} {'Source':<30}")
    print("-" * 70)
    
    for symbol, name in test_symbols:
        try:
            data = get_stock_data(symbol, stocks_db)
            if data:
                price = data.get('current_price', 'N/A')
                source = data.get('data_source', 'Unknown')
                print(f"{symbol:<8} {name:<20} {price:<10} {source:<30}")
            else:
                print(f"{symbol:<8} {name:<20} {'ERROR':<10} {'No data returned':<30}")
        except Exception as e:
            print(f"{symbol:<8} {name:<20} {'ERROR':<10} {str(e):<30}")
    
    print("-" * 70)

if __name__ == "__main__":
    test_key_stocks()
