# Saudi Stock Market Portfolio Manager - App Description

## 🎯 **Project Overview**
A clean, focused **Saudi Stock Market Portfolio Management Application** built with Python and Streamlit. The app helps users manage their Saudi stock investments with real-time data, comprehensive stock database, and Excel integration.

## 🏗️ **Current Architecture**

### **Core Components:**
1. **`saudi_portfolio_manager.py`** - Main Streamlit application (Port 8800)
2. **`saudi_stocks_database.json`** - Comprehensive Saudi stock database (80+ stocks)
3. **`saudi_stocks_fetcher.py`** - Stock data fetcher and database creator
4. **`saudi_stock_database.py`** - Database utility functions

### **Supporting Files:**
- **`portfolio_template.xlsx`** - Excel template for bulk uploads
- **`user_portfolio.json`** - User portfolio data storage
- **`requirements.txt`** - Python dependencies
- **`run_dashboard.py`** & **`run_signals.py`** - App runners

## 🌟 **Key Features**

### **1. Stock Database Integration**
- **700+ Saudi stocks** from Tadawul (Saudi Stock Exchange)
- Includes major companies: Aramco (2030), SABIC (2010), Al Rajhi Bank (1120)
- **Sectors covered**: Banking, Energy, Petrochemicals, Healthcare, Materials, etc.
- **Dual language support**: English and Arabic company names

### **2. Portfolio Management**
- **Manual stock entry** with auto-complete from database
- **Excel upload/download** functionality with predefined template
- **Real-time price fetching** via yfinance API
- **Portfolio metrics**: Total value, gains/losses, percentage changes

### **3. Stock Search & Discovery**
- **Search by symbol**: e.g., "2030" → Aramco
- **Search by company name**: e.g., "SABIC" → 2010.SR
- **Browse by sector**: Banking, Energy, Petrochemicals, etc.
- **Auto-fill company information** when adding stocks

### **4. User Interface**
- **Clean Streamlit dashboard** 
- **Responsive design** with sidebar navigation
- **Real-time data updates**
- **Excel integration** for bulk operations

## 🛠️ **Technical Stack**

### **Backend:**
- **Python 3.8+**
- **Streamlit** - Web framework
- **pandas** - Data manipulation
- **yfinance** - Real-time stock data
- **JSON** - Database storage

### **Frontend:**
- **Streamlit UI** - Interactive web interface
- **Plotly** - Charts and visualizations (ready for expansion)

### **Data Sources:**
- **yfinance API** - Real-time Saudi stock prices (.SR suffix)
- **Custom JSON database** - Saudi stock metadata
- **Excel templates** - Bulk data import/export

## 📊 **Saudi Stock Database Structure**
```json
{
  "1120": {
    "symbol": "1120.SR",
    "name_en": "Al Rajhi Bank",
    "name_ar": "مصرف الراجحي",
    "sector": "Banking"
  },
  "2030": {
    "symbol": "2030.SR", 
    "name_en": "Saudi Arabian Oil Co (Aramco)",
    "name_ar": "أرامكو السعودية",
    "sector": "Energy"
  }
}
```

## 🎮 **User Workflow**

### **1. Portfolio Creation:**
- Launch app: `streamlit run saudi_portfolio_manager.py --server.port 8800`
- Search for Saudi stocks using company name or ticker
- Add stocks manually or upload Excel template
- View real-time portfolio performance

### **2. Stock Discovery:**
- Use integrated stock search to find companies
- Browse by sector (Banking, Energy, etc.)
- Auto-complete helps find correct tickers

### **3. Data Management:**
- Download portfolio as Excel file
- Upload bulk changes via Excel template
- Real-time price updates from yfinance

## 🚀 **Deployment Status**
- ✅ **Core functionality** working
- ✅ **Stock database** populated with 80+ Saudi stocks
- ✅ **Excel integration** functional
- ✅ **Real-time data** fetching operational
- ✅ **Clean workspace** - removed old platform files

## 🎯 **Next Development Goals**
1. **Enhanced analytics** - Technical indicators, charts
2. **Portfolio optimization** - Risk analysis, sector allocation
3. **Trading signals** - Buy/sell recommendations
4. **Mobile responsiveness** - Better mobile UI
5. **Multi-user support** - User accounts and authentication

## 🛡️ **Saudi Market Specifics**
- **Trading hours**: Sunday-Thursday, 10:00 AM - 3:00 PM (Saudi time)
- **Currency**: SAR (Saudi Riyal)
- **Market index**: TASI (Tadawul All Share Index)
- **Stock format**: 4-digit codes + .SR suffix (e.g., 2030.SR)

## 📁 **Essential Files to Keep After Cleanup**
```
📁 .venv/ (Python environment)
📁 .git/ (version control)
📁 .github/ (GitHub settings)
📁 .vscode/ (VS Code settings)
📄 .env.example
📄 portfolio_template.xlsx
📄 README.md
📄 requirements.txt
📄 run_dashboard.py
📄 run_signals.py
📄 saudi_portfolio_manager.py ← MAIN APP
📄 saudi_stocks_database.json ← STOCK DATABASE
📄 saudi_stocks_fetcher.py ← STOCK FETCHER
📄 saudi_stock_database.py ← DATABASE FUNCTIONS
📄 user_portfolio.json
📄 APP_DESCRIPTION.md ← THIS FILE
```

## 🔄 **How to Start Fresh Chat**
1. Delete old/unnecessary files as listed above
2. Keep only essential files (12-15 files total)
3. Share this APP_DESCRIPTION.md in new chat
4. Continue development with clean context

---

**Status**: Ready for enhancement in new chat! 🇸🇦📈

**Last Updated**: August 16, 2025
**Version**: Clean Portfolio Manager v1.0
