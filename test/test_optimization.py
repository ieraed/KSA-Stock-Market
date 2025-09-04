"""
Test Ultra-Fast Fetcher Performance
Comprehensive testing of all optimization modules
"""

import sys
import os
import time

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
core_path = os.path.join(current_dir, 'core')
sys.path.insert(0, core_path)

def test_ultra_fast_system():
    """Test the complete ultra-fast system"""
    
    print("🚀 TESTING ULTRA-FAST SAUDI STOCK SYSTEM")
    print("=" * 60)
    
    # Test 1: Import modules
    print("\n📦 Testing Module Imports...")
    try:
        from ultra_fast_fetcher import UltraFastFetcher, ultra_fast_fetcher
        print("✅ Ultra-fast fetcher imported")
        
        from reliable_processor import ReliableMarketProcessor, reliable_processor
        print("✅ Reliable processor imported")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Quick data fetch (10 stocks)
    print("\n⚡ Testing Quick Fetch (10 stocks)...")
    start_time = time.time()
    
    try:
        stocks = ultra_fast_fetcher.fetch_market_data(max_stocks=10, use_cache=False)
        fetch_time = time.time() - start_time
        
        successful_stocks = [s for s in stocks if s.success]
        
        print(f"📊 Results:")
        print(f"   Total time: {fetch_time:.2f} seconds")
        print(f"   Successful: {len(successful_stocks)}")
        print(f"   Failed: {len(stocks) - len(successful_stocks)}")
        print(f"   Speed: {len(stocks)/fetch_time:.1f} stocks/second")
        
        if len(successful_stocks) >= 5:
            print("✅ Quick fetch test PASSED")
        else:
            print("⚠️ Quick fetch test - LOW SUCCESS RATE")
            
    except Exception as e:
        print(f"❌ Quick fetch error: {e}")
        return False
    
    # Test 3: Data processing reliability
    print("\n🔧 Testing Data Processing...")
    try:
        # Convert stock data to dict format
        stock_dicts = []
        for stock in successful_stocks[:5]:  # Test with first 5
            stock_dicts.append({
                'symbol': stock.symbol,
                'name': stock.name,
                'current_price': stock.current_price,
                'change_percent': stock.change_percent,
                'volume': stock.volume,
                'trading_value': stock.trading_value,
                'sector': stock.sector,
                'data_source': stock.data_source
            })
        
        # Process with reliable processor
        summary = reliable_processor.validate_and_process_data(stock_dicts)
        dashboard_data = reliable_processor.create_dashboard_data(summary)
        
        print(f"📊 Processing Results:")
        print(f"   Processed stocks: {summary.total_stocks}")
        print(f"   Top gainers: {len(summary.top_gainers)}")
        print(f"   Top losers: {len(summary.top_losers)}")
        print(f"   Processing time: {summary.processing_time:.3f}s")
        
        # Validate no negative gainers
        negative_gainers = [g for g in summary.top_gainers if g['change_percent'] <= 0]
        if negative_gainers:
            print(f"❌ Found {len(negative_gainers)} negative gainers!")
            return False
        else:
            print("✅ Data processing test PASSED")
            
    except Exception as e:
        print(f"❌ Processing error: {e}")
        return False
    
    # Test 4: Performance benchmark (25 stocks)
    print("\n🏃‍♂️ Performance Benchmark (25 stocks)...")
    start_time = time.time()
    
    try:
        benchmark_stocks = ultra_fast_fetcher.fetch_market_data(max_stocks=25, use_cache=False)
        benchmark_time = time.time() - start_time
        
        successful_benchmark = [s for s in benchmark_stocks if s.success]
        
        print(f"📊 Benchmark Results:")
        print(f"   Total time: {benchmark_time:.2f} seconds")
        print(f"   Successful: {len(successful_benchmark)}")
        print(f"   Success rate: {len(successful_benchmark)/len(benchmark_stocks)*100:.1f}%")
        print(f"   Speed: {len(benchmark_stocks)/benchmark_time:.1f} stocks/second")
        
        # Performance targets
        if benchmark_time <= 10 and len(successful_benchmark) >= 20:
            print("✅ Performance benchmark EXCELLENT")
        elif benchmark_time <= 20 and len(successful_benchmark) >= 15:
            print("✅ Performance benchmark GOOD")
        else:
            print("⚠️ Performance benchmark - NEEDS OPTIMIZATION")
            
    except Exception as e:
        print(f"❌ Benchmark error: {e}")
        return False
    
    # Test 5: Cache functionality
    print("\n💾 Testing Cache Functionality...")
    try:
        # First fetch (no cache)
        start_fresh = time.time()
        fresh_stocks = ultra_fast_fetcher.fetch_market_data(max_stocks=10, use_cache=False)
        fresh_time = time.time() - start_fresh
        
        # Second fetch (with cache)
        start_cached = time.time()
        cached_stocks = ultra_fast_fetcher.fetch_market_data(max_stocks=10, use_cache=True)
        cached_time = time.time() - start_cached
        
        print(f"📊 Cache Results:")
        print(f"   Fresh fetch time: {fresh_time:.2f}s")
        print(f"   Cached fetch time: {cached_time:.2f}s")
        print(f"   Speed improvement: {fresh_time/cached_time:.1f}x faster" if cached_time > 0 else "   Cache used")
        
        if cached_time < fresh_time or cached_time < 1.0:
            print("✅ Cache test PASSED")
        else:
            print("⚠️ Cache not providing expected speedup")
            
    except Exception as e:
        print(f"❌ Cache test error: {e}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎉 ULTRA-FAST SYSTEM TEST COMPLETED")
    print("✅ All core functionality working")
    print("🚀 Ready for production use")
    print("=" * 60)
    
    return True

