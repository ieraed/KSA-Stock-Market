# Saudi Stock Market Trading Signals App

A comprehensive Python application for analyzing the Saudi stock market (Tadawul) and generating buy/sell trading signals using technical indicators.

![Saudi Stock Market](https://img.shields.io/badge/Market-Saudi%20Tadawul-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-Educational-yellow)

## 🌟 Features

### 📊 **Real-time Data Analysis**
- Live and historical data from Saudi stock market (Tadawul)
- Support for popular Saudi stocks including Aramco, Al Rajhi Bank, SABIC
- Market hours and trading day awareness
- Automatic data validation and cleaning

### 🎯 **Technical Analysis & Signals**
- **RSI (Relative Strength Index)**: Identify overbought/oversold conditions
- **MACD**: Trend-following momentum indicator with crossover signals
- **Bollinger Bands**: Volatility-based buy/sell signals
- **Moving Averages**: Golden/Death cross detection
- **Stochastic Oscillator**: Momentum-based signals
- **Williams %R**: Additional momentum confirmation
- **ATR (Average True Range)**: Volatility measurement

### 📈 **Signal Generation**
- Multi-indicator signal confirmation
- Confidence scoring for each signal
- Automated signal prioritization
- Real-time signal generation

### 🔙 **Backtesting Framework**
- Test strategies on historical data
- Performance metrics (Sharpe ratio, max drawdown, win rate)
- Multi-symbol backtesting support
- Detailed trade analysis

### 💻 **Interactive Web Dashboard**
- Real-time signal monitoring
- Interactive price charts with technical indicators
- Market status and trading hours display
- Customizable indicator parameters
- Mobile-responsive design

### 💼 **Portfolio Management**
- Track stock positions and cash balance
- Profit/loss calculations
- Transaction history
- Performance metrics

### 🔔 **Alert System**
- Email notifications for trading signals
- Console alerts
- Customizable alert conditions

## 🚀 Quick Start

### 1. Setup
```bash
# Clone or download the project
cd "Saudi Stock Market App"

# Run the setup script
python setup.py

# Or install manually:
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# API_KEY=your_api_key_here
# ALERT_EMAIL=your_email@example.com
```

### 3. Run Tests
```bash
# Test the installation
python test_app.py
```

### 4. Generate Signals
```bash
# Run signal generation
python run_signals.py
```

### 5. Start Dashboard
```bash
# Launch web dashboard
python run_dashboard.py
# Open http://localhost:8501 in your browser
```

## 📁 Project Structure

```
Saudi Stock Market App/
├── src/
│   ├── data/                 # Data fetching and management
│   │   ├── __init__.py
│   │   └── market_data.py    # Yahoo Finance integration
│   ├── analysis/             # Technical analysis
│   │   ├── __init__.py
│   │   └── technical_indicators.py
│   ├── signals/              # Signal generation
│   │   ├── __init__.py
│   │   └── signal_generator.py
│   ├── backtesting/          # Strategy backtesting
│   │   ├── __init__.py
│   │   └── backtest.py
│   ├── dashboard/            # Streamlit web app
│   │   ├── __init__.py
│   │   └── app.py
│   ├── utils/                # Utilities
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   ├── alerts.py         # Alert system
│   │   └── portfolio.py      # Portfolio tracking
│   └── main.py              # Main application
├── .github/
│   └── copilot-instructions.md  # AI coding guidelines
├── .vscode/
│   └── tasks.json           # VS Code tasks
├── requirements.txt         # Python dependencies
├── run_signals.py          # Signal generation script
├── run_dashboard.py        # Dashboard launcher
├── test_app.py            # Test suite
├── setup.py               # Setup script
├── .env.example           # Environment template
└── README.md              # This file
```

## 🏦 Supported Saudi Stocks

The app focuses on popular Saudi stocks including:

| Symbol | Company Name | Sector |
|--------|-------------|---------|
| 2222.SR | Saudi Aramco | Energy |
| 1120.SR | Al Rajhi Bank | Banking |
| 2030.SR | SABIC | Petrochemicals |
| 4030.SR | Riyad Bank | Banking |
| 1210.SR | The Saudi National Bank | Banking |
| 2020.SR | SABIC Agri-Nutrients | Chemicals |
| 1180.SR | Al Rajhi Takaful | Insurance |
| 2380.SR | Petrochemical Industries Co | Petrochemicals |

## 📊 Technical Indicators

### RSI (Relative Strength Index)
- **Purpose**: Identify overbought (>70) and oversold (<30) conditions
- **Signals**: Buy when RSI < 30, Sell when RSI > 70
- **Timeframe**: 14-period default

### MACD (Moving Average Convergence Divergence)
- **Purpose**: Trend and momentum analysis
- **Signals**: Bullish/bearish crossovers between MACD and signal line
- **Parameters**: 12/26/9 (Fast/Slow/Signal)

### Bollinger Bands
- **Purpose**: Volatility-based support/resistance
- **Signals**: Buy at lower band, sell at upper band
- **Parameters**: 20-period, 2 standard deviations

### Moving Averages
- **Purpose**: Trend identification
- **Signals**: Golden cross (bullish), Death cross (bearish)
- **Types**: SMA and EMA with customizable periods

## 🔧 Configuration

### Trading Parameters
Edit `src/utils/config.py` to customize:

```python
# RSI Settings
rsi_period = 14
rsi_oversold = 30.0
rsi_overbought = 70.0

# MACD Settings
macd_fast = 12
macd_slow = 26
macd_signal = 9

# Bollinger Bands
bb_period = 20
bb_std_dev = 2.0
```

### Environment Variables
Configure `.env` file:

```env
# Data API (optional)
API_KEY=your_api_key_here

# Email Alerts
ALERT_EMAIL=your_email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_username
SMTP_PASSWORD=your_password

# Database
DATABASE_URL=sqlite:///trading_signals.db
```

## 🕐 Saudi Market Information

- **Trading Hours**: 10:00 AM - 3:00 PM (Saudi Time, UTC+3)
- **Trading Days**: Sunday to Thursday
- **Currency**: SAR (Saudi Riyal)
- **Market**: Tadawul (Saudi Stock Exchange)
- **Index**: TASI (Tadawul All Share Index)

## 🔙 Backtesting

Run backtests to evaluate strategy performance:

```python
from src.backtesting.backtest import Backtester

# Initialize backtester
backtester = Backtester(initial_capital=100000)

# Run backtest
result = backtester.run_backtest(
    symbol="2222.SR",
    start_date="2023-01-01",
    end_date="2024-01-01"
)

# View results
backtester.print_results(result, "2222.SR")
```

## 📱 Web Dashboard

Access the interactive dashboard at `http://localhost:8501` after running `python run_dashboard.py`.

### Dashboard Features:
- **Live Signals**: Real-time buy/sell recommendations
- **Stock Analysis**: Interactive charts with technical indicators
- **Market Status**: Live market hours and status
- **Settings**: Customize indicator parameters
- **About**: Documentation and disclaimer

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_app.py
```

Tests include:
- Data fetching functionality
- Technical indicator calculations
- Signal generation
- Portfolio management
- Configuration loading

## 📋 Usage Examples

### Generate Signals
```python
from src.signals.signal_generator import SignalGenerator
from src.data.market_data import MarketDataFetcher
from src.utils.config import Config

config = Config()
data_fetcher = MarketDataFetcher(config)
signal_generator = SignalGenerator(data_fetcher, config)

# Generate signals for Saudi Aramco
signals = signal_generator.generate_signals("2222.SR")
for signal in signals:
    print(f"{signal.signal_type} {signal.symbol} at {signal.price:.2f} SAR")
```

### Portfolio Tracking
```python
from src.utils.portfolio import Portfolio

portfolio = Portfolio(initial_cash=100000)
portfolio.buy_stock("2222.SR", 100, 35.50)
portfolio.sell_stock("2222.SR", 50, 36.25)
portfolio.print_portfolio_summary()
```

## 🛠️ Development

### Adding New Indicators
1. Add the indicator function to `src/analysis/technical_indicators.py`
2. Update signal generation logic in `src/signals/signal_generator.py`
3. Add dashboard visualization in `src/dashboard/app.py`

### Custom Alert Conditions
Modify `src/utils/alerts.py` to add custom alert logic:

```python
def custom_alert_condition(signal):
    # Your custom logic here
    return signal.confidence > 0.8 and signal.signal_type == "BUY"
```

## 📚 Dependencies

### Core Dependencies
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **yfinance**: Yahoo Finance data
- **streamlit**: Web dashboard
- **plotly**: Interactive charts

### Optional Dependencies
- **ta-lib**: Additional technical indicators
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework

## ⚠️ Important Disclaimers

### Educational Purpose
This application is developed for **educational and learning purposes only**. It demonstrates:
- Technical analysis concepts
- Python financial programming
- Data visualization techniques
- Web application development

### Investment Warning
- **Not Financial Advice**: Signals generated are NOT financial advice
- **Risk Warning**: Trading involves substantial risk of loss
- **Research Required**: Always conduct your own research
- **Professional Advice**: Consult qualified financial advisors

### Data Disclaimer
- Market data provided by Yahoo Finance
- Data accuracy not guaranteed
- Real-time data may be delayed
- Historical data used for analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-indicator`)
3. Make your changes following the coding guidelines in `.github/copilot-instructions.md`
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

### Coding Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Write unit tests for new features
- Update README for new functionality

## 📄 License

This project is for educational and personal use only. Please ensure compliance with:
- All applicable financial regulations
- Terms of service for data providers
- Local investment laws and guidelines

## 🆘 Support & Issues

### Common Issues
1. **Import Errors**: Ensure all dependencies are installed
2. **Data Access**: Check internet connection and API limits
3. **TA-Lib Installation**: May require additional system dependencies

### Getting Help
- Check the test suite output for diagnostic information
- Review logs in `signals.log` for detailed error messages
- Ensure Python 3.8+ is installed
- Verify all dependencies are correctly installed

### Performance Tips
- Use appropriate data periods to balance accuracy and speed
- Cache frequently accessed data
- Run backtests during off-market hours
- Monitor memory usage with large datasets

---

**Happy Trading! 📈🇸🇦**

*Remember: This is for educational purposes only. Always do your own research and invest responsibly.*
