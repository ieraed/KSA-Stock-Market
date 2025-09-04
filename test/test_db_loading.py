#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from saudi_exchange_fetcher import load_official_database, get_all_saudi_stocks

print("=== TESTING DATABASE LOADING ===")
db = load_official_database()
print(f"Official database loaded: {len(db)} stocks")

if len(db) > 50:
    print("✅ SUCCESS: Database loading is working!")
    print("Sample stocks:")
    for stock in db[:5]:
        print(f"  {stock['symbol']}: {stock['name']}")
else:
    print("❌ ISSUE: Database loading failed")

print("\n=== TESTING STOCK VERIFICATION ===")
stocks = get_all_saudi_stocks()
print(f"Verified stocks: {len(stocks)} with live data")

if len(stocks) > 10:
    print("✅ SUCCESS: Enhanced stock verification working!")
else:
    print("❌ ISSUE: Still getting minimal stock list")
