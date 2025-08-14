#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd

# Direct import of the portfolio manager without going through __init__
from src.utils.portfolio_manager import PortfolioManager

def test_portfolio():
    try:
        # Create required dependencies
        from src.data.market_data import MarketDataFetcher
        from src.utils.config import Config
        
        config = Config()
        data_fetcher = MarketDataFetcher(config)
        pm = PortfolioManager(data_fetcher, config)
        df = pm.create_sample_portfolio()
        
        print(f"✅ Total positions: {len(df)}")
        print(f"✅ Number of brokers: {df['Custodian'].nunique()}")
        print(f"Expected positions: 39")
        
        if len(df) == 39:
            print("🎉 Portfolio has exactly 39 positions as required!")
        else:
            print(f"⚠️ Portfolio has {len(df)} positions (expected 39)")
        
        # Check columns
        print(f"\nDataFrame columns: {list(df.columns)}")
        
        # Check broker breakdown
        print("\nPositions by broker:")
        broker_counts = df['Custodian'].value_counts()
        for broker, count in broker_counts.items():
            print(f"- {broker}: {count} positions")
        
        # Check for specific corrections
        print("\nChecking specific corrections:")
        
        # Check BATIC (symbol 1150)
        batic_stocks = df[df['Symbol'] == '1150']
        if not batic_stocks.empty:
            company_col = 'Company_Name' if 'Company_Name' in df.columns else 'Company'
            print(f"✅ Symbol 1150 found with company name: {batic_stocks.iloc[0][company_col]}")
        else:
            print("❌ Symbol 1150 (BATIC) not found")
        
        # Check Al Jazeera Bank (symbol 4200) 
        jazeera_stocks = df[df['Symbol'] == '4200']
        if not jazeera_stocks.empty:
            company_col = 'Company_Name' if 'Company_Name' in df.columns else 'Company'
            print(f"✅ Symbol 4200 found with company name: {jazeera_stocks.iloc[0][company_col]}")
        else:
            print("❌ Symbol 4200 (Al Jazeera Bank) not found")
        
        # Check ALBILAD (symbol 9408)
        albilad_stocks = df[df['Symbol'] == '9408']
        if not albilad_stocks.empty:
            company_col = 'Company_Name' if 'Company_Name' in df.columns else 'Company'
            print(f"✅ Symbol 9408 found with company name: {albilad_stocks.iloc[0][company_col]}")
        else:
            print("❌ Symbol 9408 (ALBILAD) not found")
        
        # Check symbols don't have .SR suffix
        has_sr_suffix = df['Symbol'].str.contains('.SR').any()
        if not has_sr_suffix:
            print("✅ All symbols are clean (no .SR suffix)")
        else:
            print("❌ Some symbols still have .SR suffix")
        
        print("\nFirst 10 positions:")
        display_cols = ['Symbol', 'Company', 'Custodian', 'Owned_Qty', 'Cost']
        print(df[display_cols].head(10).to_string())
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing portfolio: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_portfolio()
