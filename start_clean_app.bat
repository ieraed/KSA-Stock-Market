@echo off
title Saudi Stock Market App - Clean Version
echo ============================================
echo 🇸🇦 Saudi Stock Market App - Clean Version
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
echo 🧹 This is the CLEAN version with:
echo ✅ No syntax errors
echo ✅ Working signal generation
echo ✅ Clean symbol display (2222, 1120, etc.)
echo ✅ All problematic files moved to backup
echo.
echo Press Ctrl+C to stop the application
echo.

.venv\Scripts\python.exe -m streamlit run simple_working_app.py --server.port 8501

pause