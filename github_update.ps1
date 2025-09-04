# GitHub Update Script
Write-Host "=== GITHUB UPDATE SCRIPT ===" -ForegroundColor Green
Write-Host "Stopping all Python processes..." -ForegroundColor Yellow
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
Start-Sleep 3

Write-Host "Navigating to project directory..." -ForegroundColor Yellow
Set-Location "C:\Users\raed1\OneDrive\Saudi Stock Market App"

Write-Host "Adding all changes to staging..." -ForegroundColor Yellow
git add .

Write-Host "Checking git status..." -ForegroundColor Yellow
git status

Write-Host "Committing changes..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
git commit -m "Update Saudi Stock Market App with Color Bot and theme enhancements - $timestamp"

Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git push origin master

Write-Host "=== GITHUB UPDATE COMPLETE ===" -ForegroundColor Green
