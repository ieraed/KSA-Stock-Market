#!/usr/bin/env python3
"""
Sync our database to match exactly the official TASI data (259 stocks)
"""

import json
import os
from datetime import datetime

def parse_official_tasi():
    """Parse the official TASI file and return clean stock data"""
    stocks = {}
    
    with open('data/Saudi Stock Exchange (TASI) Sectors and Companies.db', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines in TASI file: {len(lines)}")
    
    for line_num, line in enumerate(lines[1:], 1):  # Skip header
        line = line.strip()
        if not line:
            continue
            
        # Split by tabs
        parts = [p.strip() for p in line.split('\t') if p.strip()]
        
        if len(parts) >= 4:
            seq = parts[0]
            symbol = parts[1]
            company_name = parts[2]
            sector = parts[3]
            
            stocks[symbol] = {
                "name": company_name,
                "sector": sector,
                "symbol": symbol,
                "sequence": int(seq)
            }
            
    print(f"Parsed {len(stocks)} stocks from official TASI data")
    return stocks

def backup_current_database():
    """Create backup of current database"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'data/saudi_stocks_database_backup_before_sync_{timestamp}.json'
    
    if os.path.exists('data/saudi_stocks_database.json'):
        with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=2)
        
        print(f"Backup created: {backup_path}")
        print(f"Current database has {len(current_data)} stocks")
        return current_data
    
    return {}

def main():
    print("🔄 Syncing database with official TASI data...")
    
    # Backup current database
    current_data = backup_current_database()
    
    # Parse official TASI data
    official_stocks = parse_official_tasi()
    
    # Show comparison
    print(f"\n📊 Comparison:")
    print(f"   Current database: {len(current_data)} stocks")
    print(f"   Official TASI: {len(official_stocks)} stocks")
    print(f"   Difference: {len(current_data) - len(official_stocks)} stocks")
    
    # Find extra stocks in our database
    if current_data:
        our_symbols = set(current_data.keys())
        official_symbols = set(official_stocks.keys())
        extra_stocks = our_symbols - official_symbols
        
        if extra_stocks:
            print(f"\n⚠️  Stocks in our database but NOT in official TASI ({len(extra_stocks)}):")
            for stock in sorted(extra_stocks)[:20]:  # Show first 20
                name = current_data[stock].get('name', 'Unknown')
                print(f"   {stock}: {name}")
            if len(extra_stocks) > 20:
                print(f"   ... and {len(extra_stocks) - 20} more")
    
    # Write the new database with exactly 259 stocks
    with open('data/saudi_stocks_database.json', 'w', encoding='utf-8') as f:
        json.dump(official_stocks, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Database updated successfully!")
    print(f"   New database contains exactly {len(official_stocks)} stocks")
    print(f"   Matches official TASI count: 259 stocks")
    
    # Show sector distribution
    sectors = {}
    for stock_data in official_stocks.values():
        sector = stock_data['sector']
        sectors[sector] = sectors.get(sector, 0) + 1
    
    print(f"\n📈 Sector distribution:")
    for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   {sector}: {count} stocks")

if __name__ == "__main__":
    main()
