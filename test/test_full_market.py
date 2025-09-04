#!/usr/bin/env python3
"""
Test Full Market Coverage
Check how many stocks we can actually fetch from the complete TASI market
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetch_all_saudi_stocks import CompleteSaudiMarketFetcher
import time

def main():
    """Test full market data fetching"""
    
    print("🚀 Testing Complete TASI Market Data Fetching...")
    print("=" * 60)
    
    # Initialize fetcher
    fetcher = CompleteSaudiMarketFetcher()
    
    print(f"📊 Total symbols to test: {len(fetcher.all_saudi_symbols)}")
    print("⏳ Starting fetch... (this may take several minutes)")
    
    start_time = time.time()
    
    # Test with smaller parallel workers to be more conservative
    results = fetcher.fetch_all_stocks_parallel(max_workers=10)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Analyze results
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]
    
    print("\n📈 RESULTS SUMMARY:")
    print("=" * 60)
    print(f"✅ Successfully fetched: {len(successful)} stocks")
    print(f"❌ Failed to fetch: {len(failed)} stocks")
    print(f"📊 Success rate: {len(successful)/len(results)*100:.1f}%")
    print(f"⏱️ Duration: {duration:.1f} seconds")
    print(f"🏃 Speed: {len(results)/duration:.1f} stocks/second")
    
    if successful:
        print(f"\n🔝 Sample of successful stocks:")
        for i, stock in enumerate(successful[:10]):
            print(f"  {i+1}. {stock['symbol']}: {stock['name']} - {stock['current_price']} SAR")
        
        # Show top movers
        top_gainers = sorted(successful, key=lambda x: x.get('change_percent', 0), reverse=True)[:5]
        print(f"\n📈 Top 5 Gainers:")
        for stock in top_gainers:
            print(f"  {stock['symbol']}: {stock['name']} +{stock['change_percent']:.2f}%")
        
        # Calculate total market metrics
        total_volume = sum(s.get('volume', 0) for s in successful)
        total_value = sum(s.get('current_price', 0) * s.get('volume', 0) for s in successful)
        
        print(f"\n💰 Market Summary:")
        print(f"  Total Volume: {total_volume:,}")
        print(f"  Total Value Traded: {total_value:,.0f} SAR")
    
    # Save results if we got good data
    if len(successful) > 50:
        try:
            # Generate market summary
            summary = fetcher.get_market_summary(results)
            
            # Save to files
            excel_file = fetcher.save_to_excel(results)
            json_file = fetcher.save_to_json(results)
            
            print(f"\n💾 Data saved:")
            print(f"  📊 Excel: {excel_file}")
            print(f"  📋 JSON: {json_file}")
            
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    return len(successful)

if __name__ == "__main__":
    successful_count = main()
    
    print(f"\n🎯 RECOMMENDATION:")
    if successful_count >= 200:
        print("   ✅ Excellent! You can use full market data in your app")
    elif successful_count >= 100:
        print("   ⚡ Good! You can significantly expand your market coverage")
    elif successful_count >= 50:
        print("   📊 Decent! You can improve current coverage")
    else:
        print("   ⚠️  Limited success - may need to optimize data sources")
    
    print(f"\n💡 To update your app to use {successful_count} stocks:")
    print("   1. Edit saudi_exchange_fetcher.py")
    print("   2. Increase the limit from 75 to", min(successful_count, 250))
    print("   3. Restart your dashboard")
