#!/usr/bin/env python3
import os
import shutil
import json
from datetime import datetime
import zipfile

def create_restore_point():
    """Create a complete restore point of the current working state"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = f"restore_point_{timestamp}"
    
    print("🛡️ CREATING RESTORE POINT")
    print("=" * 50)
    
    try:
        # Create backup directory
        os.makedirs(backup_folder, exist_ok=True)
        print(f"📁 Created backup folder: {backup_folder}")
        
        # Essential files to backup
        essential_files = [
            "enhanced_saudi_app_v2.py",  # Main application
            "user_portfolio.json",       # User portfolio data
            "saudi_stocks_database.json", # Main stock database
            "requirements.txt",          # Dependencies
            "README.md",                 # Documentation
            "APP_DESCRIPTION.md"         # App description
        ]
        
        # Backup essential files
        for file in essential_files:
            if os.path.exists(file):
                shutil.copy2(file, backup_folder)
                print(f"✅ Backed up: {file}")
        
        # Backup additional important files if they exist
        additional_files = [
            "saudi_stocks_database_corrected.json",
            "saudi_stocks_database_official.json",
            "count_stocks.py",
            "upgrade_portfolio.py"
        ]
        
        for file in additional_files:
            if os.path.exists(file):
                shutil.copy2(file, backup_folder)
                print(f"✅ Backed up: {file}")
        
        # Create a compressed archive
        archive_name = f"{backup_folder}.zip"
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_folder)
                    zipf.write(file_path, arcname)
        
        print(f"📦 Created compressed backup: {archive_name}")
        
        # Create restore instructions
        restore_instructions = f"""
# RESTORE POINT INSTRUCTIONS
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## To Restore:
1. Extract {archive_name}
2. Copy files back to main directory
3. Run: python -m streamlit run enhanced_saudi_app_v2.py --server.port 8504

## Files Included:
{chr(10).join([f"- {file}" for file in essential_files + additional_files if os.path.exists(file)])}

