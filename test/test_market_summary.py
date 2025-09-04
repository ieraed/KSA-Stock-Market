#!/usr/bin/env python3
"""
Simple test to isolate get_market_summary() issue
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
sys.path.append('.')

def test_market_summary():
    print("Testing get_market_summary() specifically...")
    
    try:
        from saudi_exchange_fetcher import get_market_summary
        print("✅ Import successful")
        
        print("Calling get_market_summary()...")
        result = get_market_summary()
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        if result:
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                print("✅ Market summary worked!")
                for key in ['top_gainers', 'top_losers', 'volume_movers', 'value_movers']:
                    count = len(result.get(key, []))
                    print(f"  {key}: {count} items")
            else:
                print(f"❌ get_market_summary failed: {result.get('error')}")
        else:
            print("❌ get_market_summary returned None")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_market_summary()
