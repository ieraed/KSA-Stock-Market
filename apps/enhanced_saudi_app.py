"""
🇸🇦 Enhanced Saudi Stock Ma# Confist.set_page_config(
    page_title="✨ TADAWUL NEXUS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)age
st.set_page_config(
    page_title="🇸🇦 Saudi Stock Market Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)p
Complete Portfolio Management + AI Trading Platform

Features:
- Portfolio Management with real-time data
- AI-Powered Trading Signals
- Saudi Stock Exchange Integration
- User-Friendly Interface
- Excel Import/Export
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

# Try to import AI features
try:
    from ai_engine.simple_ai import get_ai_signals
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("AI features not available - install dependencies to enable")

# Configure page
st.set_page_config(
    page_title="🇸🇦 Saudi Stock Market Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
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

.stSelectbox > label {
    font-weight: 600;
    color: #2c3e50;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,200,81,0.3);
}

/* Sidebar styling */
.css-1d391kg {
    background-color: #fafafa;
}

/* Navigation radio buttons */
.stRadio > div {
    background-color: white;
    padding: 0.7rem;
    border-radius: 6px;
    margin: 0.3rem 0;
    border: 1px solid #e0e0e0;
    transition: all 0.2s ease;
}

.stRadio > div:hover {
    background-color: #f3f4f6;
    border-color: #1976d2;
    transform: translateX(2px);
}

.stRadio > div[data-checked="true"] {
    background-color: #e3f2fd;
    border-color: #1976d2;
    border-width: 2px;
}

.stRadio label {
    font-weight: 500;
    color: #37474f;
    font-size: 0.95rem;
}

.stRadio > div[data-checked="true"] label {
    color: #1565c0;
    font-weight: 600;
}

/* Sidebar sections */
div[data-testid="stSidebar"] .element-container {
    margin-bottom: 0.5rem;
}

div[data-testid="stSidebar"] h3, div[data-testid="stSidebar"] h4 {
    color: #1565c0;
    font-weight: 600;
}

/* Selectbox styling for Add Stocks page */
.stSelectbox > div > div {
    background-color: white;
    border-radius: 6px;
    border: 2px solid #e0e0e0;
}

.stSelectbox > div > div:focus-within {
    border-color: #1976d2;
    box-shadow: 0 0 0 1px #1976d2;
}
</style>
""", unsafe_allow_html=True)

# Load Saudi stocks database
@st.cache_data
def load_saudi_stocks_database():
    """Load Saudi stocks database"""
    try:
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Stock database not found. Please run the setup first.")
        return {}

# Get stock data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_stock_data(symbol, period="1y"):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        if data.empty:
            return None
        
        # Get current info
        info = stock.info
        current_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100
        
        return {
            'data': data,
            'current_price': current_price,
            'change': change,
            'change_pct': change_pct,
            'info': info
        }
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None

