#!/usr/bin/env python3
"""
Check Arab National Bank availability and count total stocks
"""

import json

def main():
    # Load database
    with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    print(f"📊 Total stocks in database: {len(db)}")
    
    # Search for Arab National Bank
    found_anb = False
    arab_banks = []
    
    for symbol, data in db.items():
        name = data.get('name_en', '').lower()
        if 'arab' in name:
            arab_banks.append((symbol, data.get('name_en', '')))
            if 'national' in name:
                print(f"✅ Found Arab National Bank: {symbol} - {data.get('name_en', '')}")
                found_anb = True
    
    if not found_anb:
        print("❌ Arab National Bank (ANB) not found in database")
    
    print(f"\n🔍 All Arab-related banks ({len(arab_banks)}):")
    for symbol, name in arab_banks:
        print(f"  {symbol}: {name}")
    
    # Check if 1080 exists (from portfolio data references)
    if '1080' in db:
        print(f"\n✅ Symbol 1080 found: {db['1080']['name_en']}")
    else:
        print("\n❌ Symbol 1080 not found in database")
    
    # Summary
    print(f"\n📋 Summary:")
    print(f"  - Total stocks: {len(db)}")
    print(f"  - User expects: 259 stocks")
    print(f"  - Missing: {259 - len(db)} stocks")
    print(f"  - Arab National Bank: {'Found' if found_anb else 'Not found'}")

if __name__ == "__main__":
    main()
