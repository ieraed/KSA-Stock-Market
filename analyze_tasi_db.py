#!/usr/bin/env python3
"""
Analyze TASI Database vs JSON Database
Compare the official TASI data with current JSON database
"""

import sqlite3
import json
import pandas as pd

def analyze_tasi_database():
    """Analyze the TASI database file"""
    try:
        conn = sqlite3.connect('data/Saudi Stock Exchange (TASI) Sectors and Companies.db')
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print('📊 TASI Database Tables:')
        for table in tables:
            print(f'  - {table[0]}')
        
        # Get stock count from each table
        for table_name in [table[0] for table in tables]:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
                count = cursor.fetchone()[0]
                print(f'  📈 {table_name}: {count} records')
                
                if count > 200:  # Likely the main stocks table
                    cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 3')
                    columns = [description[0] for description in cursor.description]
                    print(f'  🏷️ Columns: {columns}')
                    
                    rows = cursor.fetchall()
                    for i, row in enumerate(rows):
                        print(f'  📄 Sample {i+1}: {dict(zip(columns, row))}')
            except Exception as e:
                print(f'  ❌ Error reading {table_name}: {e}')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f'❌ Error reading TASI database: {e}')
        return False

def analyze_json_database():
    """Analyze the current JSON database"""
    try:
        with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print(f'\n📄 JSON Database: {len(json_data)} stocks')
        
        # Show a sample
        sample_key = list(json_data.keys())[0]
        print(f'📄 JSON Sample: {sample_key} -> {json_data[sample_key]}')
        
        # Count sectors
        sectors = {}
        for symbol, data in json_data.items():
            sector = data.get('sector', 'Unknown')
            sectors[sector] = sectors.get(sector, 0) + 1
        
        print(f'\n📊 JSON Database Sectors ({len(sectors)} total):')
        for sector, count in sorted(sectors.items(), key=lambda x: x[1], reverse=True):
            print(f'  {sector}: {count} stocks')
            
        return json_data
        
    except Exception as e:
        print(f'❌ Error reading JSON database: {e}')
        return None

if __name__ == "__main__":
    print("🔍 ANALYZING DATABASES...")
    print("=" * 50)
    
    # Analyze TASI database
    tasi_available = analyze_tasi_database()
    
    # Analyze JSON database
    json_data = analyze_json_database()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    if tasi_available and json_data:
        print(f"✅ Both databases available")
        print(f"📄 JSON has {len(json_data)} stocks")
        print("🚨 Check if we need to update JSON from TASI official data")
    elif json_data:
        print(f"✅ JSON database available with {len(json_data)} stocks")
        print("⚠️ TASI database not accessible")
    else:
        print("❌ No accessible databases found")
