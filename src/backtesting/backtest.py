"""
Backtesting framework for trading strategies
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import logging
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from ..data.market_data import MarketDataFetcher
from ..signals.signal_generator import SignalGenerator, TradingSignal
from ..utils.config import Config

logger = logging.getLogger(__name__)

class BacktestResult:
    """Stores backtesting results"""
    
    def __init__(self):
        self.trades = []
        self.portfolio_value = []
        self.dates = []
        self.initial_capital = 0
        self.final_capital = 0
        self.total_return = 0
        self.total_return_pct = 0
        self.max_drawdown = 0
        self.sharpe_ratio = 0
        self.win_rate = 0
        self.total_trades = 0
        self.profitable_trades = 0
        self.losing_trades = 0
        
    def calculate_metrics(self):
        """Calculate performance metrics"""
        if not self.portfolio_value:
            return
        
        portfolio_series = pd.Series(self.portfolio_value, index=self.dates)
        
        # Returns
        self.total_return = self.final_capital - self.initial_capital
        self.total_return_pct = (self.total_return / self.initial_capital) * 100
        
        # Daily returns
        daily_returns = portfolio_series.pct_change().dropna()
        
        # Sharpe ratio (assuming risk-free rate of 0)
        if len(daily_returns) > 0 and daily_returns.std() != 0:
            self.sharpe_ratio = daily_returns.mean() / daily_returns.std() * np.sqrt(252)  # Annualized
        
        # Maximum drawdown
        peak = portfolio_series.expanding().max()
        drawdown = (portfolio_series - peak) / peak
        self.max_drawdown = drawdown.min() * 100
        
        # Trade statistics
        if self.trades:
            profitable = [t for t in self.trades if t['profit'] > 0]
            self.profitable_trades = len(profitable)
            self.losing_trades = len(self.trades) - self.profitable_trades
            self.total_trades = len(self.trades)
            self.win_rate = (self.profitable_trades / self.total_trades) * 100 if self.total_trades > 0 else 0

class Position:
    """Represents a trading position"""
    
    def __init__(self, symbol: str, shares: int, entry_price: float, entry_date: datetime):
        self.symbol = symbol
        self.shares = shares
        self.entry_price = entry_price
        self.entry_date = entry_date
        self.exit_price = None
        self.exit_date = None
        self.profit = 0
        self.is_open = True
    
    def close(self, exit_price: float, exit_date: datetime):
        """Close the position"""
        self.exit_price = exit_price
        self.exit_date = exit_date
        self.profit = (exit_price - self.entry_price) * self.shares
        self.is_open = False
        return self.profit

class Backtester:
    """Backtesting framework for trading strategies"""
    
    def __init__(self, initial_capital: float = 100000, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission  # Commission as percentage
        self.config = Config()
        self.data_fetcher = MarketDataFetcher(self.config)
        self.signal_generator = SignalGenerator(self.data_fetcher, self.config)
        
    def run_backtest(self, symbol: str, start_date: str, end_date: str, 
                    position_size: float = 0.1) -> BacktestResult:
        """
        Run backtest for a given symbol and date range
        
        Args:
            symbol: Stock symbol to backtest
            start_date: Start date for backtesting (YYYY-MM-DD)
            end_date: End date for backtesting (YYYY-MM-DD)
            position_size: Position size as fraction of portfolio (0.1 = 10%)
        
        Returns:
            BacktestResult object with performance metrics
        """
        try:
            logger.info(f"Starting backtest for {symbol} from {start_date} to {end_date}")
            
            # Fetch historical data
            data = self._fetch_historical_data(symbol, start_date, end_date)
            if data is None or data.empty:
                raise ValueError(f"No data available for {symbol}")
            
            # Initialize backtest
            result = BacktestResult()
            result.initial_capital = self.initial_capital
            
            cash = self.initial_capital
            positions = {}  # symbol -> Position
            portfolio_history = []
            
            # Process each day
            for i, (date, row) in enumerate(data.iterrows()):
                current_price = row['Close']
                
                # Generate signals for current date
                # Note: In real backtesting, we'd use data up to current date only
                signals = self._generate_signals_for_date(symbol, data[:i+1])
                
                # Process signals
                for signal in signals:
                    if signal.signal_type == "BUY" and symbol not in positions:
                        # Open long position
                        shares_to_buy = int((cash * position_size) / current_price)
                        if shares_to_buy > 0:
                            cost = shares_to_buy * current_price * (1 + self.commission)
                            if cost <= cash:
                                positions[symbol] = Position(symbol, shares_to_buy, current_price, date)
                                cash -= cost
                                logger.debug(f"Opened position: {shares_to_buy} shares of {symbol} at {current_price:.2f}")
                    
                    elif signal.signal_type == "SELL" and symbol in positions:
                        # Close position
                        position = positions[symbol]
                        proceeds = position.shares * current_price * (1 - self.commission)
                        profit = position.close(current_price, date)
                        cash += proceeds
                        
                        # Record trade
                        result.trades.append({
                            'symbol': symbol,
                            'entry_date': position.entry_date,
                            'exit_date': date,
                            'entry_price': position.entry_price,
                            'exit_price': current_price,
                            'shares': position.shares,
                            'profit': profit,
                            'return_pct': (profit / (position.entry_price * position.shares)) * 100
                        })
                        
                        del positions[symbol]
                        logger.debug(f"Closed position: {position.shares} shares of {symbol} at {current_price:.2f}, profit: {profit:.2f}")
                
                # Calculate portfolio value
                position_value = sum(pos.shares * current_price for pos in positions.values())
                total_value = cash + position_value
                
                portfolio_history.append(total_value)
                result.dates.append(date)
                result.portfolio_value.append(total_value)
            
            # Close any remaining positions
            if positions:
                final_price = data['Close'].iloc[-1]
                final_date = data.index[-1]
                
                for symbol, position in positions.items():
                    proceeds = position.shares * final_price * (1 - self.commission)
                    profit = position.close(final_price, final_date)
                    cash += proceeds
                    
                    result.trades.append({
                        'symbol': symbol,
                        'entry_date': position.entry_date,
                        'exit_date': final_date,
                        'entry_price': position.entry_price,
                        'exit_price': final_price,
                        'shares': position.shares,
                        'profit': profit,
                        'return_pct': (profit / (position.entry_price * position.shares)) * 100
                    })
            
            result.final_capital = cash + sum(pos.shares * data['Close'].iloc[-1] for pos in positions.values())
            result.calculate_metrics()
            
            logger.info(f"Backtest completed. Total return: {result.total_return_pct:.2f}%")
            return result
            
        except Exception as e:
            logger.error(f"Error during backtesting: {e}")
            raise
    
    def _fetch_historical_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Fetch historical data for backtesting"""
        try:
            # Calculate period based on date range
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            days_diff = (end - start).days
            
            if days_diff <= 30:
                period = "1mo"
            elif days_diff <= 90:
                period = "3mo"
            elif days_diff <= 180:
                period = "6mo"
            elif days_diff <= 365:
                period = "1y"
            else:
                period = "2y"
            
            data = self.data_fetcher.get_stock_data(symbol, period=period, interval="1d")
            
            if data is not None:
                # Filter data to exact date range
                data = data.loc[start_date:end_date]
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return None
    
    def _generate_signals_for_date(self, symbol: str, data: pd.DataFrame) -> List[TradingSignal]:
        """Generate signals for a specific date (using only historical data)"""
        try:
            if len(data) < 50:  # Need enough data for technical indicators
                return []
            
            # Temporarily override the data fetcher to return our historical data
            original_get_stock_data = self.data_fetcher.get_stock_data
            self.data_fetcher.get_stock_data = lambda s, **kwargs: data if s == symbol else None
            
            signals = self.signal_generator.generate_signals(symbol)
            
            # Restore original method
            self.data_fetcher.get_stock_data = original_get_stock_data
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating signals for date: {e}")
            return []
    
    def run_multiple_symbol_backtest(self, symbols: List[str], start_date: str, 
                                   end_date: str, position_size: float = 0.1) -> Dict[str, BacktestResult]:
        """
        Run backtest for multiple symbols
        
        Args:
            symbols: List of stock symbols
            start_date: Start date for backtesting
            end_date: End date for backtesting
            position_size: Position size per symbol as fraction of portfolio
        
        Returns:
            Dictionary with symbol as key and BacktestResult as value
        """
        results = {}
        
        for symbol in symbols:
            try:
                result = self.run_backtest(symbol, start_date, end_date, position_size)
                results[symbol] = result
                logger.info(f"Completed backtest for {symbol}")
            except Exception as e:
                logger.error(f"Failed to backtest {symbol}: {e}")
        
        return results
    
    def print_results(self, result: BacktestResult, symbol: str):
        """Print backtest results"""
        print(f"\n{'='*50}")
        print(f"BACKTEST RESULTS FOR {symbol}")
        print(f"{'='*50}")
        print(f"Initial Capital: {result.initial_capital:,.2f} SAR")
        print(f"Final Capital: {result.final_capital:,.2f} SAR")
        print(f"Total Return: {result.total_return:,.2f} SAR ({result.total_return_pct:.2f}%)")
        print(f"Maximum Drawdown: {result.max_drawdown:.2f}%")
        print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
        print(f"Total Trades: {result.total_trades}")
        print(f"Profitable Trades: {result.profitable_trades}")
        print(f"Losing Trades: {result.losing_trades}")
        print(f"Win Rate: {result.win_rate:.1f}%")
        
        if result.trades:
            print(f"\nTRADE SUMMARY:")
            print(f"{'Date':<12} {'Type':<6} {'Price':<8} {'Shares':<8} {'Profit':<10} {'Return %':<8}")
            print("-" * 60)
            for trade in result.trades[-10:]:  # Show last 10 trades
                print(f"{trade['exit_date'].strftime('%Y-%m-%d'):<12} "
                      f"{'SELL':<6} "
                      f"{trade['exit_price']:<8.2f} "
                      f"{trade['shares']:<8} "
                      f"{trade['profit']:<10.2f} "
                      f"{trade['return_pct']:<8.2f}")

def main():
    """Main function for running backtests"""
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize backtester
    backtester = Backtester(initial_capital=100000, commission=0.001)
    
    # Popular Saudi stocks
    symbols = ["2222.SR", "1120.SR", "2030.SR"]
    
    # Backtest parameters
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    
    print("Starting backtesting for Saudi stocks...")
    
    for symbol in symbols:
        try:
            result = backtester.run_backtest(symbol, start_date, end_date, position_size=0.3)
            backtester.print_results(result, symbol)
        except Exception as e:
            print(f"Error backtesting {symbol}: {e}")

if __name__ == "__main__":
    main()
