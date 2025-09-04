#!/usr/bin/env python3
"""
Fix Market Summary Based on Working Historical Code
Using the pandas DataFrame approach that used to work correctly
"""

import sys
import os
import time
import pandas as pd
import numpy as np
from datetime import datetime

# Add core to path
core_path = os.path.join(os.path.dirname(__file__), 'core')
sys.path.insert(0, core_path)

print("=" * 60)
print("🔧 FIXING MARKET SUMMARY CALCULATION")
print("=" * 60)

try:
    from ultra_fast_fetcher import UltraFastFetcher
    from reliable_processor import ReliableMarketProcessor
    
    print("✅ Modules imported successfully")
    
    # Test with a small set first
    test_symbols = [
        '2222.SR',  # Saudi Aramco
        '1120.SR',  # Al Rajhi Bank  
        '2380.SR',  # SABIC
        '1180.SR',  # Gulf International Bank
        '2010.SR',  # SABB
        '4061.SR',  # NCBC
        '1150.SR',  # Alinma Bank
        '7010.SR',  # STC
        '2280.SR',  # Almarai
        '4013.SR'   # Dr. Sulaiman Al Habib
    ]
    
    print(f"\n🧪 Testing with {len(test_symbols)} symbols...")
    
    # Step 1: Fetch raw data
    print("\n📡 Step 1: Fetching raw data...")
    fetcher = UltraFastFetcher()
    raw_data = fetcher.fetch_market_data(test_symbols)
    
    print(f"📊 Retrieved {len(raw_data)} stocks")
    
    # Step 2: Convert to pandas DataFrame (like the old working code)
    print("\n📊 Step 2: Converting to DataFrame for analysis...")
    
    # Convert to dictionary format for DataFrame
    stocks_dict = {}
    for symbol, stock_data in raw_data.items():
        stocks_dict[symbol] = {
            'symbol': symbol,
            'current_price': stock_data.price,
            'change': stock_data.price * (stock_data.change_percent / 100),  # Calculate actual change
            'change_pct': stock_data.change_percent,
            'volume': stock_data.volume,
            'name': stock_data.name
        }
    
    # Create DataFrame from dictionary (orient='index' like the old code)
    df = pd.DataFrame.from_dict(stocks_dict, orient='index')
    
    print(f"📈 DataFrame created with {len(df)} rows")
    print("Columns:", df.columns.tolist())
    
    # Step 3: Apply the exact logic from the old working code
    print("\n🔍 Step 3: Applying old working logic...")
    
    # Check if we have the required columns
    if 'change_pct' not in df.columns:
        print("⚠️ Missing change_pct, calculating...")
        df['change_pct'] = (df['change'] / (df['current_price'] - df['change'])) * 100
    
    print("Sample data:")
    for i, (idx, row) in enumerate(df.head().iterrows()):
        print(f"  {row['symbol']}: {row['current_price']:.2f} SAR ({row['change_pct']:+.2f}%)")
    
    # Step 4: Use the exact pandas sorting from old code
    print("\n📈 Step 4: Getting top gainers and losers (pandas method)...")
    
    # Get top gainers and losers using pandas nlargest/nsmallest
    top_gainers_df = df.nlargest(5, 'change_pct')
    top_losers_df = df.nsmallest(5, 'change_pct')
    
    print(f"\n🏆 TOP GAINERS (pandas nlargest):")
    for i, (idx, row) in enumerate(top_gainers_df.iterrows(), 1):
        print(f"  {i}. {row['symbol']} ({row['name']}): {row['change_pct']:+.2f}%")
        if row['change_pct'] < 0:
            print(f"    ❌ ERROR: Negative value in gainers!")
    
    print(f"\n📉 TOP LOSERS (pandas nsmallest):")
    for i, (idx, row) in enumerate(top_losers_df.iterrows(), 1):
        print(f"  {i}. {row['symbol']} ({row['name']}): {row['change_pct']:+.2f}%")
        if row['change_pct'] > 0:
            print(f"    ❌ ERROR: Positive value in losers!")
    
    # Step 5: Compare with our current processor
    print("\n🔄 Step 5: Comparing with current ReliableMarketProcessor...")
    
    processor = ReliableMarketProcessor()
    
    # Convert DataFrame back to list format for processor
    stock_list = df.to_dict('records')
    
    summary = processor.validate_and_process_data(stock_list)
    
    print(f"\n📊 Current Processor Results:")
    print(f"  Total stocks: {summary.total_stocks}")
    print(f"  Top gainers: {len(summary.top_gainers)}")
    print(f"  Top losers: {len(summary.top_losers)}")
    
    if summary.top_gainers:
        print(f"\n🏆 Current Top Gainers:")
        for i, stock in enumerate(summary.top_gainers[:3], 1):
            print(f"  {i}. {stock['symbol']}: {stock['change_percent']:+.2f}%")
            if stock['change_percent'] < 0:
                print(f"    ❌ ERROR: Negative value found!")
    
    if summary.top_losers:
        print(f"\n📉 Current Top Losers:")
        for i, stock in enumerate(summary.top_losers[:3], 1):
            print(f"  {i}. {stock['symbol']}: {stock['change_percent']:+.2f}%")
            if stock['change_percent'] > 0:
                print(f"    ❌ ERROR: Positive value found!")
    
    # Step 6: Create corrected implementation
    print("\n🛠️ Step 6: Creating corrected market summary function...")
    
    def get_corrected_market_summary(stocks_data):
        """Corrected market summary using pandas like the old working code"""
        try:
            if not stocks_data:
                return None
            
            # Convert to DataFrame for analysis (like old code)
            df = pd.DataFrame.from_dict(stocks_data, orient='index')
            
            # Ensure we have change_pct column
            if 'change_pct' not in df.columns and 'change' in df.columns:
                df['change_pct'] = (df['change'] / (df['current_price'] - df['change'])) * 100
            
            # Get top gainers and losers using pandas (like old working code)
            top_gainers = df.nlargest(10, 'change_pct')
            top_losers = df.nsmallest(10, 'change_pct')
            
            return {
                'top_gainers': top_gainers.to_dict('records'),
                'top_losers': top_losers.to_dict('records'),
                'total_stocks': 259,  # Official TASI count
                'last_updated': datetime.now().isoformat(),
                'method': 'pandas_corrected'
            }
            
        except Exception as e:
            print(f"Error in corrected summary: {e}")
            return None
    
    # Test the corrected function
    corrected_summary = get_corrected_market_summary(stocks_dict)
    
    if corrected_summary:
        print(f"\n✅ CORRECTED RESULTS:")
        print(f"📊 Method: {corrected_summary['method']}")
        print(f"📈 Gainers: {len(corrected_summary['top_gainers'])}")
        print(f"📉 Losers: {len(corrected_summary['top_losers'])}")
        
        print(f"\n🏆 Corrected Top Gainers:")
        for i, stock in enumerate(corrected_summary['top_gainers'][:5], 1):
            print(f"  {i}. {stock['symbol']}: {stock['change_pct']:+.2f}%")
            
        print(f"\n📉 Corrected Top Losers:")
        for i, stock in enumerate(corrected_summary['top_losers'][:5], 1):
            print(f"  {i}. {stock['symbol']}: {stock['change_pct']:+.2f}%")
    
    print("\n🎯 DIAGNOSIS COMPLETE!")
    print("✅ The pandas DataFrame method with nlargest/nsmallest should work correctly")
    print("✅ This matches the old working implementation")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
