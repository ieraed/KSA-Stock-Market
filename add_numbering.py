#!/usr/bin/env python3
"""
📊 Database Numbering Tool
Adds sequential numbering to the Saudi stocks database file
"""

import json
from collections import OrderedDict

def add_numbering_to_database():
    """Add sequential numbering to database entries"""
    
    # Load the database
    with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
        stocks = json.load(f)
    
    print(f"📊 Processing {len(stocks)} stocks...")
    
    # Sort stocks by symbol for consistent ordering
    sorted_stocks = OrderedDict(sorted(stocks.items()))
    
    # Create numbered content
    numbered_content = "{\n"
    
    for i, (symbol, data) in enumerate(sorted_stocks.items(), 1):
        # Add comment with number
        numbered_content += f'  // {i}- {symbol}: {data.get("name_en", "N/A")}\n'
        
        # Add the actual JSON entry
        numbered_content += f'  "{symbol}": {{\n'
        numbered_content += f'    "symbol": "{symbol}",\n'
        numbered_content += f'    "name_en": "{data.get("name_en", "")}",\n'
        numbered_content += f'    "name_ar": "{data.get("name_ar", "")}",\n'
        numbered_content += f'    "sector": "{data.get("sector", "")}"\n'
        
        # Add comma if not last item
        if i < len(sorted_stocks):
            numbered_content += "  },\n"
        else:
            numbered_content += "  }\n"
    
    numbered_content += "}"
    
    # Save numbered version
    with open('data/saudi_stocks_database_numbered.json', 'w', encoding='utf-8') as f:
        f.write(numbered_content)
    
    print(f"✅ Created numbered database with {len(stocks)} stocks")
    print("📁 Saved as: data/saudi_stocks_database_numbered.json")

if __name__ == "__main__":
    add_numbering_to_database()
