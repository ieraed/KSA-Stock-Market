# 🧹 MANUAL CLEANUP GUIDE

## 📋 Files Safe to Archive/Move

### 🧪 Test and Validation Files (Move to `archived_utilities/`)
- `check_anb.py`
- `count_database.py`
- `count_stocks.py`
- `test_continuous_fetcher.py`
- `validate_stock_data.py`
- `verify_database.py`
- `verify_fixes.py`
- `simple_data_test.py`

### 🔧 Utility Scripts (Move to `archived_utilities/`)
- `saudi_exchange_fetcher.py`
- `complete_saudi_fetcher.py`
- `saudi_data_integration.py`
- `unified_stock_manager.py`
- `continuous_data_fetcher.py`
- `update_database.py`
- `upgrade_portfolio.py`

### 📦 Setup and Launch Scripts (Move to `archived_utilities/`)
- `complete_setup.py`
- `quick_start.py`
- `launch_enhanced_app.py`

### 📊 Old App Versions (Move to `archived_utilities/`)
- `enhanced_saudi_app.py` (old version)
- `enhanced_saudi_app_realtime.py` (old version)
- `enhanced_portfolio_unified.py` (old version)

### 🗂️ Database Creation Scripts (Move to `archived_utilities/`)
- `create_complete_database.py`
- `fix_database.py`

## ✅ Essential Files to Keep in Main Directory
- `enhanced_saudi_app_v2.py` ⭐ (MAIN APP)
- `saudi_stocks_database.json` ⭐ (CORRECTED DATABASE)
- `user_portfolio.json` ⭐ (USER PORTFOLIO)
- `requirements_enhanced.txt` ⭐ (DEPENDENCIES)
- `README.md`
- `APP_DESCRIPTION.md`
- `portfolio_*.xlsx` files
- `.env.example`
- Config folders: `.vscode/`, `config/`, `.github/`

## 🎯 Current Status
✅ Main application: `enhanced_saudi_app_v2.py` - Fully functional
✅ Database: Corrected (9408=ALBILAD SAUDI GROWTH, 5110=Al Ahli REIT 1, 6010=NADEC)
✅ Features: Broker tracking, portfolio editing, decimal formatting
✅ Backup: Created restore point with instructions

## 🚀 Quick Commands to Start Clean App
```bash
# Run the main application
python -m streamlit run enhanced_saudi_app_v2.py --server.port 8504

# If you need to install dependencies
pip install -r requirements_enhanced.txt
```

## 📁 Manual Cleanup Steps
1. Create `archived_utilities/` folder (already created)
2. Move files listed above to `archived_utilities/`
3. Keep only essential files in main directory
4. Test application still works: `python -m streamlit run enhanced_saudi_app_v2.py --server.port 8504`

## 🛡️ Safety
- Restore point created in `RestorePoint_20250817/`
- All essential files documented
- Can restore if anything goes wrong
