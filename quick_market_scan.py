"""
Quick Saudi Market Scanner
Simple script to quickly fetch current prices and volumes for all Saudi stocks
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import json
import time
from typing import List, Dict

def get_all_saudi_symbols() -> List[str]:
    """Get all Saudi stock symbols with .SR suffix"""
    
    # All sectors combined - comprehensive list
    symbols = [
        # Banks (Major ones)
        "1010.SR", "1020.SR", "1030.SR", "1050.SR", "1060.SR", "1080.SR", 
        "1120.SR", "1140.SR", "1150.SR", "1180.SR",
        
        # Energy & Materials (Including Aramco)
        "2222.SR", "2010.SR", "2020.SR", "2030.SR", "2040.SR", "2050.SR", 
        "2060.SR", "2070.SR", "2080.SR", "2090.SR", "2170.SR", "2190.SR",
        "2210.SR", "2220.SR", "2230.SR", "2280.SR", "2290.SR", "2330.SR",
        "2350.SR", "2380.SR", "2382.SR",
        
        # Real Estate & Development
        "4020.SR", "4090.SR", "4100.SR", "4110.SR", "4130.SR", "4150.SR",
        "4160.SR", "4170.SR", "4180.SR", "4190.SR", "4220.SR", "4230.SR",
        "4240.SR", "4300.SR", "4310.SR", "4320.SR", "4321.SR", "4322.SR",
        "4323.SR", "4324.SR", "4325.SR", "4326.SR", "4327.SR", "4328.SR",
        "4330.SR", "4338.SR",
        
        # Consumer & Services
        "4001.SR", "4002.SR", "4003.SR", "4004.SR", "4005.SR", "4006.SR",
        "4007.SR", "4008.SR", "4009.SR", "4010.SR", "4050.SR", "4051.SR",
        "4070.SR", "4080.SR", "4084.SR", "4161.SR", "4162.SR", "4163.SR",
        "4164.SR", "4191.SR", "4192.SR", "4194.SR",
        
        # Telecom & Technology
        "7010.SR", "7020.SR", "7030.SR", "7040.SR", "7200.SR", "7201.SR",
        "7202.SR", "7203.SR",
        
        # Insurance
        "8010.SR", "8020.SR", "8030.SR", "8040.SR", "8050.SR", "8060.SR",
        "8070.SR", "8100.SR", "8120.SR", "8150.SR", "8160.SR", "8170.SR",
        "8180.SR", "8190.SR", "8200.SR", "8210.SR", "8230.SR", "8240.SR",
        "8250.SR", "8260.SR", "8270.SR", "8280.SR", "8300.SR", "8310.SR",
        
        # Utilities
        "5110.SR", "5120.SR",
        
        # Food & Agriculture
        "6001.SR", "6010.SR", "6020.SR", "6040.SR", "6050.SR", "6060.SR",
        "6070.SR", "6090.SR", "6015.SR",
        
        # Transportation
        "4030.SR", "4040.SR", "4260.SR", "4261.SR", "4262.SR", "4270.SR",
        
        # Additional major stocks
        "1303.SR", "1304.SR", "1810.SR", "1820.SR", "1830.SR", "1833.SR",
        "3020.SR", "3030.SR", "3040.SR", "3050.SR", "3060.SR", "3080.SR",
        "3090.SR", "3091.SR", "3092.SR", "9408.SR"
    ]
    
    return sorted(list(set(symbols)))  # Remove duplicates and sort

def fetch_stock_data(symbol: str) -> Dict:
    """Fetch current data for a single stock"""
    try:
        clean_symbol = symbol.replace('.SR', '')
        ticker = yf.Ticker(symbol)
        
        # Get recent data
        hist = ticker.history(period="5d", interval="1d")
        if hist.empty:
            return {'symbol': clean_symbol, 'success': False, 'error': 'No data'}
        
        current_price = float(hist['Close'].iloc[-1])
        volume = int(hist['Volume'].iloc[-1])
        
        # Calculate change if we have previous data
        if len(hist) > 1:
            prev_close = float(hist['Close'].iloc[-2])
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close > 0 else 0
        else:
            change = 0
            change_pct = 0
        
        return {
            'symbol': clean_symbol,
            'current_price': round(current_price, 2),
            'volume': volume,
            'change': round(change, 2),
            'change_percent': round(change_pct, 2),
            'high': round(float(hist['High'].iloc[-1]), 2),
            'low': round(float(hist['Low'].iloc[-1]), 2),
            'success': True,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'symbol': symbol.replace('.SR', ''),
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def quick_market_scan() -> Dict:
    """Quick scan of all Saudi stocks"""
    
    print("🔍 Quick Saudi Market Scanner")
    print("=" * 40)
    
    symbols = get_all_saudi_symbols()
    print(f"Scanning {len(symbols)} stocks...")
    
    results = []
    successful = 0
    
    for i, symbol in enumerate(symbols, 1):
        try:
            data = fetch_stock_data(symbol)
            results.append(data)
            
            if data.get('success'):
                successful += 1
                print(f"✅ {data['symbol']}: {data['current_price']} SAR (Vol: {data['volume']:,})")
            else:
                print(f"❌ {data['symbol']}: {data.get('error', 'Failed')}")
            
            # Progress update
            if i % 20 == 0:
                print(f"\nProgress: {i}/{len(symbols)} ({successful} successful)\n")
            
            time.sleep(0.1)  # Be nice to the API
            
        except KeyboardInterrupt:
            print("\n🛑 Scan interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error with {symbol}: {str(e)}")
            results.append({'symbol': symbol.replace('.SR', ''), 'success': False, 'error': str(e)})
    
    # Summary
    successful_stocks = [r for r in results if r.get('success')]
    
    if successful_stocks:
        # Sort by performance
        by_change = sorted(successful_stocks, key=lambda x: x.get('change_percent', 0), reverse=True)
        by_volume = sorted(successful_stocks, key=lambda x: x.get('volume', 0), reverse=True)
        
        print(f"\n📊 SCAN COMPLETE")
        print(f"Successfully scanned: {len(successful_stocks)}/{len(results)} stocks")
        
        if by_change:
            print(f"🏆 Top Gainer: {by_change[0]['symbol']} (+{by_change[0]['change_percent']:.2f}%)")
            print(f"📉 Top Loser: {by_change[-1]['symbol']} ({by_change[-1]['change_percent']:.2f}%)")
        
        if by_volume:
            print(f"📈 Highest Volume: {by_volume[0]['symbol']} ({by_volume[0]['volume']:,} shares)")
        
        return {
            'success': True,
            'total_scanned': len(successful_stocks),
            'top_gainers': by_change[:10],
            'top_losers': by_change[-10:],
            'highest_volume': by_volume[:10],
            'all_data': successful_stocks,
            'timestamp': datetime.now().isoformat()
        }
    else:
        return {'success': False, 'error': 'No successful stock data'}

def save_quick_results(data: Dict, format: str = 'json'):
    """Save results quickly"""
    if not data.get('success'):
        print("❌ No data to save")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format.lower() == 'json':
        filename = f"quick_market_scan_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Saved to {filename}")
    
    elif format.lower() == 'csv':
        filename = f"quick_market_scan_{timestamp}.csv"
        df = pd.DataFrame(data['all_data'])
        df.to_csv(filename, index=False)
        print(f"💾 Saved to {filename}")

if __name__ == "__main__":
    # Run quick scan
    results = quick_market_scan()
    
    if results.get('success'):
        # Ask user if they want to save
        save_choice = input("\nSave results? (json/csv/no): ").strip().lower()
        if save_choice in ['json', 'csv']:
            save_quick_results(results, save_choice)
        
        print("\n🎉 Quick scan completed!")
    else:
        print(f"\n❌ Scan failed: {results.get('error')}")
