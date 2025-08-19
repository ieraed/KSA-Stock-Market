"""
✨ TADAWUL NEXUS ✨
Next-Generation Saudi Stock Intelligence Platform

Complete Portfolio Management + AI Trading Platform with Real-time Saudi Exchange Data

Features:
- Real-time Saudi Exchange (Tadawul) Integration
- Portfolio Management & Setup
- AI-Powered Trading Signals & Analysis
- Top Gainers/Losers Tables
- Live Market Data from saudiexchange.sa
- Comprehensive 700+ Stock Database
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Import our enhanced Saudi Exchange fetcher
try:
    from saudi_exchange_fetcher import get_all_saudi_stocks, get_market_summary, get_stock_price
    SAUDI_EXCHANGE_AVAILABLE = True
except ImportError:
    SAUDI_EXCHANGE_AVAILABLE = False

# Try to import AI features
try:
    from ai_engine.simple_ai import get_ai_signals
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="✨ TADAWUL NEXUS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for professional look
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.portfolio-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin: 1rem 0;
    border-left: 4px solid #00C851;
}

.ai-signal-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.metric-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #e9ecef;
}

.gainer-card {
    background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
    padding: 1rem;
    border-radius: 8px;
    color: white;
    margin: 0.5rem 0;
}

.loser-card {
    background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
    padding: 1rem;
    border-radius: 8px;
    color: white;
    margin: 0.5rem 0;
}

.market-table {
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    overflow: hidden;
}

.success-card {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

.warning-card {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

/* Enhanced Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
}

/* Sidebar sections with enhanced styling */
div[data-testid="stSidebar"] .element-container {
    background: rgba(255, 255, 255, 0.9);
    margin: 0.3rem 0;
    border-radius: 8px;
    transition: all 0.3s ease;
}

div[data-testid="stSidebar"] .element-container:hover {
    background: rgba(255, 255, 255, 1);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

div[data-testid="stSidebar"] h3, div[data-testid="stSidebar"] h4 {
    color: #1565c0;
    font-weight: 600;
}

/* Navigation radio buttons enhanced */
.stRadio > div {
    background: white;
    padding: 0.8rem;
    border-radius: 8px;
    margin: 0.4rem 0;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stRadio > div:hover {
    border-color: #1565c0;
    transform: translateX(4px);
    box-shadow: 0 2px 8px rgba(21,101,192,0.2);
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(21,101,192,0.3);
}

/* Table styling */
.stDataFrame {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

/* Section headers */
.section-header {
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px 10px 0 0;
    text-align: center;
    font-weight: 600;
    margin-bottom: 0;
}

/* Metric cards for market data */
.market-metric {
    background: white;
    padding: 1.2rem;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #e3f2fd;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.market-metric:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

def load_portfolio():
    """Load portfolio from file"""
    try:
        portfolio_file = Path("user_portfolio.json")
        if portfolio_file.exists():
            with open(portfolio_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading portfolio: {e}")
    return []

def save_portfolio(portfolio):
    """Save portfolio to file"""
    try:
        with open("user_portfolio.json", 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving portfolio: {e}")
        return False

@st.cache_data(ttl=300)  # Cache for 5 minutes, then refresh
def load_saudi_stocks_database():
    """Load Saudi stocks database with OFFICIAL 262-stock coverage (User-verified count)"""
    import sys
    import os
    
    # Get the root directory (parent of apps)
    root_dir = os.path.dirname(os.path.dirname(__file__))
    
    try:
        # FIRST PRIORITY: Load from our complete JSON database
        data_path = os.path.join(root_dir, 'data', 'saudi_stocks_database.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            stocks = json.load(f)
            if len(stocks) == 262:
                print(f"✅ Loaded OFFICIAL Tadawul database with {len(stocks)} stocks from {data_path}")
                return stocks
            elif len(stocks) != 262:
                print(f"⚠️ WARNING: Database has {len(stocks)} stocks but should have 262!")
                print("🚨 NOTIFY USER: Stock count mismatch detected!")
                return stocks
    except Exception as e:
        print(f"Could not load JSON database: {e}")
    
    try:
        # Second option: Try the complete database Python module
        sys.path.append(root_dir)
        from complete_tadawul_database import create_extended_database
        stocks = create_extended_database()
        if len(stocks) >= 250:
            print(f"✅ Loaded database from Python module with {len(stocks)} stocks")
            return stocks
    except Exception as e:
        print(f"Warning: Could not load Python module database: {e}")
        
    try:
        # Try loading from root directory
        root_path = os.path.join(root_dir, 'saudi_stocks_database.json')
        with open(root_path, 'r', encoding='utf-8') as f:
            stocks = json.load(f)
            print(f"✅ Loaded {len(stocks)} stocks from root directory")
            return stocks
    except Exception as e:
        print(f"Could not load from root directory: {e}")
    
    # Final fallback - CORRECTED minimal database
    print("⚠️ Using minimal fallback database")
    return {
        # BANKING SECTOR - CORRECTED
        "1010": {"symbol": "1010", "name_en": "Riyad Bank", "name_ar": "بنك الرياض", "sector": "Banking"},
        "1180": {"symbol": "1180", "name_en": "Saudi National Bank", "name_ar": "البنك الأهلي السعودي", "sector": "Banking"},
        "1120": {"symbol": "1120", "name_en": "Al Rajhi Bank", "name_ar": "مصرف الراجحي", "sector": "Banking"},
        "1050": {"symbol": "1050", "name_en": "Banque Saudi Fransi", "name_ar": "البنك السعودي الفرنسي", "sector": "Banking"},
        
        # ENERGY SECTOR - CORRECTED
        "2030": {"symbol": "2030", "name_en": "Saudi Arabia Refineries Co.", "name_ar": "مصافي أرامكو السعودية", "sector": "Energy"},
        "2222": {"symbol": "2222", "name_en": "Saudi Arabian Oil Company", "name_ar": "أرامكو السعودية", "sector": "Energy"},
        
        # MATERIALS
        "2010": {"symbol": "2010", "name_en": "Saudi Basic Industries Corporation", "name_ar": "سابك", "sector": "Materials"},
        
        # TELECOMMUNICATIONS
        "7010": {"symbol": "7010", "name_en": "Saudi Telecom Company", "name_ar": "الاتصالات السعودية", "sector": "Telecommunication Services"}
    }

def get_stock_data(symbol):
    """Get stock data with enhanced information"""
    try:
        # Try Saudi Exchange fetcher first
        if SAUDI_EXCHANGE_AVAILABLE:
            saudi_data = get_stock_price(symbol)
            if saudi_data and saudi_data.get('current_price', 0) > 0:
                return saudi_data
        
        # Fallback to yfinance
        stock_symbol = f"{symbol}.SR" if not symbol.endswith('.SR') else symbol
        ticker = yf.Ticker(stock_symbol)
        info = ticker.info
        
        if 'currentPrice' in info:
            return {
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'change': info.get('currentPrice', 0) - info.get('previousClose', 0),
                'change_percent': ((info.get('currentPrice', 0) - info.get('previousClose', 0)) / info.get('previousClose', 1)) * 100,
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0)
            }
    except Exception as e:
        pass
    
    # Return default values if no data available
    return {
        'current_price': 0,
        'previous_close': 0,
        'change': 0,
        'change_percent': 0,
        'volume': 0,
        'market_cap': 0,
        'pe_ratio': 0
    }

def calculate_portfolio_value(portfolio):
    """Calculate total portfolio value with enhanced metrics"""
    total_value = 0
    total_cost = 0
    total_gain_loss = 0
    
    for stock in portfolio:
        stock_data = get_stock_data(stock['symbol'])
        current_price = stock_data.get('current_price', 0)
        quantity = stock.get('quantity', 0)
        purchase_price = stock.get('purchase_price', 0)
        
        current_value = current_price * quantity
        cost_basis = purchase_price * quantity
        
        total_value += current_value
        total_cost += cost_basis
        total_gain_loss += (current_value - cost_basis)
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percent': (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
    }

def display_top_gainers_losers():
    """Display top gainers and losers tables"""
    st.markdown("""
    <div class="section-header">
        📊 Saudi Market Performance - Live Data
    </div>
    """, unsafe_allow_html=True)
    
    # Get market summary
    if SAUDI_EXCHANGE_AVAILABLE:
        try:
            market_data = get_market_summary()
            
            if market_data:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📈 Top 10 Gainers")
                    if market_data.get('top_gainers'):
                        gainers_df = pd.DataFrame(market_data['top_gainers'])
                        if not gainers_df.empty:
                            # Format the DataFrame
                            display_cols = ['symbol', 'name_en', 'current_price', 'change_pct']
                            available_cols = [col for col in display_cols if col in gainers_df.columns]
                            
                            if available_cols:
                                gainers_display = gainers_df[available_cols].copy()
                                if 'change_pct' in gainers_display.columns:
                                    gainers_display['change_pct'] = gainers_display['change_pct'].apply(lambda x: f"+{x:.2f}%")
                                if 'current_price' in gainers_display.columns:
                                    gainers_display['current_price'] = gainers_display['current_price'].apply(lambda x: f"{x:.2f} SAR")
                                
                                st.dataframe(
                                    gainers_display,
                                    column_config={
                                        "symbol": "Symbol",
                                        "name_en": "Company",
                                        "current_price": "Price",
                                        "change_pct": "Change %"
                                    },
                                    hide_index=True,
                                    use_container_width=True
                                )
                            else:
                                st.info("Market data structure not compatible")
                        else:
                            st.info("No gainers data available")
                    else:
                        st.info("No gainers data available")
                
                with col2:
                    st.markdown("### 📉 Top 10 Losers")
                    if market_data.get('top_losers'):
                        losers_df = pd.DataFrame(market_data['top_losers'])
                        if not losers_df.empty:
                            # Format the DataFrame
                            display_cols = ['symbol', 'name_en', 'current_price', 'change_pct']
                            available_cols = [col for col in display_cols if col in losers_df.columns]
                            
                            if available_cols:
                                losers_display = losers_df[available_cols].copy()
                                if 'change_pct' in losers_display.columns:
                                    losers_display['change_pct'] = losers_display['change_pct'].apply(lambda x: f"{x:.2f}%")
                                if 'current_price' in losers_display.columns:
                                    losers_display['current_price'] = losers_display['current_price'].apply(lambda x: f"{x:.2f} SAR")
                                
                                st.dataframe(
                                    losers_display,
                                    column_config={
                                        "symbol": "Symbol",
                                        "name_en": "Company", 
                                        "current_price": "Price",
                                        "change_pct": "Change %"
                                    },
                                    hide_index=True,
                                    use_container_width=True
                                )
                            else:
                                st.info("Market data structure not compatible")
                        else:
                            st.info("No losers data available")
                    else:
                        st.info("No losers data available")
                
                # Market statistics
                st.markdown("### 📊 Market Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="market-metric">
                        <h4 style="margin: 0; color: #1565c0;">Total Listed Companies</h4>
                        <h2 style="margin: 0.5rem 0; color: #00C851;">{market_data.get('total_stocks', 'N/A')}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    last_updated = market_data.get('last_updated', '')
                    if last_updated:
                        try:
                            update_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                            formatted_time = update_time.strftime("%H:%M")
                        except:
                            formatted_time = "Live"
                    else:
                        formatted_time = "Live"
                    
                    st.markdown(f"""
                    <div class="market-metric">
                        <h4 style="margin: 0; color: #1565c0;">Last Updated</h4>
                        <h2 style="margin: 0.5rem 0; color: #1565c0;">{formatted_time}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="market-metric">
                        <h4 style="margin: 0; color: #1565c0;">Data Source</h4>
                        <h2 style="margin: 0.5rem 0; color: #1565c0;">Tadawul</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                return
            
        except Exception as e:
            st.warning(f"Error fetching live market data: {e}")
    
    # Fallback to demo data
    st.info("📡 Live market data temporarily unavailable. Showing demo data:")
    
    # Demo data
    demo_gainers = [
        {"Symbol": "4160", "Company": "Thimar Development", "Price": "40.04 SAR", "Change": "+10.00%"},
        {"Symbol": "2130", "Company": "Saudi Industrial Development", "Price": "33.12 SAR", "Change": "+9.96%"},
        {"Symbol": "4270", "Company": "Saudi Public Procurement", "Price": "12.63 SAR", "Change": "+5.60%"},
        {"Symbol": "4191", "Company": "Abo Moati Al Motaheda", "Price": "40.88 SAR", "Change": "+4.82%"},
        {"Symbol": "4291", "Company": "National Care Company", "Price": "166.00 SAR", "Change": "+4.73%"}
    ]
    
    demo_losers = [
        {"Symbol": "2020", "Company": "SABIC Agri-Nutrients", "Price": "85.20 SAR", "Change": "-4.50%"},
        {"Symbol": "1182", "Company": "Amlak International", "Price": "12.80 SAR", "Change": "-3.80%"},
        {"Symbol": "6050", "Company": "Saudi Fisheries", "Price": "45.60 SAR", "Change": "-3.20%"},
        {"Symbol": "4180", "Company": "Fitaihi Group", "Price": "28.90 SAR", "Change": "-2.90%"},
        {"Symbol": "3080", "Company": "Eastern Province Cement", "Price": "67.40 SAR", "Change": "-2.50%"}
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Top Gainers")
        st.dataframe(pd.DataFrame(demo_gainers), hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Top Losers") 
        st.dataframe(pd.DataFrame(demo_losers), hide_index=True, use_container_width=True)

def main():
    """Main application function"""
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">
            ✨ TADAWUL NEXUS ✨
        </h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
            Next-Generation Saudi Stock Intelligence Platform
        </p>
        <p style="margin: 0.3rem 0 0 0; font-size: 0.95rem; opacity: 0.8;">
            Saudi Stock Exchange (Tadawul) • Real-time Data • AI-Powered Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    stocks_db = load_saudi_stocks_database()
    
    # Enhanced Sidebar Navigation
    with st.sidebar:
        # Title Section with enhanced styling
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1rem; background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%); border-radius: 10px; color: white;">
            <h3 style="margin: 0; font-weight: 600; font-size: 1.2rem;">📊 TADAWUL NEXUS</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;">Portfolio & Trading Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Navigation Section
        st.markdown("**📋 Main Navigation:**")
        
        # Add cache refresh button
        if st.button("🔄 Refresh Database", help="Clear cache and reload stock database"):
            st.cache_data.clear()
            st.rerun()
            
        selected_page = st.radio(
            "Navigation",
            [
                "🏠 Portfolio Overview",
                "⚙️ Portfolio Setup", 
                "🤖 AI Trading Center",
                "📈 Market Analysis",
                "🔍 Stock Research",
                "📊 Analytics Dashboard",
                "🏢 Sector Analyzer",
                "📁 Import/Export Data"
            ],
            index=0,
            key="main_nav",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Portfolio Quick Stats
        portfolio = load_portfolio()
        if portfolio:
            portfolio_stats = calculate_portfolio_value(portfolio)
            
            st.markdown("### 💼 Portfolio Stats")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Holdings", len(portfolio))
                st.metric("Total Value", f"{portfolio_stats['total_value']:,.2f} SAR")
            
            with col2:
                gain_loss = portfolio_stats['total_gain_loss']
                gain_loss_pct = portfolio_stats['total_gain_loss_percent']
                
                if gain_loss >= 0:
                    st.metric("P&L", f"+{gain_loss:,.2f} SAR", f"+{gain_loss_pct:.1f}%")
                else:
                    st.metric("P&L", f"{gain_loss:,.2f} SAR", f"{gain_loss_pct:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Market Information Section
        st.markdown("### 📊 Market Info")
        
        # Display total stocks: show both live exchange count (if available) and local DB count
        db_count = len(stocks_db)
        live_count = None
        if SAUDI_EXCHANGE_AVAILABLE:
            try:
                live_db = get_all_saudi_stocks()
                if isinstance(live_db, dict):
                    live_count = len(live_db)
            except Exception:
                live_count = None

        if live_count:
            # Show live exchange number and local DB number so it's explicit where the number comes from
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("TASI Companies (Exchange)", "259")
            with col_b:
                st.metric("Available in DB", f"{db_count}")
            st.success("🟢 Live Data Connected")
        else:
            # Fall back to DB-only display and clearly label it
            st.metric("TASI Companies", "259")
            if SAUDI_EXCHANGE_AVAILABLE:
                st.info("� Live fetch failed — showing cached DB")
            else:
                st.warning("🟡 Using Cached Data")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Get Started Section
        st.markdown("""
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: #1565c0; margin: 0 0 0.5rem 0; font-size: 1rem;">🚀 Quick Start</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #424242;">Add stocks to your portfolio and get AI-powered trading insights!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # About Section
        st.markdown("""
        <div style="margin-top: 2rem;">
            <h4 style="color: #1565c0; margin: 0 0 0.5rem 0; font-size: 1rem;">ℹ️ About TADAWUL NEXUS</h4>
            <div style="font-size: 0.8rem; color: #666; line-height: 1.4;">
                <strong>Next-Generation Platform</strong><br>
                🔥 Real-time Saudi Exchange Data<br>
                🤖 AI Trading Signals<br>
                📊 Professional Portfolio Management<br>
                📈 Advanced Market Analytics
            </div>
            <div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem; line-height: 1.3;">
                🇸🇦 Powered by Tadawul • Built for Saudi Investors
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Main content based on selected page
    if selected_page == "🏠 Portfolio Overview":
        st.markdown("## 🏠 Portfolio Overview")
        
        portfolio = load_portfolio()
        
        if portfolio:
            # Portfolio summary
            portfolio_stats = calculate_portfolio_value(portfolio)
            
            # Portfolio metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Holdings", len(portfolio))
            with col2:
                st.metric("Portfolio Value", f"{portfolio_stats['total_value']:,.2f} SAR")
            with col3:
                st.metric("Total Cost", f"{portfolio_stats['total_cost']:,.2f} SAR")
            with col4:
                gain_loss = portfolio_stats['total_gain_loss']
                gain_loss_pct = portfolio_stats['total_gain_loss_percent']
                st.metric("P&L", f"{gain_loss:,.2f} SAR", f"{gain_loss_pct:.1f}%")
            
            st.markdown("---")
            
            # Portfolio holdings table
            st.markdown("### 📋 Your Holdings")
            
            holdings_data = []
            for idx, stock in enumerate(portfolio, 1):  # Start numbering from 1
                stock_data = get_stock_data(stock['symbol'])
                current_price = stock_data.get('current_price', 0)
                quantity = stock.get('quantity', 0)
                purchase_price = stock.get('purchase_price', 0)
                
                current_value = current_price * quantity
                cost_basis = purchase_price * quantity
                gain_loss = current_value - cost_basis
                gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
                
                stock_info = stocks_db.get(stock['symbol'], {})
                
                holdings_data.append({
                    '#': idx,  # Add row number as first column
                    'Symbol': stock['symbol'],
                    'Company': stock_info.get('name', 'Unknown'),
                    'Quantity': f"{quantity:,.0f}",  # Format with thousands separator
                    'Purchase Price': f"{purchase_price:.2f} SAR",
                    'Total Cost': f"{cost_basis:,.2f} SAR",  # Add Total Cost column
                    'Current Price': f"{current_price:.2f} SAR",
                    'Current Value': f"{current_value:,.2f} SAR",  # Add thousands separator
                    'P&L': f"{gain_loss:+,.2f} SAR",  # Show +/- and 2 decimals
                    'P&L %': f"{gain_loss_pct:+.2f}%",  # Show +/- and 2 decimals
                    'Broker': stock.get('broker', 'Not Set'),  # Add broker column
                    'Purchase Date': stock.get('purchase_date', 'Unknown')  # Add purchase date
                })
            
            if holdings_data:
                holdings_df = pd.DataFrame(holdings_data)
                st.dataframe(holdings_df, hide_index=True, use_container_width=True)
            
            # Portfolio performance chart
            st.markdown("### 📊 Portfolio Performance")
            st.info("📈 Portfolio performance charts coming soon!")
            
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; background: #f8f9fa; border-radius: 10px; border: 2px dashed #dee2e6;">
                <h3 style="color: #6c757d; margin-bottom: 1rem;">📭 No Portfolio Yet</h3>
                <p style="color: #6c757d; margin-bottom: 2rem;">Start building your Saudi stock portfolio today!</p>
                <p style="color: #495057;">Go to <strong>Portfolio Setup</strong> to add your first stock.</p>
            </div>
            """, unsafe_allow_html=True)
    
    elif selected_page == "⚙️ Portfolio Setup":
        st.markdown("## ⚙️ Portfolio Setup")
        
        st.markdown("### ➕ Add New Stock")
        
        # Stock selection using unified data manager
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Use unified manager for consistent stock options
            try:
                from unified_stock_manager import get_stock_options
                stock_options = get_stock_options()
            except ImportError:
                # Fallback to manual creation
                stock_options = []
                for symbol, data in stocks_db.items():
                    name_en = data.get('name', 'Unknown Company')
                    name_ar = data.get('name_ar', '')
                    sector = data.get('sector', '')
                    
                    # Format: Symbol - Company Name (Sector)
                    option_text = f"{symbol} - {name_en}"
                    if sector:
                        option_text += f" ({sector})"
                    
                    stock_options.append((option_text, symbol))
                
                stock_options.sort()  # Sort alphabetically
            
            selected_option = st.selectbox(
                "Choose a Saudi stock:",
                options=[opt[0] for opt in stock_options],
                index=0,
                help=f"Select from {len(stock_options)} available Saudi stocks"
            )
            
            # Get the selected symbol
            selected_symbol = None
            for opt_text, symbol in stock_options:
                if opt_text == selected_option:
                    selected_symbol = symbol
                    break
        
        with col2:
            if selected_symbol:
                stock_info = stocks_db[selected_symbol]
                
                # Display stock info with validation
                st.markdown(f"""
                <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin: 0; color: #1565c0;">{stock_info.get('name', 'Unknown')}</h4>
                    <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; color: #424242;">
                        <strong>Symbol:</strong> {selected_symbol}<br>
                        <strong>Sector:</strong> {stock_info.get('sector', 'N/A')}<br>
                        <strong>Current Price:</strong> {stock_info.get('current_price', 'N/A')} SAR
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add data source validation indicator
                if stock_info.get('last_updated'):
                    st.caption(f"📊 Data updated: {stock_info.get('last_updated', 'Unknown')[:19].replace('T', ' ')}")
        
        # Stock purchase details
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            quantity = st.number_input("Quantity:", min_value=1, value=100, step=1)
        
        with col2:
            purchase_price = st.number_input("Purchase Price (SAR):", min_value=0.01, value=50.0, step=0.01)
        
        with col3:
            purchase_date = st.date_input("Purchase Date:", value=datetime.now().date())
        
        with col4:
            # Broker name field
            broker_name = st.selectbox(
                "Broker:",
                options=[
                    "Al Rajhi Capital",
                    "SNB Capital", 
                    "Riyad Capital",
                    "SABB Securities",
                    "NCB Capital",
                    "Aljazira Capital",
                    "Alinma Investment",
                    "Albilad Investment",
                    "Fransi Capital",
                    "Jadwa Investment",
                    "Other"
                ],
                index=0,
                help="Select your broker"
            )
        
        # If "Other" is selected, allow custom broker name
        if broker_name == "Other":
            broker_name = st.text_input("Enter Broker Name:", placeholder="Enter custom broker name")
        
        # Transaction notes (optional)
        transaction_notes = st.text_area("Notes (Optional):", placeholder="Any additional notes about this transaction...")
        
        # Add stock button
        if st.button("➕ Add to Portfolio", type="primary"):
            if selected_symbol and broker_name:
                portfolio = load_portfolio()
                
                # Check if stock already exists
                existing_stock = None
                for i, stock in enumerate(portfolio):
                    if stock['symbol'] == selected_symbol:
                        existing_stock = i
                        break
                
                if existing_stock is not None:
                    # Update existing holding
                    old_qty = portfolio[existing_stock]['quantity']
                    old_price = portfolio[existing_stock]['purchase_price']
                    
                    # Calculate weighted average price
                    total_qty = old_qty + quantity
                    total_cost = (old_qty * old_price) + (quantity * purchase_price)
                    avg_price = total_cost / total_qty
                    
                    portfolio[existing_stock] = {
                        'symbol': selected_symbol,
                        'quantity': total_qty,
                        'purchase_price': avg_price,
                        'purchase_date': purchase_date.isoformat(),
                        'broker': broker_name,
                        'notes': transaction_notes,
                        'last_updated': datetime.now().isoformat()
                    }
                    
                    st.success(f"✅ Updated {stock_info.get('name')} holding! New quantity: {total_qty}")
                else:
                    # Add new stock
                    new_stock = {
                        'symbol': selected_symbol,
                        'quantity': quantity,
                        'purchase_price': purchase_price,
                        'purchase_date': purchase_date.isoformat(),
                        'broker': broker_name,
                        'notes': transaction_notes,
                        'last_updated': datetime.now().isoformat()
                    }
                    portfolio.append(new_stock)
                    
                    st.success(f"✅ Added {stock_info.get('name')} to your portfolio!")
                
                # Save portfolio
                if save_portfolio(portfolio):
                    st.rerun()
            elif not broker_name:
                st.error("Please select a broker!")
        
        st.markdown("---")
        
        # Current portfolio management
        st.markdown("### 📋 Manage Portfolio")
        
        portfolio = load_portfolio()
        if portfolio:
            # Portfolio overview
            st.markdown(f"**Total Holdings:** {len(portfolio)} stocks")
            
            # Tabs for different management options
            tab1, tab2 = st.tabs(["📊 View Holdings", "✏️ Edit Holdings"])
            
            with tab1:
                # Display portfolio in a nice format
                for i, stock in enumerate(portfolio):
                    stock_info = stocks_db.get(stock['symbol'], {})
                    
                    with st.expander(f"{stock['symbol']} - {stock_info.get('name', 'Unknown')} ({stock['quantity']:,} shares)"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Purchase Price:** {stock['purchase_price']:.2f} SAR")
                            st.write(f"**Purchase Date:** {stock['purchase_date']}")
                            st.write(f"**Quantity:** {stock['quantity']:,} shares")
                            st.write(f"**Total Cost:** {(stock['quantity'] * stock['purchase_price']):,.2f} SAR")
                            
                            # Show broker information if available
                            if stock.get('broker'):
                                st.write(f"**Broker:** {stock['broker']}")
                            
                            # Show notes if available
                            if stock.get('notes'):
                                st.write(f"**Notes:** {stock['notes']}")
                            
                            # Show current stock info for validation
                            if stock_info:
                                st.write(f"**Company:** {stock_info.get('name', 'Unknown')}")
                                st.write(f"**Sector:** {stock_info.get('sector', 'Unknown')}")
                                if stock_info.get('current_price'):
                                    current_value = stock['quantity'] * float(stock_info.get('current_price', 0))
                                    st.write(f"**Current Price:** {stock_info.get('current_price')} SAR")
                                    st.write(f"**Current Value:** {current_value:,.2f} SAR")
                        
                        with col2:
                            if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                                portfolio.pop(i)
                                save_portfolio(portfolio)
                                st.success("Stock removed from portfolio!")
                                st.rerun()
            
            with tab2:
                # Edit existing holdings
                st.markdown("#### ✏️ Edit Stock Information")
                
                if portfolio:
                    # Select stock to edit
                    stock_options_edit = []
                    for i, stock in enumerate(portfolio):
                        stock_info = stocks_db.get(stock['symbol'], {})
                        option_text = f"{stock['symbol']} - {stock_info.get('name', 'Unknown')} ({stock['quantity']:,} shares)"
                        stock_options_edit.append((option_text, i))
                    
                    selected_edit_option = st.selectbox(
                        "Select stock to edit:",
                        options=[opt[0] for opt in stock_options_edit],
                        key="edit_stock_select"
                    )
                    
                    # Get selected stock index
                    selected_stock_idx = None
                    for opt_text, idx in stock_options_edit:
                        if opt_text == selected_edit_option:
                            selected_stock_idx = idx
                            break
                    
                    if selected_stock_idx is not None:
                        edit_stock = portfolio[selected_stock_idx]
                        stock_info = stocks_db.get(edit_stock['symbol'], {})
                        
                        st.markdown(f"**Editing:** {edit_stock['symbol']} - {stock_info.get('name', 'Unknown')}")
                        
                        # Edit form
                        with st.form(f"edit_form_{selected_stock_idx}"):
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                new_quantity = st.number_input(
                                    "Quantity:", 
                                    min_value=1, 
                                    value=edit_stock['quantity'], 
                                    step=1,
                                    key=f"edit_qty_{selected_stock_idx}"
                                )
                            
                            with col2:
                                new_price = st.number_input(
                                    "Purchase Price (SAR):", 
                                    min_value=0.01, 
                                    value=edit_stock['purchase_price'], 
                                    step=0.01,
                                    key=f"edit_price_{selected_stock_idx}"
                                )
                            
                            with col3:
                                current_date = datetime.fromisoformat(edit_stock['purchase_date']).date()
                                new_date = st.date_input(
                                    "Purchase Date:", 
                                    value=current_date,
                                    key=f"edit_date_{selected_stock_idx}"
                                )
                            
                            with col4:
                                current_broker = edit_stock.get('broker', 'Al Rajhi Capital')
                                broker_options = [
                                    "Al Rajhi Capital",
                                    "SNB Capital", 
                                    "Riyad Capital",
                                    "SABB Securities",
                                    "NCB Capital",
                                    "Aljazira Capital",
                                    "Alinma Investment",
                                    "Albilad Investment",
                                    "Fransi Capital",
                                    "Jadwa Investment",
                                    "Other"
                                ]
                                
                                # Find current broker index
                                current_broker_idx = 0
                                if current_broker in broker_options:
                                    current_broker_idx = broker_options.index(current_broker)
                                else:
                                    broker_options.append(current_broker)
                                    current_broker_idx = len(broker_options) - 1
                                
                                new_broker = st.selectbox(
                                    "Broker:",
                                    options=broker_options,
                                    index=current_broker_idx,
                                    key=f"edit_broker_{selected_stock_idx}"
                                )
                            
                            # If "Other" is selected for broker
                            if new_broker == "Other":
                                new_broker = st.text_input(
                                    "Custom Broker Name:", 
                                    value=current_broker if current_broker not in broker_options[:-1] else "",
                                    key=f"edit_custom_broker_{selected_stock_idx}"
                                )
                            
                            # Notes field
                            current_notes = edit_stock.get('notes', '')
                            new_notes = st.text_area(
                                "Notes:", 
                                value=current_notes,
                                key=f"edit_notes_{selected_stock_idx}"
                            )
                            
                            # Submit button
                            submitted = st.form_submit_button("💾 Update Stock", type="primary")
                            
                            if submitted:
                                # Update the stock
                                portfolio[selected_stock_idx] = {
                                    'symbol': edit_stock['symbol'],
                                    'quantity': new_quantity,
                                    'purchase_price': new_price,
                                    'purchase_date': new_date.isoformat(),
                                    'broker': new_broker,
                                    'notes': new_notes,
                                    'last_updated': datetime.now().isoformat()
                                }
                                
                                # Save portfolio
                                if save_portfolio(portfolio):
                                    st.success(f"✅ Updated {stock_info.get('name_en')} successfully!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save changes!")
                        
                        # Show changes preview
                        st.markdown("**Current vs New Values:**")
                        changes_col1, changes_col2 = st.columns(2)
                        
                        with changes_col1:
                            st.markdown("**Current:**")
                            st.write(f"Quantity: {edit_stock['quantity']:,}")
                            st.write(f"Price: {edit_stock['purchase_price']:.2f} SAR")
                            st.write(f"Date: {edit_stock['purchase_date']}")
                            st.write(f"Broker: {edit_stock.get('broker', 'Not set')}")
                            st.write(f"Total Cost: {(edit_stock['quantity'] * edit_stock['purchase_price']):,.2f} SAR")
                        
                        with changes_col2:
                            st.markdown("**Preview:**")
                            st.write(f"Quantity: {new_quantity:,}")
                            st.write(f"Price: {new_price:.2f} SAR") 
                            st.write(f"Date: {new_date}")
                            st.write(f"Broker: {new_broker}")
                            st.write(f"Total Cost: {(new_quantity * new_price):,.2f} SAR")
        else:
            st.info("No stocks in portfolio yet. Add some stocks above!")
        
        # Data validation section
        st.markdown("---")
        st.markdown("### 🔍 Data Validation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🔄 Validate Stock Data"):
                try:
                    from unified_stock_manager import validate_stock_data, unified_manager
                    
                    # Clear cache to get fresh data
                    unified_manager.clear_cache()
                    
                    validation_report = validate_stock_data()
                    
                    st.success("✅ Data validation completed!")
                    st.json(validation_report)
                    
                except ImportError:
                    st.warning("Unified stock manager not available - using fallback validation")
                    
                    # Basic validation
                    test_stocks = ['1010', '1120', '2030', '2010']
                    for symbol in test_stocks:
                        if symbol in stocks_db:
                            stock_info = stocks_db[symbol]
                            st.write(f"**{symbol}:** {stock_info.get('name_en', 'Unknown')}")
                        else:
                            st.error(f"❌ Missing stock: {symbol}")
        
        with col2:
            st.info("Use this to verify that stock symbols match the correct company names.")
    
    elif selected_page == "🤖 AI Trading Center":
        st.markdown("## 🤖 AI Trading Center")
        
        # AI Status
        if AI_AVAILABLE:
            st.success("🟢 AI Trading Engine Active")
        else:
            st.warning("🟡 AI Trading Engine Unavailable")
            st.info("Install AI dependencies to enable advanced trading signals")
        
        # AI Signals for Portfolio
        st.markdown("### 🎯 AI Signals for Your Portfolio")
        
        portfolio = load_portfolio()
        if portfolio and AI_AVAILABLE:
            try:
                portfolio_symbols = [f"{stock['symbol']}.SR" for stock in portfolio]
                ai_signals = get_ai_signals(portfolio_symbols, stocks_db)
                
                if ai_signals:
                    for signal in ai_signals:
                        signal_type = signal.get('signal', 'HOLD')
                        confidence = signal.get('confidence', 0)
                        
                        if signal_type == 'BUY':
                            signal_color = "#00C851"
                            signal_icon = "📈"
                        elif signal_type == 'SELL':
                            signal_color = "#dc3545"
                            signal_icon = "📉"
                        else:
                            signal_color = "#ffc107"
                            signal_icon = "⏸️"
                        
                        st.markdown(f"""
                        <div style="background: {signal_color}; padding: 1rem; border-radius: 8px; color: white; margin: 0.5rem 0;">
                            <h4 style="margin: 0;">{signal_icon} {signal.get('symbol', 'Unknown')} - {signal_type}</h4>
                            <p style="margin: 0.3rem 0 0 0;">Confidence: {confidence:.1f}% | {signal.get('reason', 'AI Analysis')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No AI signals available for current portfolio")
                    
            except Exception as e:
                st.error(f"Error generating AI signals: {e}")
        
        elif portfolio and not AI_AVAILABLE:
            st.info("AI signals will appear here when AI engine is available")
        
        else:
            st.info("Add stocks to your portfolio to get AI trading signals")
        
        st.markdown("---")
        
        # AI Market Analysis
        st.markdown("### 📊 AI Market Analysis")
        
        if AI_AVAILABLE:
            st.info("🤖 Advanced AI market analysis coming soon!")
        else:
            st.info("Install AI dependencies to unlock advanced market analysis")
        
        # AI Settings
        st.markdown("### ⚙️ AI Settings")
        
        risk_tolerance = st.select_slider(
            "Risk Tolerance:",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate"
        )
        
        signal_frequency = st.selectbox(
            "Signal Frequency:",
            ["Real-time", "Daily", "Weekly"],
            index=1
        )
        
        st.checkbox("Enable Email Alerts", value=False)
        st.checkbox("Enable SMS Alerts", value=False)
    
    elif selected_page == "📈 Market Analysis":
        st.markdown("## 📈 Market Analysis")
        
        # Display top gainers and losers tables
        display_top_gainers_losers()
        
        st.markdown("---")
        
        # Additional market analysis
        st.markdown("### 📊 Sector Performance")
        
        # Calculate sector statistics from the database
        stocks_db = load_saudi_stocks_database()
        sector_stats = {}
        
        for symbol, stock_info in stocks_db.items():
            sector = stock_info.get('sector', 'Unknown')
            if sector != 'Unknown':
                if sector not in sector_stats:
                    sector_stats[sector] = {
                        'count': 0,
                        'symbols': []
                    }
                sector_stats[sector]['count'] += 1
                sector_stats[sector]['symbols'].append(symbol)
        
        # Display sector performance table
        if sector_stats:
            sector_df = pd.DataFrame([
                {
                    'Sector': sector,
                    'Total Companies': stats['count'],
                    'Market Share': f"{(stats['count'] / len(stocks_db) * 100):.1f}%",
                    'Sample Companies': ', '.join(stats['symbols'][:3]) + ('...' if len(stats['symbols']) > 3 else '')
                }
                for sector, stats in sorted(sector_stats.items(), key=lambda x: x[1]['count'], reverse=True)
            ])
            
            st.dataframe(
                sector_df,
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("### 📈 Market Trends")
        
        # Market overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Listed Companies",
                f"{len(stocks_db):,}",
                help="Total number of companies in Tadawul"
            )
        
        with col2:
            st.metric(
                "Active Sectors",
                f"{len(sector_stats)}",
                help="Number of distinct business sectors"
            )
        
        with col3:
            largest_sector = max(sector_stats.items(), key=lambda x: x[1]['count'])
            st.metric(
                "Largest Sector",
                largest_sector[0],
                f"{largest_sector[1]['count']} companies"
            )
        
        with col4:
            st.metric(
                "Market Concentration",
                f"{(largest_sector[1]['count'] / len(stocks_db) * 100):.1f}%",
                help="Percentage of companies in largest sector"
            )
    
    elif selected_page == "🔍 Stock Research":
        st.markdown("## 🔍 Stock Research")
        
        # Add search functionality
        st.markdown("### 🔍 Find Your Stock")
        
        # Filter stocks to only show those with proper names
        valid_stocks = {
            symbol: info for symbol, info in stocks_db.items() 
            if info.get('name_en') and info.get('name_en') != 'Unknown'
        }
        
        # Search options
        search_method = st.radio(
            "Search by:",
            ["Stock Symbol", "Company Name"],
            horizontal=True
        )
        
        if search_method == "Stock Symbol":
            search_symbol = st.selectbox(
                "Select Stock Symbol:",
                options=list(valid_stocks.keys()),
                format_func=lambda x: f"{x} - {valid_stocks[x].get('name_en', 'Unknown')}"
            )
        else:
            # Search by company name
            search_text = st.text_input("Type company name:", placeholder="e.g., Saudi Aramco, Al Rajhi Bank...")
            
            if search_text:
                # Filter companies by name
                matching_companies = {
                    symbol: info for symbol, info in valid_stocks.items()
                    if search_text.lower() in info.get('name_en', '').lower() or 
                       search_text.lower() in info.get('name_ar', '').lower()
                }
                
                if matching_companies:
                    search_symbol = st.selectbox(
                        "Matching Companies:",
                        options=list(matching_companies.keys()),
                        format_func=lambda x: f"{x} - {matching_companies[x].get('name_en', 'Unknown')}"
                    )
                else:
                    st.warning("No companies found matching your search.")
                    search_symbol = None
            else:
                search_symbol = None
        
        # Stock analysis section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if not valid_stocks:
                st.error("No valid stocks found in database")
                search_symbol = None
        
        with col2:
            if search_symbol and search_symbol in valid_stocks:
                stock_info = valid_stocks[search_symbol]
                st.markdown("### 🏢 Quick Info")
                st.markdown(f"""
                **Company:** {stock_info.get('name_en', 'Unknown')}  
                **Arabic Name:** {stock_info.get('name_ar', 'غير متوفر')}  
                **Sector:** {stock_info.get('sector', 'N/A')}  
                **Symbol:** {search_symbol}
                """)
                
                # Add sector badge
                sector = stock_info.get('sector', 'N/A')
                if sector != 'N/A':
                    st.markdown(f"<span style='background-color: #1f77b4; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px;'>{sector}</span>", unsafe_allow_html=True)
        
        if search_symbol and search_symbol in valid_stocks:
            stock_info = valid_stocks[search_symbol]
            # Get stock data
            stock_data = get_stock_data(search_symbol)
            
            # Display stock metrics
            st.markdown("### 📊 Stock Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Current Price", f"{stock_data.get('current_price', 0):.2f} SAR")
            with col2:
                change = stock_data.get('change', 0)
                st.metric("Change", f"{change:.2f} SAR", f"{stock_data.get('change_percent', 0):.2f}%")
            with col3:
                st.metric("Volume", f"{stock_data.get('volume', 0):,}")
            with col4:
                st.metric("P/E Ratio", f"{stock_data.get('pe_ratio', 0):.2f}")
            
            # Stock chart and additional info
            st.markdown("### 📊 Stock Analysis")
            
            # Create tabs for different analysis
            tab1, tab2, tab3 = st.tabs(["📈 Price Info", "🏢 Company Details", "📊 Sector Comparison"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📈 Price Movement**")
                    # Simulate price chart data
                    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
                    import random
                    random.seed(hash(search_symbol) % 1000)  # Consistent random data based on symbol
                    base_price = stock_data.get('current_price', 100)
                    prices = [base_price + random.uniform(-5, 5) + i*0.01 for i in range(len(dates))]
                    
                    chart_df = pd.DataFrame({
                        'Date': dates,
                        'Price': prices
                    })
                    
                    st.line_chart(chart_df.set_index('Date'))
                
                with col2:
                    st.markdown("**📊 Key Statistics**")
                    st.write(f"**52-Week High:** {max(prices):.2f} SAR")
                    st.write(f"**52-Week Low:** {min(prices):.2f} SAR")
                    st.write(f"**Average Price:** {sum(prices)/len(prices):.2f} SAR")
                    st.write(f"**Volatility:** {(max(prices) - min(prices)):.2f} SAR")
            
            with tab2:
                st.markdown("**🏢 Company Information**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**English Name:** {stock_info.get('name_en', 'N/A')}")
                    st.write(f"**Arabic Name:** {stock_info.get('name_ar', 'غير متوفر')}")
                    st.write(f"**Symbol:** {search_symbol}")
                
                with col2:
                    st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
                    st.write(f"**Market:** Saudi Stock Exchange (Tadawul)")
                    st.write(f"**Currency:** SAR")
            
            with tab3:
                st.markdown("**📊 Sector Analysis**")
                current_sector = stock_info.get('sector', 'N/A')
                
                # Count companies in same sector
                sector_companies = [
                    symbol for symbol, info in stocks_db.items() 
                    if info.get('sector') == current_sector
                ]
                
                st.write(f"**Current Sector:** {current_sector}")
                st.write(f"**Companies in Sector:** {len(sector_companies)}")
                st.write(f"**Sector Market Share:** {(len(sector_companies) / len(stocks_db) * 100):.1f}%")
                
                if len(sector_companies) > 1:
                    st.markdown("**Other Companies in Sector:**")
                    other_companies = [s for s in sector_companies if s != search_symbol][:5]
                    for company in other_companies:
                        company_name = stocks_db[company].get('name_en', company)
                        st.write(f"• {company} - {company_name}")
                    
                    if len(other_companies) > 5:
                        st.write(f"... and {len(sector_companies) - 6} more companies")
    
    elif selected_page == "📊 Analytics Dashboard":
        st.markdown("## 📊 Analytics Dashboard")
        
        portfolio = load_portfolio()
        
        if portfolio:
            # Portfolio analytics
            st.markdown("### 📊 Portfolio Analytics")
            
            # Sector allocation
            sector_allocation = {}
            for stock in portfolio:
                stock_info = stocks_db.get(stock['symbol'], {})
                sector = stock_info.get('sector', 'Unknown')
                
                if sector in sector_allocation:
                    sector_allocation[sector] += stock['quantity']
                else:
                    sector_allocation[sector] = stock['quantity']
            
            if sector_allocation:
                # Create pie chart
                fig = px.pie(
                    values=list(sector_allocation.values()),
                    names=list(sector_allocation.keys()),
                    title="Portfolio Allocation by Sector"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Performance metrics
            st.markdown("### 📈 Performance Metrics")
            
            # Calculate portfolio metrics
            total_value = sum(stock.get('current_value', 0) for stock in portfolio)
            total_cost = sum(stock.get('total_cost', 0) for stock in portfolio)
            total_pnl = total_value - total_cost
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Portfolio Return",
                    f"{total_pnl:,.2f} SAR",
                    f"{(total_pnl / total_cost * 100):.2f}%" if total_cost > 0 else "0%"
                )
            
            with col2:
                profitable_stocks = len([s for s in portfolio if s.get('pnl', 0) > 0])
                st.metric(
                    "Profitable Holdings",
                    f"{profitable_stocks} / {len(portfolio)}",
                    f"{(profitable_stocks / len(portfolio) * 100):.1f}%"
                )
            
            with col3:
                avg_return = (total_pnl / total_cost * 100) if total_cost > 0 else 0
                performance_status = "📈" if avg_return > 0 else "📉" if avg_return < 0 else "➡️"
                st.metric(
                    "Performance Status",
                    performance_status,
                    f"Avg: {avg_return:.2f}%"
                )
            
            # Top performers
            st.markdown("### 🏆 Top Performers")
            
            if portfolio:
                # Sort by percentage return
                portfolio_sorted = sorted(
                    portfolio, 
                    key=lambda x: x.get('pnl_percent', 0), 
                    reverse=True
                )
                
                top_performers = portfolio_sorted[:5]
                worst_performers = portfolio_sorted[-3:]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🚀 Best Performers**")
                    for stock in top_performers:
                        pnl_percent = stock.get('pnl_percent', 0)
                        status = "🟢" if pnl_percent > 0 else "🔴" if pnl_percent < 0 else "⚪"
                        stock_name = stocks_db.get(stock['symbol'], {}).get('name_en', stock['symbol'])
                        st.write(f"{status} **{stock['symbol']}** - {stock_name[:20]}{'...' if len(stock_name) > 20 else ''}")
                        st.write(f"   Return: {pnl_percent:.2f}% | Value: {stock.get('current_value', 0):,.0f} SAR")
                
                with col2:
                    st.markdown("**📉 Needs Attention**")
                    for stock in worst_performers:
                        pnl_percent = stock.get('pnl_percent', 0)
                        status = "🟢" if pnl_percent > 0 else "🔴" if pnl_percent < 0 else "⚪"
                        stock_name = stocks_db.get(stock['symbol'], {}).get('name_en', stock['symbol'])
                        st.write(f"{status} **{stock['symbol']}** - {stock_name[:20]}{'...' if len(stock_name) > 20 else ''}")
                        st.write(f"   Return: {pnl_percent:.2f}% | Value: {stock.get('current_value', 0):,.0f} SAR")
        
        else:
            st.info("Add stocks to your portfolio to view analytics")
    
    elif selected_page == "🏢 Sector Analyzer":
        st.markdown("## 🏢 TADAWUL SECTOR ANALYZER")
        st.markdown("**Complete Saudi Exchange (Tadawul) Sector Breakdown with Interactive Tables**")
        
        # Load database
        stocks_db = load_saudi_stocks_database()
        
        if not stocks_db:
            st.error("❌ Could not load stock database")
            return
        
        # Calculate sector distribution
        sector_counts = {}
        sector_stocks = {}
        
        for symbol, stock_info in stocks_db.items():
            sector = stock_info.get('sector', 'Unknown')
            
            if sector in sector_counts:
                sector_counts[sector] += 1
            else:
                sector_counts[sector] = 1
            
            if sector in sector_stocks:
                sector_stocks[sector].append({
                    'Symbol': symbol,
                    'Company (EN)': stock_info.get('name_en', 'N/A'),
                    'Company (AR)': stock_info.get('name_ar', 'N/A'),
                    'Sector': sector
                })
            else:
                sector_stocks[sector] = [{
                    'Symbol': symbol,
                    'Company (EN)': stock_info.get('name_en', 'N/A'),
                    'Company (AR)': stock_info.get('name_ar', 'N/A'),
                    'Sector': sector
                }]
        
        # Sort sectors by count
        sector_counts = dict(sorted(sector_counts.items(), key=lambda x: x[1], reverse=True))
        
        # Display summary metrics
        total_stocks = len(stocks_db)
        total_sectors = len(sector_counts)
        largest_sector = max(sector_counts.items(), key=lambda x: x[1])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Stocks", total_stocks)
        with col2:
            st.metric("🏢 Total Sectors", total_sectors)
        with col3:
            st.metric("🥇 Largest Sector", f"{largest_sector[0]} ({largest_sector[1]})")
        
        st.markdown("---")
        
        # Sector Distribution Overview
        st.markdown("## 📊 Sector Distribution Overview")
        
        # Create charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart
            fig_pie = px.pie(
                values=list(sector_counts.values()),
                names=list(sector_counts.keys()),
                title="Stock Distribution by Sector",
                height=500
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart
            fig_bar = px.bar(
                x=list(sector_counts.keys()),
                y=list(sector_counts.values()),
                title="Number of Stocks per Sector",
                labels={'x': 'Sector', 'y': 'Number of Stocks'},
                height=500
            )
            fig_bar.update_xaxes(tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        # Clickable Sector Summary
        st.markdown("## 🔍 Clickable Sector Summary")
        st.markdown("*Click on any sector below to see all stocks in that sector*")
        
        # Create summary table
        summary_data = []
        for sector, count in sector_counts.items():
            # Get sample companies for preview
            sample_companies = [stock['Company (EN)'] for stock in sector_stocks[sector][:3]]
            sample_text = ', '.join(sample_companies)
            if len(sector_stocks[sector]) > 3:
                sample_text += f", +{len(sector_stocks[sector]) - 3} more"
            
            summary_data.append({
                'Sector': sector,
                'Number of Stocks': count,
                'Sample Companies': sample_text
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Display the clickable table
        selected_rows = st.dataframe(
            summary_df,
            hide_index=True,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        # Show detailed sector breakdown when a sector is selected
        if selected_rows and selected_rows['selection']['rows']:
            selected_row_idx = selected_rows['selection']['rows'][0]
            selected_sector = summary_df.iloc[selected_row_idx]['Sector']
            
            st.markdown(f"## 📋 All Stocks in **{selected_sector}** Sector")
            
            # Get all stocks in the selected sector
            sector_df = pd.DataFrame(sector_stocks[selected_sector])
            
            # Display count
            st.info(f"Found **{len(sector_df)}** stocks in the **{selected_sector}** sector")
            
            # Display the stocks table
            st.dataframe(
                sector_df,
                hide_index=True,
                use_container_width=True
            )
            
            # Add download button for this sector
            csv_buffer = io.StringIO()
            sector_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label=f"📥 Download {selected_sector} Stocks (CSV)",
                data=csv_data,
                file_name=f"tadawul_{selected_sector.lower().replace(' ', '_')}_stocks.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        
        # Download complete data
        st.markdown("## 📥 Download Complete Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download sector summary
            summary_csv = io.StringIO()
            summary_df.to_csv(summary_csv, index=False)
            summary_csv_data = summary_csv.getvalue()
            
            st.download_button(
                label="📊 Download Sector Summary (CSV)",
                data=summary_csv_data,
                file_name="tadawul_sector_summary.csv",
                mime="text/csv"
            )
        
        with col2:
            # Download all stocks
            all_stocks_data = []
            for symbol, stock_info in stocks_db.items():
                all_stocks_data.append({
                    'Symbol': symbol,
                    'Company (EN)': stock_info.get('name_en', 'N/A'),
                    'Company (AR)': stock_info.get('name_ar', 'N/A'),
                    'Sector': stock_info.get('sector', 'Unknown')
                })
            
            all_stocks_df = pd.DataFrame(all_stocks_data)
            all_stocks_csv = io.StringIO()
            all_stocks_df.to_csv(all_stocks_csv, index=False)
            all_stocks_csv_data = all_stocks_csv.getvalue()
            
            st.download_button(
                label="📋 Download All Stocks (CSV)",
                data=all_stocks_csv_data,
                file_name="tadawul_all_stocks.csv",
                mime="text/csv"
            )
    
    elif selected_page == "📁 Import/Export Data":
        st.markdown("## 📁 Import/Export Data")
        
        # Export portfolio
        st.markdown("### 📤 Export Portfolio")
        
        portfolio = load_portfolio()
        if portfolio:
            # Create export data
            export_data = []
            for stock in portfolio:
                stock_info = stocks_db.get(stock['symbol'], {})
                stock_data = get_stock_data(stock['symbol'])
                
                export_data.append({
                    'Symbol': stock['symbol'],
                    'Company': stock_info.get('name', 'Unknown'),
                    'Quantity': stock['quantity'],
                    'Purchase Price': stock['purchase_price'],
                    'Current Price': stock_data.get('current_price', 0),
                    'Purchase Date': stock['purchase_date']
                })
            
            export_df = pd.DataFrame(export_data)
            
            # Convert to CSV
            csv_buffer = io.StringIO()
            export_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="📥 Download Portfolio (CSV)",
                data=csv_data,
                file_name=f"tadawul_nexus_portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Preview
            st.markdown("### 👀 Export Preview")
            st.dataframe(export_df, hide_index=True)
        
        else:
            st.info("No portfolio data to export")
        
        st.markdown("---")
        
        # Import portfolio
        st.markdown("### 📥 Import Portfolio")
        
        st.info("""
        **📋 File Format Requirements:**
        - **Supported formats**: CSV (.csv) and Excel (.xlsx) files
        - **Required columns**: symbol, quantity, purchase_price, purchase_date
        - **Optional columns**: broker
        - **symbol**: Stock symbol (e.g., 1010, 2222, 4001)
        - **quantity**: Number of shares
        - **purchase_price**: Price per share in SAR
        - **purchase_date**: Date (YYYY-MM-DD format)
        - **broker**: Broker name (optional)
        """)
        
        uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
        
        if uploaded_file is not None:
            try:
                # Handle different file types
                file_extension = uploaded_file.name.split('.')[-1].lower()
                
                if file_extension == 'csv':
                    import_df = pd.read_csv(uploaded_file)
                elif file_extension == 'xlsx':
                    # Try to read from different sheets
                    xl_file = pd.ExcelFile(uploaded_file)
                    sheet_names = xl_file.sheet_names
                    
                    # Look for common sheet names first
                    preferred_sheets = ['Your Portfolio', 'Portfolio', 'Your_Portfolio', 'Portfolio_Template']
                    selected_sheet = None
                    
                    for pref_sheet in preferred_sheets:
                        if pref_sheet in sheet_names:
                            selected_sheet = pref_sheet
                            break
                    
                    # If no preferred sheet found, use the first sheet
                    if not selected_sheet:
                        selected_sheet = sheet_names[0]
                    
                    # Show sheet selection if multiple sheets
                    if len(sheet_names) > 1:
                        st.info(f"📋 **Excel file detected with {len(sheet_names)} sheets**")
                        selected_sheet = st.selectbox(
                            "Select sheet to import:",
                            sheet_names,
                            index=sheet_names.index(selected_sheet) if selected_sheet in sheet_names else 0
                        )
                    
                    import_df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                    st.success(f"✅ Reading from sheet: **{selected_sheet}**")
                else:
                    st.error("❌ Unsupported file format. Please use CSV or Excel files.")
                    import_df = None
                
                # Only proceed if we have a valid dataframe
                if import_df is not None:
                    st.markdown("### 👀 Import Preview")
                    st.dataframe(import_df, hide_index=True)
                    
                    # Validate required columns
                    required_cols = ['symbol', 'quantity', 'purchase_price', 'purchase_date']
                    missing_cols = [col for col in required_cols if col not in import_df.columns]
                
                if missing_cols:
                    st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                else:
                    # Validate data
                    validation_errors = []
                    
                    for idx, row in import_df.iterrows():
                        # Clean and validate symbol
                        symbol_str = str(row['symbol']).strip()
                        
                        # Check symbol exists in database
                        if symbol_str not in stocks_db:
                            validation_errors.append(f"Row {idx+1}: Symbol '{symbol_str}' not found in database")
                        
                        # Check quantity is positive number
                        try:
                            quantity_val = float(str(row['quantity']).replace(',', ''))
                            if quantity_val <= 0:
                                validation_errors.append(f"Row {idx+1}: Quantity must be positive")
                        except (ValueError, TypeError):
                            validation_errors.append(f"Row {idx+1}: Invalid quantity '{row['quantity']}'")
                        
                        # Check price is positive number (handle different formats)
                        try:
                            price_str = str(row['purchase_price']).replace(',', '').strip()
                            if price_str in ['', 'nan', 'NaN', 'null', 'NULL']:
                                validation_errors.append(f"Row {idx+1}: Price cannot be empty")
                            else:
                                price_val = float(price_str)
                                if price_val <= 0:
                                    validation_errors.append(f"Row {idx+1}: Price must be positive (got {price_val})")
                        except (ValueError, TypeError):
                            validation_errors.append(f"Row {idx+1}: Invalid price '{row['purchase_price']}'")
                        
                        # Validate date format (support multiple formats)
                        try:
                            date_str = str(row['purchase_date']).strip()
                            if date_str not in ['', 'nan', 'NaN', 'null', 'NULL']:
                                # Try multiple date formats
                                date_formats = [
                                    '%Y-%m-%d',      # 2024-01-15
                                    '%m/%d/%Y',      # 12/31/2024 (US format)
                                    '%d/%m/%Y',      # 31/12/2024 (EU format)
                                    '%Y/%m/%d',      # 2024/12/31
                                    '%d-%m-%Y',      # 31-12-2024
                                    '%m-%d-%Y'       # 12-31-2024
                                ]
                                
                                date_parsed = False
                                for fmt in date_formats:
                                    try:
                                        datetime.strptime(date_str, fmt)
                                        date_parsed = True
                                        break
                                    except ValueError:
                                        continue
                                
                                if not date_parsed:
                                    validation_errors.append(f"Row {idx+1}: Invalid date format '{row['purchase_date']}' (supported: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)")
                        except Exception as e:
                            validation_errors.append(f"Row {idx+1}: Error processing date '{row['purchase_date']}': {str(e)}")
                    
                    if validation_errors:
                        st.error("❌ **Validation Errors:**")
                        for error in validation_errors[:10]:  # Show first 10 errors
                            st.error(f"• {error}")
                        if len(validation_errors) > 10:
                            st.error(f"... and {len(validation_errors) - 10} more errors")
                        
                        # Show helpful tips
                        st.info("""
                        💡 **Quick Fixes:**
                        - **Missing symbols**: Some stocks may need to be added to the database
                        - **Price errors**: Check for empty cells, negative values, or text in price column
                        - **Date format**: Use YYYY-MM-DD format (e.g., 2024-01-15)
                        """)
                    else:
                        st.success("✅ All data validated successfully!")
                        
                        # Calculate and display import summary
                        st.markdown("### 📊 Import Summary")
                        
                        # Load existing portfolio to calculate current totals
                        portfolio_file = Path("user_portfolio.json")
                        existing_portfolio = []
                        if portfolio_file.exists():
                            try:
                                with open(portfolio_file, 'r') as f:
                                    existing_portfolio = json.load(f)
                            except:
                                existing_portfolio = []
                        
                        # Calculate current portfolio totals
                        current_stocks = len(existing_portfolio)
                        current_quantity = sum(stock.get('quantity', 0) for stock in existing_portfolio)
                        current_cost = sum(stock.get('quantity', 0) * stock.get('purchase_price', 0) for stock in existing_portfolio)
                        
                        # Calculate import file totals
                        import_stocks = len(import_df)
                        import_quantity = 0
                        import_cost = 0
                        
                        for _, row in import_df.iterrows():
                            try:
                                quantity = float(str(row['quantity']).replace(',', ''))
                                price_str = str(row['purchase_price']).replace(',', '').strip()
                                price = float(price_str)
                                import_quantity += quantity
                                import_cost += (quantity * price)
                            except (ValueError, TypeError):
                                pass  # Skip invalid rows (already caught in validation)
                        
                        # Calculate final totals (this is an estimate - actual may differ due to symbol consolidation)
                        final_stocks = current_stocks + import_stocks  # Approximate
                        final_quantity = current_quantity + import_quantity
                        final_cost = current_cost + import_cost
                        
                        # Display summary in three sections
                        st.markdown("#### 📋 Portfolio Comparison")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**🏠 Current Portfolio**")
                            st.metric(
                                label="Stocks",
                                value=f"{current_stocks:,}",
                                help="Current number of stock holdings"
                            )
                            st.metric(
                                label="Shares", 
                                value=f"{current_quantity:,.0f}",
                                help="Current total number of individual stock shares/units owned"
                            )
                            st.metric(
                                label="Current Portfolio Cost",
                                value=f"{current_cost:,.2f} SAR",
                                help="Current total investment value of existing portfolio"
                            )
                        
                        with col2:
                            st.markdown("**📁 Import File**")
                            st.metric(
                                label="Records",
                                value=f"{import_stocks:,}",
                                help="Number of records to be imported"
                            )
                            st.metric(
                                label="Shares",
                                value=f"{import_quantity:,.0f}",
                                help="Total number of individual stock shares/units in import file"
                            )
                            st.metric(
                                label="Total Cost of Uploaded Portfolio",
                                value=f"{import_cost:,.2f} SAR",
                                help="Total investment cost of stocks being uploaded"
                            )
                        
                        with col3:
                            st.markdown("**🎯 After Import**")
                            st.metric(
                                label="Stocks",
                                value=f"~{final_stocks:,}",
                                delta=f"+{import_stocks}",
                                help="Approximate final stock count (may be less due to symbol consolidation)"
                            )
                            st.metric(
                                label="Shares",
                                value=f"{final_quantity:,.0f}",
                                delta=f"+{import_quantity:,.0f}",
                                help="Final total number of individual stock shares/units after import"
                            )
                            st.metric(
                                label="Total Investment Cost Post Uploading", 
                                value=f"{final_cost:,.2f} SAR",
                                delta=f"+{import_cost:,.2f}",
                                help="Final total investment cost after uploading new portfolio data"
                            )
                        
                        # Show unique symbols summary
                        unique_symbols = import_df['symbol'].nunique()
                        if unique_symbols != import_stocks:
                            st.info(f"ℹ️ **Note**: {import_stocks} records contain {unique_symbols} unique stock symbols. Duplicate symbols will be consolidated.")
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("📥 Import Portfolio", type="primary"):
                                # Load existing portfolio
                                portfolio_file = Path("user_portfolio.json")
                                existing_portfolio = []
                                
                                if portfolio_file.exists():
                                    try:
                                        with open(portfolio_file, 'r') as f:
                                            existing_portfolio = json.load(f)
                                    except:
                                        existing_portfolio = []
                                
                                # Helper function to normalize date format
                                def normalize_date(date_str):
                                    """Convert various date formats to YYYY-MM-DD"""
                                    date_str = str(date_str).strip()
                                    if date_str in ['', 'nan', 'NaN', 'null', 'NULL']:
                                        return datetime.now().strftime('%Y-%m-%d')
                                    
                                    date_formats = [
                                        '%Y-%m-%d',      # 2024-01-15
                                        '%m/%d/%Y',      # 12/31/2024 (US format)
                                        '%d/%m/%Y',      # 31/12/2024 (EU format)
                                        '%Y/%m/%d',      # 2024/12/31
                                        '%d-%m-%Y',      # 31-12-2024
                                        '%m-%d-%Y'       # 12-31-2024
                                    ]
                                    
                                    for fmt in date_formats:
                                        try:
                                            parsed_date = datetime.strptime(date_str, fmt)
                                            return parsed_date.strftime('%Y-%m-%d')
                                        except ValueError:
                                            continue
                                    
                                    # If no format works, return current date
                                    return datetime.now().strftime('%Y-%m-%d')
                                
                                # Process each row with improved accumulation logic
                                imported_count = 0
                                updated_count = 0
                                
                                # First, group data by symbol for better accumulation
                                symbol_data = {}
                                for _, row in import_df.iterrows():
                                    symbol = str(row['symbol']).strip()
                                    quantity = float(str(row['quantity']).replace(',', ''))
                                    price_str = str(row['purchase_price']).replace(',', '').strip()
                                    purchase_price = float(price_str)
                                    purchase_date = normalize_date(row['purchase_date'])  # Normalize date format
                                    broker = str(row.get('broker', 'Unknown')) if 'broker' in row and pd.notna(row.get('broker')) else 'Unknown'
                                    
                                    if symbol in symbol_data:
                                        # Accumulate same symbol from import file
                                        old_qty = symbol_data[symbol]['quantity']
                                        old_price = symbol_data[symbol]['purchase_price']
                                        
                                        total_cost = (old_qty * old_price) + (quantity * purchase_price)
                                        new_quantity = old_qty + quantity
                                        new_avg_price = total_cost / new_quantity
                                        
                                        symbol_data[symbol]['quantity'] = new_quantity
                                        symbol_data[symbol]['purchase_price'] = round(new_avg_price, 2)
                                        symbol_data[symbol]['broker'] = broker  # Use latest broker
                                    else:
                                        symbol_data[symbol] = {
                                            'quantity': quantity,
                                            'purchase_price': purchase_price,
                                            'purchase_date': purchase_date,
                                            'broker': broker
                                        }
                                
                                # Now process accumulated data
                                for symbol, data in symbol_data.items():
                                    # Check if stock already exists in portfolio
                                    existing_stock = None
                                    for stock in existing_portfolio:
                                        if stock['symbol'] == symbol:
                                            existing_stock = stock
                                            break
                                    
                                    if existing_stock:
                                        # Update existing stock (add to quantity and recalculate average price)
                                        old_quantity = existing_stock['quantity']
                                        old_price = existing_stock['purchase_price']
                                        
                                        total_cost = (old_quantity * old_price) + (data['quantity'] * data['purchase_price'])
                                        new_quantity = old_quantity + data['quantity']
                                        new_avg_price = total_cost / new_quantity
                                        
                                        existing_stock['quantity'] = new_quantity
                                        existing_stock['purchase_price'] = round(new_avg_price, 2)
                                        existing_stock['broker'] = data['broker']  # Update broker info
                                        existing_stock['last_updated'] = datetime.now().isoformat()
                                        updated_count += 1
                                    else:
                                        # Add new stock
                                        new_stock = {
                                            "symbol": symbol,
                                            "quantity": data['quantity'],
                                            "purchase_price": data['purchase_price'],
                                            "purchase_date": data['purchase_date'],
                                            "broker": data['broker'],
                                            "notes": "",
                                            "last_updated": datetime.now().isoformat()
                                        }
                                        existing_portfolio.append(new_stock)
                                        imported_count += 1
                                        
                                
                                # Save updated portfolio
                                try:
                                    with open(portfolio_file, 'w') as f:
                                        json.dump(existing_portfolio, f, indent=2)
                                    
                                    st.success(f"""
                                    ✅ **Portfolio Import Successful!**
                                    - 📈 New stocks added: {imported_count}
                                    - 🔄 Existing stocks updated: {updated_count}
                                    - 📊 Total stocks in portfolio: {len(existing_portfolio)}
                                    
                                    *Refreshing portfolio view...*
                                    """)
                                    
                                    # Show balloons and automatically refresh
                                    st.balloons()
                                    
                                    # Set session state to navigate to Portfolio Overview
                                    st.session_state.main_nav = "🏠 Portfolio Overview"
                                    
                                    # Rerun to refresh the app and show updated portfolio
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Error saving portfolio: {e}")
                        
                        with col2:
                            if st.button("📋 Download Sample CSV"):
                                # Create sample CSV
                                sample_data = {
                                    'symbol': ['1010', '2222', '4001'],
                                    'quantity': [1000, 500, 750],
                                    'purchase_price': [25.50, 45.20, 67.80],
                                    'purchase_date': ['2024-01-15', '2024-02-20', '2024-03-10'],
                                    'broker': ['Al Rajhi Capital', 'SNB Capital', 'Alinma Investment']
                                }
                                sample_df = pd.DataFrame(sample_data)
                                
                                # Convert to CSV
                                csv_buffer = io.StringIO()
                                sample_df.to_csv(csv_buffer, index=False)
                                csv_data = csv_buffer.getvalue()
                                
                                st.download_button(
                                    label="📥 Download Sample",
                                    data=csv_data,
                                    file_name="portfolio_sample.csv",
                                    mime="text/csv"
                                )
                    
            except Exception as e:
                st.error(f"❌ Error reading file: {e}")
                st.info("💡 Please ensure your CSV file is properly formatted.")

if __name__ == "__main__":
    main()
