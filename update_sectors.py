#!/usr/bin/env python3
"""
🔄 TASI SECTOR UPDATE TOOL
Import and update stock sectors from official TASI data

This tool helps update the Saudi stocks database with official 
sector classifications from Saudi Exchange (TASI).
"""

import json
import pandas as pd
import os
from datetime import datetime

def load_current_database():
    """Load the current Saudi stocks database"""
    try:
        with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Current database file not found!")
        return {}

def backup_database():
    """Create a backup of the current database"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'data/saudi_stocks_database_backup_{timestamp}.json'
    
    try:
        current_db = load_current_database()
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(current_db, f, ensure_ascii=False, indent=2)
        print(f"✅ Backup created: {backup_filename}")
        return backup_filename
    except Exception as e:
        print(f"❌ Error creating backup: {str(e)}")
        return None

def update_sectors_from_file(csv_file_path, symbol_col='Symbol', sector_col='Sector', name_col=None):
    """
    Update sectors from CSV/Excel file
    
    Args:
        csv_file_path: Path to the CSV/Excel file
        symbol_col: Column name for stock symbols
        sector_col: Column name for sectors
        name_col: Column name for company names (optional)
    """
    
    print(f"📂 Reading file: {csv_file_path}")
    
    # Read the file
    try:
        if csv_file_path.endswith('.csv'):
            df = pd.read_csv(csv_file_path)
        elif csv_file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(csv_file_path)
        else:
            print("❌ Unsupported file format. Use CSV or Excel files.")
            return False
            
        print(f"✅ File loaded successfully. Found {len(df)} rows.")
        print(f"📊 Columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return False
    
    # Validate required columns
    if symbol_col not in df.columns:
        print(f"❌ Symbol column '{symbol_col}' not found in file.")
        print(f"Available columns: {list(df.columns)}")
        return False
        
    if sector_col not in df.columns:
        print(f"❌ Sector column '{sector_col}' not found in file.")
        print(f"Available columns: {list(df.columns)}")
        return False
    
    # Load current database
    current_db = load_current_database()
    if not current_db:
        return False
    
    # Create backup
    backup_file = backup_database()
    if not backup_file:
        print("❌ Failed to create backup. Aborting update.")
        return False
    
    # Update sectors
    updated_count = 0
    new_stocks = 0
    sector_changes = []
    
    print("\n🔄 Starting sector updates...")
    
    for index, row in df.iterrows():
        symbol = str(row[symbol_col]).strip()
        new_sector = str(row[sector_col]).strip()
        
        if pd.isna(symbol) or pd.isna(new_sector) or symbol == '' or new_sector == '':
            continue
            
        # Remove any prefix/suffix from symbol (like .SR, .TADAWUL, etc.)
        symbol = symbol.replace('.SR', '').replace('.TADAWUL', '').strip()
        
        if symbol in current_db:
            old_sector = current_db[symbol].get('sector', 'Unknown')
            
            if old_sector != new_sector:
                current_db[symbol]['sector'] = new_sector
                sector_changes.append({
                    'symbol': symbol,
                    'company': current_db[symbol].get('name_en', 'Unknown'),
                    'old_sector': old_sector,
                    'new_sector': new_sector
                })
                updated_count += 1
                
            # Update company name if provided and different
            if name_col and name_col in df.columns:
                new_name = str(row[name_col]).strip()
                if not pd.isna(new_name) and new_name != '':
                    current_db[symbol]['name_en'] = new_name
                    
        else:
            # New stock not in our database
            print(f"⚠️ New stock found: {symbol} - {new_sector}")
            new_stocks += 1
            
            # Add basic entry for new stock
            current_db[symbol] = {
                'symbol': symbol,
                'name_en': row[name_col] if name_col and name_col in df.columns else f'Company {symbol}',
                'name_ar': f'شركة {symbol}',
                'sector': new_sector
            }
    
    # Save updated database
    try:
        with open('data/saudi_stocks_database.json', 'w', encoding='utf-8') as f:
            json.dump(current_db, f, ensure_ascii=False, indent=2)
        print(f"✅ Database updated successfully!")
    except Exception as e:
        print(f"❌ Error saving updated database: {str(e)}")
        return False
    
    # Print summary
    print(f"\n📊 UPDATE SUMMARY:")
    print(f"✅ Total stocks processed: {len(df)}")
    print(f"🔄 Sector updates: {updated_count}")
    print(f"🆕 New stocks added: {new_stocks}")
    print(f"📈 Total stocks in database: {len(current_db)}")
    
    if sector_changes:
        print(f"\n🔄 SECTOR CHANGES:")
        for change in sector_changes[:10]:  # Show first 10 changes
            print(f"  {change['symbol']} ({change['company']}): {change['old_sector']} → {change['new_sector']}")
        
        if len(sector_changes) > 10:
            print(f"  ... and {len(sector_changes) - 10} more changes")
            
        # Save changes log
        changes_df = pd.DataFrame(sector_changes)
        changes_file = f'sector_changes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        changes_df.to_csv(changes_file, index=False)
        print(f"📋 Detailed changes saved to: {changes_file}")
    
    return True

def analyze_sector_differences():
    """Analyze current sector distribution"""
    current_db = load_current_database()
    if not current_db:
        return
        
    sector_counts = {}
    for symbol, data in current_db.items():
        sector = data.get('sector', 'Unknown')
        sector_counts[sector] = sector_counts.get(sector, 0) + 1
    
    print("📊 CURRENT SECTOR DISTRIBUTION:")
    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {sector}: {count} stocks")
    
    print(f"\nTotal stocks: {len(current_db)}")
    print(f"Total sectors: {len(sector_counts)}")

if __name__ == "__main__":
    print("🔄 TASI SECTOR UPDATE TOOL")
    print("=" * 40)
    
    # Show current sector distribution
    print("\n1. CURRENT DATABASE ANALYSIS:")
    analyze_sector_differences()
    
    print("\n2. UPDATE OPTIONS:")
    print("To update sectors from your TASI file, use one of these methods:")
    print()
    print("Method 1 - Direct function call:")
    print("update_sectors_from_file('your_file.csv', symbol_col='Symbol', sector_col='Sector')")
    print()
    print("Method 2 - Command line with custom columns:")
    print("# Modify the column names below to match your file:")
    
    # Example usage - you can uncomment and modify this
    # UNCOMMENT AND MODIFY THE LINE BELOW TO MATCH YOUR FILE:
    # update_sectors_from_file('your_tasi_file.csv', symbol_col='Symbol', sector_col='Sector', name_col='Company Name')
    
    print("\n📋 INSTRUCTIONS:")
    print("1. Place your TASI sector file in this directory")
    print("2. Modify the function call above with your file name and column names")
    print("3. Run this script again")
    print()
    print("📄 Your file should have these columns:")
    print("  - Symbol (stock symbol like '1302', '9642', etc.)")
    print("  - Sector (official TASI sector name)")
    print("  - Company Name (optional, for updating company names)")
    
    # Check for common file names
    common_files = [
        'tasi_sectors.csv', 'saudi_sectors.csv', 'tadawul_sectors.csv',
        'stock_sectors.csv', 'sectors.csv', 'tasi_data.xlsx', 'sectors.xlsx'
    ]
    
    print(f"\n🔍 LOOKING FOR COMMON FILE NAMES:")
    found_files = []
    for filename in common_files:
        if os.path.exists(filename):
            found_files.append(filename)
            print(f"  ✅ Found: {filename}")
    
    if not found_files:
        print("  ❌ No common sector files found in current directory")
        print("  📂 Current directory contents:")
        for file in os.listdir('.'):
            if file.endswith(('.csv', '.xlsx', '.xls')):
                print(f"    - {file}")
    else:
        print(f"\n💡 SUGGESTION:")
        print(f"If {found_files[0]} is your TASI sector file, uncomment and modify this line:")
        print(f"update_sectors_from_file('{found_files[0]}', symbol_col='Symbol', sector_col='Sector')")
