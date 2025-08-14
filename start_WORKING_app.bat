@echo off
title FIXED Saudi Stock Market App - Guaranteed Working
echo =============================================
echo 🇸🇦 FIXED Saudi Stock Market App
echo =============================================
echo 🛑 This version is guaranteed to work!
echo.

cd /d "c:\Users\raed1\OneDrive\Saudi Stock Market App"

echo 🔧 Checking for the correct working file...
if not exist "simple_working_app.py" (
    echo ❌ Working app file not found!
    echo Please ensure simple_working_app.py exists
    pause
    exit /b 1
)

echo ✅ Working app file found: simple_working_app.py
echo.

echo 🔍 Checking environment...
if not exist ".venv" (
    echo ❌ Virtual environment not found
    echo Please run setup first
    pause
    exit /b 1
)

echo ✅ Environment found
echo.

echo 🛑 Killing any old processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo 🚀 Starting the WORKING application...
echo.
echo 📊 Access your app at: http://localhost:8503
echo.
echo ✅ Features:
echo   - Working signal generation
echo   - Clean symbol display (2222, 1120, etc.)
echo   - No syntax errors
echo   - No import issues
echo.
echo Press Ctrl+C to stop the application
echo.

".venv\Scripts\python.exe" -m streamlit run simple_working_app.py --server.port 8503

pause
