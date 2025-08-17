#!/usr/bin/env python3

import json

def count_stocks():
    try:
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            stock_count = len(data)
            print(f"Total number of stocks in database: {stock_count}")
            
            # Show first few symbols
            symbols = list(data.keys())[:10]
            print(f"First 10 symbols: {symbols}")
            
            # Show last few symbols
            last_symbols = list(data.keys())[-10:]
            print(f"Last 10 symbols: {last_symbols}")
            
            return stock_count
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    count_stocks()
