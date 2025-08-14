#!/usr/bin/env python3
"""
Portfolio Data Access Utility
Provides easy access to retrieve and analyze your portfolio data
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import os
import sys

class PortfolioAccessor:
    """Class to access and analyze portfolio data"""
    
    def __init__(self, portfolio_file="portfolio_corrected_costs.xlsx"):
        """Initialize with portfolio file"""
        self.portfolio_file = portfolio_file
        self.portfolio_df = None
        self.load_portfolio()
    
    def load_portfolio(self):
        """Load portfolio data from Excel file"""
        try:
            if os.path.exists(self.portfolio_file):
                self.portfolio_df = pd.read_excel(self.portfolio_file)
                print(f"✅ Portfolio loaded successfully! Found {len(self.portfolio_df)} holdings.")
                return True
            else:
                print(f"❌ Portfolio file '{self.portfolio_file}' not found!")
                return False
        except Exception as e:
            print(f"❌ Error loading portfolio: {e}")
            return False
    
    def get_portfolio_summary(self):
        """Get portfolio overview summary"""
        if self.portfolio_df is None:
            print("❌ No portfolio data loaded!")
            return None
        
        summary = {
            'total_holdings': len(self.portfolio_df),
            'unique_stocks': len(self.portfolio_df['Symbol'].unique()),
            'total_cost': (self.portfolio_df['Owned_Qty'] * self.portfolio_df['Cost']).sum(),
            'companies': self.portfolio_df['Company'].tolist(),
            'symbols': self.portfolio_df['Symbol'].unique().tolist()
        }
        
        print("📊 PORTFOLIO SUMMARY")
        print("=" * 50)
        print(f"Total Holdings: {summary['total_holdings']}")
        print(f"Unique Stocks: {summary['unique_stocks']}")
        print(f"Total Investment: {summary['total_cost']:,.2f} SAR")
        print(f"Custodians: {', '.join(self.portfolio_df['Custodian'].unique())}")
        
        return summary
    
    def get_all_holdings(self):
        """Get complete holdings data"""
        if self.portfolio_df is None:
            return None
        
        print("📋 ALL PORTFOLIO HOLDINGS")
        print("=" * 80)
        
        # Format for better display
        display_df = self.portfolio_df.copy()
        display_df['Total_Cost'] = display_df['Owned_Qty'] * display_df['Cost']
        display_df['Avg_Cost'] = display_df['Cost']
        
        print(display_df[['Company', 'Symbol', 'Owned_Qty', 'Avg_Cost', 'Total_Cost', 'Custodian']].to_string(index=False))
        
        return display_df
    
    def get_holdings_by_symbol(self, symbol):
        """Get holdings for specific symbol"""
        if self.portfolio_df is None:
            return None
        
        holdings = self.portfolio_df[self.portfolio_df['Symbol'] == symbol]
        if holdings.empty:
            print(f"❌ No holdings found for symbol: {symbol}")
            return None
        
        print(f"📈 HOLDINGS FOR {symbol}")
        print("=" * 40)
        total_qty = holdings['Owned_Qty'].sum()
        avg_cost = (holdings['Owned_Qty'] * holdings['Cost']).sum() / total_qty
        total_cost = (holdings['Owned_Qty'] * holdings['Cost']).sum()
        
        print(f"Company: {holdings['Company'].iloc[0]}")
        print(f"Total Quantity: {total_qty:,} shares")
        print(f"Average Cost: {avg_cost:.2f} SAR")
        print(f"Total Investment: {total_cost:,.2f} SAR")
        print(f"Custodian(s): {', '.join(holdings['Custodian'].unique())}")
        
        return holdings
    
    def get_holdings_by_custodian(self, custodian):
        """Get all holdings with specific custodian"""
        if self.portfolio_df is None:
            return None
        
        holdings = self.portfolio_df[self.portfolio_df['Custodian'] == custodian]
        if holdings.empty:
            print(f"❌ No holdings found for custodian: {custodian}")
            return None
        
        print(f"🏦 HOLDINGS WITH {custodian}")
        print("=" * 50)
        
        total_cost = (holdings['Owned_Qty'] * holdings['Cost']).sum()
        print(f"Total Holdings: {len(holdings)}")
        print(f"Total Investment: {total_cost:,.2f} SAR")
        print("\nDetailed Holdings:")
        print(holdings[['Company', 'Symbol', 'Owned_Qty', 'Cost']].to_string(index=False))
        
        return holdings
    
    def get_largest_holdings(self, top_n=10):
        """Get largest holdings by value"""
        if self.portfolio_df is None:
            return None
        
        df = self.portfolio_df.copy()
        df['Total_Value'] = df['Owned_Qty'] * df['Cost']
        df = df.sort_values('Total_Value', ascending=False)
        
        print(f"🏆 TOP {top_n} LARGEST HOLDINGS")
        print("=" * 60)
        
        top_holdings = df.head(top_n)
        for i, (_, row) in enumerate(top_holdings.iterrows(), 1):
            print(f"{i:2d}. {row['Company']} ({row['Symbol']})")
            print(f"    Qty: {row['Owned_Qty']:,} shares | Cost: {row['Cost']:.2f} SAR | Value: {row['Total_Value']:,.2f} SAR")
        
        return top_holdings
    
    def get_current_market_values(self):
        """Get current market values for portfolio holdings"""
        if self.portfolio_df is None:
            return None
        
        print("📈 FETCHING CURRENT MARKET VALUES...")
        print("=" * 50)
        
        unique_symbols = self.portfolio_df['Symbol'].unique()
        market_data = []
        
        for symbol in unique_symbols:
            try:
                # Get current market price
                ticker = yf.Ticker(f"{symbol}.SR")
                hist = ticker.history(period="5d")
                
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                    change_pct = ((current_price - prev_price) / prev_price) * 100
                    
                    # Get portfolio data for this symbol
                    holdings = self.portfolio_df[self.portfolio_df['Symbol'] == symbol]
                    total_qty = holdings['Owned_Qty'].sum()
                    avg_cost = (holdings['Owned_Qty'] * holdings['Cost']).sum() / total_qty
                    
                    market_value = total_qty * current_price
                    cost_basis = total_qty * avg_cost
                    pnl = market_value - cost_basis
                    pnl_pct = (pnl / cost_basis) * 100
                    
                    market_data.append({
                        'Symbol': symbol,
                        'Company': holdings['Company'].iloc[0],
                        'Quantity': total_qty,
                        'Avg_Cost': avg_cost,
                        'Current_Price': current_price,
                        'Change_%': change_pct,
                        'Cost_Basis': cost_basis,
                        'Market_Value': market_value,
                        'P&L': pnl,
                        'P&L_%': pnl_pct
                    })
                    
                    print(f"✅ {symbol}: {current_price:.2f} SAR ({change_pct:+.1f}%)")
                else:
                    print(f"❌ {symbol}: No price data available")
                    
            except Exception as e:
                print(f"❌ {symbol}: Error fetching data - {e}")
        
        if market_data:
            market_df = pd.DataFrame(market_data)
            
            print("\n📊 PORTFOLIO MARKET ANALYSIS")
            print("=" * 80)
            
            total_cost = market_df['Cost_Basis'].sum()
            total_market = market_df['Market_Value'].sum()
            total_pnl = market_df['P&L'].sum()
            total_pnl_pct = (total_pnl / total_cost) * 100
            
            print(f"Total Cost Basis: {total_cost:,.2f} SAR")
            print(f"Total Market Value: {total_market:,.2f} SAR")
            print(f"Total P&L: {total_pnl:+,.2f} SAR ({total_pnl_pct:+.1f}%)")
            
            print("\nDetailed Analysis:")
            print(market_df.to_string(index=False))
            
            return market_df
        
        return None
    
    def get_sector_analysis(self):
        """Analyze portfolio by sectors"""
        if self.portfolio_df is None:
            return None
        
        # Define sector mapping for Saudi stocks (using actual symbols from portfolio)
        sector_mapping = {
            'Riyadh Bank': 'Banks', 'BJAZ': 'Banks', 'Arabi Bank': 'Banks', 
            'Al Rajhi Bank': 'Banks', 'ALBILAD': 'Banks', 'ALINMA': 'Banks', 
            'Al Ahli Bank': 'Banks',
            'SABIC': 'Petrochemicals', 'SAUDI ARAMCO': 'Energy', 
            'CHEMICAL': 'Petrochemicals', 'YANSAB': 'Petrochemicals', 
            'TASNEE': 'Petrochemicals',
            'STC': 'Telecom', 'Zain KSA': 'Telecom',
            'A.OTHAIM MARKET': 'Consumer', 'BINDAWOOD': 'Consumer', 
            'JARIR': 'Consumer', 'ALMARAI': 'Consumer', 'NADEC': 'Consumer',
            'SAVOLA GROUP': 'Consumer',
            'SAUDI ELECTRICITY': 'Utilities',
            'RETAL': 'Real Estate', 'SUMOU': 'Real Estate', 'MASAR': 'Real Estate',
            'ALAHLI REIT 1': 'Real Estate', 'ALBILAD SAUDI GROWTH': 'Real Estate',
            'EIC': 'Industrial', 'ALYAMAMAH STEEL': 'Industrial', 'ADES': 'Industrial',
            'QACCO': 'Healthcare', 'SPIMACO': 'Healthcare',
            'DERAYAH': 'Financial Services', 'BATIC': 'Insurance', 
            'SAUDI DARB': 'Transportation', 'ACIG': 'Insurance'
        }
        
        df = self.portfolio_df.copy()
        df['Sector'] = df['Company'].map(sector_mapping).fillna('Other')
        df['Total_Value'] = df['Owned_Qty'] * df['Cost']
        
        sector_summary = df.groupby('Sector').agg({
            'Total_Value': 'sum',
            'Company': 'count'
        }).round(2)
        
        sector_summary.columns = ['Total_Investment', 'Number_of_Stocks']
        sector_summary['Percentage'] = (sector_summary['Total_Investment'] / sector_summary['Total_Investment'].sum() * 100).round(1)
        sector_summary = sector_summary.sort_values('Total_Investment', ascending=False)
        
        print("🏭 PORTFOLIO SECTOR ANALYSIS")
        print("=" * 70)
        print(f"{'Sector':<20} {'Investment (SAR)':<15} {'Stocks':<8} {'%':<8}")
        print("-" * 70)
        
        for sector, row in sector_summary.iterrows():
            print(f"{sector:<20} {row['Total_Investment']:>13,.0f} {row['Number_of_Stocks']:>6} {row['Percentage']:>6.1f}%")
        
        # Show top stocks in each major sector
        print("\n📊 TOP HOLDINGS BY SECTOR:")
        print("-" * 50)
        
        for sector in sector_summary.head(5).index:
            sector_stocks = df[df['Sector'] == sector].nlargest(2, 'Total_Value')
            print(f"\n{sector}:")
            for _, stock in sector_stocks.iterrows():
                print(f"  • {stock['Company']}: {stock['Total_Value']:,.0f} SAR")
        
        return sector_summary
    
    def get_performance_leaders(self):
        """Get best and worst performing stocks with current prices"""
        if self.portfolio_df is None:
            return None
        
        print("🎯 FETCHING PERFORMANCE DATA...")
        print("=" * 50)
        
        performance_data = []
        unique_symbols = self.portfolio_df['Symbol'].unique()
        
        for symbol in unique_symbols[:10]:  # Limit to first 10 for speed
            try:
                ticker = yf.Ticker(f"{symbol}.SR")
                hist = ticker.history(period="30d")
                
                if not hist.empty and len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    month_ago_price = hist['Close'].iloc[0]
                    monthly_return = ((current_price - month_ago_price) / month_ago_price) * 100
                    
                    holdings = self.portfolio_df[self.portfolio_df['Symbol'] == symbol]
                    avg_cost = holdings['Cost'].iloc[0]
                    total_return = ((current_price - avg_cost) / avg_cost) * 100
                    
                    performance_data.append({
                        'Symbol': symbol,
                        'Company': holdings['Company'].iloc[0],
                        'Current_Price': current_price,
                        'Avg_Cost': avg_cost,
                        'Monthly_Return_%': monthly_return,
                        'Total_Return_%': total_return,
                        'Investment': holdings['Owned_Qty'].sum() * avg_cost
                    })
                    
                    print(f"✅ {symbol}: {monthly_return:+.1f}% (30d)")
                    
            except Exception as e:
                print(f"❌ {symbol}: Error - {str(e)[:30]}...")
        
        if performance_data:
            perf_df = pd.DataFrame(performance_data)
            
            print("\n🏆 PERFORMANCE LEADERS (30-Day)")
            print("=" * 70)
            
            # Best performers
            best = perf_df.nlargest(3, 'Monthly_Return_%')
            print("📈 TOP PERFORMERS:")
            for _, stock in best.iterrows():
                print(f"  {stock['Company']} ({stock['Symbol']}): {stock['Monthly_Return_%']:+.1f}%")
            
            # Worst performers
            worst = perf_df.nsmallest(3, 'Monthly_Return_%')
            print("\n📉 UNDERPERFORMERS:")
            for _, stock in worst.iterrows():
                print(f"  {stock['Company']} ({stock['Symbol']}): {stock['Monthly_Return_%']:+.1f}%")
            
            return perf_df
        
        return None
    
    def get_dividend_tracker(self):
        """Track dividend-paying stocks in portfolio"""
        dividend_stocks = {
            'Al Rajhi Bank': {'symbol': '1120', 'last_dividend': 2.5, 'yield': 2.6},
            'SAUDI ARAMCO': {'symbol': '2222', 'last_dividend': 0.7, 'yield': 2.9},
            'STC': {'symbol': '7010', 'last_dividend': 1.0, 'yield': 2.3},
            'SABIC': {'symbol': '2010', 'last_dividend': 1.5, 'yield': 2.1},
            'ALMARAI': {'symbol': '2280', 'last_dividend': 1.2, 'yield': 2.5},
            'SAUDI ELECTRICITY': {'symbol': '5110', 'last_dividend': 0.5, 'yield': 3.4},
            'ALINMA': {'symbol': '1150', 'last_dividend': 1.8, 'yield': 2.8},
            'Riyadh Bank': {'symbol': '1010', 'last_dividend': 2.0, 'yield': 2.4}
        }
        
        print("💰 DIVIDEND TRACKING")
        print("=" * 70)
        
        portfolio_dividends = []
        total_annual_dividends = 0
        
        for company in self.portfolio_df['Company'].unique():
            if company in dividend_stocks:
                holdings = self.portfolio_df[self.portfolio_df['Company'] == company]
                qty = holdings['Owned_Qty'].sum()
                last_div = dividend_stocks[company]['last_dividend']
                annual_dividend = qty * last_div
                
                portfolio_dividends.append({
                    'Symbol': dividend_stocks[company]['symbol'],
                    'Company': company,
                    'Shares': qty,
                    'Last_Dividend': last_div,
                    'Annual_Income': annual_dividend,
                    'Yield_%': dividend_stocks[company]['yield']
                })
                
                total_annual_dividends += annual_dividend
                print(f"{dividend_stocks[company]['symbol']} - {company}")
                print(f"  Shares: {qty:,} | Dividend: {last_div} SAR | Annual: {annual_dividend:,.0f} SAR | Yield: {dividend_stocks[company]['yield']}%")
        
        if total_annual_dividends > 0:
            print(f"\n💵 TOTAL ESTIMATED ANNUAL DIVIDENDS: {total_annual_dividends:,.0f} SAR")
            
            # Calculate dividend yield on total investment in dividend stocks
            total_dividend_investment = sum([
                (self.portfolio_df[self.portfolio_df['Company'] == company]['Owned_Qty'].sum() * 
                 self.portfolio_df[self.portfolio_df['Company'] == company]['Cost'].iloc[0])
                for company in dividend_stocks.keys() 
                if company in self.portfolio_df['Company'].values
            ])
            
            if total_dividend_investment > 0:
                portfolio_yield = (total_annual_dividends / total_dividend_investment) * 100
                print(f"💰 PORTFOLIO DIVIDEND YIELD: {portfolio_yield:.1f}%")
        else:
            print("ℹ️  No dividend-paying stocks found in your portfolio.")
        
        return portfolio_dividends
    
    def export_data(self, filename=None):
        """Export portfolio data to CSV"""
        if self.portfolio_df is None:
            return False
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"portfolio_export_{timestamp}.csv"
        
        try:
            self.portfolio_df.to_csv(filename, index=False)
            print(f"✅ Portfolio data exported to: {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False

def quick_portfolio_info():
    """Quick function to get key portfolio metrics"""
    portfolio = PortfolioAccessor()
    if portfolio.portfolio_df is None:
        return None
    
    summary = portfolio.get_portfolio_summary()
    top_5 = portfolio.get_largest_holdings(5)
    
    return {
        'summary': summary,
        'top_holdings': top_5,
        'total_value': summary['total_cost'],
        'stock_count': summary['unique_stocks']
    }

def get_stock_info(symbol):
    """Quick function to get info for a specific stock"""
    portfolio = PortfolioAccessor()
    if portfolio.portfolio_df is None:
        return None
    
    return portfolio.get_holdings_by_symbol(symbol)

def main():
    """Main function for interactive use"""
    print("🚀 PORTFOLIO DATA ACCESS UTILITY")
    print("=" * 60)
    
    # Initialize portfolio accessor
    portfolio = PortfolioAccessor()
    
    if portfolio.portfolio_df is None:
        print("❌ Cannot proceed without portfolio data!")
        return
    
    while True:
        print("\n" + "="*60)
        print("📋 AVAILABLE COMMANDS:")
        print("1. Portfolio Summary")
        print("2. View All Holdings")
        print("3. Search by Symbol")
        print("4. View by Custodian")
        print("5. Top Holdings")
        print("6. Current Market Values")
        print("7. Sector Analysis")
        print("8. Performance Leaders")
        print("9. Dividend Tracker")
        print("10. Export Data")
        print("11. Exit")
        print("="*60)
        
        choice = input("Enter your choice (1-11): ").strip()
        
        if choice == '1':
            portfolio.get_portfolio_summary()
            
        elif choice == '2':
            portfolio.get_all_holdings()
            
        elif choice == '3':
            symbol = input("Enter symbol (e.g., 1120, 2222): ").strip()
            portfolio.get_holdings_by_symbol(symbol)
            
        elif choice == '4':
            custodians = portfolio.portfolio_df['Custodian'].unique()
            print("Available custodians:", ', '.join(custodians))
            custodian = input("Enter custodian name: ").strip()
            portfolio.get_holdings_by_custodian(custodian)
            
        elif choice == '5':
            try:
                n = int(input("How many top holdings to show (default 10): ") or "10")
                portfolio.get_largest_holdings(n)
            except ValueError:
                portfolio.get_largest_holdings()
                
        elif choice == '6':
            portfolio.get_current_market_values()
            
        elif choice == '7':
            portfolio.get_sector_analysis()
            
        elif choice == '8':
            portfolio.get_performance_leaders()
            
        elif choice == '9':
            portfolio.get_dividend_tracker()
            
        elif choice == '10':
            filename = input("Enter filename (press Enter for auto-generated): ").strip()
            portfolio.export_data(filename if filename else None)
            
        elif choice == '11':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please select 1-11.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
