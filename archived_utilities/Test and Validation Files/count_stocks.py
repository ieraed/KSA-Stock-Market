#!/usr/bin/env python3
import json

def count_stocks():
    try:
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Total stocks in TADAWUL NEXUS database: {len(data)}")
        
        # Count by sector
        sectors = {}
        for stock in data.values():
            sector = stock.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        print("\n📋 Stocks by sector:")
        for sector, count in sorted(sectors.items()):
            print(f"  {sector}: {count}")
        
        # Sample of new stocks added
        print("\n🆕 Sample of recently added stocks:")
        new_stocks = ['1070', '1090', '9408', '9409', '9410', '4330', '4340', '1080']
        for symbol in new_stocks:
            if symbol in data:
                stock = data[symbol]
                print(f"  {symbol}: {stock['name_en']} ({stock['sector']})")
        
        return len(data)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

if __name__ == "__main__":
    total = count_stocks()
    progress = (total / 259) * 100
    print(f"\n✅ Progress toward 259 stocks: {total}/259 ({progress:.1f}%)")
    if total >= 259:
        print("🎉 Target achieved!")
    else:
        remaining = 259 - total
        print(f"📈 Need {remaining} more stocks to reach target")
