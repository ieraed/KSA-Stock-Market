"""
Live Saudi Market Data Provider  
NO HARDCODED DATA - Uses real-time data from Saudi Exchange fetcher
"""

import json
import time
from datetime import datetime

def get_instant_market_data():
    """Get LIVE market data from Saudi Exchange fetcher - NO HARDCODED DATA"""
    try:
        # Import saudi_exchange_fetcher to get LIVE data
        from saudi_exchange_fetcher import get_all_saudi_stocks_with_prices
        
        print("🔴 NO HARDCODED DATA: Fetching LIVE market data from Saudi Exchange...")
        start_time = time.time()
        
        # Get live data for all stocks
        all_stocks = get_all_saudi_stocks_with_prices()
        
        if not all_stocks:
            print("❌ NO LIVE DATA AVAILABLE")
            return {'success': False, 'error': 'No live data available'}
        
        # Sort by change percentage for gainers and losers
        gainers = []
        losers = []
        
        for stock in all_stocks:
            if stock.get('success') and stock.get('change_pct') is not None:
                stock_data = {
                    'symbol': stock['symbol'],
                    'name': stock.get('name', stock['symbol']),
                    'current_price': stock['current_price'],
                    'change': stock.get('change', 0),
                    'change_pct': stock['change_pct'], 
                    'volume': stock.get('volume', 0),
                    'sector': stock.get('sector', 'Unknown')
                }
                
                if stock['change_pct'] > 0:
                    gainers.append(stock_data)
                elif stock['change_pct'] < 0:
                    losers.append(stock_data)
        
        # Sort gainers by change percentage (descending)
        gainers.sort(key=lambda x: x['change_pct'], reverse=True)
        # Sort losers by change percentage (ascending - most negative first)
        losers.sort(key=lambda x: x['change_pct'])
        
        # Sort by volume for movers
        volume_movers = [stock for stock in all_stocks if stock.get('success') and stock.get('volume')]
        volume_movers.sort(key=lambda x: x.get('volume', 0), reverse=True)
        
        movers_by_volume = []
        for stock in volume_movers[:10]:
            movers_by_volume.append({
                'symbol': stock['symbol'],
                'name': stock.get('name', stock['symbol']),
                'current_price': stock['current_price'],
                'change': stock.get('change', 0),
                'change_pct': stock.get('change_pct', 0),
                'volume': stock.get('volume', 0),
                'sector': stock.get('sector', 'Unknown')
            })
        
        # Calculate market value movers
        value_movers = []
        for stock in all_stocks:
            if stock.get('success') and stock.get('volume') and stock.get('current_price'):
                market_value = stock['volume'] * stock['current_price']
                value_movers.append({
                    'symbol': stock['symbol'],
                    'name': stock.get('name', stock['symbol']),
                    'current_price': stock['current_price'],
                    'change': stock.get('change', 0),
                    'change_pct': stock.get('change_pct', 0),
                    'volume': stock.get('volume', 0),
                    'market_value': market_value,
                    'sector': stock.get('sector', 'Unknown')
                })
        
        value_movers.sort(key=lambda x: x['market_value'], reverse=True)
        
        end_time = time.time()
        loading_time = end_time - start_time
        
        result = {
            'success': True,
            'top_gainers': gainers[:10],
            'top_losers': losers[:10], 
            'movers_by_volume': movers_by_volume[:10],
            'movers_by_value': value_movers[:10],
            'market_summary': {
                'total_stocks_processed': len(all_stocks),
                'gainers_count': len(gainers),
                'losers_count': len(losers),
                'active_stocks': len([s for s in all_stocks if s.get('volume', 0) > 0])
            },
            'loading_time': round(loading_time, 2),
            'total_stocks_fetched': len(all_stocks),
            'data_source': 'LIVE Saudi Exchange (Real-time)',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"✅ LIVE DATA SUCCESS: {len(gainers)} gainers, {len(losers)} losers, {loading_time:.2f}s")
        return result
        
    except Exception as e:
        print(f"❌ LIVE DATA ERROR: {str(e)}")
        return {
            'success': False, 
            'error': f'Failed to fetch live data: {str(e)}',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
