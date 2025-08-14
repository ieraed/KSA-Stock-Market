"""
Run signal generation for Saudi stocks
"""

import sys
import os
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

# Load environment variables
load_dotenv()

from data.market_data import MarketDataFetcher
from signals.signal_generator import SignalGenerator
from utils.config import Config

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('signals.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to run signal generation"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("[SA] Saudi Stock Market Trading Signals Generator")
    print("=" * 50)
    
    try:
        # Initialize components
        config = Config()
        data_fetcher = MarketDataFetcher(config)
        signal_generator = SignalGenerator(data_fetcher, config)
        
        # Popular Saudi stocks to analyze
        saudi_stocks = {
            "2222.SR": "Saudi Aramco",
            "1120.SR": "Al Rajhi Bank", 
            "2030.SR": "SABIC",
            "4030.SR": "Riyad Bank",
            "1210.SR": "The Saudi National Bank",
            "2020.SR": "SABIC Agri-Nutrients",
            "1180.SR": "Al Rajhi Takaful",
            "2380.SR": "Petrochemical Industries Co"
        }
        
        print(f"🔍 Analyzing {len(saudi_stocks)} Saudi stocks...")
        print(f"⏰ Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Check market status
        market_open = data_fetcher.is_market_open()
        market_status = "🟢 OPEN" if market_open else "🔴 CLOSED"
        print(f"📊 Market Status: {market_status}")
        print()
        
        all_signals = []
        
        # Generate signals for each stock
        for symbol, name in saudi_stocks.items():
            print(f"📈 Analyzing {name} ({symbol})...")
            
            try:
                signals = signal_generator.generate_signals(symbol)
                
                if signals:
                    print(f"✅ Found {len(signals)} signal(s) for {name}")
                    for signal in signals:
                        print(f"   🎯 {signal}")
                        all_signals.append(signal)
                else:
                    print(f"ℹ️  No signals generated for {name}")
                    
            except Exception as e:
                print(f"❌ Error analyzing {name}: {e}")
                logger.error(f"Error analyzing {symbol}: {e}")
            
            print()
        
        # Summary
        print("=" * 50)
        print("📋 SUMMARY")
        print("=" * 50)
        
        if all_signals:
            buy_signals = [s for s in all_signals if s.signal_type == "BUY"]
            sell_signals = [s for s in all_signals if s.signal_type == "SELL"]
            
            print(f"🟢 BUY signals: {len(buy_signals)}")
            print(f"🔴 SELL signals: {len(sell_signals)}")
            print(f"📊 Total signals: {len(all_signals)}")
            
            if buy_signals:
                print(f"\n🟢 BUY RECOMMENDATIONS:")
                for signal in sorted(buy_signals, key=lambda x: x.confidence, reverse=True):
                    print(f"   • {signal.symbol} at {signal.price:.2f} SAR (Confidence: {signal.confidence:.1%})")
                    print(f"     Reason: {signal.reason}")
            
            if sell_signals:
                print(f"\n🔴 SELL RECOMMENDATIONS:")
                for signal in sorted(sell_signals, key=lambda x: x.confidence, reverse=True):
                    print(f"   • {signal.symbol} at {signal.price:.2f} SAR (Confidence: {signal.confidence:.1%})")
                    print(f"     Reason: {signal.reason}")
        else:
            print("ℹ️  No trading signals generated at this time.")
        
        print(f"\n⚠️  DISCLAIMER: These signals are for educational purposes only.")
        print(f"   Always do your own research before making investment decisions.")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
