@echo off
title Saudi Stock Market App - Working Version
echo ============================================
echo �🇦 Saudi Stock Market App
echo ============================================
echo Starting the Trading Platform...
echo.

cd /d "c:\Users\raed1\OneDrive\Saudi Stock Market App"

echo 🔍 Checking environment...
if not exist ".venv" (
    echo ❌ Virtual environment not found
    echo Please run setup first
    pause
    exit /b 1
)

echo ✅ Environment found
echo 🚀 Starting application...
echo.
echo 📊 Access your app at: http://localhost:8501
echo.
echo Features Available:
echo ✅ Market Dashboard
echo ✅ Trading Signals (WORKING!)
echo ✅ Stock Analysis
echo ✅ Clean Symbol Display (2222, 1120, etc.)
echo.
echo Press Ctrl+C to stop the application
echo.

.venv\Scripts\python.exe -m streamlit run simple_working_app.py --server.port 8501

pause
