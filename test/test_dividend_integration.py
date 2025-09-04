"""
Test script to verify dividend tracker integration with main app

This script tests:
1. Import of dividend tracker modules
2. Basic functionality of each module
3. Integration with the main app structure
"""

import sys
import os

# Add the project root to the path (parent directory of test folder)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_dividend_imports():
    """Test if dividend tracker modules can be imported"""
    try:
        from dividend_tracker.fetch_dividends import fetch_dividend_table
        from dividend_tracker.summarize_dividends import summarize_user_dividends
        from dividend_tracker.style_config import style_dividend_table
        print("✅ All dividend tracker modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(f"   Current working directory: {os.getcwd()}")
        print(f"   Project root: {project_root}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_main_app_import():
    """Test if main app can import with dividend tracker"""
    try:
        # Test if enhanced_saudi_app_v2 can be imported with dividend features
        from apps.enhanced_saudi_app_v2 import dividend_tracker_available
        print(f"✅ Main app imports successfully. Dividend tracker available: {dividend_tracker_available}")
        return True
    except ImportError as e:
        print(f"❌ Main app import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in main app: {e}")
        return False

def test_module_functionality():
    """Test basic functionality of dividend modules"""
    try:
        from dividend_tracker.style_config import style_dividend_table
        import pandas as pd
        
        # Create a test dataframe
        test_data = {
            'Symbol': ['1234'],
            'Company Name': ['Test Company'],
            'Ex-Date': ['2024-01-01'],
            'Dividend Yield (%)': [5.0]
        }
        test_df = pd.DataFrame(test_data)
        
        # Test styling function
        styled_df = style_dividend_table(test_df)
        print("✅ Dividend table styling works correctly")
        return True
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Dividend Tracker Integration\n")
    
    # Run tests
    tests = [
        ("Import Test", test_dividend_imports),
        ("Main App Integration", test_main_app_import),
        ("Module Functionality", test_module_functionality)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("📋 Test Results Summary:")
    print("-" * 30)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🚀 Dividend Tracker is ready to use in the main app!")
        print("   Navigate to '💰 Dividend Tracker' in the app sidebar to access the new features.")
