#!/usr/bin/env python3
import json
import sys

def fix_database():
    try:
        # Load the existing database
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Original database has {len(data)} stocks")
        
        # Check for duplicates
        symbols = []
        for key, stock in data.items():
            if stock['symbol'] in symbols:
                print(f"Duplicate found: {stock['symbol']} - {stock['name_en']}")
            else:
                symbols.append(stock['symbol'])
        
        print(f"Unique stocks: {len(symbols)}")
        
        # Create a clean database with no duplicates
        clean_data = {}
        for key, stock in data.items():
            symbol = stock['symbol']
            if symbol not in clean_data:
                clean_data[symbol] = stock
            else:
                print(f"Skipping duplicate: {symbol}")
        
        # Save the clean database
        with open('saudi_stocks_database_clean.json', 'w', encoding='utf-8') as f:
            json.dump(clean_data, f, ensure_ascii=False, indent=2)
        
        print(f"Clean database saved with {len(clean_data)} stocks")
        
        return len(clean_data)
        
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    fix_database()
