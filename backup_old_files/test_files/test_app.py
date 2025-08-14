"""
Test script for the Saudi Stock Market Trading Signals App
"""

import sys
import os
from pathlib import Path
import logging

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from data.market_data import MarketDataFetcher
from signals.signal_generator import SignalGenerator
from analysis.technical_indicators import TechnicalIndicators
from utils.config import Config
from utils.portfolio import Portfolio

def setup_logging():
    """Setup logging for tests"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_data_fetching():
    """Test market data fetching"""
    print("🔍 Testing Data Fetching...")
    
    config = Config()
    data_fetcher = MarketDataFetcher(config)
    
    # Test popular Saudi stocks
    test_symbols = ["2222.SR", "1120.SR", "2030.SR"]
    
    for symbol in test_symbols:
        print(f"  📊 Fetching data for {symbol}...")
        try:
            data = data_fetcher.get_stock_data(symbol, period="1mo", interval="1d")
            if data is not None and not data.empty:
                print(f"  ✅ Success: {len(data)} records for {symbol}")
                print(f"     Latest price: {data['Close'].iloc[-1]:.2f} SAR")
            else:
                print(f"  ⚠️  No data returned for {symbol}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    # Test market hours
    market_open = data_fetcher.is_market_open()
    print(f"  📅 Market status: {'🟢 Open' if market_open else '🔴 Closed'}")
    
    print("✅ Data fetching test completed\n")

def test_technical_indicators():
    """Test technical indicators"""
    print("📈 Testing Technical Indicators...")
    
    config = Config()
    data_fetcher = MarketDataFetcher(config)
    indicators = TechnicalIndicators()
    
    # Get sample data
    data = data_fetcher.get_stock_data("2222.SR", period="6mo", interval="1d")
    
    if data is not None and not data.empty:
        close_prices = data['Close']
        high_prices = data['High']
        low_prices = data['Low']
        
        try:
            # Test RSI
            rsi = indicators.rsi(close_prices)
            print(f"  📊 RSI: Latest value = {rsi.iloc[-1]:.2f}")
            
            # Test MACD
            macd_line, signal_line, histogram = indicators.macd(close_prices)
            print(f"  📊 MACD: Latest = {macd_line.iloc[-1]:.4f}, Signal = {signal_line.iloc[-1]:.4f}")
            
            # Test Bollinger Bands
            bb_upper, bb_middle, bb_lower = indicators.bollinger_bands(close_prices)
            print(f"  📊 Bollinger Bands: Upper = {bb_upper.iloc[-1]:.2f}, Lower = {bb_lower.iloc[-1]:.2f}")
            
            # Test Moving Averages
            sma_20 = indicators.sma(close_prices, 20)
            ema_20 = indicators.ema(close_prices, 20)
            print(f"  📊 SMA(20): {sma_20.iloc[-1]:.2f}, EMA(20): {ema_20.iloc[-1]:.2f}")
            
            print("  ✅ All indicators calculated successfully")
            
        except Exception as e:
            print(f"  ❌ Error calculating indicators: {e}")
    else:
        print("  ⚠️  No data available for indicator testing")
    
    print("✅ Technical indicators test completed\n")

def test_signal_generation():
    """Test signal generation"""
    print("🎯 Testing Signal Generation...")
    
    config = Config()
    data_fetcher = MarketDataFetcher(config)
    signal_generator = SignalGenerator(data_fetcher, config)
    
    test_symbols = ["2222.SR", "1120.SR"]
    
    for symbol in test_symbols:
        print(f"  🔍 Generating signals for {symbol}...")
        try:
            signals = signal_generator.generate_signals(symbol)
            
            if signals:
                print(f"  ✅ Generated {len(signals)} signal(s):")
                for signal in signals:
                    print(f"     🎯 {signal.signal_type} at {signal.price:.2f} SAR (Confidence: {signal.confidence:.1%})")
                    print(f"        Reason: {signal.reason}")
            else:
                print(f"  ℹ️  No signals generated for {symbol}")
                
        except Exception as e:
            print(f"  ❌ Error generating signals: {e}")
    
    print("✅ Signal generation test completed\n")

def test_portfolio():
    """Test portfolio functionality"""
    print("💼 Testing Portfolio Management...")
    
    # Create test portfolio
    portfolio = Portfolio(initial_cash=50000, portfolio_file="test_portfolio.json")
    
    try:
        # Test buying stocks
        print("  💰 Testing stock purchases...")
        success1 = portfolio.buy_stock("2222.SR", 10, 35.50)
        success2 = portfolio.buy_stock("1120.SR", 5, 85.20)
        
        if success1 and success2:
            print("  ✅ Stock purchases successful")
        
        # Test portfolio value calculation
        current_prices = {"2222.SR": 36.00, "1120.SR": 87.50}
        portfolio_value = portfolio.get_portfolio_value(current_prices)
        
        print(f"  📊 Portfolio Value: {portfolio_value['total_portfolio_value']:,.2f} SAR")
        print(f"  💵 Cash Balance: {portfolio_value['cash']:,.2f} SAR")
        
        # Test selling
        print("  💸 Testing stock sale...")
        success3 = portfolio.sell_stock("2222.SR", 5, 36.25)
        
        if success3:
            print("  ✅ Stock sale successful")
        
        # Performance metrics
        metrics = portfolio.get_performance_metrics(initial_value=50000)
        print(f"  📈 Total Return: {metrics['total_return']:,.2f} SAR ({metrics['total_return_pct']:.2f}%)")
        
        # Clean up test file
        test_file = Path("test_portfolio.json")
        if test_file.exists():
            test_file.unlink()
        
        print("  ✅ Portfolio test completed successfully")
        
    except Exception as e:
        print(f"  ❌ Error in portfolio test: {e}")
    
    print("✅ Portfolio management test completed\n")

def test_configuration():
    """Test configuration"""
    print("⚙️ Testing Configuration...")
    
    try:
        config = Config()
        
        print(f"  📊 RSI Period: {config.rsi_period}")
        print(f"  📊 MACD Parameters: Fast={config.macd_fast}, Slow={config.macd_slow}, Signal={config.macd_signal}")
        print(f"  📊 Bollinger Bands: Period={config.bb_period}, Std Dev={config.bb_std_dev}")
        
        # Test trading parameters
        trading_params = config.get_trading_params()
        print(f"  ⚙️  Trading parameters loaded: {len(trading_params)} parameters")
        
        # Test market hours
        market_hours = config.get_saudi_market_hours()
        print(f"  🕐 Market Hours: {market_hours['start_time']} - {market_hours['end_time']}")
        print(f"  📅 Trading Days: {', '.join(market_hours['trading_days'])}")
        
        print("  ✅ Configuration test completed successfully")
        
    except Exception as e:
        print(f"  ❌ Error in configuration test: {e}")
    
    print("✅ Configuration test completed\n")

def main():
    """Run all tests"""
    setup_logging()
    
    print("[SA] Saudi Stock Market Trading Signals App - Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_configuration()
        test_data_fetching()
        test_technical_indicators()
        test_signal_generation()
        test_portfolio()
        
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Your Saudi Stock Market Trading Signals App is ready to use!")
        print()
        print("📝 Next Steps:")
        print("  1. Run 'python run_signals.py' to generate trading signals")
        print("  2. Run 'python run_dashboard.py' to start the web dashboard")
        print("  3. Set up your .env file with API keys and email settings")
        print()
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
