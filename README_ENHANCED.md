# 🇸🇦 Enhanced Saudi Stock Market App

A complete **Portfolio Management + AI Trading Platform** specifically designed for the Saudi Stock Exchange (Tadawul). This app combines user-friendly portfolio management with cutting-edge AI features to help you make better investment decisions.

## 🌟 Key Features

### 📈 Portfolio Management
- **Real-time Saudi stock data** from Tadawul
- **Add/Remove stocks** with automatic price updates
- **Portfolio tracking** with profit/loss calculations
- **Visual analytics** with charts and metrics
- **Excel import/export** for bulk operations

### 🤖 AI Trading Features
- **AI-powered signals** (BUY/SELL/HOLD recommendations)
- **Confidence scores** for each prediction
- **Risk assessment** (LOW/MEDIUM/HIGH)
- **Technical analysis** with RSI, moving averages, momentum
- **Smart reasoning** explaining each AI decision

### 🔍 Stock Discovery
- **Comprehensive database** of 30+ major Saudi stocks
- **Search by company name** or stock symbol
- **Filter by sector** (Banking, Energy, Petrochemicals, etc.)
- **Both English and Arabic** company names
- **Real-time price information**

### 📊 Advanced Analytics
- **Interactive price charts** with Plotly
- **Technical indicators** (SMA, RSI, etc.)
- **Portfolio allocation** pie charts
- **Performance metrics** and trend analysis

## 🚀 Quick Start

### 1. Complete Setup (Recommended)
```bash
python complete_setup.py
```
This will automatically:
- Install all dependencies
- Create the Saudi stocks database
- Set up a sample portfolio
- Test everything works

### 2. Launch the App
```bash
python launch_enhanced_app.py
```
Or manually:
```bash
streamlit run enhanced_saudi_app.py
```

### 3. Open in Browser
The app will open at: **http://localhost:8501**

## 📋 Manual Installation

If you prefer to install manually:

### Install Dependencies
```bash
pip install streamlit pandas numpy yfinance plotly openpyxl xlsxwriter scikit-learn
```

### Run the App
```bash
streamlit run enhanced_saudi_app.py --server.port 8501
```

## 🎯 How to Use

### Portfolio Management
1. **Add Stocks**: Go to "➕ Add Stocks" → Search for Saudi companies → Add to portfolio
2. **View Portfolio**: "🏠 Portfolio Overview" shows your holdings, profits/losses, and metrics
3. **Import/Export**: Use "📁 Import/Export" for Excel file operations

### AI Trading Signals
1. **Generate Signals**: Go to "🤖 AI Signals" → Click "Generate AI Signals"
2. **Review Recommendations**: AI analyzes technical indicators and provides BUY/SELL/HOLD signals
3. **Check Confidence**: Each signal includes confidence level and risk assessment
4. **Read Reasoning**: Understand why AI made each recommendation

### Stock Research
1. **Search Stocks**: Use "🔍 Stock Search" to explore available Saudi stocks
2. **Filter by Sector**: Find stocks in Banking, Energy, Petrochemicals, etc.
3. **View Analytics**: "📊 Analytics" provides detailed charts and technical analysis

## 🏗️ App Structure

```
enhanced_saudi_app.py          # Main Streamlit application
ai_engine/
  └── simple_ai.py            # AI trading engine
saudi_stocks_database.json    # Saudi stocks database
user_portfolio.json          # Your portfolio data
complete_setup.py            # Automated setup script
launch_enhanced_app.py       # App launcher
requirements_enhanced.txt    # Dependencies list
```

## 📊 Saudi Stocks Database

The app includes major Saudi stocks:

**Banking**: Al Rajhi Bank (1120), Saudi National Bank (1010), Banque Saudi Fransi (1150)
**Energy**: Saudi Aramco (2030), Saudi Electricity (2040)
**Petrochemicals**: SABIC (2010), Petrochemical Industries (2380)
**Telecommunications**: STC (7040), Mobily (7020)
**And many more...**

## 🤖 AI Features Explained

### Technical Analysis
- **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
- **Moving Averages**: Short-term (20-day) and long-term (50-day) trends
- **Price Momentum**: 5-day and 20-day price changes
- **Volume Analysis**: Unusual trading volume detection

### AI Decision Logic
- **BUY Signal**: Strong upward trend + oversold conditions + high volume
- **SELL Signal**: Downward trend + overbought conditions + negative momentum  
- **HOLD Signal**: Mixed signals or insufficient data
- **Confidence**: Based on agreement between multiple indicators
- **Risk Assessment**: Volatility-based risk scoring

## 💡 Pro Tips

### Portfolio Management
- **Diversify**: Add stocks from different sectors
- **Regular Updates**: Check portfolio daily for price changes
- **Use Excel**: Export portfolio for external analysis
- **Track Performance**: Monitor profit/loss percentages

### AI Trading
- **High Confidence**: Signals >70% confidence are more reliable
- **Consider Risk**: Balance high-return potential with risk level
- **Multiple Signals**: Wait for consistent signals over time
- **Do Your Research**: AI complements but doesn't replace fundamental analysis

## 🛠️ Troubleshooting

### App Won't Start
```bash
# Check if all dependencies are installed
pip list | grep streamlit

# Reinstall if needed
pip install --upgrade streamlit pandas numpy yfinance plotly
```

### No AI Signals
```bash
# Install AI dependencies
pip install scikit-learn

# Check if yfinance can fetch data
python -c "import yfinance; print(yfinance.Ticker('2030.SR').history(period='1mo'))"
```

### Database Missing
```bash
# Run setup again
python complete_setup.py
```

## 🔄 Updates and Enhancements

This app is designed to be easily extensible. Future enhancements could include:

- **More AI Models**: LSTM neural networks, ensemble methods
- **Real-time Alerts**: Push notifications for signal changes
- **Advanced Charts**: Candlestick charts, technical overlays
- **Portfolio Optimization**: AI-powered allocation recommendations
- **News Integration**: Arabic news sentiment analysis
- **Mobile App**: React Native or Flutter mobile version

## 📈 Saudi Market Information

**Trading Hours**: Sunday - Thursday, 10:00 AM - 3:00 PM (Saudi Time)
**Currency**: Saudi Riyal (SAR)
**Market Index**: TASI (Tadawul All Share Index)
**Stock Format**: 4-digit codes + .SR suffix (e.g., 2030.SR for Aramco)

## 🤝 Support

For questions or issues:
1. Check this README first
2. Run `python complete_setup.py` to reset everything
3. Ensure you have stable internet for real-time data
4. Verify you're in the correct directory with all files

## 🎉 Ready to Start Trading!

Your Enhanced Saudi Stock Market App is ready to help you:
- **Manage your portfolio** professionally
- **Get AI-powered insights** for better decisions  
- **Track Saudi stocks** in real-time
- **Make data-driven investments** in Tadawul

**Launch the app now and start exploring! 🚀📈**
