"""
🇸🇦 Continuous Saudi Exchange Real-time Data Fetcher
Fetches live stock data continuously from saudiexchange.sa theoretical market watch
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import re
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Tuple
import threading
from concurrent.futures import ThreadPoolExecutor
import sqlite3
from dataclasses import dataclass
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('saudi_exchange_fetcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class StockData:
    """Stock data structure"""
    symbol: str
    name: str
    price: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class ContinuousSaudiExchangeFetcher:
    """Continuous real-time Saudi Exchange data fetcher"""
    
    def __init__(self, update_interval: int = 30, max_retries: int = 3):
        """
        Initialize the continuous fetcher
        
        Args:
            update_interval: Time between updates in seconds (default: 30s)
            max_retries: Maximum retries for failed requests
        """
        self.base_url = "https://www.saudiexchange.sa"
        self.target_url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch/theoritical-market-watch-today?locale=en"
        self.update_interval = update_interval
        self.max_retries = max_retries
        self.is_running = False
        self._stop_event = threading.Event()
        
        # Data storage
        self.latest_data: Dict[str, StockData] = {}
        self.data_history: List[Dict[str, StockData]] = []
        self.callbacks: List[callable] = []
        
        # Database setup
        self.db_path = "saudi_stocks_continuous.db"
        self._setup_database()
        
        # Request session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })
        
        logger.info(f"🚀 Continuous Saudi Exchange Fetcher initialized")
        logger.info(f"📊 Target URL: {self.target_url}")
        logger.info(f"⏱️ Update interval: {update_interval} seconds")
    
    def _setup_database(self):
        """Setup SQLite database for storing historical data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stock_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    name TEXT,
                    price REAL,
                    change_value REAL,
                    change_percent REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX(symbol),
                    INDEX(timestamp)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fetch_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    stocks_count INTEGER,
                    success BOOLEAN,
                    error_message TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("✅ Database setup completed")
            
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
    
    def parse_stock_data(self, html_content: str) -> Dict[str, StockData]:
        """
        Parse stock data from HTML content
        
        Args:
            html_content: Raw HTML content from the website
            
        Returns:
            Dictionary of stock symbol -> StockData
        """
        stocks = {}
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find table rows with stock data
            # The website uses table format: | Symbol | Name | Price | Change | Change% |
            table_rows = soup.find_all('tr')
            
            for row in table_rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    try:
                        # Extract data from cells
                        if len(cells) >= 5:
                            symbol_text = cells[0].get_text(strip=True)
                            name_text = cells[1].get_text(strip=True)
                            price_text = cells[2].get_text(strip=True)
                            change_text = cells[3].get_text(strip=True)
                            change_percent_text = cells[4].get_text(strip=True) if len(cells) > 4 else ""
                            
                            # Clean and validate symbol
                            symbol = symbol_text.strip()
                            if not symbol or not symbol.isdigit():
                                continue
                                
                            # Clean and parse price
                            price_clean = re.sub(r'[^\d\.]', '', price_text)
                            if not price_clean:
                                continue
                            price = float(price_clean)
                            
                            # Parse change value
                            change = None
                            if change_text and change_text != '-':
                                change_clean = re.sub(r'[^\d\.\-\+]', '', change_text)
                                if change_clean:
                                    change = float(change_clean)
                            
                            # Parse change percentage
                            change_percent = None
                            if change_percent_text and '%' in change_percent_text:
                                percent_clean = re.sub(r'[^\d\.\-\+]', '', change_percent_text)
                                if percent_clean:
                                    change_percent = float(percent_clean)
                            
                            # Create stock data object
                            stock_data = StockData(
                                symbol=symbol,
                                name=name_text.strip(),
                                price=price,
                                change=change,
                                change_percent=change_percent,
                                timestamp=datetime.now()
                            )
                            
                            stocks[symbol] = stock_data
                            
                    except (ValueError, IndexError) as e:
                        continue  # Skip malformed rows
            
            # Alternative parsing method using regex for better data extraction
            if not stocks:
                stocks = self._parse_with_regex(html_content)
                        
        except Exception as e:
            logger.error(f"❌ Error parsing stock data: {e}")
            
        return stocks
    
    def _parse_with_regex(self, html_content: str) -> Dict[str, StockData]:
        """Alternative parsing method using regex patterns"""
        stocks = {}
        
        try:
            # Look for patterns like: | 2030 | SARCO | 56.95 | - | - |
            pattern = r'\|\s*(\d{4})\s*\|\s*([^|]+?)\s*\|\s*([\d\.]+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|'
            matches = re.findall(pattern, html_content)
            
            for match in matches:
                symbol, name, price_str, change_str, change_percent_str = match
                
                try:
                    price = float(price_str.strip())
                    
                    # Parse change
                    change = None
                    if change_str.strip() != '-' and change_str.strip():
                        change_clean = re.sub(r'[^\d\.\-\+]', '', change_str)
                        if change_clean:
                            change = float(change_clean)
                    
                    # Parse change percent
                    change_percent = None
                    if change_percent_str.strip() != '-' and '%' in change_percent_str:
                        percent_clean = re.sub(r'[^\d\.\-\+]', '', change_percent_str)
                        if percent_clean:
                            change_percent = float(percent_clean)
                    
                    stock_data = StockData(
                        symbol=symbol.strip(),
                        name=name.strip(),
                        price=price,
                        change=change,
                        change_percent=change_percent,
                        timestamp=datetime.now()
                    )
                    
                    stocks[symbol] = stock_data
                    
                except ValueError:
                    continue
                    
        except Exception as e:
            logger.error(f"❌ Regex parsing error: {e}")
            
        return stocks
    
    def fetch_current_data(self) -> Optional[Dict[str, StockData]]:
        """
        Fetch current stock data from the website
        
        Returns:
            Dictionary of stock data or None if failed
        """
        for attempt in range(self.max_retries):
            try:
                logger.info(f"📡 Fetching data from Saudi Exchange (attempt {attempt + 1}/{self.max_retries})")
                
                response = self.session.get(self.target_url, timeout=30)
                response.raise_for_status()
                
                stocks = self.parse_stock_data(response.text)
                
                if stocks:
                    logger.info(f"✅ Successfully fetched {len(stocks)} stocks")
                    self._log_fetch_success(len(stocks))
                    return stocks
                else:
                    logger.warning("⚠️ No stock data found in response")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Request failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)  # Wait before retry
                    
            except Exception as e:
                logger.error(f"❌ Unexpected error (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
        
        self._log_fetch_failure("Max retries exceeded")
        return None
    
    def _log_fetch_success(self, stocks_count: int):
        """Log successful fetch to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fetch_logs (stocks_count, success) VALUES (?, ?)",
                (stocks_count, True)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Failed to log success: {e}")
    
    def _log_fetch_failure(self, error_message: str):
        """Log failed fetch to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO fetch_logs (stocks_count, success, error_message) VALUES (?, ?, ?)",
                (0, False, error_message)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"❌ Failed to log failure: {e}")
    
    def save_to_database(self, stocks: Dict[str, StockData]):
        """Save stock data to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for stock in stocks.values():
                cursor.execute('''
                    INSERT INTO stock_data (symbol, name, price, change_value, change_percent, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    stock.symbol,
                    stock.name,
                    stock.price,
                    stock.change,
                    stock.change_percent,
                    stock.timestamp
                ))
            
            conn.commit()
            conn.close()
            logger.info(f"💾 Saved {len(stocks)} stocks to database")
            
        except Exception as e:
            logger.error(f"❌ Database save failed: {e}")
    
    def add_callback(self, callback: callable):
        """Add a callback function to be called when new data is available"""
        self.callbacks.append(callback)
        logger.info(f"📞 Added callback: {callback.__name__}")
    
    def _notify_callbacks(self, stocks: Dict[str, StockData]):
        """Notify all registered callbacks of new data"""
        for callback in self.callbacks:
            try:
                callback(stocks)
            except Exception as e:
                logger.error(f"❌ Callback {callback.__name__} failed: {e}")
    
    def start_continuous_fetching(self):
        """Start continuous fetching in a background thread"""
        if self.is_running:
            logger.warning("⚠️ Fetcher is already running")
            return
        
        self.is_running = True
        self._stop_event.clear()
        
        def fetch_loop():
            logger.info("🚀 Starting continuous data fetching...")
            
            while not self._stop_event.is_set():
                try:
                    # Fetch current data
                    stocks = self.fetch_current_data()
                    
                    if stocks:
                        # Update latest data
                        self.latest_data = stocks
                        
                        # Add to history (keep last 100 updates)
                        self.data_history.append(stocks.copy())
                        if len(self.data_history) > 100:
                            self.data_history.pop(0)
                        
                        # Save to database
                        self.save_to_database(stocks)
                        
                        # Notify callbacks
                        self._notify_callbacks(stocks)
                        
                        logger.info(f"📊 Updated {len(stocks)} stocks at {datetime.now().strftime('%H:%M:%S')}")
                    
                    # Wait for next update
                    self._stop_event.wait(self.update_interval)
                    
                except Exception as e:
                    logger.error(f"❌ Error in fetch loop: {e}")
                    self._stop_event.wait(10)  # Wait 10 seconds before retry
            
            logger.info("🛑 Continuous fetching stopped")
        
        # Start in background thread
        self.fetch_thread = threading.Thread(target=fetch_loop, daemon=True)
        self.fetch_thread.start()
        
        logger.info("✅ Continuous fetching started")
    
    def stop_continuous_fetching(self):
        """Stop continuous fetching"""
        if not self.is_running:
            logger.warning("⚠️ Fetcher is not running")
            return
        
        self.is_running = False
        self._stop_event.set()
        
        # Wait for thread to finish
        if hasattr(self, 'fetch_thread'):
            self.fetch_thread.join(timeout=5)
        
        logger.info("🛑 Continuous fetching stopped")
    
    def get_latest_data(self) -> Dict[str, StockData]:
        """Get the latest fetched data"""
        return self.latest_data.copy()
    
    def get_stock(self, symbol: str) -> Optional[StockData]:
        """Get data for a specific stock symbol"""
        return self.latest_data.get(symbol)
    
    def get_stocks_by_change(self, min_change_percent: float = None) -> List[StockData]:
        """Get stocks filtered by change percentage"""
        stocks = []
        for stock in self.latest_data.values():
            if stock.change_percent is not None:
                if min_change_percent is None or stock.change_percent >= min_change_percent:
                    stocks.append(stock)
        
        return sorted(stocks, key=lambda x: x.change_percent or 0, reverse=True)
    
    def get_top_gainers(self, limit: int = 10) -> List[StockData]:
        """Get top gaining stocks"""
        gainers = [s for s in self.latest_data.values() if s.change_percent and s.change_percent > 0]
        return sorted(gainers, key=lambda x: x.change_percent, reverse=True)[:limit]
    
    def get_top_losers(self, limit: int = 10) -> List[StockData]:
        """Get top losing stocks"""
        losers = [s for s in self.latest_data.values() if s.change_percent and s.change_percent < 0]
        return sorted(losers, key=lambda x: x.change_percent)[:limit]
    
    def export_to_json(self, filename: str = None) -> str:
        """Export latest data to JSON file"""
        if filename is None:
            filename = f"saudi_stocks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'stocks_count': len(self.latest_data),
            'stocks': {
                symbol: {
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'price': stock.price,
                    'change': stock.change,
                    'change_percent': stock.change_percent,
                    'timestamp': stock.timestamp.isoformat()
                }
                for symbol, stock in self.latest_data.items()
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Exported {len(self.latest_data)} stocks to {filename}")
        return filename
    
    def get_statistics(self) -> Dict:
        """Get statistics about the current data"""
        if not self.latest_data:
            return {}
        
        prices = [s.price for s in self.latest_data.values()]
        changes = [s.change_percent for s in self.latest_data.values() if s.change_percent is not None]
        
        positive_changes = [c for c in changes if c > 0]
        negative_changes = [c for c in changes if c < 0]
        
        return {
            'total_stocks': len(self.latest_data),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'min_price': min(prices) if prices else 0,
            'max_price': max(prices) if prices else 0,
            'gainers_count': len(positive_changes),
            'losers_count': len(negative_changes),
            'unchanged_count': len(self.latest_data) - len(positive_changes) - len(negative_changes),
            'avg_change_percent': sum(changes) / len(changes) if changes else 0,
            'max_gain': max(changes) if changes else 0,
            'max_loss': min(changes) if changes else 0,
            'last_update': max([s.timestamp for s in self.latest_data.values()]).isoformat() if self.latest_data else None
        }

def main():
    """Example usage of the continuous fetcher"""
    
    def on_data_update(stocks: Dict[str, StockData]):
        """Callback function for data updates"""
        print(f"📊 Received update: {len(stocks)} stocks at {datetime.now().strftime('%H:%M:%S')}")
        
        # Print top 5 gainers
        gainers = sorted([s for s in stocks.values() if s.change_percent and s.change_percent > 0], 
                        key=lambda x: x.change_percent, reverse=True)[:5]
        
        if gainers:
            print("🔥 Top 5 Gainers:")
            for stock in gainers:
                print(f"  {stock.symbol} ({stock.name}): {stock.price} SAR (+{stock.change_percent:.2f}%)")
    
    # Create fetcher
    fetcher = ContinuousSaudiExchangeFetcher(update_interval=60)  # Update every minute
    
    # Add callback
    fetcher.add_callback(on_data_update)
    
    try:
        # Start continuous fetching
        fetcher.start_continuous_fetching()
        
        # Run for demo (in production, this would run indefinitely)
        time.sleep(300)  # Run for 5 minutes
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping fetcher...")
    finally:
        fetcher.stop_continuous_fetching()
        
        # Export final data
        filename = fetcher.export_to_json()
        print(f"📄 Final data exported to: {filename}")
        
        # Print statistics
        stats = fetcher.get_statistics()
        print("📈 Final Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
