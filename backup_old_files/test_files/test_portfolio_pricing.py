#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pandas as pd
import yfinance as yf

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

def test_portfolio_pricing():
    """Test portfolio pricing functionality"""
    try:
        from src.utils.portfolio_manager import PortfolioManager
        from src.data.market_data import MarketDataFetcher
        from src.utils.config import Config
        
        print("✅ Successfully imported portfolio modules")
        
        # Initialize
        config = Config()
        data_fetcher = MarketDataFetcher(config)
        pm = PortfolioManager(data_fetcher, config)
        
        print("✅ Successfully created portfolio manager")
        
        # Get portfolio
        portfolio_df = pm.create_sample_portfolio()
        print(f"✅ Portfolio loaded: {len(portfolio_df)} positions")
        
        # Test price fetching for a few stocks
        test_symbols = ['2222', '1120', '2010']  # Aramco, Al Rajhi, SABIC
        
        print("\n📊 Testing direct yfinance price fetching:")
        for symbol in test_symbols:
            try:
                ticker = yf.Ticker(f"{symbol}.SR")
                hist = ticker.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                    print(f"  {symbol}: {price:.2f} SAR ✅")
                else:
                    print(f"  {symbol}: No data ❌")
            except Exception as e:
                print(f"  {symbol}: Error - {str(e)} ❌")
        
        # Test portfolio manager pricing
        print("\n💼 Testing portfolio manager pricing:")
        try:
            test_df = portfolio_df.head(5)  # Test first 5 stocks
            prices = pm.get_current_prices(test_df)
            
            for symbol, price in prices.items():
                status = "✅" if price > 0 else "❌"
                print(f"  {symbol}: {price:.2f} SAR {status}")
                
        except Exception as e:
            print(f"Portfolio manager pricing failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_portfolio_pricing()
