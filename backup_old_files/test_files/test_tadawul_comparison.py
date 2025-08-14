"""
Data Comparison Tool - Saudi Stock Market
Compare our app data with Tadawul website data to understand differences
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import time

def test_tadawul_symbols():
    """Test the symbols from your Tadawul image"""
    
    print("=" * 60)
    print("TADAWUL DATA COMPARISON TEST")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 60)
    
    # Symbols from your image
    test_symbols = {
        # Gainers from your image
        'BAWAN': {'yahoo': '1302.SR', 'tadawul': '1302', 'expected_gain': 9.94},
        'BANAN': {'yahoo': '1201.SR', 'tadawul': '1201', 'expected_gain': 9.73},
        'ALSAGR': {'yahoo': '8312.SR', 'tadawul': '8312', 'expected_gain': 5.76},
        'ENTAJ': {'yahoo': '1020.SR', 'tadawul': '1020', 'expected_gain': 4.74},
        'MEDGULF': {'yahoo': '4162.SR', 'tadawul': '4162', 'expected_gain': 4.43},
        
        # Losers from your image  
        'ABO_MOATI': {'yahoo': '6004.SR', 'tadawul': '6004', 'expected_loss': -4.83},
        'ALHAMMADI': {'yahoo': '4013.SR', 'tadawul': '4013', 'expected_loss': -4.44},
        'SRMG': {'yahoo': '1321.SR', 'tadawul': '1321', 'expected_loss': -3.03},
        'CENOMI_RETAIL': {'yahoo': '4003.SR', 'tadawul': '4003', 'expected_loss': -2.98},
        'CENOMI_CENTERS': {'yahoo': '4004.SR', 'tadawul': '4004', 'expected_loss': -2.88}
    }
    
    print("Testing symbols from your Tadawul image...\n")
    
    results = []
    
    for name, info in test_symbols.items():
        print(f"Testing {name} ({info['tadawul']})...")
        
        try:
            # Get data from Yahoo Finance
            ticker = yf.Ticker(info['yahoo'])
            hist = ticker.history(period="2d")
            
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                change_pct = ((current_price - prev_close) / prev_close) * 100
                
                # Compare with expected
                expected = info.get('expected_gain', info.get('expected_loss', 0))
                difference = abs(change_pct - expected)
                
                results.append({
                    'Symbol': name,
                    'Tadawul_Code': info['tadawul'],
                    'Yahoo_Symbol': info['yahoo'],
                    'Our_Change%': f"{change_pct:+.2f}%",
                    'Expected_Change%': f"{expected:+.2f}%",
                    'Difference': f"{difference:.2f}%",
                    'Data_Available': 'Yes',
                    'Current_Price': f"{current_price:.2f}"
                })
                
                print(f"  ✅ Our data: {change_pct:+.2f}% | Expected: {expected:+.2f}% | Diff: {difference:.2f}%")
                
            else:
                results.append({
                    'Symbol': name,
                    'Tadawul_Code': info['tadawul'],
                    'Yahoo_Symbol': info['yahoo'],
                    'Our_Change%': 'No Data',
                    'Expected_Change%': f"{info.get('expected_gain', info.get('expected_loss', 0)):+.2f}%",
                    'Difference': 'N/A',
                    'Data_Available': 'No',
                    'Current_Price': 'N/A'
                })
                print(f"  ❌ No data available for {info['yahoo']}")
                
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
            results.append({
                'Symbol': name,
                'Tadawul_Code': info['tadawul'],
                'Yahoo_Symbol': info['yahoo'],
                'Our_Change%': 'Error',
                'Expected_Change%': f"{info.get('expected_gain', info.get('expected_loss', 0)):+.2f}%",
                'Difference': 'N/A',
                'Data_Available': 'Error',
                'Current_Price': 'N/A'
            })
        
        time.sleep(0.5)  # Rate limiting
    
    # Create summary
    df = pd.DataFrame(results)
    
    print("\n" + "=" * 60)
    print("SUMMARY COMPARISON TABLE")
    print("=" * 60)
    print(df.to_string(index=False))
    
    # Analysis
    print("\n" + "=" * 60)
    print("ANALYSIS & RECOMMENDATIONS")
    print("=" * 60)
    
    available_data = df[df['Data_Available'] == 'Yes']
    
    if len(available_data) > 0:
        avg_difference = pd.to_numeric(available_data['Difference'].str.replace('%', ''), errors='coerce').mean()
        print(f"Average difference from Tadawul data: {avg_difference:.2f}%")
        
        if avg_difference > 2:
            print("🔴 HIGH DISCREPANCY - Consider alternative data sources")
        elif avg_difference > 1:
            print("🟡 MODERATE DISCREPANCY - Acceptable for general analysis")
        else:
            print("🟢 LOW DISCREPANCY - Good data quality")
    
    print("\nReasons for differences:")
    print("1. Data timing: Yahoo Finance has 15-20 minute delays")
    print("2. Currency conversion: Some prices may be in different currencies")
    print("3. Symbol mapping: Yahoo uses .SR suffix, Tadawul uses plain numbers")
    print("4. Market hours: Data updates during different windows")
    print("5. Corporate actions: Splits, dividends may be handled differently")
    
    print("\nSolutions:")
    print("1. Use official Tadawul API (paid subscription required)")
    print("2. Implement real-time WebSocket feeds")
    print("3. Use professional data providers (Reuters, Bloomberg)")
    print("4. Add data timestamp warnings in your app")
    print("5. Implement multiple data source cross-validation")
    
    return df

if __name__ == "__main__":
    results = test_tadawul_symbols()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tadawul_comparison_{timestamp}.csv"
    results.to_csv(filename, index=False)
    print(f"\nResults saved to: {filename}")
