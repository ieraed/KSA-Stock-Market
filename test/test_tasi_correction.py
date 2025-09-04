"""
Test TASI Price Correction Implementation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from saudi_exchange_fetcher import get_stock_price
import time

def test_tasi_correction():
    """Test the TASI price correction functionality"""
    print("=== TESTING TASI PRICE CORRECTION ===")
    print("This test will verify that our prices now match TASI more closely")
    print()
    
    # Test symbols with known TASI prices
    test_data = {
        '1835': {'name': 'TAMKEEN', 'expected_price': 56.75, 'expected_change': 1.98},
        '1151': {'name': 'EAST PIPES', 'expected_price': 107.60, 'expected_change': 1.61},
        '2020': {'name': 'SABIC AGRI-NUTRIENTS', 'expected_price': 120.80, 'expected_change': 1.35},
        '1211': {'name': 'MAADEN', 'expected_price': 52.85, 'expected_change': 0.96}
    }
    
    print("Symbol | Company             | Our Price | Our Change% | Expected Price | Expected Change% | Price Accuracy | Change Accuracy")
    print("-" * 120)
    
    total_price_accuracy = 0
    total_change_accuracy = 0
    successful_tests = 0
    
    for symbol, expected in test_data.items():
        try:
            result = get_stock_price(symbol)
            
            if result.get('success'):
                our_price = result['current_price']
                our_change = result.get('change_percent', 0)
                
                # Calculate accuracy (100% - percentage difference)
                price_diff_pct = abs(our_price - expected['expected_price']) / expected['expected_price'] * 100
                change_diff_pct = abs(our_change - expected['expected_change']) / abs(expected['expected_change']) * 100 if expected['expected_change'] != 0 else 0
                
                price_accuracy = max(0, 100 - price_diff_pct)
                change_accuracy = max(0, 100 - change_diff_pct)
                
                total_price_accuracy += price_accuracy
                total_change_accuracy += change_accuracy
                successful_tests += 1
                
                # Show if TASI correction was applied
                correction_status = "✅ CORRECTED" if result.get('tasi_corrected') else "⚪ NO CORRECTION"
                
                print(f"{symbol:6} | {expected['name']:19} | {our_price:9.2f} | {our_change:10.2f}% | {expected['expected_price']:13.2f} | {expected['expected_change']:15.2f}% | {price_accuracy:13.1f}% | {change_accuracy:14.1f}%")
                print(f"       | {correction_status} | Source: {result.get('data_source', 'Unknown')}")
                
                if result.get('tasi_corrected'):
                    print(f"       | Original: {result.get('original_price', 'N/A'):.2f} SAR ({result.get('original_change_pct', 'N/A'):.2f}%)")
                
                print()
            else:
                print(f"{symbol:6} | {expected['name']:19} | ERROR: {result.get('error', 'Unknown error')}")
                print()
                
        except Exception as e:
            print(f"{symbol:6} | {expected['name']:19} | EXCEPTION: {str(e)}")
            print()
            
        time.sleep(1)  # Avoid rate limiting
    
    if successful_tests > 0:
        avg_price_accuracy = total_price_accuracy / successful_tests
        avg_change_accuracy = total_change_accuracy / successful_tests
        
        print("=== SUMMARY ===")
        print(f"Successful tests: {successful_tests}/{len(test_data)}")
        print(f"Average price accuracy: {avg_price_accuracy:.1f}%")
        print(f"Average change accuracy: {avg_change_accuracy:.1f}%")
        print()
        
        if avg_price_accuracy > 95 and avg_change_accuracy > 90:
            print("🎉 EXCELLENT: Price correction is working very well!")
        elif avg_price_accuracy > 90 and avg_change_accuracy > 80:
            print("✅ GOOD: Price correction is working well!")
        elif avg_price_accuracy > 80 and avg_change_accuracy > 70:
            print("⚠️  FAIR: Price correction is helping but could be improved")
        else:
            print("❌ POOR: Price correction needs more work")
            
        print()
        print("Expected outcome: TAMKEEN should now rank correctly vs other stocks")
        print("The ranking discrepancy issue should be resolved!")

if __name__ == "__main__":
    test_tasi_correction()
