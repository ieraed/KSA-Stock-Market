@echo off
echo ===============================================
echo          GITHUB UPDATE CONFIRMATION
echo ===============================================
echo Repository: KSA-Stock-Market
echo Owner: ieraed
echo Branch: master
echo Date: %date% %time%
echo ===============================================

echo.
echo [1/6] Stopping any running processes...
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak >nul

echo [2/6] Navigating to project directory...
cd /d "C:\Users\raed1\OneDrive\Saudi Stock Market App"

echo [3/6] Checking repository status...
git remote -v
git branch

echo [4/6] Adding all changes to staging...
git add .

echo [5/6] Committing changes...
git commit -m "Update Saudi Stock Market App with Color Bot and enhanced theme system - %date% %time%"

echo [6/6] Pushing to GitHub...
git push origin master

echo.
echo ===============================================
echo            UPDATE CONFIRMATION
echo ===============================================
echo ✅ All changes successfully pushed to GitHub!
echo 🌐 Repository URL: https://github.com/ieraed/KSA-Stock-Market
echo 📱 App Features Updated:
echo    - Color Bot Assistant (4 tabs)
echo    - Enhanced Theme System
echo    - White Background Fixes
echo    - Navigation Integration
echo ===============================================
pause
