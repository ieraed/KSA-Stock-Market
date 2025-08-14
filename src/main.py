"""
Saudi Stock Market Trading Signals App
Main entry point for the application
"""

import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.append(str(src_path))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_signals.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    logger.info("Starting Saudi Stock Market Trading Signals App")
    
    try:
        from .signals.signal_generator import SignalGenerator
        from .data.market_data import MarketDataFetcher
        from .utils.config import Config
        
        # Initialize configuration
        config = Config()
        
        # Initialize data fetcher
        data_fetcher = MarketDataFetcher(config)
        
        # Initialize signal generator
        signal_generator = SignalGenerator(data_fetcher, config)
        
        # Generate signals for popular Saudi stocks
        popular_stocks = [
            "2222.SR",  # Saudi Aramco
            "1120.SR",  # Al Rajhi Bank
            "2030.SR",  # SABIC
            "4030.SR",  # Riyad Bank
            "1210.SR",  # The Saudi National Bank
        ]
        
        logger.info(f"Generating signals for {len(popular_stocks)} stocks")
        
        for symbol in popular_stocks:
            try:
                signals = signal_generator.generate_signals(symbol)
                if signals:
                    logger.info(f"Generated {len(signals)} signals for {symbol}")
                    for signal in signals:
                        logger.info(f"Signal: {signal}")
            except Exception as e:
                logger.error(f"Error generating signals for {symbol}: {e}")
        
        logger.info("Signal generation completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
