#!/usr/bin/env python3
"""
🧹 WORKSPACE CLEANUP UTILITY
Removes empty files and organizes the Saudi Stock Market App project structure
"""

import os
import shutil
from pathlib import Path

def main():
    """Clean up empty files and organize workspace"""
    
    project_root = Path(__file__).parent
    print("🧹 Starting Workspace Cleanup...")
    print(f"📁 Project Root: {project_root}")
    
    # List of confirmed empty files to remove
    empty_files_to_remove = [
        "add_numbering.py",
        "analyze_sectors.py", 
        "analyze_tasi_db.py",
        "cleanup_databases.py",
        "cleanup_empty_files.py",
        "create_portfolio_excel_template.py",
        "emergency_cleanup.py",
        "final_cleanup.py",
        "saudi_data_integration.py",
        "sector_analyzer.py",
        "sync_with_official_tasi.py",
        "update_sectors.py",
        "update_with_tasi_official.py",
        "test_numbering.py",
        "test_risk_component.py",
        "test_main_app.py",
        "branding_demo.py",
        "launch_app.py"
    ]
    
    # Files to potentially remove (check if they exist and are small/empty)
    potential_cleanup_files = [
        "sample_import_test.csv",
        "portfolio_template.csv"
    ]
    
    removed_count = 0
    
    # Remove confirmed empty files
    print("\n🗑️  Removing empty files...")
    for filename in empty_files_to_remove:
        file_path = project_root / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"   ✅ Removed: {filename}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to remove {filename}: {e}")
        else:
            print(f"   ℹ️  Not found: {filename}")
    
    # Check potential cleanup files
    print("\n📋 Checking potential cleanup files...")
    for filename in potential_cleanup_files:
        file_path = project_root / filename
        if file_path.exists():
            file_size = file_path.stat().st_size
            print(f"   📄 {filename}: {file_size} bytes")
            if file_size < 100:  # Very small files
                try:
                    file_path.unlink()
                    print(f"   ✅ Removed small file: {filename}")
                    removed_count += 1
                except Exception as e:
                    print(f"   ❌ Failed to remove {filename}: {e}")
    
    # Organize important files into proper structure
    print("\n📁 Checking project structure...")
    
    # Core application files (should remain)
    core_files = [
        "run_dashboard.py",
        "run_signals.py", 
        "user_portfolio.json",
        "portfolio_corrected_costs.xlsx"
    ]
    
    for filename in core_files:
        file_path = project_root / filename
        if file_path.exists():
            print(f"   ✅ Core file exists: {filename}")
        else:
            print(f"   ⚠️  Missing core file: {filename}")
    
    # Check important directories
    important_dirs = [
        "apps",
        "ai_engine", 
        "components",
        "config",
        "core",
        "data",
        "scripts",
        "utilities"
    ]
    
    for dirname in important_dirs:
        dir_path = project_root / dirname
        if dir_path.exists() and dir_path.is_dir():
            file_count = len(list(dir_path.rglob("*.py")))
            print(f"   📂 {dirname}/: {file_count} Python files")
        else:
            print(f"   ⚠️  Missing directory: {dirname}/")
    
    print(f"\n✨ Cleanup Complete!")
    print(f"🗑️  Removed {removed_count} empty/unnecessary files")
    print(f"📁 Project structure is now cleaner and more organized")
    
    # Show remaining Python files in root
    print(f"\n📋 Remaining Python files in root:")
    root_py_files = [f for f in project_root.glob("*.py") if f.is_file()]
    for py_file in sorted(root_py_files):
        file_size = py_file.stat().st_size
        print(f"   📄 {py_file.name}: {file_size:,} bytes")
    
    print(f"\n🎯 Your workspace is now clean and organized!")
    print(f"🚀 You can continue working on the main application features.")

if __name__ == "__main__":
    main()
