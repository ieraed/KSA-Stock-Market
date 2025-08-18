# Test that our main app loads the complete database correctly
import sys
sys.path.append('apps')
from enhanced_saudi_app_v2 import load_saudi_stocks_database

stocks = load_saudi_stocks_database()
print(f'🎯 Main app loads {len(stocks)} stocks')

# Verify critical stocks are present
critical_stocks = ['1010', '1140', '1150', '2030', '2222', '3040', '4001']
all_present = True
for stock in critical_stocks:
    if stock in stocks:
        print(f'  ✅ {stock}: {stocks[stock]["name_en"]}')
    else:
        print(f'  ❌ {stock}: Missing!')
        all_present = False

if all_present and len(stocks) == 259:
    print(f'\n🏆 SUCCESS: Main app has complete 259-stock database!')
else:
    print(f'\n⚠️ WARNING: Database incomplete!')