# Portfolio functions
def load_portfolio():
    """Load user portfolio"""
    try:
        with open('user_portfolio.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_portfolio(portfolio):
    """Save user portfolio"""
    with open('user_portfolio.json', 'w') as f:
        json.dump(portfolio, f, indent=2)

def add_stock_to_portfolio(symbol, quantity, purchase_price):
    """Add stock to portfolio"""
    portfolio = load_portfolio()
    
    # Check if stock already exists
    for stock in portfolio:
        if stock['symbol'] == symbol:
            # Update existing stock
            total_value = (stock['quantity'] * stock['purchase_price']) + (quantity * purchase_price)
            total_quantity = stock['quantity'] + quantity
            stock['purchase_price'] = total_value / total_quantity
            stock['quantity'] = total_quantity
            save_portfolio(portfolio)
            return True
    
    # Add new stock
    portfolio.append({
        'symbol': symbol,
        'quantity': quantity,
        'purchase_price': purchase_price,
        'date_added': datetime.now().strftime('%Y-%m-%d')
    })
    save_portfolio(portfolio)
    return True

def remove_stock_from_portfolio(symbol):
    """Remove stock from portfolio"""
    portfolio = load_portfolio()
    portfolio = [stock for stock in portfolio if stock['symbol'] != symbol]
    save_portfolio(portfolio)

# AI Integration Functions
def display_ai_signals(stocks_db):
    """Display AI trading signals"""
    if not AI_AVAILABLE:
        st.warning("🤖 AI features not available. Install AI dependencies to enable.")
        return
    
    st.markdown("## 🤖 AI Trading Signals")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Generate AI Signals", type="primary"):
            with st.spinner("🤖 AI analyzing market data..."):
                try:
                    # Get stocks from database for AI analysis
                    available_stocks = list(stocks_db.keys())
                    if len(available_stocks) >= 3:
                        # Use actual stocks from database
                        popular_stocks = [f"{code}.SR" for code in available_stocks[:5]]
                    else:
                        # Fallback to well-known Saudi stocks
                        popular_stocks = ['2030.SR', '1120.SR', '2010.SR']
                    
                    signals = get_ai_signals(popular_stocks, stocks_db)
                    st.session_state['ai_signals'] = signals
                    st.success(f"✅ Generated {len(signals)} AI signals")
                except Exception as e:
                    st.error(f"❌ AI signal generation failed: {e}")
    
    # Display signals if available
    if 'ai_signals' in st.session_state:
        signals = st.session_state['ai_signals']
        
        for signal in signals:
            # Signal type styling
            if signal.signal_type == 'BUY':
                signal_color = "#00C851"
                signal_emoji = "🟢"
            elif signal.signal_type == 'SELL':
                signal_color = "#ff4444"
                signal_emoji = "🔴"
            else:
                signal_color = "#ffbb33"
                signal_emoji = "🟡"
            
            with st.container():
                st.markdown(f"""
                <div class="ai-signal-card" style="background: linear-gradient(135deg, {signal_color}20 0%, {signal_color}40 100%); border-left: 4px solid {signal_color};">
                    <h3>{signal_emoji} {signal.company_name}</h3>
                    <p><strong>Symbol:</strong> {signal.symbol}</p>
                    <div style="display: flex; justify-content: space-between; margin: 1rem 0;">
                        <div>
                            <h4 style="color: {signal_color};">{signal.signal_type}</h4>
                            <p><strong>Confidence:</strong> {signal.confidence:.1%}</p>
                            <p><strong>Risk Level:</strong> {signal.risk_level}</p>
                        </div>
                        <div>
                            <p><strong>Current Price:</strong> {signal.current_price:.2f} SAR</p>
                            <p><strong>Predicted Price:</strong> {signal.predicted_price:.2f} SAR</p>
                            <p><strong>Expected Return:</strong> {signal.expected_return:+.1f}%</p>
                        </div>
                    </div>
                    <p><strong>AI Reasoning:</strong> {signal.reasoning}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Progress bars
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Confidence Level**")
                    st.progress(signal.confidence)
                with col2:
                    st.markdown("**Risk Level**")
                    risk_value = 0.3 if signal.risk_level == 'LOW' else 0.6 if signal.risk_level == 'MEDIUM' else 0.9
                    st.progress(risk_value)
                
                st.markdown("---")
    else:
        st.info("Click 'Generate AI Signals' to see AI-powered trading recommendations")

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>✨ TADAWUL NEXUS ✨</h1>
        <p>Next-Generation Saudi Stock Intelligence Platform</p>
        <p><strong>Saudi Stock Exchange (Tadawul) • Real-time Data • AI-Powered Insights</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    stocks_db = load_saudi_stocks_database()
    
    # Sidebar Navigation
    with st.sidebar:
        # Title Section
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <h3 style="color: #1e88e5; margin: 0; font-weight: 600;">📊 Navigation</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Main Navigation Section
        st.markdown("**Choose a page:**")
        selected_page = st.radio(
            "Navigation",
            [
                "🏠 Portfolio Overview",
                "➕ Add Stocks", 
                "🔍 Stock Search",
                "🤖 AI Signals",
                "📊 Analytics",
                "📁 Import/Export"
            ],
            index=0,
            key="main_nav",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Get Started Section
        st.markdown("""
        <div style="background: #e3f2fd; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="color: #1565c0; margin: 0 0 0.5rem 0; font-size: 1rem;">🚀 Get Started</h4>
            <p style="margin: 0; font-size: 0.85rem; color: #424242;">Add your first stock to start tracking your portfolio!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # About Section
        st.markdown("""
        <div style="margin-top: 2rem;">
            <h4 style="color: #1565c0; margin: 0 0 0.5rem 0; font-size: 1rem;">📋 About</h4>
            <div style="font-size: 0.8rem; color: #666; line-height: 1.4;">
                <strong>TADAWUL NEXUS</strong><br>
                Portfolio Management +<br>
                AI Trading Platform
            </div>
            <div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem; line-height: 1.3;">
                🇸🇦 Tadawul Stocks • Real-time Data • AI Insights
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats in sidebar
        portfolio = load_portfolio()
        if portfolio:
            st.markdown("### 📈 Quick Stats")
            total_stocks = len(portfolio)
            st.metric("Total Stocks", total_stocks)
            
            # Calculate total value quickly
            total_value = 0
            for stock in portfolio:
                try:
                    stock_info = get_stock_data(stock['symbol'])
                    if stock_info:
                        total_value += stock_info['current_price'] * stock['quantity']
                except:
                    pass
            
            if total_value > 0:
                st.metric("Portfolio Value", f"{total_value:.0f} SAR")
        else:
            st.markdown("### 🚀 Get Started")
            st.info("Add your first stock to start tracking your portfolio!")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("**TADAWUL NEXUS**")
        st.markdown("Portfolio Management + AI Trading Platform")
        st.markdown("🇸🇦 Tadawul Stocks • Real-time Data • AI Insights")
    
    
    # Portfolio Overview Page
    if selected_page == "🏠 Portfolio Overview":
        st.markdown("## 📈 Portfolio Overview")
        
        portfolio = load_portfolio()
        
        if not portfolio:
            st.info("Your portfolio is empty. Add some stocks to get started!")
            
            # Show quick start guide
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🚀 Quick Start")
                st.markdown("""
                1. **Add Stocks**: Use "➕ Add Stocks" to browse complete TASI database
                2. **Search Database**: Explore available stocks in "🔍 Stock Search"  
                3. **Get AI Signals**: Try "🤖 AI Signals" for trading recommendations
                4. **Import Data**: Use "📁 Import/Export" to upload an existing portfolio
                """)
            
            with col2:
                st.markdown("### 📊 Saudi Stock Market")
                st.markdown(f"**Available Stocks**: {len(stocks_db)} companies")
                st.markdown("**Sectors**: Banking, Energy, Petrochemicals, Telecommunications")
                st.markdown("**Real-time Data**: Live prices from Tadawul")
                st.markdown("**AI Features**: Machine learning predictions")
        else:
            # Calculate portfolio metrics
            total_value = 0
            total_cost = 0
            portfolio_data = []
            
            for stock in portfolio:
                stock_info = get_stock_data(stock['symbol'])
                if stock_info:
                    current_value = stock_info['current_price'] * stock['quantity']
                    cost = stock['purchase_price'] * stock['quantity']
                    profit_loss = current_value - cost
                    profit_loss_pct = (profit_loss / cost) * 100
                    
                    total_value += current_value
                    total_cost += cost
                    
                    portfolio_data.append({
                        'Symbol': stock['symbol'],
                        'Company': stocks_db.get(stock['symbol'].replace('.SR', ''), {}).get('name_en', 'Unknown'),
                        'Quantity': stock['quantity'],
                        'Purchase Price': f"{stock['purchase_price']:.2f} SAR",
                        'Current Price': f"{stock_info['current_price']:.2f} SAR",
                        'Current Value': f"{current_value:.2f} SAR",
                        'Profit/Loss': f"{profit_loss:+.2f} SAR",
                        'P/L %': f"{profit_loss_pct:+.1f}%"
                    })
            
            # Portfolio summary
            total_profit_loss = total_value - total_cost
            total_profit_loss_pct = (total_profit_loss / total_cost) * 100 if total_cost > 0 else 0
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{total_value:.2f} SAR</h3>
                    <p>Total Value</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3>{total_cost:.2f} SAR</h3>
                    <p>Total Cost</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                color = "green" if total_profit_loss >= 0 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {color}">{total_profit_loss:+.2f} SAR</h3>
                    <p>Profit/Loss</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                color = "green" if total_profit_loss_pct >= 0 else "red"
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: {color}">{total_profit_loss_pct:+.1f}%</h3>
                    <p>Return %</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Portfolio table
            if portfolio_data:
                st.markdown("### 📋 Portfolio Details")
                df = pd.DataFrame(portfolio_data)
                st.dataframe(df, use_container_width=True)
            
            # Portfolio chart
            if len(portfolio_data) > 0:
                st.markdown("### 📊 Portfolio Allocation")
                values = [float(item['Current Value'].replace(' SAR', '')) for item in portfolio_data]
                labels = [item['Symbol'] for item in portfolio_data]
                
                fig = px.pie(values=values, names=labels, title="Portfolio Allocation by Value")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
    
    # Add Stocks Page
    elif selected_page == "➕ Add Stocks":
        st.markdown("## ➕ Add Stocks to Portfolio")
        st.markdown("Build your portfolio by selecting stocks from the Saudi Stock Exchange (Tadawul)")
        
        # Create three columns for better layout
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("### 🎯 Select Stock")
            
            # Create dropdown list of all stocks
            stock_options = []
            stock_mapping = {}
            
            # Sort stocks by name for better UX
            sorted_stocks = sorted(stocks_db.items(), key=lambda x: x[1]['name_en'])
            
            for code, stock in sorted_stocks:
                display_name = f"{stock['name_en']} ({stock['symbol']}) - {stock.get('sector', 'N/A')}"
                stock_options.append(display_name)
                stock_mapping[display_name] = (code, stock)
            
            # Dropdown selection
            selected_stock_display = st.selectbox(
                "Choose a stock from TASI:",
                [""] + stock_options,
                index=0,
                help="Select a stock from the complete list of Saudi Stock Exchange companies"
            )
            
            if selected_stock_display:
                code, selected_stock_data = stock_mapping[selected_stock_display]
                
                # Display stock details
                st.markdown("### 📊 Stock Information")
                
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.markdown(f"**Company Name (EN):** {selected_stock_data['name_en']}")
                    st.markdown(f"**Company Name (AR):** {selected_stock_data.get('name_ar', 'N/A')}")
                    st.markdown(f"**Symbol:** {selected_stock_data['symbol']}")
                
                with info_col2:
                    st.markdown(f"**Code:** {code}")
                    st.markdown(f"**Sector:** {selected_stock_data.get('sector', 'N/A')}")
                    
                    # Try to get current price
                    try:
                        import yfinance as yf
                        ticker = yf.Ticker(f"{selected_stock_data['symbol']}.SR")
                        hist = ticker.history(period="1d")
                        if not hist.empty:
                            current_price = hist['Close'].iloc[-1]
                            st.markdown(f"**Current Price:** {current_price:.2f} SAR")
                        else:
                            st.markdown("**Current Price:** Data not available")
                    except:
                        st.markdown("**Current Price:** Loading...")
                
                # Quick actions
                st.markdown("### ⚡ Quick Actions")
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    if st.button("📈 View Chart", key="view_chart"):
                        st.session_state['chart_stock'] = selected_stock_data['symbol']
                        st.success(f"Chart view for {selected_stock_data['name_en']} will be shown in Stock Search page")
                
                with action_col2:
                    if st.button("🤖 Get AI Signal", key="get_signal"):
                        st.session_state['ai_stock'] = selected_stock_data['symbol']
                        st.success(f"AI signal for {selected_stock_data['name_en']} will be shown in AI Signals page")
                
                with action_col3:
                    if st.button("➕ Quick Add", key="quick_add"):
                        st.session_state['selected_stock'] = selected_stock_data['symbol']
                        st.session_state['selected_name'] = selected_stock_data['name_en']
                        st.success("Stock selected! Add details in the panel →")
        
        with col2:
            if 'selected_stock' in st.session_state:
                st.markdown("### 📝 Add Stock")
                st.write(f"**Selected:** {st.session_state['selected_name']}")
                st.write(f"**Symbol:** {st.session_state['selected_stock']}")
                
                # Get current price
                stock_info = get_stock_data(st.session_state['selected_stock'])
                if stock_info:
                    st.write(f"**Current Price:** {stock_info['current_price']:.2f} SAR")
                
                quantity = st.number_input("Quantity:", min_value=1, value=1)
                purchase_price = st.number_input("Purchase Price (SAR):", 
                                               min_value=0.01, 
                                               value=stock_info['current_price'] if stock_info else 1.0,
                                               format="%.2f")
                
                if st.button("✅ Add to Portfolio", type="primary"):
                    if add_stock_to_portfolio(st.session_state['selected_stock'], quantity, purchase_price):
                        st.success(f"✅ Added {quantity} shares of {st.session_state['selected_name']} to portfolio!")
                        del st.session_state['selected_stock']
                        del st.session_state['selected_name']
                        st.rerun()
            else:
                st.info("Search for a stock above or select from popular stocks to add to your portfolio.")
                
                st.markdown("### 📊 Quick Stats")
                st.metric("Available Stocks", len(stocks_db))
                sectors = list(set(stock.get('sector', 'Other') for stock in stocks_db.values()))
                st.metric("Sectors", len(sectors))
    
    # Stock Search Page
    elif selected_page == "🔍 Stock Search":
        st.markdown("## 🔍 Stock Database Explorer")
        
        # Sector filter
        sectors = list(set(stock.get('sector', 'Other') for stock in stocks_db.values()))
        selected_sector = st.selectbox("Filter by Sector:", ["All"] + sorted(sectors))
        
        # Display stocks
        filtered_stocks = []
        for code, stock in stocks_db.items():
            if selected_sector == "All" or stock.get('sector') == selected_sector:
                filtered_stocks.append({
                    'Code': code,
                    'Symbol': stock['symbol'],
                    'Company (EN)': stock['name_en'],
                    'Company (AR)': stock.get('name_ar', ''),
                    'Sector': stock.get('sector', 'Other')
                })
        
        df = pd.DataFrame(filtered_stocks)
        st.dataframe(df, use_container_width=True)
        
        st.info(f"📊 Showing {len(filtered_stocks)} stocks from Saudi Stock Exchange (Tadawul)")
    
    # AI Signals Page
    elif selected_page == "🤖 AI Signals":
        display_ai_signals(stocks_db)
    
    # Analytics Page
    elif selected_page == "📊 Analytics":
        st.markdown("## 📊 Portfolio Analytics")
        
        portfolio = load_portfolio()
        if not portfolio:
            st.info("Add stocks to your portfolio to see analytics.")
        else:
            # Select stock for detailed analysis
            stock_symbols = [stock['symbol'] for stock in portfolio]
            selected_symbol = st.selectbox("Select stock for detailed analysis:", stock_symbols)
            
            if selected_symbol:
                stock_info = get_stock_data(selected_symbol, period="6mo")
                if stock_info:
                    # Price chart
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=stock_info['data'].index,
                        y=stock_info['data']['Close'],
                        mode='lines',
                        name='Price',
                        line=dict(color='#00C851', width=2)
                    ))
                    
                    fig.update_layout(
                        title=f"{selected_symbol} - 6 Month Price Chart",
                        xaxis_title="Date",
                        yaxis_title="Price (SAR)",
                        template="plotly_white"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Technical indicators
                    col1, col2, col3 = st.columns(3)
                    
                    data = stock_info['data']
                    current_price = stock_info['current_price']
                    
                    # Simple moving averages
                    sma_20 = data['Close'].rolling(20).mean().iloc[-1]
                    sma_50 = data['Close'].rolling(50).mean().iloc[-1]
                    
                    with col1:
                        st.metric("Current Price", f"{current_price:.2f} SAR", 
                                 f"{stock_info['change']:+.2f} ({stock_info['change_pct']:+.1f}%)")
                    
                    with col2:
                        st.metric("20-day SMA", f"{sma_20:.2f} SAR")
                    
                    with col3:
                        st.metric("50-day SMA", f"{sma_50:.2f} SAR")
    
    # Import/Export Page
    elif selected_page == "📁 Import/Export":
        st.markdown("## 📁 Portfolio Import/Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📥 Import Portfolio")
            uploaded_file = st.file_uploader("Upload Excel file:", type=['xlsx', 'xls'])
            
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.write("Preview:")
                    st.dataframe(df.head())
                    
                    if st.button("Import Portfolio"):
                        # Process and import
                        portfolio = []
                        for _, row in df.iterrows():
                            portfolio.append({
                                'symbol': row.get('Symbol', ''),
                                'quantity': row.get('Quantity', 0),
                                'purchase_price': row.get('Purchase_Price', 0),
                                'date_added': datetime.now().strftime('%Y-%m-%d')
                            })
                        save_portfolio(portfolio)
                        st.success("✅ Portfolio imported successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error importing file: {e}")
        
        with col2:
            st.markdown("### 📤 Export Portfolio")
            portfolio = load_portfolio()
            
            if portfolio:
                # Create Excel file
                df = pd.DataFrame(portfolio)
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Portfolio')
                
                st.download_button(
                    label="📄 Download Portfolio (Excel)",
                    data=output.getvalue(),
                    file_name=f"portfolio_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("No portfolio data to export.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        ✨ <strong>TADAWUL NEXUS</strong> | Built for Tadawul Investors<br>
        Real-time data • AI-powered insights • Professional portfolio management
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
