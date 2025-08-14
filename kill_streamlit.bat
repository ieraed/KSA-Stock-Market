@echo off
title Kill All Streamlit Processes
echo ============================================
echo 🛑 Stopping All Streamlit Processes
echo ============================================
echo.

echo 🔍 Finding streamlit processes...
tasklist /FI "IMAGENAME eq python.exe" /FO TABLE | find "python.exe"

echo.
echo 🛑 Killing all python processes (including streamlit)...
taskkill /F /IM python.exe >nul 2>&1

echo.
echo ✅ All streamlit processes stopped
echo ✅ You can now start the clean app
echo.
pause
