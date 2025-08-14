"""
Fix encoding issues for signal generation
"""

import sys
import os

# Set UTF-8 encodinSg for Windows
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
# Add current directory to path for imports
sys.path.append(os.path.join(os.getcwd(), 'src'))

from signals.signal_generator import SignalGenerator
from data.market_data import MarketDataFetcher
from utils.config import Config

def test_signal_generation():
    """Test signal generation with proper encoding"""
    try:
        print("🔄 Testing signal generation...")
        
        config = Config()
        data_fetcher = MarketDataFetcher(config)
        signal_generator = SignalGenerator(data_fetcher, config)
        
        # Test with one stock
        test_symbol = "2222.SR"  # Aramco
        print(f"📊 Analyzing {test_symbol}...")
        
        signals = signal_generator.generate_signals(test_symbol)
        
        if signals:
            print(f"✅ Generated {len(signals)} signals!")
            for signal in signals:
                print(f"📈 {signal}")
        else:
            print("⚠️ No signals generated")
            
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_signal_generation()
