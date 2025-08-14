#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.utils.portfolio_manager import PortfolioManager

def test_portfolio():
    pm = PortfolioManager()
    df = pm.create_sample_portfolio()
    
    print(f"Total positions: {len(df)}")
    print(f"Number of brokers: {df['Custodian'].nunique()}")
    print(f"Expected positions: 39")
    
    # Check broker breakdown
    print("\nPositions by broker:")
    broker_counts = df['Custodian'].value_counts()
    for broker, count in broker_counts.items():
        print(f"- {broker}: {count} positions")
    
    # Check if we have the corrected symbols and company names
    print("\nSample positions (first 10):")
    print(df[['Symbol', 'Company_Name', 'Custodian', 'Quantity', 'Avg_Cost']].head(10).to_string())
    
    # Check for specific corrections
    print("\nChecking specific corrections:")
    batic_stocks = df[df['Symbol'] == '1150']
    if not batic_stocks.empty:
        print(f"✅ Symbol 1150 found with company name: {batic_stocks.iloc[0]['Company_Name']}")
    
    jazeera_stocks = df[df['Symbol'] == '4200']
    if not jazeera_stocks.empty:
        print(f"✅ Symbol 4200 found with company name: {jazeera_stocks.iloc[0]['Company_Name']}")
    
    albilad_stocks = df[df['Symbol'] == '9408']
    if not albilad_stocks.empty:
        print(f"✅ Symbol 9408 found with company name: {albilad_stocks.iloc[0]['Company_Name']}")

if __name__ == "__main__":
    test_portfolio()
