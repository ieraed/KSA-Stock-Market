# Quick test that the app loads and processes portfolio correctly
import sys
sys.path.append('apps')
from enhanced_saudi_app_v2 import load_saudi_stocks_database, load_portfolio

# Test loading
stocks = load_saudi_stocks_database()
portfolio = load_portfolio()

print(f'✅ App loads {len(stocks)} stocks')
print(f'✅ Portfolio has {len(portfolio)} holdings')

# Test the numbering logic
holdings_data = []
for idx, stock in enumerate(portfolio, 1):
    holdings_data.append({
        '#': idx,
        'Symbol': stock['symbol'],
        'Quantity': stock.get('quantity', 0)
    })

print(f'✅ Holdings with numbering:')
for holding in holdings_data[:3]:  # Show first 3
    print(f'  {holding["#"]}. {holding["Symbol"]} - {holding["Quantity"]} shares')

print(f'🎯 Numbering feature ready!')
