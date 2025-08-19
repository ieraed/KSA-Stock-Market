#!/usr/bin/env python3
"""
Emergency cleanup - Remove restored old files that shouldn't be in root directory
"""

import os
import shutil
from datetime import datetime

def cleanup_restored_files():
    """Remove files that were restored but should stay cleaned up"""
    
    # Files that should NOT be in root directory
    files_to_remove = [
        # Old database files (corrupted)
        'saudi_stocks_database.json',
        'saudi_stocks_database_corrected.json', 
        'saudi_stocks_database_official.json',
        
        # Old documentation files  
        'CLEANUP_GUIDE.md',
        'CLEANUP_STATUS.md',
        'COMPLETION_SUMMARY.md',
        'CONTINUOUS_DATA_README.md',
        'DATA_UNIFICATION_README.md',
        'ORGANIZATION_PLAN.md',
        'UPDATES_COMPLETED.md',
        'VALIDATION_REPORT.md',
        'ISSUE_RESOLUTION_REPORT.md',
        'FINAL_CLEANUP_SUMMARY.md',
        'CLEANUP_COMPLETED.md',
        'APP_READY.md',
        'README_ENHANCED.md',
        
        # Old app versions
        'enhanced_saudi_app.py',  # We use enhanced_saudi_app_v2.py in apps/ folder
        'enhanced_saudi_app_v2.py',  # Should be in apps/ folder only
        
        # Old scripts
        'check_database.py',
        'cleanup_and_backup.py',
        'cleanup_archive.bat', 
        'cleanup_archive.ps1',
        'complete_tadawul_database.py',
        'correct_saudi_stocks.py',
        'create_complete_database.py',
        'final_verification.py',
        'launch_enhanced_app.py',
        'new_features_summary.py',
        'test_app_database.py',
        'verify_database.py',
        'verify_fixes.py',
        
        # Old requirements
        'requirements_enhanced.txt'  # We use requirements.txt
    ]
    
    print("🧹 EMERGENCY CLEANUP - Removing restored old files...")
    print("=" * 60)
    
    # Create backup directory for removed files
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = f'removed_files_emergency_{timestamp}'
    os.makedirs(backup_dir, exist_ok=True)
    
    removed_count = 0
    backed_up_count = 0
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                # Backup before removing
                backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.copy2(file_path, backup_path)
                backed_up_count += 1
                
                # Remove the file
                os.remove(file_path)
                removed_count += 1
                print(f"✅ Removed: {file_path}")
                
            except Exception as e:
                print(f"❌ Error removing {file_path}: {e}")
        else:
            print(f"✅ Already clean: {file_path}")
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"   Files removed: {removed_count}")
    print(f"   Files backed up: {backed_up_count}")
    print(f"   Backup location: {backup_dir}")
    
    # Verify our main database is still intact
    try:
        import json
        with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            stocks = json.load(f)
        print(f"\n✅ MAIN DATABASE VERIFIED: {len(stocks)} stocks")
        
        # Check BAWAN
        if '1302' in stocks:
            bawan = stocks['1302']
            print(f"✅ BAWAN (1302): {bawan['sector']}")
        
    except Exception as e:
        print(f"❌ ERROR: Main database issue: {e}")
    
    print(f"\n🎯 STATUS: Root directory cleaned, main database protected")

if __name__ == "__main__":
    cleanup_restored_files()
