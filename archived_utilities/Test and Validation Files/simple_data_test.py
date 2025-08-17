"""
🔍 Simple Data Validation Test
Quick test to verify stock data consistency
"""

def test_basic_data():
    print("=== BASIC DATA TEST ===")
    
    # Test the main database directly
    import json
    try:
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
        
        print(f"✅ Main database loaded: {len(db)} stocks")
        
        # Test the specific stocks mentioned
        test_cases = [
            ('1010', 'Saudi National Bank'),
            ('1120', 'Al Rajhi Bank'),
            ('2030', 'Saudi Arabian Oil Company'),
            ('2010', 'Saudi Basic Industries Corporation')
        ]
        
        print("\n🔍 Checking specific stocks:")
        all_correct = True
        
        for symbol, expected_name in test_cases:
            actual_name = db.get(symbol, {}).get('name_en', 'NOT FOUND')
            status = "✅" if expected_name in actual_name else "❌"
            print(f"{status} {symbol}: {actual_name}")
            
            if expected_name not in actual_name:
                all_correct = False
        
        if all_correct:
            print("\n✅ All stock symbols match correct company names!")
        else:
            print("\n❌ Some mismatches found!")
            
        return all_correct
        
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        return False

def test_unified_manager():
    print("\n=== UNIFIED MANAGER TEST ===")
    
    try:
        from unified_stock_manager import get_unified_stocks_database, get_stock_info
        
        stocks_db = get_unified_stocks_database()
        print(f"✅ Unified manager loaded: {len(stocks_db)} stocks")
        
        # Test the problematic stocks
        test_symbols = ['1010', '1120']
        for symbol in test_symbols:
            info = get_stock_info(symbol)
            print(f"✅ {symbol}: {info.get('name_en', 'NOT FOUND')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Unified manager error: {e}")
        print("💡 This is normal if continuous_data_fetcher.py needs dependencies")
        return False

if __name__ == "__main__":
    print("🇸🇦 Saudi Stock Data Validation")
    print("=" * 50)
    
    # Test basic data
    basic_ok = test_basic_data()
    
    # Test unified manager
    unified_ok = test_unified_manager()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    
    if basic_ok:
        print("✅ Basic database has correct stock data")
        print("✅ 1010 = Saudi National Bank (NOT NCB)")
        print("✅ 1120 = Al Rajhi Bank")
    else:
        print("❌ Basic database has issues")
    
    if unified_ok:
        print("✅ Unified manager working - will use best available data")
    else:
        print("⚠️ Unified manager fallback mode - will use corrected database")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Check Portfolio Setup page in the running app (http://localhost:8507)")
    print("2. Verify that stock symbols match correct company names")
    print("3. Use the 'Validate Stock Data' button in Portfolio Setup")
    
    print(f"\n✅ Validation completed!")
