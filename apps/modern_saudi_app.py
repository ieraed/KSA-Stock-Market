"""
✨ TADAWUL NEXUS - Modern Professional Edition ✨
Next-Generation Saudi Stock Intelligence Platform

A professional, modern interface inspired by leading trading platforms
with Saudi-themed design elements and maximum usability.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime as dt, timedelta
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Utility functions
def normalize_broker_name(broker_name):
    """Normalize broker names for consistency"""
    if not broker_name:
        return 'Not Set'
    
    broker_lower = broker_name.lower().strip()
    
    # BSF Capital / Fransi Capital standardization
    if any(term in broker_lower for term in ['bsf', 'fransi']):
        return 'BSF Capital'
    
    # Al Inma Capital standardization
    if any(term in broker_lower for term in ['inma', 'al inma']):
        return 'Al Inma Capital'
    
    # Al Rajhi Capital variations
    if 'rajhi' in broker_lower:
        return 'Al Rajhi Capital'
    
    # NCB Capital / AlAhli Capital variations
    if any(term in broker_lower for term in ['ncb', 'alahli', 'al ahli']):
        return 'NCB Capital'
    
    # Samba Capital variations
    if 'samba' in broker_lower:
        return 'Samba Capital'
    
    # Al Jazira Capital variations
    if 'jazira' in broker_lower:
        return 'Al Jazira Capital'
    
    return broker_name.title()

def normalize_symbol(symbol):
    """Normalize stock symbols to prevent duplicates"""
    if not symbol:
        return symbol
    
    normalized = symbol.strip().upper()
    if normalized.endswith('.SR'):
        normalized = normalized[:-3]
    normalized = normalized.rstrip(' .')
    
    return normalized

# Configure page
st.set_page_config(
    page_title="✨ TADAWUL NEXUS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://tadawul.com.sa',
        'Report a bug': 'mailto:support@tadawulnexus.com',
        'About': "TADAWUL NEXUS - Professional Saudi Stock Intelligence Platform"
    }
)

# Modern Professional CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Modern professional dark trading platform background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f1419 0%,
        #1a2332 25%,
        #0f1419 50%,
        #243447 75%,
        #0f1419 100%
    );
    background-attachment: fixed;
    min-height: 100vh;
    position: relative;
}

/* Professional grid overlay effect */
.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 50px 50px;
    z-index: -1;
    pointer-events: none;
}

/* Trading charts effect at bottom */
.stApp::after {
    content: '';
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 200px;
    background: linear-gradient(
        to top,
        rgba(0, 200, 83, 0.05) 0%,
        rgba(0, 200, 83, 0.02) 50%,
        transparent 100%
    );
    background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 200"><path d="M0,180 L50,160 L100,140 L150,120 L200,100 L250,85 L300,70 L350,55 L400,45 L450,35 L500,40 L550,50 L600,65 L650,80 L700,95 L750,110 L800,125 L850,140 L900,155 L950,170 L1000,185 L1050,180 L1100,175 L1150,170 L1200,165" stroke="%2300c853" stroke-width="2" fill="none" opacity="0.3"/></svg>') bottom center/cover no-repeat;
    z-index: -1;
    pointer-events: none;
}

/* Modern glass morphism cards */
.main .block-container {
    background: rgba(255, 255, 255, 0.98) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 16px !important;
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.1),
        0 2px 8px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
    padding: 2rem !important;
    margin: 1rem !important;
    position: relative;
    z-index: 1;
}

/* Professional typography with maximum readability */
.main .block-container h1,
.main .block-container h2,
.main .block-container h3,
.main .block-container h4,
.main .block-container h5,
.main .block-container h6 {
    color: #1a202c !important;
    font-weight: 700 !important;
    text-shadow: none !important;
    margin: 1.5rem 0 1rem 0 !important;
    line-height: 1.2 !important;
}

.main .block-container h1 {
    font-size: 2.5rem !important;
    background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.main .block-container h2 {
    font-size: 2rem !important;
    color: #2d3748 !important;
}

.main .block-container h3 {
    font-size: 1.5rem !important;
    color: #4a5568 !important;
}

/* Professional text with perfect contrast */
.main .block-container p,
.main .block-container span,
.main .block-container div:not([data-testid]),
.main .block-container label {
    color: #2d3748 !important;
    font-weight: 500 !important;
    line-height: 1.6 !important;
    text-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
    border: none !important;
    margin: 0.25rem 0 !important;
}

/* Modern form elements */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background: rgba(255, 255, 255, 0.95) !important;
    color: #2d3748 !important;
    border: 2px solid rgba(226, 232, 240, 0.8) !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div:focus-within,
.stNumberInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: #00c851 !important;
    box-shadow: 0 0 0 3px rgba(0, 200, 81, 0.1) !important;
    outline: none !important;
}

/* Professional form labels */
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stDateInput label,
.stRadio label {
    color: #4a5568 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 8px !important;
}

/* Modern professional tab navigation */
.stRadio > div {
    display: flex;
    flex-direction: row;
    gap: 2px;
    background: rgba(241, 245, 249, 0.8);
    padding: 4px;
    border-radius: 12px;
    margin: 1.5rem 0;
    box-shadow: 
        0 4px 6px rgba(0, 0, 0, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
}

.stRadio > div label {
    background: transparent !important;
    color: #64748b !important;
    font-weight: 500 !important;
    padding: 12px 24px;
    border: none !important;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 14px;
    text-align: center;
    min-width: 120px;
    margin: 0;
    border-radius: 8px;
    text-shadow: none !important;
    position: relative;
    z-index: 1;
}

.stRadio > div label:hover {
    background: rgba(255, 255, 255, 0.6) !important;
    color: #1e293b !important;
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stRadio > div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(135deg, #00c851 0%, #00a844 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 
        0 4px 12px rgba(0, 200, 81, 0.4),
        0 2px 4px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
    z-index: 2;
}

/* Modern data tables */
.stDataFrame {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 
        0 4px 6px rgba(0, 0, 0, 0.05),
        0 1px 3px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(226, 232, 240, 0.8);
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(10px);
    margin: 1.5rem 0;
    transition: all 0.3s ease;
}

.stDataFrame:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 8px 25px rgba(0, 0, 0, 0.1),
        0 4px 12px rgba(0, 0, 0, 0.05);
    border-color: rgba(0, 200, 81, 0.3);
}

/* Modern table headers */
.stDataFrame thead th {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
    color: #1e293b !important;
    font-weight: 600 !important;
    padding: 1rem !important;
    text-align: center !important;
    font-size: 0.875rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    border-bottom: 2px solid #e2e8f0 !important;
    border-right: 1px solid #f1f5f9 !important;
}

/* Table rows */
.stDataFrame tbody td {
    padding: 0.875rem !important;
    border-bottom: 1px solid #f1f5f9 !important;
    border-right: 1px solid #f8fafc !important;
    color: #334155 !important;
    font-weight: 500 !important;
}

.stDataFrame tbody tr:hover {
    background: rgba(0, 200, 81, 0.05) !important;
}

/* Portfolio metrics cards */
div[data-testid="column"] {
    background: rgba(255, 255, 255, 0.7) !important;
    border-radius: 16px;
    padding: 1.5rem !important;
    margin: 0.5rem !important;
    box-shadow: 
        0 4px 6px rgba(0, 0, 0, 0.05),
        0 1px 3px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(226, 232, 240, 0.5);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

div[data-testid="column"]:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 8px 25px rgba(0, 0, 0, 0.1),
        0 4px 12px rgba(0, 0, 0, 0.05);
    background: rgba(255, 255, 255, 0.85) !important;
}

/* Professional header matching reference design */
.main-header {
    background: linear-gradient(135deg, #00c851 0%, #00a844 100%);
    color: white;
    padding: 2rem 3rem;
    border-radius: 20px;
    text-align: center;
    margin: 0 0 2rem 0;
    box-shadow: 
        0 8px 32px rgba(0, 200, 81, 0.3),
        0 2px 8px rgba(0, 0, 0, 0.1);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '🇸🇦';
    position: absolute;
    top: 1rem;
    right: 2rem;
    font-size: 2rem;
    opacity: 0.3;
}

.main-header h1 {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    background: none !important;
    color: white !important;
    padding: 0 !important;
    border: none !important;
}

.main-header p {
    color: rgba(255, 255, 255, 0.95) !important;
    font-weight: 500 !important;
    background: none !important;
    padding: 0 !important;
    border: none !important;
    margin: 0.5rem 0 !important;
}

/* Sidebar professional styling */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    border-right: 1px solid rgba(226, 232, 240, 0.8);
}

div[data-testid="stSidebar"] h3,
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] label {
    color: #1e293b !important;
    background: none !important;
    padding: 0.25rem 0 !important;
    border: none !important;
}

/* Enhanced buttons */
.stButton > button {
    background: linear-gradient(135deg, #00c851 0%, #00a844 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(0, 200, 81, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 200, 81, 0.4);
    background: linear-gradient(135deg, #00a844 0%, #007e33 100%);
}

/* Modern metrics display */
.stMetric {
    background: rgba(255, 255, 255, 0.8) !important;
    border-radius: 12px;
    padding: 1rem !important;
    border: 1px solid rgba(226, 232, 240, 0.5);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
}

.stMetric:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Cache functions for performance
@st.cache_data(ttl=900)
def load_saudi_stocks_database():
    """Load the Saudi stocks database with caching"""
    database_path = os.path.join("data", "saudi_stocks_database.json")
    if os.path.exists(database_path):
        with open(database_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

@st.cache_data(ttl=300)
def load_portfolio():
    """Load portfolio from file with caching"""
    portfolio_file = "data/portfolio.json"
    
    if os.path.exists(portfolio_file):
        try:
            with open(portfolio_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error("Portfolio file is corrupted. Please check the file.")
            return []
    return []

def save_portfolio(portfolio):
    """Save portfolio to file"""
    portfolio_file = "data/portfolio.json"
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    try:
        with open(portfolio_file, 'w', encoding='utf-8') as f:
            json.dump(portfolio, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving portfolio: {str(e)}")
        return False

@st.cache_data(ttl=300)
def calculate_portfolio_value(portfolio):
    """Calculate portfolio statistics with caching"""
    if not portfolio:
        return {
            'total_value': 0,
            'total_cost': 0,
            'total_gain_loss': 0,
            'total_gain_loss_percent': 0
        }
    
    total_value = 0
    total_cost = 0
    
    for stock in portfolio:
        quantity = stock.get('quantity', 0)
        purchase_price = stock.get('purchase_price', 0)
        current_price = stock.get('current_price', purchase_price)
        
        stock_value = quantity * current_price
        stock_cost = quantity * purchase_price
        
        total_value += stock_value
        total_cost += stock_cost
    
    total_gain_loss = total_value - total_cost
    total_gain_loss_percent = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percent': total_gain_loss_percent
    }

def main():
    """Main application function"""
    
    # Professional header
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
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1rem; background: linear-gradient(135deg, #00c851 0%, #00a844 100%); border-radius: 12px; color: white;">
            <h3 style="margin: 0; font-weight: 600; font-size: 1.2rem;">📊 TADAWUL NEXUS</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;">Portfolio & Trading Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        selected_page = st.selectbox(
            "Navigate to:",
            [
                "🏠 Portfolio Overview",
                "📈 Portfolio Setup",
                "📊 Market Intelligence",
                "🔧 Tools & Settings"
            ],
            index=0
        )
        
        # Portfolio stats in sidebar
        portfolio = load_portfolio()
        if portfolio:
            portfolio_stats = calculate_portfolio_value(portfolio)
            unique_companies = len(set(normalize_symbol(stock['symbol']) for stock in portfolio))
            
            st.markdown("---")
            st.markdown("### 📈 Portfolio Stats")
            st.metric("Holdings", f"{unique_companies} companies")
            st.metric("Total Value", f"{portfolio_stats['total_value']:,.0f} SAR")
            gain_loss = portfolio_stats['total_gain_loss']
            gain_loss_pct = portfolio_stats['total_gain_loss_percent']
            st.metric("P&L", f"{gain_loss:,.0f} SAR", f"{gain_loss_pct:.1f}%")
    
    # Main content based on selected page
    if selected_page == "🏠 Portfolio Overview":
        st.markdown("## 🏠 Portfolio Overview")
        
        portfolio = load_portfolio()
        
        if portfolio:
            # Portfolio summary
            portfolio_stats = calculate_portfolio_value(portfolio)
            unique_companies = len(set(normalize_symbol(stock['symbol']) for stock in portfolio))
            
            # Portfolio metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Holdings", f"{unique_companies} companies")
            with col2:
                st.metric("Portfolio Value", f"{portfolio_stats['total_value']:,.2f} SAR")
            with col3:
                st.metric("Total Cost", f"{portfolio_stats['total_cost']:,.2f} SAR")
            with col4:
                gain_loss = portfolio_stats['total_gain_loss']
                gain_loss_pct = portfolio_stats['total_gain_loss_percent']
                st.metric("P&L", f"{gain_loss:,.2f} SAR", f"{gain_loss_pct:.1f}%")
            
            st.markdown("---")
            
            # Portfolio view options
            st.markdown("### 📋 Your Holdings")
            
            # View toggle options
            col1, col2 = st.columns([3, 2])
            
            with col1:
                view_option = st.radio(
                    "Portfolio View:",
                    ["📊 All Holdings", "🏢 By Broker", "🔗 Consolidated View"],
                    horizontal=True
                )
            
            with col2:
                if view_option == "🏢 By Broker":
                    brokers = list(set(normalize_broker_name(stock.get('broker', 'Not Set')) for stock in portfolio))
                    brokers = [b for b in brokers if b]
                    if 'Not Set' in [normalize_broker_name(stock.get('broker', 'Not Set')) for stock in portfolio]:
                        brokers.append('Not Set')
                    
                    selected_broker = st.selectbox(
                        "Select Broker:",
                        options=["All Brokers"] + sorted(brokers)
                    )
            
            # Display portfolio data
            filtered_portfolio = portfolio.copy()
            
            if view_option == "🏢 By Broker" and 'selected_broker' in locals() and selected_broker != "All Brokers":
                filtered_portfolio = [stock for stock in portfolio 
                                    if normalize_broker_name(stock.get('broker', 'Not Set')) == selected_broker]
            
            if filtered_portfolio:
                # Create display DataFrame
                holdings_data = []
                
                if view_option == "🔗 Consolidated View":
                    # Group by symbol
                    consolidated = {}
                    for stock in filtered_portfolio:
                        symbol = normalize_symbol(stock['symbol'])
                        if symbol not in consolidated:
                            consolidated[symbol] = {
                                'symbol': stock['symbol'],
                                'company': stock.get('company', 'N/A'),
                                'quantity': 0,
                                'total_cost': 0,
                                'brokers': set()
                            }
                        
                        consolidated[symbol]['quantity'] += stock.get('quantity', 0)
                        consolidated[symbol]['total_cost'] += stock.get('quantity', 0) * stock.get('purchase_price', 0)
                        consolidated[symbol]['brokers'].add(normalize_broker_name(stock.get('broker', 'Not Set')))
                    
                    for symbol, data in consolidated.items():
                        current_price = data['total_cost'] / data['quantity'] if data['quantity'] > 0 else 0
                        current_value = data['quantity'] * current_price
                        gain_loss = current_value - data['total_cost']
                        gain_loss_pct = (gain_loss / data['total_cost'] * 100) if data['total_cost'] > 0 else 0
                        
                        holdings_data.append({
                            'Symbol': data['symbol'],
                            'Company': data['company'],
                            'Quantity': data['quantity'],
                            'Avg. Price': data['total_cost'] / data['quantity'] if data['quantity'] > 0 else 0,
                            'Current Value': current_value,
                            'P&L': gain_loss,
                            'P&L %': gain_loss_pct,
                            'Brokers': ', '.join(sorted(data['brokers']))
                        })
                else:
                    # Individual holdings
                    for stock in filtered_portfolio:
                        current_price = stock.get('current_price', stock.get('purchase_price', 0))
                        quantity = stock.get('quantity', 0)
                        purchase_price = stock.get('purchase_price', 0)
                        current_value = quantity * current_price
                        cost_basis = quantity * purchase_price
                        gain_loss = current_value - cost_basis
                        gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
                        
                        holdings_data.append({
                            'Symbol': stock['symbol'],
                            'Company': stock.get('company', 'N/A'),
                            'Quantity': quantity,
                            'Purchase Price': purchase_price,
                            'Current Price': current_price,
                            'Current Value': current_value,
                            'P&L': gain_loss,
                            'P&L %': gain_loss_pct,
                            'Broker': normalize_broker_name(stock.get('broker', 'Not Set')),
                            'Purchase Date': stock.get('purchase_date', 'N/A')
                        })
                
                if holdings_data:
                    df = pd.DataFrame(holdings_data)
                    
                    # Format numeric columns
                    numeric_cols = ['Purchase Price', 'Current Price', 'Current Value', 'P&L', 'Avg. Price']
                    for col in numeric_cols:
                        if col in df.columns:
                            df[col] = df[col].apply(lambda x: f"{x:,.2f} SAR" if pd.notnull(x) else "N/A")
                    
                    if 'P&L %' in df.columns:
                        df['P&L %'] = df['P&L %'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No holdings found for the selected criteria.")
            else:
                st.info("No holdings found for the selected broker.")
        else:
            st.info("📝 No portfolio data found. Go to Portfolio Setup to add your first stock!")
            if st.button("🚀 Set up Portfolio"):
                st.session_state.current_page = "📈 Portfolio Setup"
                st.rerun()
    
    elif selected_page == "📈 Portfolio Setup":
        st.markdown("## 📈 Portfolio Setup")
        
        # Portfolio management tabs
        tab1, tab2 = st.tabs(["➕ Add Stock", "📊 Import Data"])
        
        with tab1:
            st.markdown("### Add New Stock to Portfolio")
            
            stocks_db = load_saudi_stocks_database()
            
            if stocks_db:
                # Create stock options for selectbox
                stock_options = []
                for symbol, info in stocks_db.items():
                    name = info.get('name_en', info.get('name_ar', 'N/A'))
                    stock_options.append(f"{symbol} - {name}")
                
                # Form for adding stocks
                with st.form("add_stock_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        selected_stock = st.selectbox(
                            "Select Stock:",
                            options=[""] + sorted(stock_options),
                            help="Choose a stock from the Tadawul database"
                        )
                        
                        if selected_stock:
                            symbol = selected_stock.split(" - ")[0]
                            company_name = selected_stock.split(" - ")[1]
                        else:
                            symbol = ""
                            company_name = ""
                    
                    with col2:
                        quantity = st.number_input("Quantity:", min_value=1, value=100, step=1)
                    
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        purchase_price = st.number_input("Purchase Price (SAR):", min_value=0.01, value=50.0, step=0.01)
                    
                    with col4:
                        purchase_date = st.date_input("Purchase Date:", value=dt.now().date())
                    
                    # Broker selection
                    broker_name = st.selectbox(
                        "Broker:",
                        options=[
                            "BSF Capital",
                            "Al Inma Capital", 
                            "Al Rajhi Capital",
                            "NCB Capital",
                            "Samba Capital",
                            "Al Jazira Capital",
                            "Other"
                        ]
                    )
                    
                    if broker_name == "Other":
                        broker_name = st.text_input("Enter Broker Name:")
                    
                    # Submit button
                    submitted = st.form_submit_button("Add to Portfolio", use_container_width=True)
                    
                    if submitted and selected_stock and broker_name:
                        # Add stock to portfolio
                        portfolio = load_portfolio()
                        
                        new_stock = {
                            'symbol': symbol,
                            'company': company_name,
                            'quantity': quantity,
                            'purchase_price': purchase_price,
                            'current_price': purchase_price,  # Default to purchase price
                            'purchase_date': str(purchase_date),
                            'broker': broker_name
                        }
                        
                        portfolio.append(new_stock)
                        
                        if save_portfolio(portfolio):
                            st.success(f"✅ Added {quantity} shares of {symbol} to your portfolio!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save portfolio. Please try again.")
        
        with tab2:
            st.markdown("### Import Portfolio Data")
            st.info("📋 Upload a CSV or Excel file with your portfolio data")
            
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['csv', 'xlsx', 'xls'],
                help="File should contain columns: Symbol, Company, Quantity, Purchase Price, Purchase Date, Broker"
            )
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.markdown("#### Preview of uploaded data:")
                    st.dataframe(df.head(), use_container_width=True)
                    
                    if st.button("Import Data", use_container_width=True):
                        # Process and import data
                        portfolio = load_portfolio()
                        imported_count = 0
                        
                        for _, row in df.iterrows():
                            try:
                                new_stock = {
                                    'symbol': str(row.get('Symbol', '')).strip(),
                                    'company': str(row.get('Company', row.get('company', 'N/A'))).strip(),
                                    'quantity': int(row.get('Quantity', row.get('quantity', 0))),
                                    'purchase_price': float(row.get('Purchase Price', row.get('purchase_price', 0))),
                                    'current_price': float(row.get('Current Price', row.get('current_price', row.get('Purchase Price', row.get('purchase_price', 0))))),
                                    'purchase_date': str(row.get('Purchase Date', row.get('purchase_date', dt.now().date()))),
                                    'broker': normalize_broker_name(str(row.get('Broker', row.get('broker', 'Not Set'))))
                                }
                                
                                if new_stock['symbol'] and new_stock['quantity'] > 0:
                                    portfolio.append(new_stock)
                                    imported_count += 1
                            except Exception as e:
                                st.warning(f"⚠️ Skipped row due to error: {str(e)}")
                        
                        if save_portfolio(portfolio):
                            st.success(f"✅ Successfully imported {imported_count} stocks to your portfolio!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save imported portfolio data.")
                
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
    
    elif selected_page == "📊 Market Intelligence":
        st.markdown("## 📊 Market Intelligence")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Market Overview")
            st.info("📊 Market data integration coming soon...")
            
            # Demo data for visualization
            demo_data = {
                'TASI': 11500,
                'Change': '+2.3%',
                'Volume': '1.2B SAR'
            }
            
            for key, value in demo_data.items():
                st.metric(key, value)
        
        with col2:
            st.markdown("### 🔍 Stock Search")
            
            stocks_db = load_saudi_stocks_database()
            
            if stocks_db:
                search_term = st.text_input("Search for stocks:", placeholder="Enter symbol or company name")
                
                if search_term:
                    search_results = []
                    search_lower = search_term.lower()
                    
                    for symbol, info in stocks_db.items():
                        name_en = info.get('name_en', '').lower()
                        name_ar = info.get('name_ar', '').lower()
                        
                        if (search_lower in symbol.lower() or 
                            search_lower in name_en or 
                            search_lower in name_ar):
                            search_results.append({
                                'Symbol': symbol,
                                'Name (EN)': info.get('name_en', 'N/A'),
                                'Name (AR)': info.get('name_ar', 'N/A'),
                                'Sector': info.get('sector', 'N/A')
                            })
                    
                    if search_results:
                        st.dataframe(pd.DataFrame(search_results), use_container_width=True, hide_index=True)
                    else:
                        st.info("No stocks found matching your search.")
    
    elif selected_page == "🔧 Tools & Settings":
        st.markdown("## 🔧 Tools & Settings")
        
        tab1, tab2 = st.tabs(["🗃️ Data Management", "⚙️ Settings"])
        
        with tab1:
            st.markdown("### Portfolio Data Management")
            
            portfolio = load_portfolio()
            
            if portfolio:
                st.markdown(f"**Portfolio Size:** {len(portfolio)} holdings")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Export Portfolio", use_container_width=True):
                        df = pd.DataFrame(portfolio)
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"portfolio_{dt.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.button("🗑️ Clear Portfolio", use_container_width=True, type="secondary"):
                        if st.confirm("Are you sure you want to clear your entire portfolio?"):
                            if save_portfolio([]):
                                st.success("Portfolio cleared successfully!")
                                st.rerun()
            else:
                st.info("No portfolio data to manage.")
        
        with tab2:
            st.markdown("### Application Settings")
            st.info("⚙️ Settings panel coming soon...")
            
            # Demo settings
            st.checkbox("Enable real-time updates", value=True)
            st.checkbox("Show Arabic names", value=False)
            st.selectbox("Default currency", ["SAR", "USD", "EUR"])

if __name__ == "__main__":
    main()
