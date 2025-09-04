#!/usr/bin/env python3
"""
Test script to verify the accuracy of stock price and volume data
after implementing the real-time data fixes.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
sys.path.append('.')

from saudi_exchange_fetcher import get_stock_price
from datetime import datetime

def test_data_accuracy():
    """Test the stocks mentioned in the accuracy issue"""
    
    print("=" * 80)
    print("DATA ACCURACY TESTING - Real-time Price & Volume Verification")
    print("=" * 80)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test stocks with expected values (from user report)
    test_cases = [
        {
            'symbol': '2010',
            'name': 'Saudi Basic Industries Corp (SABIC)',
            'expected_price': 60.2,
            'reported_price': 123.20,
            'issue': 'Price double what it should be'
        },
        {
            'symbol': '2130', 
            'name': 'Saudi Industrial Development',
            'expected_price': 28.98,
            'reported_price': 33.12,
            'issue': 'Price higher than expected'
        },
        {
            'symbol': '4270',
            'name': 'Saudi Public Procurement', 
            'expected_price': 11.29,
            'reported_price': 12.63,
            'issue': 'Price higher than expected'
        },
        {
            'symbol': '1120',
            'name': 'Al Rajhi Bank',
            'expected_volume': 2089095,
            'reported_volume': 8750280,
            'issue': 'Volume much higher than TASI'
        },
        {
            'symbol': '7010',
            'name': 'Saudi Telecom Company',
            'expected_volume': 3660263,
            'reported_volume': 5240180,
            'issue': 'Volume higher than TASI'
        },
        {
            'symbol': '2222',
            'name': 'Saudi Arabian Oil Company (Aramco)',
            'expected_volume': 11323364,
            'reported_volume': 15420150,
            'issue': 'Volume higher than TASI'
        }
    ]
    
    print("TESTING PRICE & VOLUME ACCURACY:")
    print("-" * 80)
    
    for i, test in enumerate(test_cases, 1):
        symbol = test['symbol']
        name = test['name']
        
        print(f"\n{i}. Testing {symbol} - {name}")
        print(f"   Issue: {test['issue']}")
        
        if 'expected_price' in test:
            print(f"   Expected Price: {test['expected_price']} SAR")
            print(f"   Previously Reported: {test['reported_price']} SAR")
        
        if 'expected_volume' in test:
            print(f"   Expected Volume (TASI): {test['expected_volume']:,}")
            print(f"   Previously Reported: {test['reported_volume']:,}")
        
        # Fetch current data
        print("   Fetching real-time data...")
        result = get_stock_price(symbol)
        
        if result.get('success'):
            current_price = result['current_price']
            volume = result.get('volume', 0)
            data_source = result.get('data_source', 'Unknown')
            data_quality = result.get('data_quality', 'Unknown')
            
            print(f"   ✅ Current Price: {current_price} SAR")
            print(f"   ✅ Current Volume: {volume:,}")
            print(f"   📊 Data Source: {data_source}")
            print(f"   🎯 Data Quality: {data_quality}")
            
            # Analysis
            if 'expected_price' in test:
                price_diff = abs(current_price - test['expected_price'])
                price_accuracy = (1 - price_diff / test['expected_price']) * 100
                print(f"   📈 Price Accuracy: {price_accuracy:.1f}% (diff: {price_diff:.2f} SAR)")
                
                if price_accuracy > 95:
                    print("   ✅ PRICE ACCURACY: EXCELLENT")
                elif price_accuracy > 85:
                    print("   ⚠️  PRICE ACCURACY: GOOD")
                else:
                    print("   ❌ PRICE ACCURACY: NEEDS IMPROVEMENT")
            
            if 'expected_volume' in test:
                if volume > 0:
                    volume_diff = abs(volume - test['expected_volume'])
                    volume_accuracy = (1 - volume_diff / test['expected_volume']) * 100 if test['expected_volume'] > 0 else 0
                    print(f"   📊 Volume Accuracy: {volume_accuracy:.1f}% (diff: {volume_diff:,})")
                    
                    if volume_accuracy > 90:
                        print("   ✅ VOLUME ACCURACY: EXCELLENT")
                    elif volume_accuracy > 70:
                        print("   ⚠️  VOLUME ACCURACY: GOOD")
                    else:
                        print("   ❌ VOLUME ACCURACY: NEEDS IMPROVEMENT")
                else:
                    print("   ❌ VOLUME DATA: NOT AVAILABLE")
        else:
            print(f"   ❌ ERROR: {result.get('error', 'Unknown error')}")
    
    print("\n" + "=" * 80)
    print("DATA ACCURACY TEST COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_data_accuracy()
