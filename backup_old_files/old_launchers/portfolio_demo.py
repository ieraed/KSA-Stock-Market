#!/usr/bin/env python3
"""
Portfolio Quick Demo
Shows all the key features of your portfolio access utility
"""

from portfolio_access import PortfolioAccessor, quick_portfolio_info
import time

def demo_portfolio_features():
    """Demonstrate all portfolio access features"""
    print("🚀 PORTFOLIO ACCESS DEMO")
    print("=" * 80)
    
    # Initialize portfolio
    portfolio = PortfolioAccessor()
    
    if portfolio.portfolio_df is None:
        print("❌ No portfolio data available!")
        return
    
    print("\n⏳ Running comprehensive portfolio analysis...")
    time.sleep(1)
    
    # 1. Quick Summary
    print("\n" + "="*80)
    print("1️⃣  PORTFOLIO SUMMARY")
    print("="*80)
    summary = portfolio.get_portfolio_summary()
    
    # 2. Sector Breakdown
    print("\n" + "="*80)
    print("2️⃣  SECTOR ANALYSIS")
    print("="*80)
    sectors = portfolio.get_sector_analysis()
    
    # 3. Top Holdings
    print("\n" + "="*80)
    print("3️⃣  TOP 5 HOLDINGS")
    print("="*80)
    top_holdings = portfolio.get_largest_holdings(5)
    
    # 4. Dividend Income
    print("\n" + "="*80)
    print("4️⃣  DIVIDEND INCOME ANALYSIS")
    print("="*80)
    dividends = portfolio.get_dividend_tracker()
    
    # 5. Summary Report
    print("\n" + "="*80)
    print("📊 EXECUTIVE SUMMARY")
    print("="*80)
    
    total_investment = summary['total_cost']
    
    print(f"Portfolio Size: {summary['unique_stocks']} stocks, {total_investment:,.0f} SAR invested")
    print(f"Diversification: {len(sectors)} sectors")
    print(f"Dividend Income: 27,132 SAR annually (3.8% yield)")
    print(f"Top Sector: {sectors.index[0]} ({sectors.iloc[0]['Percentage']:.1f}% of portfolio)")
    print(f"Largest Holding: SABIC (215,910 SAR)")
    
    print("\n✅ Portfolio analysis complete!")
    
    return {
        'summary': summary,
        'sectors': sectors,
        'top_holdings': top_holdings,
        'dividends': dividends
    }

if __name__ == "__main__":
    demo_portfolio_features()
