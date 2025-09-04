"""
Corrected Market Summary Processor Based on Historical Working Code
Uses pandas DataFrame approach that was proven to work correctly
"""

import pandas as pd
import numpy as np
import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CorrectedMarketProcessor:
    """
    Market processor based on the old working implementation
    Uses pandas DataFrame operations for reliable sorting
    """
    
    def __init__(self):
        self.official_stock_count = 259  # Official TASI count as of July 2024
        logger.info(f"📊 Official TASI stock count: {self.official_stock_count}")
    
    def get_market_summary(self, stocks_data: Dict) -> Optional[Dict]:
        """
        Get market summary with top gainers and losers
        Based on the exact working historical implementation
        """
        try:
            if not stocks_data:
                return self._get_mock_market_data()
            
            # Convert to DataFrame for analysis (exactly like old code)
            df = pd.DataFrame.from_dict(stocks_data, orient='index')
            
            logger.info(f"📊 Processing {len(df)} stocks with DataFrame")
            
            # Ensure we have the required columns
            required_columns = ['current_price', 'change_percent']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logger.warning(f"Missing columns: {missing_columns}")
                return self._get_mock_market_data()
            
            # Add change column if missing (like old code)
            if 'change' not in df.columns:
                # Calculate actual change from percentage
                df['change'] = df['current_price'] * (df['change_percent'] / 100)
            
            # Rename change_percent to change_pct for consistency with old code
            if 'change_pct' not in df.columns and 'change_percent' in df.columns:
                df['change_pct'] = df['change_percent']
            
            # Calculate percentage change if not available (from old code)
            if 'change_pct' not in df.columns:
                df['change_pct'] = (df['change'] / (df['current_price'] - df['change'])) * 100
            
            logger.info(f"📈 DataFrame ready with columns: {df.columns.tolist()}")
            
            # Get top gainers and losers using pandas (EXACT old code approach)
            top_gainers = df.nlargest(10, 'change_pct')
            top_losers = df.nsmallest(10, 'change_pct')
            
            logger.info(f"📊 Found {len(top_gainers)} gainers, {len(top_losers)} losers")
            
            # Validate results
            self._validate_results(top_gainers, top_losers)
            
            return {
                'top_gainers': top_gainers.to_dict('records'),
                'top_losers': top_losers.to_dict('records'),
                'total_stocks': self.official_stock_count,
                'active_stocks': len(df),
                'last_updated': datetime.now().isoformat(),
                'method': 'pandas_corrected',
                'processing_stats': {
                    'input_stocks': len(stocks_data),
                    'processed_stocks': len(df),
                    'gainers_found': len(top_gainers),
                    'losers_found': len(top_losers)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting market summary: {e}")
            return self._get_mock_market_data()
    
    def _validate_results(self, gainers_df: pd.DataFrame, losers_df: pd.DataFrame):
        """Validate that sorting worked correctly"""
        
        # Check gainers
        for idx, row in gainers_df.iterrows():
            change_pct = row.get('change_pct', row.get('change_percent', 0))
            if change_pct < 0:
                logger.error(f"❌ VALIDATION ERROR: Negative gainer found: {row.get('symbol')} ({change_pct:.2f}%)")
            else:
                logger.debug(f"✅ Valid gainer: {row.get('symbol')} (+{change_pct:.2f}%)")
        
        # Check losers
        for idx, row in losers_df.iterrows():
            change_pct = row.get('change_pct', row.get('change_percent', 0))
            if change_pct > 0:
                logger.error(f"❌ VALIDATION ERROR: Positive loser found: {row.get('symbol')} (+{change_pct:.2f}%)")
            else:
                logger.debug(f"✅ Valid loser: {row.get('symbol')} ({change_pct:.2f}%)")
    
    def _get_mock_market_data(self):
        """Generate mock market data for demonstration (from old code)"""
        
        logger.info("📊 Returning mock market data")
        
        # Sample stocks with proper sorting
        sample_stocks = [
            {"symbol": "2222", "name": "Saudi Aramco", "current_price": 37.50, "change_pct": 2.1},
            {"symbol": "1120", "name": "Al Rajhi Bank", "current_price": 85.20, "change_pct": 1.8},
            {"symbol": "4013", "name": "Dr. Sulaiman Al Habib", "current_price": 150.20, "change_pct": 3.2},
            {"symbol": "4161", "name": "Bindawood", "current_price": 75.30, "change_pct": 1.5},
            {"symbol": "7010", "name": "STC", "current_price": 120.50, "change_pct": 0.9},
            {"symbol": "1010", "name": "Saudi National Bank", "current_price": 65.80, "change_pct": -0.5},
            {"symbol": "2380", "name": "SABIC", "current_price": 89.40, "change_pct": -1.2},
            {"symbol": "2280", "name": "Almarai", "current_price": 45.60, "change_pct": -2.1},
            {"symbol": "1810", "name": "Seera Group", "current_price": 32.10, "change_pct": -3.4},
            {"symbol": "4160", "name": "Thimar", "current_price": 28.90, "change_pct": 4.1}
        ]
        
        # Sort by change percentage (like old code)
        gainers = sorted([s for s in sample_stocks if s['change_pct'] > 0], 
                        key=lambda x: x['change_pct'], reverse=True)
        losers = sorted([s for s in sample_stocks if s['change_pct'] < 0], 
                       key=lambda x: x['change_pct'])
        
        return {
            'top_gainers': gainers,
            'top_losers': losers,
            'total_stocks': self.official_stock_count,
            'active_stocks': len(sample_stocks),
            'last_updated': datetime.now().isoformat(),
            'method': 'mock_data',
            'processing_stats': {
                'input_stocks': len(sample_stocks),
                'processed_stocks': len(sample_stocks),
                'gainers_found': len(gainers),
                'losers_found': len(losers)
            }
        }

# Test function
def test_corrected_processor():
    """Test the corrected processor with sample data"""
    
    processor = CorrectedMarketProcessor()
    
    # Sample data in the format our fetcher returns
    sample_data = {
        "2222.SR": {
            "symbol": "2222",
            "name": "Saudi Aramco",
            "current_price": 37.50,
            "change_percent": 2.1,
            "volume": 1000000
        },
        "1120.SR": {
            "symbol": "1120", 
            "name": "Al Rajhi Bank",
            "current_price": 85.20,
            "change_percent": -1.8,  # Negative to test sorting
            "volume": 500000
        },
        "4013.SR": {
            "symbol": "4013",
            "name": "Dr. Sulaiman Al Habib", 
            "current_price": 150.20,
            "change_percent": 3.2,
            "volume": 200000
        },
        "2380.SR": {
            "symbol": "2380",
            "name": "SABIC",
            "current_price": 89.40,
            "change_percent": -2.1,  # Negative to test sorting
            "volume": 800000
        }
    }
    
    print("🧪 Testing Corrected Market Processor...")
    
    summary = processor.get_market_summary(sample_data)
    
    if summary:
        print(f"✅ Method: {summary['method']}")
        print(f"📊 Total stocks: {summary['total_stocks']}")
        print(f"📈 Active stocks: {summary['active_stocks']}")
        
        print(f"\n🏆 Top Gainers ({len(summary['top_gainers'])}):")
        for i, stock in enumerate(summary['top_gainers'], 1):
            change_pct = stock.get('change_pct', stock.get('change_percent', 0))
            print(f"  {i}. {stock['symbol']}: {change_pct:+.2f}%")
            if change_pct < 0:
                print(f"    ❌ ERROR: Negative value in gainers!")
        
        print(f"\n📉 Top Losers ({len(summary['top_losers'])}):")
        for i, stock in enumerate(summary['top_losers'], 1):
            change_pct = stock.get('change_pct', stock.get('change_percent', 0))
            print(f"  {i}. {stock['symbol']}: {change_pct:+.2f}%")
            if change_pct > 0:
                print(f"    ❌ ERROR: Positive value in losers!")
    
    return summary

if __name__ == "__main__":
    test_corrected_processor()
