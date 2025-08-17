"""
🚀 Quick Start Script for Continuous Saudi Stock Data Fetching

This script demonstrates how to use the continuous data fetching system.
Run this to start getting real-time data from the Saudi Exchange.
"""

import sys
import os
import time
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🇸🇦 TADAWUL NEXUS - Continuous Data Fetching System")
    print("=" * 60)
    
    try:
        # Import the continuous fetcher
        from continuous_data_fetcher import ContinuousSaudiExchangeFetcher
        print("✅ Continuous data fetcher imported successfully")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Please install required packages:")
        print("   pip install beautifulsoup4 aiohttp")
        return
    
    print("\n📡 Testing single data fetch...")
    
    try:
        # Create fetcher instance
        fetcher = ContinuousSaudiExchangeFetcher(update_interval=60)
        print("✅ Fetcher created successfully")
        
        # Test single fetch
        print("🔍 Fetching data from Saudi Exchange...")
        stocks = fetcher.fetch_current_data()
        
        if stocks:
            print(f"🎉 SUCCESS! Retrieved {len(stocks)} stocks")
            
            # Show some sample data
            print("\n📊 Sample stocks:")
            count = 0
            for symbol, stock in stocks.items():
                if count < 5:
                    change_text = f"+{stock.change_percent:.2f}%" if stock.change_percent > 0 else f"{stock.change_percent:.2f}%"
                    print(f"  {symbol}: {stock.name} - {stock.price} SAR ({change_text})")
                    count += 1
                else:
                    break
            
            # Show statistics
            stats = fetcher.get_statistics()
            print(f"\n📈 Market Statistics:")
            print(f"  Total stocks: {stats.get('total_stocks', 0)}")
            print(f"  Gainers: {stats.get('gainers_count', 0)}")
            print(f"  Losers: {stats.get('losers_count', 0)}")
            print(f"  Average change: {stats.get('avg_change_percent', 0):.2f}%")
            
            # Export data
            filename = fetcher.export_to_json()
            print(f"\n💾 Data exported to: {filename}")
            
            print("\n✅ Single fetch test completed successfully!")
            
            # Ask if user wants to start continuous fetching
            print("\n🔄 Would you like to start continuous fetching?")
            print("   This will fetch data every 60 seconds and update your database.")
            response = input("   Enter 'y' for yes, any other key for no: ").lower().strip()
            
            if response == 'y':
                start_continuous_fetching(fetcher)
            else:
                print("👋 Exiting. You can run this script again anytime!")
                
        else:
            print("❌ No data retrieved. This could be due to:")
            print("   - Network connectivity issues")
            print("   - Saudi Exchange website being unavailable")
            print("   - Website structure changes")
            print("   - Firewall or proxy blocking the request")
            
    except Exception as e:
        print(f"❌ Error during fetch: {e}")
        import traceback
        traceback.print_exc()

def start_continuous_fetching(fetcher):
    """Start continuous fetching with user feedback"""
    
    print("\n🚀 Starting continuous data fetching...")
    print("🕐 Updates every 60 seconds")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 40)
    
    def on_update(stocks):
        """Callback for data updates"""
        current_time = datetime.now().strftime("%H:%M:%S")
        gainers = len([s for s in stocks.values() if s.change_percent and s.change_percent > 0])
        losers = len([s for s in stocks.values() if s.change_percent and s.change_percent < 0])
        
        print(f"📊 {current_time} - Updated {len(stocks)} stocks | "
              f"Gainers: {gainers} | Losers: {losers}")
    
    # Add callback
    fetcher.add_callback(on_update)
    
    try:
        # Start continuous fetching
        fetcher.start_continuous_fetching()
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping continuous fetching...")
        fetcher.stop_continuous_fetching()
        print("✅ Stopped successfully!")
        
        # Show final statistics
        if fetcher.latest_data:
            print(f"\n📊 Final Update: {len(fetcher.latest_data)} stocks in cache")
        
        print("👋 Thank you for using TADAWUL NEXUS!")

if __name__ == "__main__":
    main()
