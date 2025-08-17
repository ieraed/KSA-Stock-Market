@echo off
echo Starting cleanup process...

REM Create subdirectories in archived_utilities
mkdir "archived_utilities\test_files" 2>nul
mkdir "archived_utilities\utility_scripts" 2>nul
mkdir "archived_utilities\old_apps" 2>nul
mkdir "archived_utilities\setup_scripts" 2>nul
mkdir "archived_utilities\database_scripts" 2>nul

echo Moving test and validation files...
move "count_stocks.py" "archived_utilities\test_files\" 2>nul
move "verify_database.py" "archived_utilities\test_files\" 2>nul
move "verify_fixes.py" "archived_utilities\test_files\" 2>nul

echo Moving utility scripts...
move "saudi_exchange_fetcher.py" "archived_utilities\utility_scripts\" 2>nul
move "unified_stock_manager.py" "archived_utilities\utility_scripts\" 2>nul
move "update_database.py" "archived_utilities\utility_scripts\" 2>nul
move "upgrade_portfolio.py" "archived_utilities\utility_scripts\" 2>nul
move "saudi_stock_database.py" "archived_utilities\utility_scripts\" 2>nul

echo Moving old app versions...
move "enhanced_saudi_app.py" "archived_utilities\old_apps\" 2>nul
move "enhanced_saudi_app_realtime.py" "archived_utilities\old_apps\" 2>nul
move "enhanced_portfolio_unified.py" "archived_utilities\old_apps\" 2>nul

echo Moving setup scripts...
move "complete_setup.py" "archived_utilities\setup_scripts\" 2>nul
move "quick_start.py" "archived_utilities\setup_scripts\" 2>nul
move "launch_enhanced_app.py" "archived_utilities\setup_scripts\" 2>nul
move "new_features_summary.py" "archived_utilities\setup_scripts\" 2>nul

echo Moving database scripts...
move "create_complete_database.py" "archived_utilities\database_scripts\" 2>nul
move "fix_database.py" "archived_utilities\database_scripts\" 2>nul

echo Cleanup complete!
echo.
echo Essential files remaining in main directory:
dir enhanced_saudi_app_v2.py 2>nul
dir saudi_stocks_database.json 2>nul
dir user_portfolio.json 2>nul
dir requirements_enhanced.txt 2>nul

echo.
echo Archived files summary:
echo Test files: archived_utilities\test_files\
echo Utility scripts: archived_utilities\utility_scripts\
echo Old apps: archived_utilities\old_apps\
echo Setup scripts: archived_utilities\setup_scripts\
echo Database scripts: archived_utilities\database_scripts\

pause
