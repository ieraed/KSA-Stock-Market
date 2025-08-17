# PowerShell Cleanup Script
Write-Host "🧹 Starting cleanup process..." -ForegroundColor Green

# Create subdirectories
$baseDir = "archived_utilities"
New-Item -ItemType Directory -Path "$baseDir\test_files" -Force | Out-Null
New-Item -ItemType Directory -Path "$baseDir\utility_scripts" -Force | Out-Null
New-Item -ItemType Directory -Path "$baseDir\old_apps" -Force | Out-Null
New-Item -ItemType Directory -Path "$baseDir\setup_scripts" -Force | Out-Null
New-Item -ItemType Directory -Path "$baseDir\database_scripts" -Force | Out-Null

Write-Host "📁 Created archive subdirectories" -ForegroundColor Yellow

# Test and validation files
$testFiles = @("count_stocks.py", "verify_database.py", "verify_fixes.py")
foreach ($file in $testFiles) {
    if (Test-Path $file) {
        Move-Item $file "$baseDir\test_files\" -Force
        Write-Host "✅ Moved $file" -ForegroundColor Green
    }
}

# Utility scripts
$utilityFiles = @("saudi_exchange_fetcher.py", "unified_stock_manager.py", "update_database.py", "upgrade_portfolio.py", "saudi_stock_database.py")
foreach ($file in $utilityFiles) {
    if (Test-Path $file) {
        Move-Item $file "$baseDir\utility_scripts\" -Force
        Write-Host "✅ Moved $file" -ForegroundColor Green
    }
}

# Old app versions
$oldApps = @("enhanced_saudi_app.py", "enhanced_saudi_app_realtime.py", "enhanced_portfolio_unified.py")
foreach ($file in $oldApps) {
    if (Test-Path $file) {
        Move-Item $file "$baseDir\old_apps\" -Force
        Write-Host "✅ Moved $file" -ForegroundColor Green
    }
}

# Setup scripts
$setupFiles = @("complete_setup.py", "quick_start.py", "launch_enhanced_app.py", "new_features_summary.py")
foreach ($file in $setupFiles) {
    if (Test-Path $file) {
        Move-Item $file "$baseDir\setup_scripts\" -Force
        Write-Host "✅ Moved $file" -ForegroundColor Green
    }
}

# Database scripts
$dbFiles = @("create_complete_database.py", "fix_database.py")
foreach ($file in $dbFiles) {
    if (Test-Path $file) {
        Move-Item $file "$baseDir\database_scripts\" -Force
        Write-Host "✅ Moved $file" -ForegroundColor Green
    }
}

Write-Host "`n🎉 Cleanup completed!" -ForegroundColor Green
Write-Host "📊 Essential files remaining:" -ForegroundColor Yellow
if (Test-Path "enhanced_saudi_app_v2.py") { Write-Host "  ✅ enhanced_saudi_app_v2.py" -ForegroundColor Green }
if (Test-Path "saudi_stocks_database.json") { Write-Host "  ✅ saudi_stocks_database.json" -ForegroundColor Green }
if (Test-Path "user_portfolio.json") { Write-Host "  ✅ user_portfolio.json" -ForegroundColor Green }
if (Test-Path "requirements_enhanced.txt") { Write-Host "  ✅ requirements_enhanced.txt" -ForegroundColor Green }

Write-Host "`n📁 Archive structure created:" -ForegroundColor Yellow
Write-Host "  📂 archived_utilities\test_files\" -ForegroundColor Cyan
Write-Host "  📂 archived_utilities\utility_scripts\" -ForegroundColor Cyan
Write-Host "  📂 archived_utilities\old_apps\" -ForegroundColor Cyan
Write-Host "  📂 archived_utilities\setup_scripts\" -ForegroundColor Cyan
Write-Host "  📂 archived_utilities\database_scripts\" -ForegroundColor Cyan