## Current State:
- Portfolio entries: {get_portfolio_count()}
- Database stocks: {get_database_count()}
- App version: Enhanced Saudi App v2 with broker tracking
"""
        
        with open(f"{backup_folder}/RESTORE_INSTRUCTIONS.txt", 'w') as f:
            f.write(restore_instructions)
        
        print(f"📋 Created restore instructions")
        print(f"✅ Restore point created successfully!")
        return backup_folder
        
    except Exception as e:
        print(f"❌ Error creating restore point: {e}")
        return None

def get_portfolio_count():
    """Get number of portfolio entries"""
    try:
        with open('user_portfolio.json', 'r') as f:
            portfolio = json.load(f)
        return len(portfolio)
    except:
        return 0

def get_database_count():
    """Get number of stocks in database"""
    try:
        with open('saudi_stocks_database.json', 'r') as f:
            database = json.load(f)
        return len(database)
    except:
        return 0

def identify_cleanup_candidates():
    """Identify files that can be safely removed"""
    
    print("\n🧹 IDENTIFYING CLEANUP CANDIDATES")
    print("=" * 50)
    
    # Test/temporary files
    test_files = [
        "test_app.py",
        "test_continuous_fetcher.py", 
        "simple_data_test.py",
        "quick_stock_test.py",
        "verify_fixes.py",
        "verify_database.py",
        "validate_stock_data.py",
        "fix_database.py",
        "count_stocks.py",
        "new_features_summary.py"
    ]
    
    # Duplicate/old versions
    old_versions = [
        "enhanced_saudi_app.py",
        "enhanced_saudi_app_realtime.py", 
        "enhanced_portfolio_unified.py",
        "professional_portfolio.py",
        "web_launcher_professional.py",
        "ai_launcher.py",
        "web_launcher_new.py",
        "advanced_ai_trading_hub.py",
        "realtime_ai_dashboard.py",
        "ai_portfolio_manager.py",
        "professional_ai_platform.py",
        "platform_launcher.py"
    ]
    
    # Utility scripts (keep but archive)
    utility_scripts = [
        "saudi_exchange_fetcher.py",
        "saudi_data_integration.py", 
        "unified_stock_manager.py",
        "complete_saudi_fetcher.py",
        "update_database.py",
        "upgrade_portfolio.py"
    ]
    
    cleanup_report = {
        "safe_to_delete": [],
        "archive_candidates": [],
        "keep_essential": []
    }
    
    # Check which files exist
    for file in test_files:
        if os.path.exists(file):
            cleanup_report["safe_to_delete"].append(file)
    
    for file in old_versions:
        if os.path.exists(file):
            cleanup_report["safe_to_delete"].append(file)
    
    for file in utility_scripts:
        if os.path.exists(file):
            cleanup_report["archive_candidates"].append(file)
    
    # Essential files to keep
    essential = [
        "enhanced_saudi_app_v2.py",
        "user_portfolio.json", 
        "saudi_stocks_database.json",
        "run_dashboard.py",
        "run_signals.py",
        "requirements.txt",
        "README.md",
        "APP_DESCRIPTION.md"
    ]
    
    for file in essential:
        if os.path.exists(file):
            cleanup_report["keep_essential"].append(file)
    
    return cleanup_report

def perform_cleanup(cleanup_report, backup_folder):
    """Perform the actual cleanup"""
    
    print("\n🗂️ PERFORMING CLEANUP")
    print("=" * 50)
    
    # Create archive folder for utility scripts
    archive_folder = "archived_utilities"
    os.makedirs(archive_folder, exist_ok=True)
    
    # Archive utility scripts
    for file in cleanup_report["archive_candidates"]:
        if os.path.exists(file):
            shutil.move(file, os.path.join(archive_folder, file))
            print(f"📦 Archived: {file}")
    
    # Create cleanup folder for safe deletion
    cleanup_folder = "cleaned_files"
    os.makedirs(cleanup_folder, exist_ok=True)
    
    # Move files to cleanup folder (safer than deleting)
    for file in cleanup_report["safe_to_delete"]:
        if os.path.exists(file):
            shutil.move(file, os.path.join(cleanup_folder, file))
            print(f"🗑️ Moved to cleanup: {file}")
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print(f"✅ Files kept: {len(cleanup_report['keep_essential'])}")
    print(f"📦 Files archived: {len(cleanup_report['archive_candidates'])}")
    print(f"🗑️ Files moved to cleanup: {len(cleanup_report['safe_to_delete'])}")
    
    return True

def main():
    """Main cleanup and backup process"""
    
    print("🛡️ SAUDI STOCK APP - CLEANUP & RESTORE POINT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Create restore point
    backup_folder = create_restore_point()
    if not backup_folder:
        print("❌ Failed to create restore point. Aborting cleanup.")
        return False
    
    # Step 2: Identify cleanup candidates
    cleanup_report = identify_cleanup_candidates()
    
    # Step 3: Show cleanup plan
    print(f"\n📋 CLEANUP PLAN:")
    print(f"Safe to delete: {len(cleanup_report['safe_to_delete'])} files")
    print(f"Archive: {len(cleanup_report['archive_candidates'])} files") 
    print(f"Keep essential: {len(cleanup_report['keep_essential'])} files")
    
    # Step 4: Perform cleanup
    if perform_cleanup(cleanup_report, backup_folder):
        print("\n✅ CLEANUP COMPLETED SUCCESSFULLY!")
        print(f"🛡️ Restore point: {backup_folder}.zip")
        print(f"📁 Archived utilities: archived_utilities/")
        print(f"🗑️ Cleaned files: cleaned_files/")
        print("\n🚀 Your app is now clean and organized!")
        print("📱 Run: python -m streamlit run enhanced_saudi_app_v2.py --server.port 8504")
    
    return True

if __name__ == "__main__":
    main()
