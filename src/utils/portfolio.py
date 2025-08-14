"""
Portfolio tracking and management
"""

import pandas as pd
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Portfolio:
    """Portfolio management class"""
    
    def __init__(self, initial_cash: float = 100000, portfolio_file: str = "portfolio.json"):
        self.portfolio_file = Path(portfolio_file)
        self.cash = initial_cash
        self.positions = {}  # symbol -> {'shares': int, 'avg_price': float, 'total_cost': float}
        self.transactions = []  # List of all transactions
        self.load_portfolio()
    
    def buy_stock(self, symbol: str, shares: int, price: float, date: datetime = None) -> bool:
        """
        Buy stocks and update portfolio
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to buy
            price: Price per share
            date: Transaction date (default: now)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if date is None:
                date = datetime.now()
            
            total_cost = shares * price
            
            # Check if we have enough cash
            if total_cost > self.cash:
                logger.warning(f"Insufficient cash to buy {shares} shares of {symbol}")
                return False
            
            # Update cash
            self.cash -= total_cost
            
            # Update positions
            if symbol in self.positions:
                # Add to existing position
                old_shares = self.positions[symbol]['shares']
                old_total_cost = self.positions[symbol]['total_cost']
                
                new_shares = old_shares + shares
                new_total_cost = old_total_cost + total_cost
                new_avg_price = new_total_cost / new_shares
                
                self.positions[symbol] = {
                    'shares': new_shares,
                    'avg_price': new_avg_price,
                    'total_cost': new_total_cost
                }
            else:
                # Create new position
                self.positions[symbol] = {
                    'shares': shares,
                    'avg_price': price,
                    'total_cost': total_cost
                }
            
            # Record transaction
            self.transactions.append({
                'type': 'BUY',
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'total': total_cost,
                'date': date.isoformat(),
                'remaining_cash': self.cash
            })
            
            self.save_portfolio()
            logger.info(f"Bought {shares} shares of {symbol} at {price:.2f} SAR")
            return True
            
        except Exception as e:
            logger.error(f"Error buying stock: {e}")
            return False
    
    def sell_stock(self, symbol: str, shares: int, price: float, date: datetime = None) -> bool:
        """
        Sell stocks and update portfolio
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to sell
            price: Price per share
            date: Transaction date (default: now)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if date is None:
                date = datetime.now()
            
            # Check if we have the position
            if symbol not in self.positions:
                logger.warning(f"No position in {symbol} to sell")
                return False
            
            available_shares = self.positions[symbol]['shares']
            if shares > available_shares:
                logger.warning(f"Trying to sell {shares} shares but only have {available_shares}")
                return False
            
            total_proceeds = shares * price
            
            # Update cash
            self.cash += total_proceeds
            
            # Update position
            if shares == available_shares:
                # Selling entire position
                avg_cost = self.positions[symbol]['avg_price']
                del self.positions[symbol]
            else:
                # Partial sale
                remaining_shares = available_shares - shares
                cost_per_share = self.positions[symbol]['total_cost'] / available_shares
                remaining_cost = remaining_shares * cost_per_share
                
                self.positions[symbol] = {
                    'shares': remaining_shares,
                    'avg_price': self.positions[symbol]['avg_price'],
                    'total_cost': remaining_cost
                }
                avg_cost = self.positions[symbol]['avg_price']
            
            # Calculate profit/loss
            profit_loss = (price - avg_cost) * shares
            
            # Record transaction
            self.transactions.append({
                'type': 'SELL',
                'symbol': symbol,
                'shares': shares,
                'price': price,
                'total': total_proceeds,
                'profit_loss': profit_loss,
                'date': date.isoformat(),
                'remaining_cash': self.cash
            })
            
            self.save_portfolio()
            logger.info(f"Sold {shares} shares of {symbol} at {price:.2f} SAR (P&L: {profit_loss:.2f} SAR)")
            return True
            
        except Exception as e:
            logger.error(f"Error selling stock: {e}")
            return False
    
    def get_portfolio_value(self, current_prices: Dict[str, float]) -> Dict[str, float]:
        """
        Calculate current portfolio value
        
        Args:
            current_prices: Dictionary of symbol -> current price
        
        Returns:
            Dictionary with portfolio metrics
        """
        total_position_value = 0
        position_details = {}
        
        for symbol, position in self.positions.items():
            current_price = current_prices.get(symbol, position['avg_price'])
            position_value = position['shares'] * current_price
            unrealized_pnl = position_value - position['total_cost']
            unrealized_pnl_pct = (unrealized_pnl / position['total_cost']) * 100
            
            position_details[symbol] = {
                'shares': position['shares'],
                'avg_price': position['avg_price'],
                'current_price': current_price,
                'position_value': position_value,
                'total_cost': position['total_cost'],
                'unrealized_pnl': unrealized_pnl,
                'unrealized_pnl_pct': unrealized_pnl_pct
            }
            
            total_position_value += position_value
        
        total_portfolio_value = self.cash + total_position_value
        
        return {
            'cash': self.cash,
            'total_position_value': total_position_value,
            'total_portfolio_value': total_portfolio_value,
            'positions': position_details
        }
    
    def get_performance_metrics(self, initial_value: float = None) -> Dict[str, float]:
        """Calculate portfolio performance metrics"""
        if initial_value is None:
            initial_value = 100000  # Default initial value
        
        # Calculate realized P&L from transactions
        realized_pnl = sum(
            t.get('profit_loss', 0) for t in self.transactions if t['type'] == 'SELL'
        )
        
        # Get current portfolio value (assuming current prices = avg prices for simplicity)
        current_prices = {symbol: pos['avg_price'] for symbol, pos in self.positions.items()}
        portfolio_metrics = self.get_portfolio_value(current_prices)
        
        total_value = portfolio_metrics['total_portfolio_value']
        total_return = total_value - initial_value
        total_return_pct = (total_return / initial_value) * 100
        
        return {
            'initial_value': initial_value,
            'current_value': total_value,
            'total_return': total_return,
            'total_return_pct': total_return_pct,
            'realized_pnl': realized_pnl,
            'cash_balance': self.cash,
            'invested_amount': portfolio_metrics['total_position_value']
        }
    
    def save_portfolio(self):
        """Save portfolio to file"""
        try:
            portfolio_data = {
                'cash': self.cash,
                'positions': self.positions,
                'transactions': self.transactions,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.portfolio_file, 'w') as f:
                json.dump(portfolio_data, f, indent=2)
            
        except Exception as e:
            logger.error(f"Error saving portfolio: {e}")
    
    def load_portfolio(self):
        """Load portfolio from file"""
        try:
            if self.portfolio_file.exists():
                with open(self.portfolio_file, 'r') as f:
                    portfolio_data = json.load(f)
                
                self.cash = portfolio_data.get('cash', self.cash)
                self.positions = portfolio_data.get('positions', {})
                self.transactions = portfolio_data.get('transactions', [])
                
                logger.info("Portfolio loaded successfully")
            else:
                logger.info("No existing portfolio file found, starting fresh")
                
        except Exception as e:
            logger.error(f"Error loading portfolio: {e}")
    
    def get_transaction_history(self, days: int = 30) -> pd.DataFrame:
        """Get transaction history as DataFrame"""
        if not self.transactions:
            return pd.DataFrame()
        
        # Filter transactions by date
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_transactions = [
            t for t in self.transactions 
            if datetime.fromisoformat(t['date']) >= cutoff_date
        ]
        
        if not recent_transactions:
            return pd.DataFrame()
        
        df = pd.DataFrame(recent_transactions)
        df['date'] = pd.to_datetime(df['date'])
        return df.sort_values('date', ascending=False)
    
    def print_portfolio_summary(self):
        """Print portfolio summary to console"""
        print("\n" + "="*60)
        print("💼 PORTFOLIO SUMMARY")
        print("="*60)
        
        # Performance metrics
        metrics = self.get_performance_metrics()
        print(f"💰 Cash Balance: {self.cash:,.2f} SAR")
        print(f"📊 Total Portfolio Value: {metrics['current_value']:,.2f} SAR")
        print(f"📈 Total Return: {metrics['total_return']:,.2f} SAR ({metrics['total_return_pct']:.2f}%)")
        print(f"💵 Invested Amount: {metrics['invested_amount']:,.2f} SAR")
        print(f"✅ Realized P&L: {metrics['realized_pnl']:,.2f} SAR")
        
        # Current positions
        if self.positions:
            print(f"\n📋 CURRENT POSITIONS:")
            print("-" * 60)
            for symbol, position in self.positions.items():
                print(f"{symbol}: {position['shares']} shares @ {position['avg_price']:.2f} SAR avg")
                print(f"   Total Cost: {position['total_cost']:,.2f} SAR")
        else:
            print(f"\nℹ️  No current positions")
        
        print("="*60)
