#!/usr/bin/env python3
"""
Update Database with Official TASI Sectors
Import the official TASI sector data and update our JSON database
"""

import json
import pandas as pd
import os
from datetime import datetime

def load_official_tasi_data():
    """Load the official TASI sectors data"""
    try:
        # Read the tab-separated file
        tasi_file = 'data/Saudi Stock Exchange (TASI) Sectors and Companies.db'
        
        # Read as tab-separated values
        df = pd.read_csv(tasi_file, sep='\t', encoding='utf-8')
        
        print(f"📊 Loaded {len(df)} records from official TASI data")
        print(f"📄 Columns: {list(df.columns)}")
        
        # Show sample data
        print("\n📋 Sample TASI Data:")
        print(df.head())
        
        # Show sector distribution
        if 'Sector' in df.columns:
            sector_counts = df['Sector'].value_counts()
            print(f"\n🏢 Official TASI Sectors ({len(sector_counts)} total):")
            for sector, count in sector_counts.items():
                print(f"  {sector}: {count} stocks")
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading TASI data: {e}")
        return None

def update_json_database_with_tasi(tasi_df):
    """Update the JSON database with official TASI sector data"""
    try:
        # Load current JSON database
        json_path = 'data/saudi_stocks_database.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            json_db = json.load(f)
        
        print(f"📄 Current JSON database: {len(json_db)} stocks")
        
        # Create backup
        backup_path = f"data/saudi_stocks_database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(json_db, f, ensure_ascii=False, indent=2)
        print(f"💾 Backup created: {backup_path}")
        
        # Update sectors based on TASI data
        updates_made = 0
        new_stocks_added = 0
        sector_changes = []
        
        for _, row in tasi_df.iterrows():
            symbol = str(row['Symbol']).strip()
            company_name = str(row['Company Name']).strip()
            tasi_sector = str(row['Sector']).strip()
            
            if symbol in json_db:
                # Update existing stock
                old_sector = json_db[symbol].get('sector', 'Unknown')
                if old_sector != tasi_sector:
                    sector_changes.append({
                        'symbol': symbol,
                        'company': company_name,
                        'old_sector': old_sector,
                        'new_sector': tasi_sector
                    })
                    json_db[symbol]['sector'] = tasi_sector
                    updates_made += 1
                
                # Update company name if different
                if 'name_en' not in json_db[symbol] or json_db[symbol]['name_en'] != company_name:
                    json_db[symbol]['name_en'] = company_name
            else:
                # Add new stock
                json_db[symbol] = {
                    'symbol': symbol,
                    'name_en': company_name,
                    'name_ar': '',  # Will need to be filled separately
                    'sector': tasi_sector
                }
                new_stocks_added += 1
        
        # Save updated database
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_db, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Database updated successfully!")
        print(f"📊 Total stocks after update: {len(json_db)}")
        print(f"🔄 Sector updates: {updates_made}")
        print(f"➕ New stocks added: {new_stocks_added}")
        
        if sector_changes:
            print(f"\n📋 Sector Changes Made ({len(sector_changes)}):")
            for change in sector_changes[:10]:  # Show first 10
                print(f"  {change['symbol']} ({change['company']}): {change['old_sector']} → {change['new_sector']}")
            if len(sector_changes) > 10:
                print(f"  ... and {len(sector_changes) - 10} more changes")
        
        # Show final sector distribution
        final_sectors = {}
        for symbol, data in json_db.items():
            sector = data.get('sector', 'Unknown')
            final_sectors[sector] = final_sectors.get(sector, 0) + 1
        
        print(f"\n🏢 Final Sector Distribution ({len(final_sectors)} sectors):")
        for sector, count in sorted(final_sectors.items(), key=lambda x: x[1], reverse=True):
            print(f"  {sector}: {count} stocks")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        return False

if __name__ == "__main__":
    print("🔄 UPDATING DATABASE WITH OFFICIAL TASI SECTORS")
    print("=" * 60)
    
    # Load official TASI data
    tasi_df = load_official_tasi_data()
    
    if tasi_df is not None:
        print("\n" + "=" * 60)
        # Update JSON database
        success = update_json_database_with_tasi(tasi_df)
        
        if success:
            print("\n🎉 SUCCESS! Database updated with official TASI sectors")
            print("📱 Your app will now use the correct sector classifications")
            print("🔄 Restart the app to see the changes")
        else:
            print("\n❌ FAILED to update database")
    else:
        print("\n❌ Could not load TASI data")
