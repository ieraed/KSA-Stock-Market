"""
Professional Portfolio Management System
Handles portfolio data with data integrity and validation
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import yfinance as yf

class ProfessionalPortfolioManager:
    def __init__(self, portfolio_file="portfolio_template.xlsx"):
        self.portfolio_file = Path(portfolio_file)
        self.portfolio_data = None
        self.validation_errors = []
        
    def load_portfolio(self):
        """Load portfolio with robust error handling"""
        try:
            # Try multiple file sources
            sources = [
                self.portfolio_file,
                Path("portfolio_template.xlsx"),
                Path("portfolio_corrected_costs.xlsx"),
                Path("src/utils/portfolio_template.xlsx")
            ]
            
            for source in sources:
                if source.exists():
                    try:
                        self.portfolio_data = pd.read_excel(source)
                        if self._validate_portfolio():
                            print(f"✅ Portfolio loaded from {source}")
                            return True
                    except Exception as e:
                        print(f"❌ Error reading {source}: {e}")
                        continue
            
            # If no file found, check session state
            import streamlit as st
            if hasattr(st, 'session_state') and 'manual_portfolio' in st.session_state:
                if st.session_state.manual_portfolio:
                    self.portfolio_data = pd.DataFrame(st.session_state.manual_portfolio)
                    if self._validate_portfolio():
                        print("✅ Portfolio loaded from session state")
                        return True
            
            # If still no portfolio, create sample
            self._create_sample_portfolio()
            return True
            
        except Exception as e:
            print(f"❌ Critical error loading portfolio: {e}")
            self._create_sample_portfolio()
            return False
    
    def _validate_portfolio(self):
        """Validate portfolio data integrity"""
        if self.portfolio_data is None or self.portfolio_data.empty:
            self.validation_errors.append("Portfolio is empty")
            return False
        
        required_columns = ['Symbol', 'Owned_Qty']
        missing_columns = [col for col in required_columns if col not in self.portfolio_data.columns]
        
        if missing_columns:
            self.validation_errors.append(f"Missing required columns: {missing_columns}")
            return False
        
        # Check for valid symbols
        invalid_symbols = self.portfolio_data[
            (self.portfolio_data['Symbol'].isna()) | 
            (self.portfolio_data['Symbol'] == '') |
            (self.portfolio_data['Owned_Qty'] <= 0)
        ]
        
        if not invalid_symbols.empty:
            self.validation_errors.append(f"Invalid symbols or quantities found: {len(invalid_symbols)} rows")
            # Clean invalid data
            self.portfolio_data = self.portfolio_data[
                (self.portfolio_data['Symbol'].notna()) & 
                (self.portfolio_data['Symbol'] != '') &
                (self.portfolio_data['Owned_Qty'] > 0)
            ]
        
        print(f"✅ Portfolio validation passed: {len(self.portfolio_data)} valid positions")
        return True
    
    def _create_sample_portfolio(self):
        """Create a sample portfolio for testing"""
        sample_data = [
            {'Symbol': '2222', 'Company': 'Saudi Aramco', 'Owned_Qty': 100, 'Cost': 29.50, 'Custodian': 'Al Rajhi Capital'},
            {'Symbol': '1120', 'Company': 'Al Rajhi Bank', 'Owned_Qty': 50, 'Cost': 85.20, 'Custodian': 'Al Rajhi Capital'},
            {'Symbol': '2010', 'Company': 'SABIC', 'Owned_Qty': 25, 'Cost': 120.00, 'Custodian': 'SNB Capital'},
            {'Symbol': '7010', 'Company': 'STC', 'Owned_Qty': 75, 'Cost': 45.30, 'Custodian': 'Al Inma Capital'},
            {'Symbol': '1210', 'Company': 'SABB', 'Owned_Qty': 60, 'Cost': 45.30, 'Custodian': 'BSF Capital'}
        ]
        
        self.portfolio_data = pd.DataFrame(sample_data)
        print(f"📋 Created sample portfolio with {len(sample_data)} positions")
    
    def get_portfolio_symbols(self):
        """Get list of portfolio symbols for signal generation"""
        if self.portfolio_data is None:
            self.load_portfolio()
        
        if self.portfolio_data is not None and not self.portfolio_data.empty:
            symbols = self.portfolio_data['Symbol'].astype(str).tolist()
            # Add .SR suffix for yfinance compatibility
            yf_symbols = [f"{symbol}.SR" for symbol in symbols]
            return symbols, yf_symbols
        
        return [], []
    
    def get_portfolio_summary(self):
        """Get comprehensive portfolio summary"""
        if self.portfolio_data is None:
            self.load_portfolio()
        
        if self.portfolio_data is None or self.portfolio_data.empty:
            return None
        
        summary = {
            'total_positions': len(self.portfolio_data),
            'total_shares': self.portfolio_data['Owned_Qty'].sum(),
            'symbols': self.portfolio_data['Symbol'].tolist(),
            'companies': self.portfolio_data.get('Company', ['Unknown'] * len(self.portfolio_data)).tolist(),
            'holdings': self.portfolio_data.to_dict('records')
        }
        
        if 'Cost' in self.portfolio_data.columns:
            self.portfolio_data['Total_Value'] = self.portfolio_data['Owned_Qty'] * self.portfolio_data['Cost']
            summary['total_investment'] = self.portfolio_data['Total_Value'].sum()
        
        return summary
    
    def save_portfolio(self, data=None):
        """Save portfolio data with backup"""
        try:
            if data is not None:
                self.portfolio_data = pd.DataFrame(data)
            
            if self.portfolio_data is not None:
                # Save to Excel
                self.portfolio_data.to_excel(self.portfolio_file, index=False)
                
                # Create backup
                backup_file = f"portfolio_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                self.portfolio_data.to_excel(backup_file, index=False)
                
                print(f"✅ Portfolio saved to {self.portfolio_file}")
                return True
                
        except Exception as e:
            print(f"❌ Error saving portfolio: {e}")
            return False

# Global portfolio manager instance
portfolio_manager = ProfessionalPortfolioManager()

def get_portfolio_for_signals():
    """Get portfolio data specifically for signal generation"""
    try:
        # Load portfolio
        if portfolio_manager.load_portfolio():
            symbols, yf_symbols = portfolio_manager.get_portfolio_symbols()
            
            if symbols:
                print(f"✅ Portfolio loaded for signals: {len(symbols)} symbols")
                return {
                    'symbols': symbols,
                    'yf_symbols': yf_symbols,
                    'data': portfolio_manager.portfolio_data,
                    'summary': portfolio_manager.get_portfolio_summary()
                }
            else:
                print("❌ No valid symbols found in portfolio")
                return None
        else:
            print("❌ Failed to load portfolio")
            return None
            
    except Exception as e:
        print(f"❌ Error getting portfolio for signals: {e}")
        return None

if __name__ == "__main__":
    # Test the portfolio manager
    print("Testing Professional Portfolio Manager...")
    
    manager = ProfessionalPortfolioManager()
    if manager.load_portfolio():
        summary = manager.get_portfolio_summary()
        print(f"Portfolio Summary: {summary}")
        
        symbols, yf_symbols = manager.get_portfolio_symbols()
        print(f"Symbols: {symbols}")
        print(f"YFinance Symbols: {yf_symbols}")
    else:
        print("Failed to load portfolio")
