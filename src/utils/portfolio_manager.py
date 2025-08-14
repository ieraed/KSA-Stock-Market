"""
Portfolio Import and Management System for Saudi Stock Market App
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import streamlit as st
from ..data.market_data import MarketDataFetcher
from ..utils.config import Config

class PortfolioManager:
    """Manage multi-broker portfolio data"""
    
    def __init__(self, data_fetcher: MarketDataFetcher, config: Config):
        self.data_fetcher = data_fetcher
        self.config = config
        
    def parse_portfolio_from_csv(self, csv_data: str) -> pd.DataFrame:
        """Parse portfolio data from CSV format"""
        try:
            # Convert the CSV data to DataFrame
            from io import StringIO
            df = pd.read_csv(StringIO(csv_data))
            return df
        except Exception as e:
            st.error(f"Error parsing CSV: {e}")
            return pd.DataFrame()
    
    def create_sample_portfolio(self) -> pd.DataFrame:
        """Create sample portfolio based on user's corrected holdings"""
        portfolio_data = [
            # Al Inma Capital Holdings
            {"Company": "ALINMA", "Symbol": "1150", "Owned_Qty": 3722, "Cost": 27.02, "Custodian": "Al Inma Capital"},
            {"Company": "ACIG", "Symbol": "8150", "Owned_Qty": 1500, "Cost": 15.14, "Custodian": "Al Inma Capital"},
            {"Company": "NADEC", "Symbol": "2190", "Owned_Qty": 2967, "Cost": 22.28, "Custodian": "Al Inma Capital"},
            {"Company": "SUMOU", "Symbol": "4323", "Owned_Qty": 1300, "Cost": 42.86, "Custodian": "Al Inma Capital"},
            {"Company": "ALBILAD", "Symbol": "1140", "Owned_Qty": 1500, "Cost": 27.31, "Custodian": "Al Inma Capital"},
            {"Company": "SAUDI ELECTRICITY", "Symbol": "5110", "Owned_Qty": 3000, "Cost": 17.05, "Custodian": "Al Inma Capital"},
            {"Company": "SABIC", "Symbol": "2010", "Owned_Qty": 3000, "Cost": 71.97, "Custodian": "Al Inma Capital"},
            {"Company": "YANSAB", "Symbol": "2290", "Owned_Qty": 3877, "Cost": 34.34, "Custodian": "Al Inma Capital"},
            {"Company": "RETAL", "Symbol": "4322", "Owned_Qty": 4000, "Cost": 14.43, "Custodian": "Al Inma Capital"},
            {"Company": "JARIR", "Symbol": "4190", "Owned_Qty": 8573, "Cost": 13.57, "Custodian": "Al Inma Capital"},
            {"Company": "QACCO", "Symbol": "3040", "Owned_Qty": 972, "Cost": 62.51, "Custodian": "Al Inma Capital"},
            {"Company": "ALBILAD SAUDI GROWTH", "Symbol": "9408", "Owned_Qty": 1000, "Cost": 11.19, "Custodian": "Al Inma Capital"},
            {"Company": "A.OTHAIM MARKET", "Symbol": "4001", "Owned_Qty": 9500, "Cost": 10.75, "Custodian": "Al Inma Capital"},
            {"Company": "BINDAWOOD", "Symbol": "4161", "Owned_Qty": 4000, "Cost": 7.79, "Custodian": "Al Inma Capital"},
            {"Company": "ALAHLI REIT 1", "Symbol": "4338", "Owned_Qty": 3000, "Cost": 8.11, "Custodian": "Al Inma Capital"},
            {"Company": "BJAZ", "Symbol": "1020", "Owned_Qty": 10546, "Cost": 13.67, "Custodian": "Al Inma Capital"},
            
            # BSF Capital Holdings
            {"Company": "EIC", "Symbol": "1303", "Owned_Qty": 2950, "Cost": 5.13, "Custodian": "BSF Capital"},
            {"Company": "TASNEE", "Symbol": "2060", "Owned_Qty": 5500, "Cost": 10.86, "Custodian": "BSF Capital"},
            {"Company": "SAVOLA GROUP", "Symbol": "2050", "Owned_Qty": 1061, "Cost": 62.74, "Custodian": "BSF Capital"},
            {"Company": "SAUDI ARAMCO", "Symbol": "2222", "Owned_Qty": 2550, "Cost": 26.61, "Custodian": "BSF Capital"},
            {"Company": "SAUDI DARB", "Symbol": "4130", "Owned_Qty": 2000, "Cost": 4.71, "Custodian": "BSF Capital"},
            {"Company": "ALYAMAMAH STEEL", "Symbol": "1304", "Owned_Qty": 1000, "Cost": 38.69, "Custodian": "BSF Capital"},
            {"Company": "SPIMACO", "Symbol": "2070", "Owned_Qty": 1500, "Cost": 31.99, "Custodian": "BSF Capital"},
            {"Company": "ALMARAI", "Symbol": "2280", "Owned_Qty": 646, "Cost": 0.00, "Custodian": "BSF Capital"},
            {"Company": "BATIC", "Symbol": "4110", "Owned_Qty": 6800, "Cost": 3.62, "Custodian": "BSF Capital"},
            {"Company": "DERAYAH", "Symbol": "4084", "Owned_Qty": 10, "Cost": 30.00, "Custodian": "BSF Capital"},
            {"Company": "MASAR", "Symbol": "4325", "Owned_Qty": 1015, "Cost": 23.00, "Custodian": "BSF Capital"},
            
            # Al Rajhi Capital Holdings
            {"Company": "SISCO HOLDING", "Symbol": "2190", "Owned_Qty": 1000, "Cost": 28.83, "Custodian": "Al Rajhi Capital"},
            {"Company": "Riyadh Bank", "Symbol": "1010", "Owned_Qty": 3811, "Cost": 27.58, "Custodian": "Al Rajhi Capital"},
            {"Company": "ARAMCO", "Symbol": "2222", "Owned_Qty": 231, "Cost": 27.25, "Custodian": "Al Rajhi Capital"},
            {"Company": "Electrical Industries Co.", "Symbol": "1303", "Owned_Qty": 7500, "Cost": 7.13, "Custodian": "Al Rajhi Capital"},
            {"Company": "Al Ahli Bank", "Symbol": "1180", "Owned_Qty": 2000, "Cost": 33.43, "Custodian": "Al Rajhi Capital"},
            {"Company": "STC", "Symbol": "7010", "Owned_Qty": 3000, "Cost": 41.39, "Custodian": "Al Rajhi Capital"},
            {"Company": "Arabi Bank", "Symbol": "1080", "Owned_Qty": 3666, "Cost": 20.32, "Custodian": "Al Rajhi Capital"},
            {"Company": "Zain KSA", "Symbol": "7030", "Owned_Qty": 9400, "Cost": 11.41, "Custodian": "Al Rajhi Capital"},
            {"Company": "SAUDI DARB", "Symbol": "4130", "Owned_Qty": 6470, "Cost": 4.02, "Custodian": "Al Rajhi Capital"},
            {"Company": "ADES", "Symbol": "2382", "Owned_Qty": 1000, "Cost": 14.72, "Custodian": "Al Rajhi Capital"},
            {"Company": "CHEMICAL", "Symbol": "2230", "Owned_Qty": 1000, "Cost": 7.62, "Custodian": "Al Rajhi Capital"},
            {"Company": "Al Rajhi Bank", "Symbol": "1120", "Owned_Qty": 500, "Cost": 92.60, "Custodian": "Al Rajhi Capital"},
        ]
        
        return pd.DataFrame(portfolio_data)
    
    def get_current_prices(self, portfolio_df: pd.DataFrame) -> Dict[str, float]:
        """Get current market prices for all symbols in portfolio"""
        prices = {}
        symbols = portfolio_df['Symbol'].unique().tolist()
        
        for symbol in symbols:
            try:
                # Add .SR suffix for Yahoo Finance API
                yahoo_symbol = f"{symbol}.SR"
                data = self.data_fetcher.get_stock_data(yahoo_symbol, period="1d")
                if not data.empty and len(data) > 0:
                    current_price = float(data['Close'].iloc[-1])
                    if current_price > 0:
                        prices[symbol] = current_price
                    else:
                        prices[symbol] = 0.0
                else:
                    prices[symbol] = 0.0
            except Exception as e:
                print(f"Could not get price for {symbol}: {e}")
                prices[symbol] = 0.0
        
        return prices
    
    def get_stock_info(self, symbol: str) -> Dict[str, str]:
        """Get stock information including company name"""
        # Stock symbol to company name mapping for Saudi stocks
        stock_names = {
            "1150": "Al Inma Bank",
            "8150": "ACIG",
            "6010": "NADEC",
            "4323": "SIMOUI",
            "1140": "ALDLAD",
            "5110": "Saudi Electricity Company",
            "2010": "SABIC",
            "2290": "YANSAB",
            "4322": "RETAL",
            "4190": "Jarir Marketing Company",
            "3040": "QACCO",
            "9408": "AlBilad Saudi Growth Fund",
            "4001": "Al Othaim Markets",
            "4161": "Bindawood Holding",
            "4338": "Al Ahli REIT Fund 1",
            "1020": "Bank AlJazira",
            "1303": "Electrical Industries Company",
            "2060": "TASNEE",
            "2050": "Savola Group",
            "2222": "Saudi Aramco",
            "4130": "Saudi Automotive Services",
            "1304": "Al Hammadi Company",
            "2070": "SPIMACO",
            "2280": "Almarai",
            "4110": "BATIC",
            "4084": "Derayah Financial",
            "2190": "Sisco Holding",
            "1010": "Riyad Bank",
            "1180": "Al Ahli Bank",
            "7010": "Saudi Telecom Company",
            "1080": "Arab Bank",
            "7030": "Zain KSA",
            "2382": "ADES",
            "2230": "Petrochemical Industries",
            "1120": "Al Rajhi Bank"
        }
        
        return {
            "name": stock_names.get(symbol, f"Company {symbol}"),
            "symbol": symbol
        }
    
    def calculate_portfolio_metrics(self, portfolio_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate portfolio metrics with current prices"""
        if portfolio_df.empty:
            return portfolio_df
        
        # Get current prices
        symbols = portfolio_df['Symbol'].unique()
        current_prices = self.get_current_prices(symbols)
        
        # Add stock names and current prices to dataframe
        portfolio_df['Stock_Name'] = portfolio_df['Symbol'].apply(lambda x: self.get_stock_info(x)['name'])
        portfolio_df['Current_Price'] = portfolio_df['Symbol'].map(current_prices)
        
        # Calculate metrics
        portfolio_df['Total_Cost'] = portfolio_df['Owned_Qty'] * portfolio_df['Cost']
        portfolio_df['Market_Value'] = portfolio_df['Owned_Qty'] * portfolio_df['Current_Price']
        portfolio_df['Gain_Loss'] = portfolio_df['Market_Value'] - portfolio_df['Total_Cost']
        portfolio_df['Gain_Loss_Pct'] = (portfolio_df['Gain_Loss'] / portfolio_df['Total_Cost'] * 100).round(2)
        
        # Handle division by zero and infinite values
        portfolio_df['Gain_Loss_Pct'] = portfolio_df['Gain_Loss_Pct'].replace([np.inf, -np.inf], 0)
        portfolio_df['Gain_Loss_Pct'] = portfolio_df['Gain_Loss_Pct'].fillna(0)
        
        # Format numeric columns to 2 decimal places
        numeric_columns = ['Cost', 'Current_Price', 'Total_Cost', 'Market_Value', 'Gain_Loss']
        for col in numeric_columns:
            portfolio_df[col] = portfolio_df[col].round(2)
        
        return portfolio_df
    
    def get_portfolio_summary(self, portfolio_df: pd.DataFrame) -> Dict:
        """Get portfolio summary statistics"""
        if portfolio_df.empty:
            return {}
        
        summary = {
            'total_cost': portfolio_df['Total_Cost'].sum(),
            'total_market_value': portfolio_df['Market_Value'].sum(),
            'total_gain_loss': portfolio_df['Gain_Loss'].sum(),
            'total_gain_loss_pct': ((portfolio_df['Market_Value'].sum() - portfolio_df['Total_Cost'].sum()) / portfolio_df['Total_Cost'].sum() * 100),
            'num_positions': len(portfolio_df),
            'num_brokers': portfolio_df['Custodian'].nunique(),
            'top_holding': portfolio_df.loc[portfolio_df['Market_Value'].idxmax(), 'Company'] if len(portfolio_df) > 0 else '',
            'best_performer': portfolio_df.loc[portfolio_df['Gain_Loss_Pct'].idxmax(), 'Company'] if len(portfolio_df) > 0 else '',
            'worst_performer': portfolio_df.loc[portfolio_df['Gain_Loss_Pct'].idxmin(), 'Company'] if len(portfolio_df) > 0 else ''
        }
        
        return summary
