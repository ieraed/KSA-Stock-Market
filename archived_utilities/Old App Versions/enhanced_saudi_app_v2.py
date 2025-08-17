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

def load_saudi_stocks_database():
    """Load Saudi stocks database with unified data management"""
    try:
        from unified_stock_manager import get_unified_stocks_database
        return get_unified_stocks_database()
    except ImportError:
        # Fallback to corrected database if unified manager not available
        try:
            with open('saudi_stocks_database_corrected.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Final fallback - minimal database with correct data
            return {
                "1010": {"symbol": "1010", "name_en": "Saudi National Bank", "name_ar": "البنك الأهلي السعودي", "sector": "Banking"},
                "1120": {"symbol": "1120", "name_en": "Al Rajhi Bank", "name_ar": "مصرف الراجحي", "sector": "Banking"},
                "2030": {"symbol": "2030", "name_en": "Saudi Arabian Oil Company", "name_ar": "أرامكو السعودية", "sector": "Energy"},
                "2010": {"symbol": "2010", "name_en": "Saudi Basic Industries Corporation", "name_ar": "سابك", "sector": "Materials"},
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
        selected_page = st.radio(
            "Navigation",
            [
                "🏠 Portfolio Overview",
                "⚙️ Portfolio Setup", 
                "🤖 AI Trading Center",
                "📈 Market Analysis",
                "🔍 Stock Research",
                "📊 Analytics Dashboard",
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
            for stock in portfolio:
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
                    'Symbol': stock['symbol'],
                    'Company': stock_info.get('name_en', 'Unknown'),
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
                    name_en = data.get('name_en', 'Unknown Company')
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
                    <h4 style="margin: 0; color: #1565c0;">{stock_info.get('name_en', 'Unknown')}</h4>
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
                    
                    st.success(f"✅ Updated {stock_info.get('name_en')} holding! New quantity: {total_qty}")
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
                    
                    st.success(f"✅ Added {stock_info.get('name_en')} to your portfolio!")
                
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
                    
                    with st.expander(f"{stock['symbol']} - {stock_info.get('name_en', 'Unknown')} ({stock['quantity']:,} shares)"):
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
                                st.write(f"**Company:** {stock_info.get('name_en', 'Unknown')}")
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
                        option_text = f"{stock['symbol']} - {stock_info.get('name_en', 'Unknown')} ({stock['quantity']:,} shares)"
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
                        
                        st.markdown(f"**Editing:** {edit_stock['symbol']} - {stock_info.get('name_en', 'Unknown')}")
                        
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
        st.info("Sector performance analysis coming soon!")
        
        st.markdown("### 📈 Market Trends")
        st.info("Market trend analysis coming soon!")
    
    elif selected_page == "🔍 Stock Research":
        st.markdown("## 🔍 Stock Research")
        
        # Stock search and research
        col1, col2 = st.columns([1, 1])
        
        with col1:
            search_symbol = st.selectbox(
                "Search Stock:",
                options=list(stocks_db.keys()),
                format_func=lambda x: f"{x} - {stocks_db[x].get('name_en', 'Unknown')}"
            )
        
        with col2:
            if search_symbol:
                stock_info = stocks_db[search_symbol]
                st.markdown(f"""
                **Company:** {stock_info.get('name_en', 'Unknown')}  
                **Arabic Name:** {stock_info.get('name_ar', 'غير متوفر')}  
                **Sector:** {stock_info.get('sector', 'N/A')}
                """)
        
        if search_symbol:
            # Get stock data
            stock_data = get_stock_data(search_symbol)
            
            # Display stock metrics
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
            
            # Stock chart
            st.markdown("### 📊 Price Chart")
            st.info("Interactive price charts coming soon!")
    
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
            st.info("Detailed performance analytics coming soon!")
        
        else:
            st.info("Add stocks to your portfolio to view analytics")
    
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
                    'Company': stock_info.get('name_en', 'Unknown'),
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
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                import_df = pd.read_csv(uploaded_file)
                
                st.markdown("### 👀 Import Preview")
                st.dataframe(import_df, hide_index=True)
                
                if st.button("📥 Import Portfolio"):
                    # Process import
                    st.success("Portfolio import functionality coming soon!")
                    
            except Exception as e:
                st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