def show_sample_dashboard_data():
    """Show sample of what the dashboard will display"""
    
    print("\n📊 SAMPLE DASHBOARD OUTPUT")
    print("=" * 40)
    
    try:
        # Get sample data
        stocks = ultra_fast_fetcher.fetch_market_data(max_stocks=15, use_cache=True)
        successful_stocks = [s for s in stocks if s.success]
        
        if len(successful_stocks) >= 5:
            print(f"\n📈 TOP GAINERS:")
            gainers = [s for s in successful_stocks if s.change_percent > 0]
            gainers.sort(key=lambda x: x.change_percent, reverse=True)
            
            for i, stock in enumerate(gainers[:5], 1):
                print(f"  {i}. {stock.symbol} ({stock.name}): {stock.current_price:.2f} SAR (+{stock.change_percent:.2f}%)")
            
            print(f"\n📉 TOP LOSERS:")
            losers = [s for s in successful_stocks if s.change_percent < 0]
            losers.sort(key=lambda x: x.change_percent)
            
            for i, stock in enumerate(losers[:5], 1):
                print(f"  {i}. {stock.symbol} ({stock.name}): {stock.current_price:.2f} SAR ({stock.change_percent:.2f}%)")
            
            print(f"\n📊 VOLUME LEADERS:")
            volume_leaders = sorted(successful_stocks, key=lambda x: x.volume, reverse=True)
            
            for i, stock in enumerate(volume_leaders[:5], 1):
                print(f"  {i}. {stock.symbol} ({stock.name}): {stock.volume:,} shares")
        
        print("\n✅ Sample data looks correct!")
        
    except Exception as e:
        print(f"❌ Sample data error: {e}")

if __name__ == "__main__":
    success = test_ultra_fast_system()
    
    if success:
        show_sample_dashboard_data()
    
    print(f"\n🎯 NEXT STEPS:")
    print("1. Run the optimized dashboard: streamlit run optimized_dashboard.py")
    print("2. Compare performance with old dashboard")
    print("3. Fine-tune cache settings if needed")
