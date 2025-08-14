# Files Analysis and Cleanup Plan

## ✅ ESSENTIAL FILES (Keep These):
- simple_working_app.py               # Our main working app
- web_launcher_fixed.py               # Clean backup version  
- start_enhanced_app.bat              # Main launcher
- kill_streamlit.bat                  # Process killer
- requirements.txt                    # Dependencies
- setup.py                           # Setup script
- README.md                          # Documentation
- .venv/                             # Virtual environment
- .vscode/                           # VS Code config
- src/                               # Source modules
- saudi_stocks.db                    # Database
- portfolio_template.xlsx            # Template file

## ⚠️ CORRUPTED/PROBLEMATIC FILES (Move to backup):
- web_launcher_new.py                # Has syntax errors causing crashes
- web_launcher.py                    # Original problematic version
- run_dashboard.py                   # Has import issues

## 📂 OLD LAUNCHER FILES (Move to backup):
- ai_launcher.py                     # Old AI version
- launcher.py                        # Original launcher
- professional_launcher.py           # Professional version
- simple_launcher.py                 # Simple version
- portfolio_demo.py                  # Demo version
- professional_portfolio.py          # Professional portfolio

## 🧪 TEST FILES (Move to backup):
- test_app.py                        # Test files
- test_app_integration.py
- test_portfolio.py
- test_portfolio_pricing.py
- test_portfolio_simple.py
- test_signal_fixes.py
- test_tadawul_comparison.py

## 🔧 UTILITY/FIX FILES (Move to backup):
- fix_encoding.py                    # Encoding fixes
- fix_encoding_app.py
- fix_navigation.py
- create_corrected_portfolio.py      # Portfolio fixes
- create_portfolio_template.py
- generate_corrected_portfolio.py
- check_portfolio_costs.py
- showcase_integration.py
- portfolio_access.py

## 📊 OLD DATA FILES (Keep but could backup):
- portfolio_corrected_costs.xlsx     # Data file
- tadawul_comparison_20250808_164023.csv
- signals.log                        # Log file

## 📄 DOCUMENTATION (Keep):
- AI_TRADING_ENHANCEMENT.md
- ARCHITECTURE_PLAN.md
- CLEANUP_ANALYSIS.md
- DEPLOYMENT_GUIDE.md
- ENHANCED_DEPLOYMENT_GUIDE.md
- SIGNAL_FIXES_SUMMARY.md

## 🔗 API/SERVER FILES (Keep for features):
- api_server.py                      # API server
- saudi_exchange_fetcher.py          # Data fetcher
- run_signals.py                     # Signal runner

## 🎛️ BATCH FILES (Keep main ones):
- start_enhanced_app.bat             # MAIN LAUNCHER
- start_clean_app.bat                # Clean version
- start_professional_app.bat         # Professional version
- start_web_launcher.bat             # Web launcher

## 📦 REQUIREMENTS (Keep):
- requirements.txt                   # Main requirements
- requirements_ai.txt                # AI requirements  
- requirements_professional.txt      # Professional requirements

## CLEANUP ACTION PLAN:
1. Stop all streamlit processes
2. Move problematic files to backup_old_files/
3. Update launchers to use simple_working_app.py
4. Test the clean environment
