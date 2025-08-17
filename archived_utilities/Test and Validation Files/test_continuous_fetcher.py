"""
🇸🇦 Test Continuous Saudi Exchange Data Fetching
Test script to verify the continuous data fetching system
"""

import time
import json
from datetime import datetime
from saudi_data_integration import get_data_manager, get_all_saudi_stocks, get_market_summary

def test_data_fetching():
    """Test the continuous data fetching system"""
    
    print("🇸🇦 Testing Saudi Exchange Continuous Data Fetching")
    print("=" * 60)
    
    # Get data manager
    print("📊 Initializing data manager...")
    manager = get_data_manager()
    
    # Wait a moment for initial fetch
    print("⏳ Waiting for initial data fetch...")
    time.sleep(5)
    
    # Test getting all stocks
    print("\n📈 Testing get_all_saudi_stocks()...")
    stocks = get_all_saudi_stocks()
    print(f"✅ Retrieved {len(stocks)} stocks")
    
    if stocks:
        # Show sample stocks
        print("\n📋 Sample stocks:")
        count = 0
        for symbol, data in stocks.items():
            if count < 5:  # Show first 5
                print(f"  {symbol}: {data['name_en']} - {data['price']} SAR ({data['change_percent']:+.2f}%)")
                count += 1
            else:
                break
    
    # Test market summary
    print("\n📊 Testing market summary...")
    summary = get_market_summary()
    print("✅ Market Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Test top movers
    print("\n🔥 Testing top movers...")
    movers = manager.get_top_movers(5)
    
    print("📈 Top 5 Gainers:")
    for stock in movers['gainers']:
        print(f"  {stock['symbol']}: {stock['name']} (+{stock['change_percent']:.2f}%)")
    
    print("\n📉 Top 5 Losers:")
    for stock in movers['losers']:
        print(f"  {stock['symbol']}: {stock['name']} ({stock['change_percent']:.2f}%)")
    
    # Test data freshness
    print(f"\n🕐 Data freshness: {'Fresh' if manager.is_data_fresh() else 'Stale'}")
    print(f"🕐 Last update: {manager.last_update}")
    
    # Test export
    print("\n💾 Testing data export...")
    json_file = manager.export_current_data("json")
    print(f"✅ Exported to: {json_file}")
    
    # Test specific stock lookup
    print("\n🔍 Testing specific stock lookup...")
    test_symbols = ["2030.SR", "1120.SR", "7010.SR"]  # SARCO, ALRAJHI, STC
    for symbol in test_symbols:
        stock = manager.get_stock_by_symbol(symbol)
        if stock:
            print(f"  {symbol}: {stock['name_en']} - {stock['price']} SAR")
        else:
            print(f"  {symbol}: Not found")
    
    print("\n✅ Test completed successfully!")
    print("🔄 Continuous fetching is now running in the background...")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        # Keep running to show continuous updates
        for i in range(10):  # Run for 10 update cycles
            time.sleep(30)  # Wait 30 seconds between checks
            
            current_time = datetime.now().strftime("%H:%M:%S")
            fresh = "Fresh" if manager.is_data_fresh() else "Stale"
            print(f"🕐 {current_time} - Data status: {fresh} - Stocks: {len(manager.data_cache)}")
            
            # Show a quick market snapshot every few iterations
            if i % 3 == 0:
                stats = manager.fetcher.get_statistics()
                print(f"📊 Market snapshot: {stats.get('gainers_count', 0)} gainers, {stats.get('losers_count', 0)} losers")
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping test...")
    
    finally:
        manager.stop()
        print("✅ Test completed and data fetching stopped")

def test_single_fetch():
    """Test a single data fetch without continuous mode"""
    
    print("🇸🇦 Testing Single Data Fetch")
    print("=" * 40)
    
    from continuous_data_fetcher import ContinuousSaudiExchangeFetcher
    
    # Create fetcher without continuous mode
    fetcher = ContinuousSaudiExchangeFetcher()
    
    print("📡 Fetching current data...")
    stocks = fetcher.fetch_current_data()
    
    if stocks:
        print(f"✅ Successfully fetched {len(stocks)} stocks")
        
        # Show statistics
        stats = fetcher.get_statistics()
        print("\n📊 Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Export data
        filename = fetcher.export_to_json()
        print(f"\n💾 Data exported to: {filename}")
        
        # Show top gainers
        gainers = fetcher.get_top_gainers(5)
        if gainers:
            print("\n🔥 Top 5 Gainers:")
            for stock in gainers:
                print(f"  {stock.symbol}: {stock.name} (+{stock.change_percent:.2f}%)")
        
        # Show top losers
        losers = fetcher.get_top_losers(5)
        if losers:
            print("\n📉 Top 5 Losers:")
            for stock in losers:
                print(f"  {stock.symbol}: {stock.name} ({stock.change_percent:.2f}%)")
        
    else:
        print("❌ Failed to fetch data")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "single":
        test_single_fetch()
    else:
        test_data_fetching()
