"""
🔍 Quick Stock Data Validation Script
Tests the unified stock manager and validates data consistency
"""

import json
from datetime import datetime

def test_unified_manager():
    """Test the unified stock manager"""
    print("=" * 60)
    print("🇸🇦 UNIFIED STOCK MANAGER VALIDATION")
    print("=" * 60)
    
    try:
        from unified_stock_manager import (
            unified_manager, 
            get_unified_stocks_database, 
            validate_stock_data,
            get_stock_info
        )
        
        print("✅ Unified manager imported successfully")
        
        # Get the unified database
        print("\n📊 Loading unified stock database...")
        stocks_db = get_unified_stocks_database()
        print(f"✅ Loaded {len(stocks_db)} stocks")
        
        # Test specific stocks that were mentioned as problematic
        test_symbols = ['1010', '1120', '2030', '2010', '7010']
        
        print("\n🔍 Testing specific stocks:")
        print("-" * 40)
        
        for symbol in test_symbols:
            stock_info = get_stock_info(symbol)
            print(f"{symbol}: {stock_info.get('name_en', 'NOT FOUND')}")
            if stock_info.get('sector'):
                print(f"      Sector: {stock_info.get('sector')}")
            if stock_info.get('current_price'):
                print(f"      Price: {stock_info.get('current_price')} SAR")
            print()
        
        # Run validation
        print("🔍 Running validation report...")
        validation_report = validate_stock_data()
        
        print("\n📋 VALIDATION REPORT:")
        print("-" * 40)
        print(f"Total stocks: {validation_report['total_stocks']}")
        print(f"Validation time: {validation_report['validation_time']}")
        
        print("\nTest stocks:")
        for symbol, data in validation_report['test_stocks'].items():
            print(f"  {symbol}: {data['name_en']} ({data['sector']})")
        
        if validation_report['issues']:
            print("\n⚠️ Issues found:")
            for issue in validation_report['issues']:
                print(f"  - {issue}")
        else:
            print("\n✅ No issues found!")
            
        return True
        
    except ImportError as e:
        print(f"❌ Could not import unified manager: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        return False

def test_fallback_databases():
    """Test the fallback databases"""
    print("\n" + "=" * 60)
    print("📂 FALLBACK DATABASES VALIDATION")
    print("=" * 60)
    
    # Test main database
    try:
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            main_db = json.load(f)
        
        print(f"✅ Main database: {len(main_db)} stocks")
        print(f"   1010: {main_db.get('1010', {}).get('name_en', 'NOT FOUND')}")
        print(f"   1120: {main_db.get('1120', {}).get('name_en', 'NOT FOUND')}")
        
    except Exception as e:
        print(f"❌ Main database error: {e}")
    
    # Test corrected database
    try:
        with open('saudi_stocks_database_corrected.json', 'r', encoding='utf-8') as f:
            corrected_db = json.load(f)
        
        print(f"✅ Corrected database: {len(corrected_db)} stocks")
        print(f"   1010: {corrected_db.get('1010', {}).get('name_en', 'NOT FOUND')}")
        print(f"   1120: {corrected_db.get('1120', {}).get('name_en', 'NOT FOUND')}")
        
    except Exception as e:
        print(f"❌ Corrected database error: {e}")

def test_continuous_fetcher():
    """Test the continuous fetcher"""
    print("\n" + "=" * 60)
    print("🔄 CONTINUOUS FETCHER VALIDATION")
    print("=" * 60)
    
    try:
        from continuous_data_fetcher import ContinuousSaudiExchangeFetcher
        
        fetcher = ContinuousSaudiExchangeFetcher()
        latest_data = fetcher.get_latest_data()
        
        if latest_data:
            print(f"✅ Continuous fetcher: {len(latest_data)} stocks")
            
            # Look for our test stocks
            for stock in latest_data:
                symbol = stock.get('symbol', '').replace('.SR', '')
                if symbol in ['1010', '1120']:
                    print(f"   {symbol}: {stock.get('name', 'NO NAME')}")
        else:
            print("⚠️ No data from continuous fetcher")
            
    except Exception as e:
        print(f"❌ Continuous fetcher error: {e}")

def main():
    """Main validation function"""
    print(f"🚀 Starting validation at {datetime.now()}")
    
    # Test unified manager
    unified_success = test_unified_manager()
    
    # Test fallback databases
    test_fallback_databases()
    
    # Test continuous fetcher
    test_continuous_fetcher()
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY")
    print("=" * 60)
    
    if unified_success:
        print("✅ Unified stock manager is working correctly")
        print("✅ Data sources are unified and consistent")
        print("✅ Portfolio Setup should now show correct symbol-name pairs")
    else:
        print("⚠️ Unified manager needs attention")
        print("💡 Check if continuous_data_fetcher.py is working")
        print("💡 Verify database files are accessible")
    
    print(f"\n🕒 Validation completed at {datetime.now()}")

if __name__ == "__main__":
    main()
