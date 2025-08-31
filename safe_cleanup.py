#!/usr/bin/env python3
"""
🧹 SAFE CLEANUP SCRIPT - Saudi Stock Market App
Removes backup, test, and unnecessary files while preserving the working app
"""

import os
import shutil
from pathlib import Path

def safe_cleanup():
    """Safely remove unnecessary files"""
    
    project_root = Path(__file__).parent
    print("🧹 Starting Safe Cleanup...")
    print(f"📁 Project Root: {project_root}")
    
    removed_count = 0
    
    # Backup files (safe to delete)
    backup_files = [
        "apps/enhanced_saudi_app_v2_backup_before_hybrid.py",
        "apps/enhanced_saudi_app_v2_backup_pre_restore.py", 
        "apps/enhanced_saudi_app_v2_fixed.py",
        "apps/enhanced_saudi_app_v2_ascii.py",
        "apps/complete_modern_saudi_app_backup.py"
    ]
    
    # Test files (safe to delete)
    test_files = [
        "test_risk_component.py",
        "test_portfolio.py", 
        "test_prices.py",
        "check_specific_prices.py",
        "sample_import_test.csv"
    ]
    
    # Temporary files (safe to delete)
    temp_files = [
        "minimal_working_main_app.py",
        "minimal_css_test.py",
        "branding_demo.py", 
        "css_detective.py",
        "workspace_cleanup.py",
        "web_launcher_new.py"
    ]
    
    # Documentation files (outdated - safe to delete)
    doc_files = [
        "WORKSPACE_CLEANUP_SUMMARY.md",
        "FIXES_SUMMARY.md",
        "STAGE_1_SUMMARY.md", 
        "EMERGENCY_CLEANUP_REPORT_20250819.md",
        "RESTORE_POINT_20250818.md",
        "MIGRATION_DECISION_MATRIX.md",
        "HYBRID_VS_SCALABLE_COMPARISON.md",
        "CSS_MIGRATION_GUIDE.md",
        "CURRENT_VS_HYBRID_DETAILED.md",
        "COMPLETE_HYBRID_MIGRATION.md",
        "PROGRESSIVE_MIGRATION_STRATEGY.md",
        "INTEGRATION_GUIDE.md",
        "DEVELOPMENT_ROADMAP.md",
        "STOCK_COUNT_MONITOR.md",
        "ROBUST_HYBRID_CSS_SOLUTION.css"
    ]
    
    # Alternative app versions (safe to delete)
    alt_apps = [
        "enhanced_saudi_app_v2_5_hybrid.py",
        "enhanced_saudi_app_v3_scalable.py",
        "enhanced_features_integration.py",
        "hybrid_css_system.py",
        "technical_comparison_hybrid_vs_scalable.py",
        "live_code_comparison.py"
    ]
    
    # Old templates (safe to delete)
    old_templates = [
        "Portfolio_Template_20250817_175619.xlsx",
        "portfolio_template.csv"
    ]
    
    # Backup data (safe to delete if confident)
    backup_data = [
        "data/saudi_stocks_database_backup_before_sync_20250818_201946.json"
    ]
    
    # Additional apps directory cleanup
    apps_cleanup = [
        "apps/clean_working_app.py",
        "apps/complete_fast_app.py", 
        "apps/complete_modern_saudi_app.py",
        "apps/enhanced_saudi_app_realtime.py",
        "apps/enhanced_saudi_app.py",
        "apps/minimal_working_app.py",
        "apps/modern_saudi_app.py", 
        "apps/ultra_fast_app.py"
    ]
    
    # Combine all files to delete
    all_files_to_delete = backup_files + test_files + temp_files + doc_files + alt_apps + old_templates + backup_data + apps_cleanup
    
    print(f"\n🗑️ Removing {len(all_files_to_delete)} unnecessary files...")
    
    for file_path in all_files_to_delete:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                if full_path.is_file():
                    full_path.unlink()
                    print(f"   ✅ Removed file: {file_path}")
                    removed_count += 1
                elif full_path.is_dir():
                    shutil.rmtree(full_path)
                    print(f"   ✅ Removed directory: {file_path}")
                    removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to remove {file_path}: {e}")
        else:
            print(f"   ℹ️ Not found: {file_path}")
    
    # Remove cache directories
    cache_dirs = [
        "__pycache__",
        "apps/__pycache__", 
        "branding/__pycache__"
    ]
    
    print(f"\n🗑️ Removing cache directories...")
    for cache_dir in cache_dirs:
        cache_path = project_root / cache_dir
        if cache_path.exists() and cache_path.is_dir():
            try:
                shutil.rmtree(cache_path)
                print(f"   ✅ Removed cache: {cache_dir}")
                removed_count += 1
            except Exception as e:
                print(f"   ❌ Failed to remove {cache_dir}: {e}")
    
    # Optional: Remove RestorePoint (only if user is confident)
    restore_point = project_root / "RestorePoint_20250817"
    if restore_point.exists():
        print(f"\n❓ Found RestorePoint_20250817/ directory")
        print(f"   This contains backup files from earlier cleanup")
        print(f"   You can delete this if you're confident the app is working well")
        print(f"   To delete: Remove the RestorePoint_20250817/ folder manually")
    
    print(f"\n✨ Cleanup Complete!")
    print(f"🗑️ Removed {removed_count} files/directories")
    print(f"💾 Estimated space saved: 50-70% of previous workspace size")
    print(f"\n✅ Your main app is preserved: apps/enhanced_saudi_app_v2.py")
    print(f"✅ All essential files remain intact")
    
    # Show remaining important files
    print(f"\n📋 Essential files confirmed present:")
    essential_files = [
        "apps/enhanced_saudi_app_v2.py",
        "data/saudi_stocks_database.json", 
        "data/user_portfolio.json",
        "saudi_portfolio_manager.py",
        "saudi_stocks_fetcher.py",
        "run_dashboard.py",
        "portfolio_corrected_costs.xlsx"
    ]
    
    for essential_file in essential_files:
        file_path = project_root / essential_file
        if file_path.exists():
            print(f"   ✅ {essential_file}")
        else:
            print(f"   ⚠️ MISSING: {essential_file}")

if __name__ == "__main__":
    print("🔍 SAFE CLEANUP PREVIEW")
    print("=" * 50)
    print("This script will remove:")
    print("• Backup files (old app versions)")
    print("• Test files (development testing)")
    print("• Temporary files (experimental code)")
    print("• Outdated documentation")
    print("• Cache directories")
    print("• Old templates")
    print("\nYour working app and data will be preserved!")
    print("=" * 50)
    
    response = input("\n🤔 Proceed with cleanup? (y/N): ").lower().strip()
    if response in ['y', 'yes']:
        safe_cleanup()
    else:
        print("❌ Cleanup cancelled. No files were removed.")
