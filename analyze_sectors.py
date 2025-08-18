#!/usr/bin/env python3
"""
Analyze sector distribution in Saudi stocks database
"""

import json
from collections import Counter

def analyze_sectors():
    with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
        stocks = json.load(f)

    sector_counts = Counter()
    stocks_by_sector = {}

    for symbol, data in stocks.items():
        sector = data.get('sector', 'Unknown')
        sector_counts[sector] += 1
        
        if sector not in stocks_by_sector:
            stocks_by_sector[sector] = []
        stocks_by_sector[sector].append({
            'symbol': symbol,
            'name': data.get('name_en', 'Unknown')
        })

    print('=== SECTOR ANALYSIS ===')
    print(f'Total stocks: {len(stocks)}')
    print()

    print('Sector Distribution:')
    for sector, count in sorted(sector_counts.items()):
        print(f'  {sector}: {count} stocks')
        
    print()
    print('=== SAMPLE STOCKS BY SECTOR ===')
    for sector in sorted(stocks_by_sector.keys()):
        print(f'\n{sector} ({sector_counts[sector]} stocks):')
        for stock in stocks_by_sector[sector][:3]:
            symbol = stock['symbol']
            name = stock['name']
            print(f'  {symbol}: {name}')
        if len(stocks_by_sector[sector]) > 3:
            remaining = len(stocks_by_sector[sector]) - 3
            print(f'  ... and {remaining} more')

    # Check for specific issues mentioned
    print('\n=== CHECKING SPECIFIC ISSUES ===')
    
    # Check for stock 9642 "Time"
    if '9642' in stocks:
        print(f'Stock 9642: {stocks["9642"]}')
    else:
        print('Stock 9642 not found in database')
    
    # Check BAWAN (1302)
    if '1302' in stocks:
        print(f'BAWAN (1302): {stocks["1302"]}')
    else:
        print('BAWAN (1302) not found in database')

if __name__ == '__main__':
    analyze_sectors()
