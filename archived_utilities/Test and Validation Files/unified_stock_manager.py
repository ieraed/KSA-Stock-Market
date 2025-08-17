"""
🇸🇦 Unified Saudi Stock Data Manager
Ensures all stock data comes from a single, authoritative source
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

class UnifiedSaudiStockManager:
    """
    Unified manager for Saudi stock data ensuring consistency across the application
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._cached_stocks = None
        self._last_update = None
        self._cache_duration = 300  # 5 minutes cache
        
    def get_unified_stock_database(self) -> Dict:
        """
        Get unified stock database from the most reliable source
        Priority: 1) Continuous fetcher latest data, 2) Corrected database, 3) Main database
        """
        
        # Check cache first
        if (self._cached_stocks and self._last_update and 
            (datetime.now() - self._last_update).seconds < self._cache_duration):
            return self._cached_stocks
        
        stocks_db = {}
        
        # Priority 1: Try continuous fetcher data
        try:
            from continuous_data_fetcher import ContinuousSaudiExchangeFetcher
            fetcher = ContinuousSaudiExchangeFetcher()
            
            # Check if we have recent data from the database
            latest_data = fetcher.get_latest_data()
            if latest_data and len(latest_data) > 200:  # Should have ~259 stocks
                self.logger.info(f"Using continuous fetcher data: {len(latest_data)} stocks")
                
                # Convert to our format
                for stock in latest_data:
                    symbol = stock.get('symbol', '').replace('.SR', '')
                    if symbol and symbol.isdigit():
                        stocks_db[symbol] = {
                            'symbol': symbol,
                            'name_en': stock.get('name', 'Unknown Company'),
                            'name_ar': stock.get('name_ar', ''),
                            'sector': stock.get('sector', 'Unknown'),
                            'current_price': stock.get('price', 0),
                            'change': stock.get('change', 0),
                            'change_percent': stock.get('change_percent', 0),
                            'last_updated': stock.get('timestamp', datetime.now().isoformat())
                        }
                
                if len(stocks_db) > 200:
                    self._cached_stocks = stocks_db
                    self._last_update = datetime.now()
                    return stocks_db
                    
        except Exception as e:
            self.logger.warning(f"Could not load continuous fetcher data: {e}")
        
        # Priority 2: Corrected database
        try:
            with open('saudi_stocks_database_corrected.json', 'r', encoding='utf-8') as f:
                corrected_db = json.load(f)
            
            if len(corrected_db) > 200:
                self.logger.info(f"Using corrected database: {len(corrected_db)} stocks")
                
                # Ensure consistent format
                for symbol, data in corrected_db.items():
                    if symbol not in stocks_db:  # Don't override continuous data
                        stocks_db[symbol] = {
                            'symbol': symbol,
                            'name_en': data.get('name_en', 'Unknown Company'),
                            'name_ar': data.get('name_ar', ''),
                            'sector': data.get('sector', 'Unknown'),
                            'current_price': data.get('current_price', 0),
                            'change': data.get('change', 0),
                            'change_percent': data.get('change_percent', 0),
                            'last_updated': data.get('last_updated', datetime.now().isoformat())
                        }
                
        except Exception as e:
            self.logger.warning(f"Could not load corrected database: {e}")
        
        # Priority 3: Main database as fallback
        try:
            with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
                main_db = json.load(f)
            
            self.logger.info(f"Using main database as fallback: {len(main_db)} stocks")
            
            for symbol, data in main_db.items():
                if symbol not in stocks_db:  # Don't override better data
                    stocks_db[symbol] = {
                        'symbol': symbol,
                        'name_en': data.get('name_en', 'Unknown Company'),
                        'name_ar': data.get('name_ar', ''),
                        'sector': data.get('sector', 'Unknown'),
                        'current_price': data.get('current_price', 0),
                        'change': data.get('change', 0),
                        'change_percent': data.get('change_percent', 0),
                        'last_updated': data.get('last_updated', datetime.now().isoformat())
                    }
                
        except Exception as e:
            self.logger.error(f"Could not load any database: {e}")
            # Return minimal fallback
            stocks_db = self._get_minimal_fallback()
        
        # Cache the result
        self._cached_stocks = stocks_db
        self._last_update = datetime.now()
        
        self.logger.info(f"Unified database loaded: {len(stocks_db)} stocks")
        return stocks_db
    
    def _get_minimal_fallback(self) -> Dict:
        """Minimal fallback database with correct data"""
        return {
            "1010": {
                "symbol": "1010",
                "name_en": "Saudi National Bank", 
                "name_ar": "البنك الأهلي السعودي",
                "sector": "Banking"
            },
            "1120": {
                "symbol": "1120", 
                "name_en": "Al Rajhi Bank",
                "name_ar": "مصرف الراجحي", 
                "sector": "Banking"
            },
            "2030": {
                "symbol": "2030",
                "name_en": "Saudi Arabian Oil Company",
                "name_ar": "أرامكو السعودية",
                "sector": "Energy"
            },
            "2010": {
                "symbol": "2010",
                "name_en": "Saudi Basic Industries Corporation",
                "name_ar": "سابك",
                "sector": "Materials"
            },
            "7010": {
                "symbol": "7010",
                "name_en": "Saudi Telecom Company", 
                "name_ar": "الاتصالات السعودية",
                "sector": "Telecommunication Services"
            }
        }
    
    def get_stock_info(self, symbol: str) -> Dict:
        """Get information for a specific stock"""
        stocks_db = self.get_unified_stock_database()
        return stocks_db.get(symbol, {
            'symbol': symbol,
            'name_en': 'Unknown Company',
            'name_ar': '',
            'sector': 'Unknown',
            'current_price': 0,
            'change': 0,
            'change_percent': 0,
            'last_updated': datetime.now().isoformat()
        })
    
    def get_stock_options_for_dropdown(self) -> List[tuple]:
        """Get formatted stock options for dropdown menus"""
        stocks_db = self.get_unified_stock_database()
        stock_options = []
        
        for symbol, data in stocks_db.items():
            name_en = data.get('name_en', 'Unknown Company')
            sector = data.get('sector', '')
            
            # Format: Symbol - Company Name (Sector)
            option_text = f"{symbol} - {name_en}"
            if sector and sector != 'Unknown':
                option_text += f" ({sector})"
            
            stock_options.append((option_text, symbol))
        
        stock_options.sort()  # Sort alphabetically
        return stock_options
    
    def validate_stock_data(self) -> Dict:
        """Validate stock data consistency and return validation report"""
        stocks_db = self.get_unified_stock_database()
        
        validation_report = {
            'total_stocks': len(stocks_db),
            'validation_time': datetime.now().isoformat(),
            'test_stocks': {},
            'issues': []
        }
        
        # Test specific stocks that were mentioned as problematic
        test_symbols = ['1010', '1120', '2030', '2010']
        
        for symbol in test_symbols:
            if symbol in stocks_db:
                stock_data = stocks_db[symbol]
                validation_report['test_stocks'][symbol] = {
                    'name_en': stock_data.get('name_en'),
                    'sector': stock_data.get('sector'),
                    'has_price': bool(stock_data.get('current_price', 0) > 0)
                }
            else:
                validation_report['issues'].append(f"Missing stock symbol: {symbol}")
        
        return validation_report
    
    def clear_cache(self):
        """Clear the internal cache to force fresh data load"""
        self._cached_stocks = None
        self._last_update = None
        self.logger.info("Stock data cache cleared")

# Global instance
unified_manager = UnifiedSaudiStockManager()

# Convenience functions for backward compatibility
def get_unified_stocks_database():
    """Get unified stock database"""
    return unified_manager.get_unified_stock_database()

def get_stock_info(symbol):
    """Get stock information"""
    return unified_manager.get_stock_info(symbol)

def get_stock_options():
    """Get stock options for dropdown"""
    return unified_manager.get_stock_options_for_dropdown()

def validate_stock_data():
    """Validate stock data"""
    return unified_manager.validate_stock_data()
