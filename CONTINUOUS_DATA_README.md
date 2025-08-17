# 🇸🇦 TADAWUL NEXUS - Continuous Data Fetching System

## 📊 Real-time Saudi Stock Market Data

This system provides continuous, real-time data fetching from the Saudi Stock Exchange (Tadawul) website. It automatically updates your stock database with the latest prices, changes, and market information.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install beautifulsoup4 aiohttp pandas plotly streamlit
```

### 2. Test the System
```bash
python quick_start.py
```

### 3. Run the Enhanced App
```bash
streamlit run enhanced_saudi_app_realtime.py
```

## 📁 System Components

### Core Files
- `continuous_data_fetcher.py` - Main continuous fetching engine
- `saudi_data_integration.py` - Integration with existing application
- `enhanced_saudi_app_realtime.py` - Enhanced Streamlit app with real-time data
- `quick_start.py` - Simple test and demo script
- `test_continuous_fetcher.py` - Comprehensive testing script

### Configuration
- `config/fetcher_config.json` - System configuration settings

### Data Storage
- `saudi_stocks_continuous.db` - SQLite database for historical data
- `saudi_stocks_database.json` - Main JSON database (updated automatically)
- `backup/` - Automatic backups of database files

## 🎯 Key Features

### Real-time Data Fetching
- ✅ Fetches data every 30 seconds (configurable)
- ✅ Parses stock prices, changes, and percentages
- ✅ Handles network errors with automatic retry
- ✅ Validates data integrity

### Data Management
- ✅ SQLite database for historical storage
- ✅ JSON export for application compatibility
- ✅ Automatic backups
- ✅ Data freshness validation

### Market Analysis
- ✅ Top gainers and losers tracking
- ✅ Market statistics and summaries
- ✅ Price change distribution analysis
- ✅ Market status detection (open/closed)

### Integration
- ✅ Seamless integration with existing app
- ✅ Backward compatibility
- ✅ Real-time dashboard updates
- ✅ Export capabilities (JSON, CSV)

## 🔧 Configuration

Edit `config/fetcher_config.json` to customize:

```json
{
  "continuous_fetching": {
    "enabled": true,
    "update_interval": 30,
    "max_retries": 3
  },
  "saudi_exchange": {
    "target_url": "https://www.saudiexchange.sa/wps/portal/saudiexchange/ourmarkets/main-market-watch/theoritical-market-watch-today?locale=en"
  },
  "market_hours": {
    "trading_days": [0, 1, 2, 3, 4],
    "open_time": "10:00",
    "close_time": "15:00"
  }
}
```

## 💻 Usage Examples

### Basic Usage
```python
from saudi_data_integration import get_data_manager

# Get the data manager
manager = get_data_manager()

# Get all stocks
stocks = manager.get_latest_stocks()
print(f"Retrieved {len(stocks)} stocks")

# Get market summary
summary = manager.get_market_summary()
print(f"Gainers: {summary['gainers']}, Losers: {summary['losers']}")

# Get top movers
movers = manager.get_top_movers(10)
print("Top gainers:", movers['gainers'][:3])
```

### Advanced Usage
```python
from continuous_data_fetcher import ContinuousSaudiExchangeFetcher

# Create custom fetcher
fetcher = ContinuousSaudiExchangeFetcher(update_interval=60)

# Add custom callback
def my_callback(stocks):
    print(f"Received update: {len(stocks)} stocks")
    # Your custom logic here

fetcher.add_callback(my_callback)

# Start fetching
fetcher.start_continuous_fetching()

# Get specific stock
stock = fetcher.get_stock("2030")  # SARCO
if stock:
    print(f"{stock.name}: {stock.price} SAR ({stock.change_percent:+.2f}%)")
```

## 📊 Data Format

The system provides data in the following format:

### Stock Data Object
```python
{
    "symbol": "2030.SR",
    "name_en": "SARCO",
    "name_ar": "سارك",
    "price": 56.95,
    "change": 0.10,
    "change_percent": 0.18,
    "volume": 0,
    "market_cap": 0,
    "last_update": "2025-08-16T14:30:00",
    "currency": "SAR"
}
```

### Market Summary
```python
{
    "total_stocks": 259,
    "gainers": 142,
    "losers": 87,
    "unchanged": 30,
    "avg_change": 0.25,
    "max_gain": 8.50,
    "max_loss": -5.20,
    "market_status": "open"
}
```

## 🔄 Integration with Existing App

The system automatically integrates with your existing Saudi stock market app:

1. **Database Updates**: Automatically updates `saudi_stocks_database.json`
2. **Backward Compatibility**: Existing code continues to work
3. **Enhanced Features**: New real-time capabilities added
4. **Data Preservation**: Existing metadata (sectors, etc.) preserved

## 📈 Market Hours

The system respects Saudi market trading hours:
- **Trading Days**: Sunday to Thursday
- **Trading Hours**: 10:00 AM to 3:00 PM (Riyadh time)
- **Market Status**: Automatically detected

## 🛡️ Error Handling

The system includes robust error handling:
- **Network Errors**: Automatic retry with exponential backoff
- **Data Validation**: Ensures data integrity
- **Graceful Degradation**: Falls back to cached data if needed
- **Logging**: Comprehensive logging for debugging

## 📊 Monitoring and Logging

### Log Files
- `saudi_exchange_fetcher.log` - Main application log
- Database logs stored in SQLite for analysis

### Monitoring
```python
# Check data freshness
manager = get_data_manager()
is_fresh = manager.is_data_fresh(max_age_minutes=5)

# Get statistics
stats = manager.fetcher.get_statistics()
print(f"Last update: {stats['last_update']}")
```

## 🔧 Troubleshooting

### Common Issues

1. **No Data Retrieved**
   - Check network connectivity
   - Verify Saudi Exchange website is accessible
   - Check firewall/proxy settings

2. **Import Errors**
   ```bash
   pip install beautifulsoup4 aiohttp pandas
   ```

3. **Database Issues**
   - Check file permissions
   - Ensure disk space available
   - Verify database integrity

4. **Performance Issues**
   - Increase update interval
   - Reduce number of stocks tracked
   - Optimize database queries

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Advanced Features

### Custom Data Sources
You can extend the system to fetch from multiple sources:

```python
# Add backup URL
fetcher.backup_urls = [
    "https://alternative-source.com/api",
    "https://backup-source.com/data"
]
```

### Real-time Alerts
```python
def price_alert(stocks):
    for stock in stocks.values():
        if abs(stock.change_percent) > 5:
            print(f"ALERT: {stock.name} moved {stock.change_percent:.2f}%")

fetcher.add_callback(price_alert)
```

### Data Export
```python
# Export to various formats
fetcher.export_to_json("market_data.json")
manager.export_current_data("csv")
```

## 🎯 Performance Optimization

### Recommended Settings
- **Update Interval**: 30-60 seconds for real-time needs
- **Max Retries**: 3-5 for reliability
- **Database Cleanup**: Run weekly to maintain performance

### Memory Management
The system automatically manages memory by:
- Limiting historical data retention
- Efficient data structures
- Garbage collection of old records

## 📞 Support

For issues or questions:
1. Check the log files for error messages
2. Run `quick_start.py` to test the system
3. Verify network connectivity to Saudi Exchange
4. Check system requirements and dependencies

## 📄 License

This system is part of the TADAWUL NEXUS Saudi Stock Market Trading Application.

---

**🇸🇦 Built for the Saudi Stock Market - TADAWUL NEXUS**
