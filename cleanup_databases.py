#!/usr/bin/env python3
"""
Database Cleanup and Confirmation Tool
Identify the main database file and remove unnecessary duplicates
"""

import json
import os
import shutil
from datetime import datetime

def analyze_database_files():
    """Analyze all database files to understand what we have"""
    
    files_to_check = [
        'data/saudi_stocks_database.json',  # MAIN FILE - App uses this
        'data/saudi_stocks_database_numbered.json',
        'data/saudi_stocks_database_backup_20250818_200610.json',
        'RestorePoint_20250817/essential_files/saudi_stocks_database.json',
        'RestorePoint_20250817/essential_files/saudi_stocks_database_official.json'
    ]
    
    print("🔍 ANALYZING ALL STOCK DATABASE FILES")
    print("=" * 60)
    
    file_analysis = {}
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Get file size
                file_size = os.path.getsize(file_path)
                
                # Count sectors
                sectors = {}
                for symbol, stock_data in data.items():
                    sector = stock_data.get('sector', 'Unknown')
                    sectors[sector] = sectors.get(sector, 0) + 1
                
                file_analysis[file_path] = {
                    'stock_count': len(data),
                    'file_size': file_size,
                    'sector_count': len(sectors),
                    'top_sectors': sorted(sectors.items(), key=lambda x: x[1], reverse=True)[:3],
                    'sample_data': dict(list(data.items())[:2])
                }
                
                print(f"📄 {file_path}")
                print(f"   📊 Stocks: {len(data)}")
                print(f"   💾 Size: {file_size:,} bytes")
                print(f"   🏢 Sectors: {len(sectors)}")
                print(f"   🥇 Top sectors: {', '.join([f'{s}({c})' for s, c in file_analysis[file_path]['top_sectors']])}")
                print()
                
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
                print()
    
    return file_analysis

def confirm_main_database():
    """Confirm which file the app actually uses"""
    
    print("🎯 APP DATABASE CONFIRMATION")
    print("=" * 60)
    
    # This is exactly what the app does
    import sys
    sys.path.append('.')
    
    try:
        # Simulate the app's load function
        root_dir = '.'
        data_path = os.path.join(root_dir, 'data', 'saudi_stocks_database.json')
        
        with open(data_path, 'r', encoding='utf-8') as f:
            stocks = json.load(f)
        
        print(f"✅ MAIN APP DATABASE: {data_path}")
        print(f"📊 Stock count: {len(stocks)}")
        print(f"🎯 This is the file your app ACTUALLY uses")
        
        # Show sample
        sample_key = list(stocks.keys())[0]
        print(f"📋 Sample: {sample_key} -> {stocks[sample_key]}")
        
        return data_path, len(stocks)
        
    except Exception as e:
        print(f"❌ Error loading main database: {e}")
        return None, 0

def cleanup_unnecessary_files(file_analysis, main_db_path):
    """Remove unnecessary duplicate files"""
    
    print("\n🧹 CLEANUP RECOMMENDATIONS")
    print("=" * 60)
    
    # Files that are safe to remove (backups and duplicates)
    files_to_remove = []
    files_to_keep = []
    
    for file_path in file_analysis.keys():
        if file_path == main_db_path:
            files_to_keep.append(file_path)
            print(f"✅ KEEP: {file_path} (MAIN APP DATABASE)")
        elif 'backup' in file_path:
            files_to_remove.append(file_path)
            print(f"🗑️ SAFE TO REMOVE: {file_path} (Backup)")
        elif 'RestorePoint' in file_path:
            files_to_keep.append(file_path)
            print(f"📦 KEEP: {file_path} (Restore point)")
        elif 'numbered' in file_path:
            files_to_remove.append(file_path)
            print(f"🗑️ SAFE TO REMOVE: {file_path} (Duplicate with numbers)")
        else:
            files_to_keep.append(file_path)
            print(f"❓ REVIEW: {file_path}")
    
    print(f"\n📊 SUMMARY:")
    print(f"✅ Files to keep: {len(files_to_keep)}")
    print(f"🗑️ Files to remove: {len(files_to_remove)}")
    
    return files_to_remove, files_to_keep

def execute_cleanup(files_to_remove):
    """Actually remove the unnecessary files"""
    
    print(f"\n🗑️ EXECUTING CLEANUP")
    print("=" * 60)
    
    removed_count = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                # Create a backup in case we need it
                backup_dir = 'cleanup_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
                os.makedirs(backup_dir, exist_ok=True)
                
                backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, backup_path)
                
                # Remove the original
                os.remove(file_path)
                
                print(f"✅ Removed: {file_path}")
                print(f"   💾 Backup: {backup_path}")
                removed_count += 1
                
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
        else:
            print(f"⚠️ File not found: {file_path}")
    
    print(f"\n🎉 Cleanup complete! Removed {removed_count} files")

if __name__ == "__main__":
    print("🔍 STOCK DATABASE CLEANUP TOOL")
    print("=" * 60)
    
    # 1. Analyze all files
    file_analysis = analyze_database_files()
    
    # 2. Confirm main database
    main_db_path, main_stock_count = confirm_main_database()
    
    if main_db_path:
        # 3. Get cleanup recommendations
        files_to_remove, files_to_keep = cleanup_unnecessary_files(file_analysis, main_db_path)
        
        # 4. Ask user for confirmation
        if files_to_remove:
            print(f"\n❓ Would you like to remove {len(files_to_remove)} unnecessary files?")
            print("   (Backups will be created)")
            
            # For now, just show what would be removed
            print("\n📋 Files that would be removed:")
            for file_path in files_to_remove:
                print(f"   🗑️ {file_path}")
            
            print(f"\n💡 To execute cleanup, uncomment the line at the bottom of this script")
            # execute_cleanup(files_to_remove)
        else:
            print("\n✅ No unnecessary files found!")
    
    print(f"\n🎯 FINAL CONFIRMATION:")
    print(f"   📁 Your app uses: {main_db_path}")
    print(f"   📊 Stock count: {main_stock_count}")
    print(f"   🎯 This is the ONLY file that matters for your app!")
