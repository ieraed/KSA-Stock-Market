"""
🚀 TADAWUL NEXUS COMPLETE - OPTIMIZED FOR SPEED 🚀
Fast-Loading Complete Saudi Stock Portfolio Management Platform
- Immediate UI display
- Lazy feature loading
- All features preserved
- CSS loaded after content
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configure for maximum speed - UI shows immediately
st.set_page_config(
    page_title="TADAWUL NEXUS 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show immediate loading placeholder
st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
">
    <h1>🚀 TADAWUL NEXUS COMPLETE</h1>
    <p>Professional Saudi Stock Portfolio Management Platform</p>
    <p><em>Loading optimized interface...</em></p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for performance
if 'app_loaded' not in st.session_state:
    st.session_state.app_loaded = False
if 'stocks_db' not in st.session_state:
    st.session_state.stocks_db = None
if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = None

# Fast cached functions
@st.cache_data(ttl=3600, show_spinner=False)
def load_saudi_stocks_database():
    """Ultra-fast cached stock database loader"""
    try:
        with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"stocks": {}}

@st.cache_data(ttl=300, show_spinner=False)  
def simulate_current_prices(stocks_db):
    """Generate simulated prices for demo purposes"""
    np.random.seed(42)  # Consistent prices
    prices = {}
    
    for symbol, info in stocks_db.get("stocks", {}).items():
        base_price = 50 + (hash(symbol) % 200)
        change_pct = np.random.normal(0, 2)
        current_price = base_price * (1 + change_pct/100)
        prices[symbol] = {
            'current_price': round(current_price, 2),
            'change_pct': round(change_pct, 2),
            'volume': np.random.randint(10000, 1000000)
        }
    return prices

@st.cache_data(ttl=60, show_spinner=False)
def load_portfolio_template():
    """Load portfolio with caching"""
    try:
        return pd.read_excel('portfolio_template.xlsx')
    except:
        return pd.DataFrame()

# Enhanced Portfolio Display Function
def display_enhanced_portfolio_view(portfolio_df, stock_prices, stocks_db):
    """Enhanced portfolio view with all calculations"""
    if portfolio_df.empty:
        st.warning("📄 No portfolio data found. Please upload a portfolio template.")
        return
    
    st.subheader("📊 Portfolio Overview")
    
    # Calculate enhanced metrics
    portfolio_df['Current_Price'] = portfolio_df['Symbol'].apply(
        lambda x: stock_prices.get(x, {}).get('current_price', 0)
    )
    portfolio_df['Market_Value'] = portfolio_df['Shares'] * portfolio_df['Current_Price']
    portfolio_df['Total_Cost'] = portfolio_df['Shares'] * portfolio_df['Average_Price']
    portfolio_df['P&L'] = portfolio_df['Market_Value'] - portfolio_df['Total_Cost']
    portfolio_df['P&L_Pct'] = ((portfolio_df['Current_Price'] - portfolio_df['Average_Price']) / portfolio_df['Average_Price'] * 100).round(2)
    
    # Add company names
    portfolio_df['Company_Name'] = portfolio_df['Symbol'].apply(
        lambda x: stocks_db.get("stocks", {}).get(x, {}).get('name', 'Unknown')
    )
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Market Value", f"SAR {portfolio_df['Market_Value'].sum():,.2f}")
    with col2:
        st.metric("📈 Total Cost", f"SAR {portfolio_df['Total_Cost'].sum():,.2f}")
    with col3:
        total_pnl = portfolio_df['P&L'].sum()
        st.metric("💹 Total P&L", f"SAR {total_pnl:,.2f}", f"{(total_pnl/portfolio_df['Total_Cost'].sum()*100):.2f}%")
    with col4:
        st.metric("📊 Total Positions", len(portfolio_df))
    
    # Enhanced table display
    display_df = portfolio_df[['Symbol', 'Company_Name', 'Shares', 'Average_Price', 'Current_Price', 'Market_Value', 'P&L', 'P&L_Pct']].copy()
    display_df.columns = ['Symbol', 'Company', 'Shares', 'Avg Price', 'Current Price', 'Market Value', 'P&L (SAR)', 'P&L (%)']
    
    # Format for display
    for col in ['Avg Price', 'Current Price', 'Market Value', 'P&L (SAR)']:
        display_df[col] = display_df[col].apply(lambda x: f"{x:,.2f}")
    display_df['P&L (%)'] = display_df['P&L (%)'].apply(lambda x: f"{x:.2f}%")
    display_df['Shares'] = display_df['Shares'].apply(lambda x: f"{x:,}")
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Performance visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Portfolio allocation pie chart
        fig_pie = px.pie(
            portfolio_df, 
            values='Market_Value', 
            names='Company_Name',
            title="Portfolio Allocation by Market Value"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # P&L bar chart
        fig_bar = px.bar(
            portfolio_df, 
            x='Company_Name', 
            y='P&L',
            color='P&L',
            color_continuous_scale=['red', 'yellow', 'green'],
            title="Profit & Loss by Position"
        )
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)

# Main navigation
st.sidebar.title("🚀 TADAWUL NEXUS")
st.sidebar.markdown("*Professional Saudi Stock Platform*")

page = st.sidebar.radio(
    "Navigate:",
    ["🏠 Dashboard", "📊 Portfolio", "🔍 Stock Analysis", "💰 Trading Signals", "⚙️ Settings"]
)

# Load data with caching
if not st.session_state.app_loaded:
    with st.spinner("Loading optimized data..."):
        st.session_state.stocks_db = load_saudi_stocks_database()
        st.session_state.app_loaded = True

stocks_db = st.session_state.stocks_db
stock_prices = simulate_current_prices(stocks_db)

# Clear loading placeholder and show content
st.empty()

# Main content based on navigation
if page == "🏠 Dashboard":
    st.title("🏠 Portfolio Dashboard")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Market Status", "Open", "▲ Active Trading")
    with col2:
        st.metric("🕐 Last Updated", datetime.now().strftime("%H:%M:%S"))
    with col3:
        st.metric("📊 Tracked Stocks", len(stocks_db.get("stocks", {})))
    with col4:
        st.metric("💹 Active Positions", "Loading...")
    
    # Recent market activity simulation
    st.subheader("📊 Market Activity")
    
    # Create sample market data
    sample_stocks = list(stocks_db.get("stocks", {}).keys())[:10]
    market_data = []
    
    for symbol in sample_stocks:
        price_info = stock_prices.get(symbol, {})
        market_data.append({
            'Symbol': symbol,
            'Company': stocks_db.get("stocks", {}).get(symbol, {}).get('name', 'Unknown'),
            'Price': price_info.get('current_price', 0),
            'Change %': price_info.get('change_pct', 0),
            'Volume': price_info.get('volume', 0)
        })
    
    market_df = pd.DataFrame(market_data)
    if not market_df.empty:
        st.dataframe(market_df, use_container_width=True)

elif page == "📊 Portfolio":
    st.title("📊 Portfolio Management")
    
    # Portfolio upload/management
    uploaded_file = st.file_uploader(
        "📁 Upload Portfolio Excel File", 
        type=['xlsx', 'xls'],
        help="Upload your portfolio template file"
    )
    
    if uploaded_file:
        try:
            portfolio_df = pd.read_excel(uploaded_file)
            st.session_state.portfolio_data = portfolio_df
            st.success("✅ Portfolio uploaded successfully!")
        except Exception as e:
            st.error(f"❌ Error loading portfolio: {str(e)}")
    
    # Load existing portfolio
    if st.session_state.portfolio_data is None:
        portfolio_df = load_portfolio_template()
        if not portfolio_df.empty:
            st.session_state.portfolio_data = portfolio_df
    
    # Display portfolio
    if st.session_state.portfolio_data is not None and not st.session_state.portfolio_data.empty:
        display_enhanced_portfolio_view(st.session_state.portfolio_data, stock_prices, stocks_db)
    else:
        st.info("📋 No portfolio loaded. Please upload a portfolio file or ensure portfolio_template.xlsx exists.")

elif page == "🔍 Stock Analysis":
    st.title("🔍 Stock Analysis")
    
    # Stock search and analysis
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Search Stocks")
        search_term = st.text_input("🔎 Search by symbol or name")
        
        # Filter stocks based on search
        filtered_stocks = {}
        if search_term:
            for symbol, info in stocks_db.get("stocks", {}).items():
                if (search_term.lower() in symbol.lower() or 
                    search_term.lower() in info.get('name', '').lower()):
                    filtered_stocks[symbol] = info
        else:
            filtered_stocks = dict(list(stocks_db.get("stocks", {}).items())[:20])
        
        # Display filtered stocks
        for symbol, info in filtered_stocks.items():
            price_info = stock_prices.get(symbol, {})
            current_price = price_info.get('current_price', 0)
            change_pct = price_info.get('change_pct', 0)
            
            color = "🟢" if change_pct >= 0 else "🔴"
            st.write(f"{color} **{symbol}** - {info.get('name', 'Unknown')}")
            st.write(f"💰 SAR {current_price:.2f} ({change_pct:+.2f}%)")
            st.write("---")
    
    with col2:
        st.subheader("Stock Details")
        
        selected_symbol = st.selectbox(
            "Select a stock for detailed analysis:",
            options=list(filtered_stocks.keys()) if filtered_stocks else [],
            index=0 if filtered_stocks else None
        )
        
        if selected_symbol:
            stock_info = stocks_db.get("stocks", {}).get(selected_symbol, {})
            price_info = stock_prices.get(selected_symbol, {})
            
            st.markdown(f"### {stock_info.get('name', 'Unknown')} ({selected_symbol})")
            
            # Stock metrics
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Current Price", f"SAR {price_info.get('current_price', 0):.2f}")
            with col_b:
                st.metric("Daily Change", f"{price_info.get('change_pct', 0):+.2f}%")
            with col_c:
                st.metric("Volume", f"{price_info.get('volume', 0):,}")
            
            # Simulated price chart
            dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
            np.random.seed(hash(selected_symbol) % 1000)
            prices = [price_info.get('current_price', 50)]
            
            for _ in range(29):
                change = np.random.normal(0, 0.02)
                prices.append(prices[-1] * (1 + change))
            
            chart_df = pd.DataFrame({
                'Date': dates,
                'Price': prices[::-1]  # Reverse to show chronological order
            })
            
            fig = px.line(chart_df, x='Date', y='Price', title=f"{selected_symbol} - 30 Day Price Chart")
            st.plotly_chart(fig, use_container_width=True)

elif page == "💰 Trading Signals":
    st.title("💰 AI Trading Signals")
    
    st.info("🤖 AI-powered trading signals coming soon!")
    
    # Placeholder for trading signals
    st.subheader("📊 Signal Dashboard")
    
    # Sample signals
    signals_data = [
        {"Symbol": "2222", "Signal": "BUY", "Confidence": "85%", "Target": "45.50", "Stop": "40.00"},
        {"Symbol": "2010", "Signal": "HOLD", "Confidence": "72%", "Target": "185.00", "Stop": "170.00"},
        {"Symbol": "1180", "Signal": "SELL", "Confidence": "78%", "Target": "28.50", "Stop": "32.00"},
    ]
    
    signals_df = pd.DataFrame(signals_data)
    st.dataframe(signals_df, use_container_width=True)

elif page == "⚙️ Settings":
    st.title("⚙️ Application Settings")
    
    st.subheader("🎨 Display Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox("🌙 Theme", ["Dark", "Light", "Auto"])
        st.selectbox("💱 Currency", ["SAR", "USD", "EUR"])
        st.slider("📊 Refresh Rate (seconds)", 5, 60, 30)
    
    with col2:
        st.checkbox("🔔 Enable Notifications", True)
        st.checkbox("📧 Email Alerts", False)
        st.checkbox("📱 Mobile Sync", True)
    
    st.subheader("💾 Data Management")
    
    if st.button("🔄 Refresh Stock Database"):
        st.session_state.stocks_db = None
        st.session_state.app_loaded = False
        st.rerun()
    
    if st.button("📤 Export Portfolio"):
        if st.session_state.portfolio_data is not None:
            st.download_button(
                "💾 Download Portfolio CSV",
                st.session_state.portfolio_data.to_csv(index=False),
                "portfolio_export.csv",
                "text/csv"
            )

# Load CSS at the end for styling (after content is displayed)
if st.session_state.app_loaded:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0f1419 0%, #243447 50%, #0f1419 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Enhanced Tables */
        .stDataFrame {
            background: linear-gradient(145deg, 
                rgba(147, 51, 234, 0.95) 0%, 
                rgba(124, 58, 237, 0.95) 25%, 
                rgba(139, 92, 246, 0.95) 50%, 
                rgba(168, 85, 247, 0.95) 75%, 
                rgba(147, 51, 234, 0.95) 100%) !important;
            border-radius: 20px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Modern Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(0, 206, 76, 0.1) 0%, rgba(0, 158, 56, 0.1) 100%);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(0, 206, 76, 0.2);
        }
        
        /* Sidebar styling */
        .sidebar .element-container .stRadio > div {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 0.5rem;
            margin: 0.3rem 0;
        }
        
        /* Charts */
        .stPlotlyChart {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.8rem;'>
        🚀 TADAWUL NEXUS COMPLETE - Optimized for Speed | 
        Built with ❤️ for Saudi Stock Market | 
        Last Updated: {time}
    </div>
    """.format(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
