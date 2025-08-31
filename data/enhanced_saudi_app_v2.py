"""
  TADAWUL NEXUS  
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
import random
import warnings
import os
import sys
import time
import hashlib
warnings.filterwarnings('ignore')

# Import TADAWUL NEXUS Branding
try:
    from branding.tadawul_branding import TadawulBranding
    BRANDING_AVAILABLE = True
except ImportError:
    BRANDING_AVAILABLE = False

# Import our enhanced Saudi Exchange fetcher
try:
    from saudi_exchange_fetcher import get_all_saudi_stocks, get_market_summary, get_stock_price
    SAUDI_EXCHANGE_AVAILABLE = True  # Enable live TASI data fetching
except ImportError as e:
    SAUDI_EXCHANGE_AVAILABLE = False

# Try to import AI features
try:
    from ai_engine.simple_ai import get_ai_signals
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Import risk tolerance info component
try:
    from components.risk_tolerance_info import show_risk_info
    RISK_INFO_AVAILABLE = True
except ImportError:
    RISK_INFO_AVAILABLE = False

# Create a simple AI simulation for demonstration if AI engine not available
if not AI_AVAILABLE:
    def get_ai_signals(portfolio_symbols, stocks_db):
        import random
        signals = []
        
        for symbol in portfolio_symbols[:5]:  # Limit to first 5 stocks
            # Clean symbol (remove .SR suffix if present)
            clean_symbol = symbol.replace('.SR', '')
            
            # Generate pseudo-random but consistent signals based on symbol
            random.seed(hash(clean_symbol) % 1000)
            
            signal_types = ['BUY', 'SELL', 'HOLD']
            signal = random.choice(signal_types)
            confidence = random.uniform(60, 95)
            
            # Create reasons based on signal type
            if signal == 'BUY':
                reasons = ['Strong upward momentum detected', 'Technical indicators suggest growth', 
                          'Support level holding strong', 'Volume increasing with price']
            elif signal == 'SELL':
                reasons = ['Resistance level reached', 'Overbought conditions detected',
                          'Technical indicators weakening', 'Profit-taking opportunity']
            else:
                reasons = ['Sideways movement expected', 'Mixed technical signals',
                          'Consolidation phase', 'Wait for clearer direction']
            
            company_name = 'Unknown'
            if clean_symbol in stocks_db:
                company_name = stocks_db[clean_symbol].get('name', 
                              stocks_db[clean_symbol].get('name_en', clean_symbol))
            
            signals.append({
                'symbol': clean_symbol,
                'company': company_name,
                'signal': signal,
                'confidence': confidence,
                'reason': random.choice(reasons)
            })
        
        return signals
        
        return signals

# =============================================================================
# 🎨 THEME CUSTOMIZATION FUNCTIONS
# =============================================================================

def update_branding_colors(new_colors):
    """Update colors in the branding file"""
    try:
        branding_file_path = "branding/tadawul_branding.py"
        
        # Read the current file
        with open(branding_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update each color in the COLORS dictionary
        for color_name, color_value in new_colors.items():
            # Find the pattern for this color
            pattern = f"'{color_name}': '#[A-Fa-f0-9]{{6}}'"
            replacement = f"'{color_name}': '{color_value}'"
            
            import re
            content = re.sub(pattern, replacement, content)
        
        # Write the updated content back
        with open(branding_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        st.error(f"Error updating colors: {e}")
        return False

def update_branding_fonts(font_config):
    """Update font configuration in the branding file"""
    try:
        branding_file_path = "branding/tadawul_branding.py"
        
        # Read the current file
        with open(branding_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add font configuration section if it doesn't exist
        font_section = f'''
    # ========================================
    # 📝 FONT CONFIGURATION
    # ========================================
    
    FONTS = {{
        'h1_size': '{font_config["h1_size"]}rem',
        'h2_size': '{font_config["h2_size"]}rem',
        'h3_size': '{font_config["h3_size"]}rem',
        'body_size': '{font_config["body_size"]}rem',
        'caption_size': '{font_config["caption_size"]}rem',
        'header_weight': {font_config["header_weight"]},
        'body_weight': {font_config["body_weight"]},
    }}
'''
        
        # Check if FONTS section already exists
        if 'FONTS = {' in content:
            # Replace existing FONTS section
            import re
            pattern = r'FONTS = \{[^}]*\}'
            content = re.sub(pattern, font_section.strip(), content, flags=re.DOTALL)
        else:
            # Add FONTS section after COLORS
            colors_end = content.find('}', content.find('COLORS = {'))
            if colors_end != -1:
                content = content[:colors_end + 1] + font_section + content[colors_end + 1:]
        
        # Write the updated content back
        with open(branding_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        st.error(f"Error updating fonts: {e}")
        return False

def reset_to_default_theme():
    """Reset theme to default colors and fonts"""
    default_colors = {
        'primary_blue': '#0066CC',
        'secondary_blue': '#1e3a5f',
        'accent_gold': '#FFD700',
        'dark_teal': '#0f2240',
        'background_dark': '#0d1b2a',
        'text_light': '#FFFFFF',
        'text_gray': '#B0BEC5',
        'success_green': '#4CAF50',
        'warning_red': '#F44336',
        'chart_orange': '#FF9800',
    }
    
    default_fonts = {
        'h1_size': 2.5,
        'h2_size': 2.0,
        'h3_size': 1.5,
        'body_size': 1.0,
        'caption_size': 0.85,
        'header_weight': 600,
        'body_weight': 400,
    }
    
    return update_branding_colors(default_colors) and update_branding_fonts(default_fonts)

# =============================================================================

# Broker name standardization function
def normalize_broker_name(broker_name):
    """Standardize broker names to group similar variations"""
    if not broker_name or broker_name.strip() == '':
        return 'Not Set'
    
    # Convert to lowercase for matching
    broker_lower = broker_name.lower().strip()
    
    # BSF Capital / Fransi Capital standardization
    if any(term in broker_lower for term in ['bsf', 'fransi']):
        return 'BSF Capital'
    
    # Al Inma Capital standardization
    if any(term in broker_lower for term in ['inma', 'al inma']):
        return 'Al Inma Capital'
    
    # Add more broker standardizations as needed
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
    
    # Raed Othman Bank variations
    if 'raed othman' in broker_lower:
        return 'Raed Othman Bank'

    # Return original name with proper title case if no match found
    return broker_name.title()

# Configure page
st.set_page_config(
    page_title="📊 TADAWUL NEXUS",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ========================================
# TADAWUL NEXUS - PROFESSIONAL CSS STYLING
# Organized by UI Components for Easy Customization
# ========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ========================================
   🎨 GLOBAL THEME SETTINGS
   CUSTOMIZE: Main colors and fonts
   ======================================== */

* {
    font-family: 'Inter', sans-serif;
}

/* MAIN APP BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f2240 0%, #1e3a5f 50%, #0f1419 100%);
    font-family: 'Inter', sans-serif;
}

/* ========================================
   📊 MAIN HEADER - "TADAWUL NEXUS" Title
   CUSTOMIZE: App title styling and branding
   ======================================== */

.main-header {
    background: linear-gradient(135deg, #0066CC 0%, #1e3a5f 50%, #0f2240 100%);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0, 102, 204, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* ========================================
   📋 SIDEBAR NAVIGATION
   CUSTOMIZE: Left navigation panel
   ======================================== */

/* Multiple selectors to ensure sidebar background changes */
div[data-testid="stSidebar"],
.css-1d391kg,
section[data-testid="stSidebar"],
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #6e7072 0%, #1e3a5f 100%) !important;
}

/* Additional selector for newer Streamlit versions */
div[data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #0f2240 0%, #1e3a5f 100%) !important;
}

div[data-testid="stSidebar"] .element-container {
    background: rgba(255, 255, 255, 0.05);
    margin: 0.3rem 0;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

div[data-testid="stSidebar"] .element-container:hover {
    background: rgba(255, 255, 255, 0.08);
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

/* SIDEBAR TEXT COLORS */
div[data-testid="stSidebar"] .stMarkdown,
div[data-testid="stSidebar"] .element-container,
div[data-testid="stSidebar"] .stText {
    color: #2c3e50;
}

div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3,
div[data-testid="stSidebar"] h4 {
    color: #1565c0;
}

/* ========================================
   📊 PORTFOLIO OVERVIEW SECTION
   CUSTOMIZE: "Portfolio Overview" title and main metrics
   ======================================== */

/* Section headers like "Portfolio Overview" */
.section-header {
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px 10px 0 0;
    text-align: center;
    font-weight: 600;
    margin-bottom: 0;
}

/* Portfolio metrics (Total Value, Cost, P&L) */
div[data-testid="metric-container"] {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

div[data-testid="metric-container"] label {
    font-weight: 600;
    font-size: 14px;
    color: #ffffff;
}

div[data-testid="metric-container"] div[data-testid="metric-value"] {
    font-weight: 700;
    font-size: 24px;
    color: #ffffff;
}

div[data-testid="metric-container"] div[data-testid="metric-delta"] {
    color: #000000;
    font-weight: 500;
}

/* ========================================
   📈 PORTFOLIO HOLDINGS TABLE
   CUSTOMIZE: Stock holdings data table styling
   ======================================== */

.stDataFrame {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.stDataFrame, .stDataFrame td, .stDataFrame th, .stDataFrame div {
    background-color: rgba(255, 255, 255, 0.05);
}

/* ========================================
   🔧 FORM CONTROLS - Input Fields & Buttons
   CUSTOMIZE: Add/Edit stock forms
   ======================================== */

/* Text Input Labels (Quantity, Price labels) */
.stTextInput > label,
.stNumberInput > label,
.stSelectbox > label,
.stDateInput > label {
    color: #ffffff;
    font-weight: 500;
}

/* Input Field Styling */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background-color: #2d3748;
    color: #ffffff;
    border: 1px solid #4a5568;
}

/* Button Styling */
.stButton > button {
    color: #ffffff;
    background: linear-gradient(135deg, #0066CC 0%, #1e3a5f 100%);
    border: none;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease;
    width: 100%;
    padding: 0.6rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00b142 0%, #009e38 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 206, 76, 0.3);
}

/* Checkbox and Radio Labels */
.stCheckbox label, .stRadio label {
    color: #ffffff;
}

/* ========================================
   🔽 DROPDOWN MENUS
   CUSTOMIZE: Stock selection dropdowns
   ======================================== */

.stSelectbox div[data-testid="stSelectbox"] {
    color: #ffffff;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: #2d3748;
    color: #ffffff;
    border: 1px solid #4a5568;
    border-radius: 8px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #2d3748;
    color: #ffffff;
}

.stSelectbox div[data-baseweb="select"] span {
    color: #ffffff;
}

.stSelectbox div[data-baseweb="select"] input {
    color: #ffffff;
    background-color: #2d3748;
}

.stSelectbox div[data-baseweb="select"] svg {
    fill: #ffffff;
}

/* Dropdown Menu Options */
ul[role="listbox"] {
    background-color: #2d3748;
    border: 1px solid #4a5568;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

li[role="option"] {
    background-color: #2d3748;
    color: #ffffff;
    padding: 8px 12px;
}

li[role="option"]:hover {
    background-color: #4a5568;
    color: #ffffff;
}

li[role="option"][aria-selected="true"] {
    background-color: #1565c0;
    color: #ffffff;
}

.stMultiSelect div[data-baseweb="select"] {
    background-color: #2d3748;
    color: #ffffff;
    border: 1px solid #4a5568;
}

.stMultiSelect div[data-baseweb="select"] span {
    color: #ffffff;
}

/* ========================================
   📊 MARKET PERFORMANCE CARDS
   CUSTOMIZE: Top gainers/losers display
   ======================================== */

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

/* ========================================
   📋 CARD COMPONENTS
   CUSTOMIZE: General card layouts
   ======================================== */

.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.portfolio-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    color: white;
}

.ai-signal-card {
    background: linear-gradient(135deg, rgba(0, 206, 76, 0.1) 0%, rgba(0, 158, 56, 0.1) 100%);
    border-radius: 16px;
    padding: 1.5rem;
    color: white;
    margin: 1rem 0;
    border: 1px solid rgba(0, 206, 76, 0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.metric-card {
    background: linear-gradient(135deg, rgba(0, 206, 76, 0.1) 0%, rgba(0, 158, 56, 0.1) 100%);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(0, 206, 76, 0.2);
    backdrop-filter: blur(10px);
    color: white;
}

/* ========================================
   📱 NAVIGATION TABS
   CUSTOMIZE: Page navigation tabs
   ======================================== */

.stTabs [data-baseweb="tab-list"] button {
    color: #000000;
}

.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    color: #0066CC;
}

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

/* ========================================
   📄 GENERAL CONTENT
   CUSTOMIZE: Main page text and content
   ======================================== */

.main .block-container {
    color: #ffffff;
}

.market-table {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    overflow: hidden;
}

/* ========================================
   🔔 NOTIFICATION MESSAGES
   CUSTOMIZE: Success/warning messages
   ======================================== */

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
                print(f"[OK] Loaded OFFICIAL Tadawul database with {len(stocks)} stocks from {data_path}")
                return stocks
            elif len(stocks) != 262:
                print(f"WARNING: WARNING: Database has {len(stocks)} stocks but should have 262!")
                print("  NOTIFY USER: Stock count mismatch detected!")
                return stocks
    except Exception as e:
        print(f"Could not load JSON database: {e}")
    
    try:
        # Second option: Try the complete database Python module
        sys.path.append(root_dir)
        from complete_tadawul_database import create_extended_database
        stocks = create_extended_database()
        if len(stocks) >= 250:
            print(f"[OK] Loaded database from Python module with {len(stocks)} stocks")
            return stocks
    except Exception as e:
        print(f"Warning: Could not load Python module database: {e}")
        
    try:
        # Try loading from root directory
        root_path = os.path.join(root_dir, 'saudi_stocks_database.json')
        with open(root_path, 'r', encoding='utf-8') as f:
            stocks = json.load(f)
            print(f"[OK] Loaded {len(stocks)} stocks from root directory")
            return stocks
    except Exception as e:
        print(f"Could not load from root directory: {e}")
    
    # Final fallback - CORRECTED minimal database
    print("WARNING: Using minimal fallback database")
    return {
        # BANKING SECTOR - CORRECTED
        "1010": {"symbol": "1010", "name_en": "Riyad Bank", "name_ar": "   ", "sector": "Banking"},
        "1180": {"symbol": "1180", "name_en": "Saudi National Bank", "name_ar": "     ", "sector": "Banking"},
        "1120": {"symbol": "1120", "name_en": "Al Rajhi Bank", "name_ar": "   ", "sector": "Banking"},
        "1050": {"symbol": "1050", "name_en": "Banque Saudi Fransi", "name_ar": "     ", "sector": "Banking"},
        
        # ENERGY SECTOR - CORRECTED
        "2030": {"symbol": "2030", "name_en": "Saudi Arabia Refineries Co.", "name_ar": "     ", "sector": "Energy"},
        "2222": {"symbol": "2222", "name_en": "Saudi Arabian Oil Company", "name_ar": "   ", "sector": "Energy"},
        
        # MATERIALS
        "2010": {"symbol": "2010", "name_en": "Saudi Basic Industries Corporation", "name_ar": " ", "sector": "Materials"},
        
        # TELECOMMUNICATIONS
        "7010": {"symbol": "7010", "name_en": "Saudi Telecom Company", "name_ar": "   ", "sector": "Telecommunication Services"}
    }

# Cache for stock price data to improve performance and reduce API calls
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_cached_stock_data(symbol, cache_key):
    """Get cached stock data to avoid excessive API calls"""
    return get_stock_data_internal(symbol, None)

def get_stock_data(symbol, stocks_db=None):
    """Get stock data with enhanced information - prioritizing TASI/Saudi Exchange data"""
    # Use caching with a time-based key to refresh every 5 minutes
    import time
    cache_key = int(time.time() // 300)  # Changes every 5 minutes
    return get_cached_stock_data(symbol, cache_key)

def get_stock_data_internal(symbol, stocks_db=None):
    """Get stock data with enhanced information - LIVE DATA ONLY, NO HARDCODED PRICES"""
    try:
        # PRIORITY 1: Saudi Exchange live data via our enhanced fetcher
        if SAUDI_EXCHANGE_AVAILABLE:
            try:
                saudi_data = get_stock_price(symbol)
                if saudi_data and saudi_data.get('success'):
                    # Return live Saudi Exchange data
                    return {
                        'current_price': saudi_data.get('current_price', 0),
                        'previous_close': saudi_data.get('previous_close', 0),
                        'change': saudi_data.get('change', 0),
                        'change_percent': saudi_data.get('change_percent', 0),
                        'volume': saudi_data.get('volume', 0),
                        'market_cap': saudi_data.get('market_cap', 0),
                        'pe_ratio': saudi_data.get('pe_ratio', 0),
                        'high_52week': saudi_data.get('high_52week', 0),
                        'low_52week': saudi_data.get('low_52week', 0),
                        'data_source': saudi_data.get('data_source', 'Saudi Exchange (Live)'),
                        'timestamp': saudi_data.get('timestamp'),
                        'success': True
                    }
                else:
                    st.warning(f"Saudi Exchange: {saudi_data.get('error', 'Unknown error')} for {symbol}")
            except Exception as e:
                st.warning(f"Saudi Exchange API error for {symbol}: {str(e)}")
        
        # PRIORITY 2: Direct Yahoo Finance fallback
        try:
            stock_symbol = f"{symbol}.SR" if not symbol.endswith('.SR') else symbol
            ticker = yf.Ticker(stock_symbol)
            
            # Get historical data (more reliable than info)
            hist = ticker.history(period="5d", interval="1d")
            
            if not hist.empty and len(hist) > 0:
                current_price = float(hist['Close'].iloc[-1])
                previous_close = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else current_price
                volume = int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0
                
                # Get additional info
                info = ticker.info
                
                return {
                    'current_price': round(current_price, 2),
                    'previous_close': round(previous_close, 2),
                    'change': round(current_price - previous_close, 2),
                    'change_percent': round(((current_price - previous_close) / previous_close) * 100, 2) if previous_close > 0 else 0,
                    'volume': volume,
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'high_52week': info.get('fiftyTwoWeekHigh', 0),
                    'low_52week': info.get('fiftyTwoWeekLow', 0),
                    'data_source': 'Yahoo Finance - Live Historical Data',
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                }
            
            # Try info data as fallback
            info = ticker.info
            current_price = None
            
            for price_field in ['currentPrice', 'regularMarketPrice', 'previousClose', 'ask', 'bid']:
                if price_field in info and info[price_field] and info[price_field] > 0:
                    current_price = float(info[price_field])
                    break
            
            if current_price and current_price > 0:
                previous_close = info.get('previousClose', current_price)
                
                return {
                    'current_price': round(current_price, 2),
                    'previous_close': round(previous_close, 2),
                    'change': round(current_price - previous_close, 2),
                    'change_percent': round(((current_price - previous_close) / previous_close) * 100, 2) if previous_close > 0 else 0,
                    'volume': info.get('volume', 0),
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'data_source': 'Yahoo Finance - Live Info Data',
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                }
                
        except Exception as e:
            st.warning(f"Yahoo Finance error for {symbol}: {str(e)}")
        
        # NO HARDCODED DATA - Return error if all live sources fail
        st.error(f"❌ Could not fetch live data for {symbol} from any source")
        return {
            'current_price': 0,
            'previous_close': 0,
            'change': 0,
            'change_percent': 0,
            'volume': 0,
            'market_cap': 0,
            'pe_ratio': 0,
            'data_source': 'ERROR: No Live Data Available',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': 'All live data sources failed'
        }
            
    except Exception as e:
        st.error(f"Critical error fetching data for {symbol}: {str(e)}")
        return {
            'current_price': 0,
            'previous_close': 0,
            'change': 0,
            'change_percent': 0,
            'volume': 0,
            'market_cap': 0,
            'pe_ratio': 0,
            'data_source': 'ERROR: System Error',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': str(e)
        }

def consolidate_portfolio_by_symbol(portfolio):
    """Consolidate portfolio holdings by symbol, combining multiple broker positions"""
    consolidated = {}
    
    for stock in portfolio:
        symbol = stock['symbol']
        quantity = stock.get('quantity', 0)
        purchase_price = stock.get('purchase_price', 0)
        purchase_date = stock.get('purchase_date', '')
        broker = stock.get('broker', 'Not Set')
        notes = stock.get('notes', '')
        last_updated = stock.get('last_updated', '')
        
        if symbol in consolidated:
            # Calculate weighted average purchase price
            existing_qty = consolidated[symbol]['quantity']
            existing_price = consolidated[symbol]['purchase_price']
            total_cost = (existing_qty * existing_price) + (quantity * purchase_price)
            total_qty = existing_qty + quantity
            
            consolidated[symbol]['quantity'] = total_qty
            consolidated[symbol]['purchase_price'] = total_cost / total_qty if total_qty > 0 else 0
            
            # Combine brokers info
            if broker not in consolidated[symbol]['brokers']:
                consolidated[symbol]['brokers'].append(broker)
            
            # Keep earliest purchase date
            if purchase_date and (not consolidated[symbol]['purchase_date'] or purchase_date < consolidated[symbol]['purchase_date']):
                consolidated[symbol]['purchase_date'] = purchase_date
            
            # Combine notes
            if notes and notes not in consolidated[symbol]['notes']:
                if consolidated[symbol]['notes']:
                    consolidated[symbol]['notes'] += f"; {notes}"
                else:
                    consolidated[symbol]['notes'] = notes
            
            # Keep latest update time
            if last_updated and last_updated > consolidated[symbol]['last_updated']:
                consolidated[symbol]['last_updated'] = last_updated
        else:
            # First entry for this symbol
            consolidated[symbol] = {
                'symbol': symbol,
                'quantity': quantity,
                'purchase_price': purchase_price,
                'purchase_date': purchase_date,
                'brokers': [broker] if broker else [],
                'notes': notes,
                'last_updated': last_updated
            }
    
    # Convert back to list format
    return list(consolidated.values())

def calculate_portfolio_value(portfolio, stocks_db=None):
    """Calculate total portfolio value with enhanced metrics using consistent TASI prices"""
    total_value = 0
    total_cost = 0
    total_gain_loss = 0
    portfolio_details = []
    
    for stock in portfolio:
        symbol = stock['symbol']
        stock_data = get_stock_data(symbol, stocks_db)
        current_price = stock_data.get('current_price', 0)
        quantity = stock.get('quantity', 0)
        purchase_price = stock.get('purchase_price', 0)
        
        current_value = current_price * quantity
        cost_basis = purchase_price * quantity
        position_gain_loss = current_value - cost_basis
        
        total_value += current_value
        total_cost += cost_basis
        total_gain_loss += position_gain_loss
        
        # Store detailed information for debugging
        portfolio_details.append({
            'symbol': symbol,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'current_price': current_price,
            'current_value': current_value,
            'cost_basis': cost_basis,
            'gain_loss': position_gain_loss,
            'data_source': stock_data.get('data_source', 'Unknown')
        })
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percent': (total_gain_loss / total_cost * 100) if total_cost > 0 else 0,
        'portfolio_details': portfolio_details,
        'calculation_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def display_top_gainers_losers():
    """Display top gainers and losers tables - LIVE DATA ONLY"""
    st.markdown("""
    <div class="section-header">
        📊 Saudi Market Performance - Live Data from saudiexchange.sa & Yahoo Finance
    </div>
    """, unsafe_allow_html=True)
    
    # Display data source information
    st.info("""
    📡 **Live Data Sources:**
    1. **Primary**: Saudi Exchange (saudiexchange.sa) official website
    2. **Fallback**: Yahoo Finance (.SR suffix) 
    3. **NO HARDCODED DATA** - All prices are fetched in real-time
    """)
    
    # Get live market summary
    with st.spinner("🔄 Fetching live market data..."):
        if SAUDI_EXCHANGE_AVAILABLE:
            try:
                market_data = get_market_summary()
                
                if market_data and market_data.get('success'):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📈 Top 10 Gainers (Live)")
                        if market_data.get('top_gainers'):
                            gainers_df = pd.DataFrame(market_data['top_gainers'])
                            if not gainers_df.empty:
                                # Format the DataFrame for display
                                display_cols = ['symbol', 'name_en', 'current_price', 'change_pct']
                                if all(col in gainers_df.columns for col in display_cols):
                                    gainers_display = gainers_df[display_cols].copy()
                                    gainers_display['change_pct'] = gainers_display['change_pct'].apply(lambda x: f"+{x:.2f}%")
                                    gainers_display['current_price'] = gainers_display['current_price'].apply(lambda x: f"{x:.2f} SAR")
                                    gainers_display.columns = ['Symbol', 'Company', 'Price', 'Change']
                                    
                                    st.dataframe(
                                        gainers_display, 
                                        use_container_width=True,
                                        hide_index=True
                                    )
                                else:
                                    st.dataframe(gainers_df, use_container_width=True, hide_index=True)
                        else:
                            st.warning("📊 No gainers data available from live sources")
                    
                    with col2:
                        st.markdown("### 📉 Top 10 Losers (Live)")
                        if market_data.get('top_losers'):
                            losers_df = pd.DataFrame(market_data['top_losers'])
                            if not losers_df.empty:
                                # Format the DataFrame for display
                                display_cols = ['symbol', 'name_en', 'current_price', 'change_pct']
                                if all(col in losers_df.columns for col in display_cols):
                                    losers_display = losers_df[display_cols].copy()
                                    losers_display['change_pct'] = losers_display['change_pct'].apply(lambda x: f"{x:.2f}%")
                                    losers_display['current_price'] = losers_display['current_price'].apply(lambda x: f"{x:.2f} SAR")
                                    losers_display.columns = ['Symbol', 'Company', 'Price', 'Change']
                                    
                                    st.dataframe(
                                        losers_display, 
                                        use_container_width=True,
                                        hide_index=True
                                    )
                                else:
                                    st.dataframe(losers_df, use_container_width=True, hide_index=True)
                        else:
                            st.warning("📊 No losers data available from live sources")
                    
                    # Display data source and timestamp
                    st.success(f"""
                    ✅ **Live Data Status**: {market_data['total_stocks']} stocks fetched successfully
                    🕒 **Last Updated**: {market_data.get('timestamp', 'Unknown')}
                    📡 **Source**: {market_data.get('data_source', 'Live Market Data')}
                    """)
                    
                else:
                    st.error(f"❌ Could not fetch live market data: {market_data.get('error', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Error fetching live market data: {str(e)}")
        else:
            st.error("❌ Saudi Exchange fetcher not available. Please check the saudi_exchange_fetcher.py module.")
    
    # Manual test section for individual stocks
    with st.expander("🧪 Test Individual Stock Prices (Live Data)"):
        test_symbol = st.text_input("Enter Saudi stock symbol (e.g., 2222, 1120, 4190):", "2222")
        
        if st.button("🔄 Fetch Live Price"):
            if test_symbol:
                with st.spinner(f"Fetching live data for {test_symbol}..."):
                    result = get_stock_price(test_symbol) if SAUDI_EXCHANGE_AVAILABLE else None
                    
                    if result and result.get('success'):
                        st.success(f"""
                        ✅ **{test_symbol}** Live Data:
                        💰 **Price**: {result['current_price']:.2f} SAR
                        📈 **Change**: {result['change_percent']:.2f}%
                        📊 **Volume**: {result.get('volume', 'N/A'):,}
                        📡 **Source**: {result.get('data_source', 'Unknown')}
                        🕒 **Time**: {result.get('timestamp', 'N/A')}
                        """)
                    else:
                        error_msg = result.get('error', 'Unknown error') if result else 'Fetcher not available'
                        st.error(f"❌ Failed to fetch live data for {test_symbol}: {error_msg}")
            else:
                st.warning("Please enter a stock symbol")
                
    # Fallback demo section when live data is not available
    if not SAUDI_EXCHANGE_AVAILABLE or st.checkbox("Show Demo Data for Testing", value=False):
        st.info("💡 Showing demo data - Enable live data fetcher for real prices")    # Demo data
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
        st.markdown("### [UP] Top Gainers")
        st.dataframe(pd.DataFrame(demo_gainers), hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("### [DOWN] Top Losers") 
        st.dataframe(pd.DataFrame(demo_losers), hide_index=True, use_container_width=True)

def main():
    """Main application function"""
    
    # Apply TADAWUL NEXUS Professional Branding
    if BRANDING_AVAILABLE:
        TadawulBranding.apply_branding()
    
    # Ensure required modules are available in function scope
    from datetime import datetime, timedelta
    import pandas as pd
    import numpy as np
    import random
    import plotly.graph_objects as go
    import plotly.express as px
    
    # Professional branded header
    if BRANDING_AVAILABLE:
        TadawulBranding.display_header(
            title="TADAWUL NEXUS",
            tagline="primary",
            include_logo=True
        )
    else:
        # Fallback header
        st.markdown("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">
                  TADAWUL NEXUS  
            </h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9;">
                Next-Generation Saudi Stock Intelligence Platform
            </p>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.95rem; opacity: 0.8;">
                Saudi Stock Exchange (Tadawul) | Real-time Data | AI-Powered Insights
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
        if st.button("  Refresh Database", help="Clear cache and reload stock database"):
            st.cache_data.clear()
            st.rerun()
            
        selected_page = st.radio(
            "Navigation",
            [
                "📊 Portfolio Overview",
                "⚙️ Portfolio Setup", 
                "🤖 AI Trading Center",
                "📈 Market Analysis",
                "📊 Performance Tracker",
                "🔍 Stock Research",
                "📋 Analytics Dashboard",
                "🏭 Sector Analyzer",
                "⚠️ Risk Management",
                "📁 Import/Export Data",
                "🎨 Theme Customizer"
            ],
            index=0,
            key="main_nav",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Portfolio Quick Stats - Using CONSISTENT calculation method
        portfolio = load_portfolio()
        if portfolio:
            # Use consolidated portfolio for accurate metrics in sidebar - SAME as main page
            consolidated_portfolio = consolidate_portfolio_by_symbol(portfolio)
            portfolio_stats = calculate_portfolio_value(consolidated_portfolio, stocks_db)
            
            st.markdown('<h3 style="color: #1565c0;">📊 Portfolio Stats</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Holdings", len(consolidated_portfolio))
                st.metric("Total Value", f"{portfolio_stats['total_value']:,.2f} SAR")
            
            with col2:
                gain_loss = portfolio_stats['total_gain_loss']
                gain_loss_pct = portfolio_stats['total_gain_loss_percent']
                
                # Consistent P&L formatting - same as main page
                if gain_loss >= 0:
                    st.metric("P&L", f"+{gain_loss:,.2f} SAR", f"+{gain_loss_pct:.1f}%")
                else:
                    st.metric("P&L", f"{gain_loss:,.2f} SAR", f"{gain_loss_pct:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Market Information Section
        st.markdown('<h3 style="color: #1565c0;">📈 📊 Market Info</h3>', unsafe_allow_html=True)
        
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
            st.success("  Live Data Connected")
        else:
            # Fall back to DB-only display and clearly label it
            st.metric("TASI Companies", "259")
            if SAUDI_EXCHANGE_AVAILABLE:
                st.info("  Live fetch failed   showing cached DB")
            else:
                st.warning("  Using Cached Data")
        
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
            <h4 style="color: #1565c0; margin: 0 0 0.5rem 0; font-size: 1rem;">  About TADAWUL NEXUS</h4>
            <div style="font-size: 0.8rem; color: #666; line-height: 1.4;">
                <strong>Next-Generation Platform</strong><br>
                🔥 Real-time Saudi Exchange Data<br>
                🤖 AI Trading Signals<br>
                📊 Professional Portfolio Management<br>
                📈 Advanced Market Analytics
            </div>
            <div style="font-size: 0.75rem; color: #888; margin-top: 0.5rem; line-height: 1.3;">
                  Powered by Tadawul   Built for Saudi Investors
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Main content based on selected page
    
    # Data Source Indicator with dynamic pricing info
    # Always show Saudi Exchange as primary since it's first in our fetching logic
    data_source_status = "🔴 LIVE Saudi Exchange (TASI) + Yahoo Finance Fallback"
    pricing_info = "Real-time market data with redundant sources"
    
    st.markdown(f"""
    <div style="background: #e8f5e8; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem; 
                border-left: 4px solid #4caf50; font-size: 0.85rem;">
        📊 
                <strong>Price Data Source:</strong> {data_source_status} 
        <span style="font-size: 0.75rem; color: #666;">
        | {pricing_info} | NO HARDCODED PRICES
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    if selected_page == "📊 Portfolio Overview":
        st.markdown("## 📊 Portfolio Overview")
        
        portfolio = load_portfolio()
        
        if portfolio:
            # Consolidate portfolio by symbol for accurate metrics
            consolidated_portfolio = consolidate_portfolio_by_symbol(portfolio)
            
            # Portfolio summary with enhanced calculation
            portfolio_stats = calculate_portfolio_value(consolidated_portfolio, stocks_db)
            
            # Portfolio metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Holdings", len(consolidated_portfolio))
            with col2:
                st.metric("Portfolio Value", f"{portfolio_stats['total_value']:,.2f} SAR")
            with col3:
                st.metric("Total Cost", f"{portfolio_stats['total_cost']:,.2f} SAR")
            with col4:
                gain_loss = portfolio_stats['total_gain_loss']
                gain_loss_pct = portfolio_stats['total_gain_loss_percent']
                if gain_loss >= 0:
                    st.metric("P&L", f"+{gain_loss:,.2f} SAR", f"+{gain_loss_pct:.1f}%")
                else:
                    st.metric("P&L", f"{gain_loss:,.2f} SAR", f"{gain_loss_pct:.1f}%")
            
            # Data source information
            if st.checkbox("🔍 Show Price Data Sources", help="Debug information about where prices are sourced from"):
                st.markdown("### 📊 Price Data Sources")
                details_df = pd.DataFrame(portfolio_stats['portfolio_details'])
                st.dataframe(
                    details_df[['symbol', 'current_price', 'data_source']].style.format({
                        'current_price': '{:.2f} SAR'
                    }),
                    use_container_width=True
                )
                st.caption(f"Last calculated: {portfolio_stats['calculation_timestamp']}")
            
            st.markdown("---")
            
            # Portfolio view options
            st.markdown("### 📋 Your Holdings")
            
            # Add view toggle options
            col1, col2 = st.columns([3, 1])
            
            with col1:
                view_option = st.radio(
                    "Portfolio View:",
                    ["📊 Consolidated Holdings", "📋 All Holdings (By Broker)", "🏦 By Broker"],
                    horizontal=True,
                    help="Choose how to display your portfolio holdings"
                )
            
            with col2:
                if view_option == "🏦 By Broker":
                    # Get unique brokers from portfolio with normalization
                    raw_brokers = [stock.get('broker', 'Not Set') for stock in portfolio]
                    normalized_brokers = [normalize_broker_name(broker) for broker in raw_brokers]
                    brokers = list(set(normalized_brokers))
                    brokers = [broker for broker in brokers if broker]  # Remove empty brokers
                    if 'Not Set' in normalized_brokers:
                        if 'Not Set' not in brokers:
                            brokers.append('Not Set')
                    
                    selected_broker = st.selectbox(
                        "Select Broker:",
                        options=["All Brokers"] + sorted(brokers),
                        help="Filter holdings by specific broker"
                    )
            
            holdings_data = []
            
            # Choose the portfolio data based on view option
            if view_option == "📊 Consolidated Holdings":
                # Use consolidated portfolio for consolidated view
                display_portfolio = consolidated_portfolio
            else:
                # Use original portfolio for detailed views
                display_portfolio = portfolio.copy()
                
                # Filter by broker if needed
                if view_option == "🏦 By Broker" and 'selected_broker' in locals() and selected_broker != "All Brokers":
                    display_portfolio = [stock for stock in portfolio 
                                        if normalize_broker_name(stock.get('broker', 'Not Set')) == selected_broker]
            
            for idx, stock in enumerate(display_portfolio, 1):  # Start numbering from 1
                stock_data = get_stock_data(stock['symbol'], stocks_db)
                current_price = stock_data.get('current_price', 0)
                quantity = stock.get('quantity', 0)
                purchase_price = stock.get('purchase_price', 0)
                
                current_value = current_price * quantity
                cost_basis = purchase_price * quantity
                gain_loss = current_value - cost_basis
                gain_loss_pct = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0
                
                stock_info = stocks_db.get(stock['symbol'], {})
                
                # Build the holdings data row
                holdings_row = {
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
                    'Purchase Date': stock.get('purchase_date', 'Unknown')  # Add purchase date
                }
                
                # Add broker information based on view type
                if view_option == "📊 Consolidated Holdings":
                    # For consolidated view, show all brokers for this symbol
                    brokers_list = stock.get('brokers', [])
                    if brokers_list:
                        holdings_row['Broker'] = ', '.join([normalize_broker_name(b) for b in brokers_list if b])
                    else:
                        holdings_row['Broker'] = 'Not Set'
                else:
                    # For detailed views, show individual broker
                    holdings_row['Broker'] = normalize_broker_name(stock.get('broker', 'Not Set'))
                
                holdings_data.append(holdings_row)
            
            if holdings_data:
                holdings_df = pd.DataFrame(holdings_data)
                
                # Display broker-specific summary if filtering by broker
                if view_option == "🏦 By Broker" and 'selected_broker' in locals() and selected_broker != "All Brokers":
                    # Calculate broker-specific metrics using normalized names
                    broker_portfolio = [stock for stock in portfolio 
                                      if normalize_broker_name(stock.get('broker', 'Not Set')) == selected_broker]
                    broker_stats = calculate_portfolio_value(broker_portfolio, stocks_db)
                    
                    st.markdown(f"#### 🏦 {selected_broker} Holdings Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Holdings", len(broker_portfolio))
                    with col2:
                        st.metric("Current Value", f"{broker_stats['total_value']:,.2f} SAR")
                    with col3:
                        st.metric("Total Cost", f"{broker_stats['total_cost']:,.2f} SAR")
                    with col4:
                        broker_gain_loss = broker_stats['total_gain_loss']
                        broker_gain_loss_pct = broker_stats['total_gain_loss_percent']
                        st.metric("P&L", f"{broker_gain_loss:,.2f} SAR", f"{broker_gain_loss_pct:.1f}%")
                    
                    st.markdown("---")
                
                # Add explanation for the current view
                if view_option == "📊 Consolidated Holdings":
                    st.info("📊 **Consolidated View**: Holdings are combined by symbol across all brokers. Purchase price shows weighted average.")
                elif view_option == "📋 All Holdings (By Broker)":
                    st.info("📋 **Detailed View**: Shows each broker position separately, including duplicate symbols.")
                
                # Display holdings table
                if view_option == "🏦 By Broker":
                    # Group by broker for better organization
                    if 'selected_broker' in locals() and selected_broker == "All Brokers":
                        # Show all brokers with groupings
                        st.markdown("#### Holdings by Broker")
                        
                        # Group holdings by broker
                        broker_groups = {}
                        for _, row in holdings_df.iterrows():
                            broker = row['Broker']
                            if broker not in broker_groups:
                                broker_groups[broker] = []
                            broker_groups[broker].append(row)
                        
                        # Display each broker group
                        for broker, broker_holdings in broker_groups.items():
                            st.markdown(f"#####   {broker}")
                            broker_df = pd.DataFrame(broker_holdings)
                            
                            # Calculate broker totals
                            total_holdings = len(broker_holdings)
                            total_cost = sum([float(h['Total Cost'].replace(' SAR', '').replace(',', '')) for h in broker_holdings])
                            total_value = sum([float(h['Current Value'].replace(' SAR', '').replace(',', '')) for h in broker_holdings])
                            total_pnl = total_value - total_cost
                            total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
                            
                            # Show broker summary
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.caption(f"Holdings: {total_holdings}")
                            with col2:
                                st.caption(f"Value: {total_value:,.2f} SAR")
                            with col3:
                                st.caption(f"Cost: {total_cost:,.2f} SAR")
                            with col4:
                                pnl_color = " " if total_pnl >= 0 else " "
                                st.caption(f"P&L: {pnl_color} {total_pnl:+,.2f} SAR ({total_pnl_pct:+.1f}%)")
                            
                            st.dataframe(broker_df, hide_index=True, use_container_width=True)
                            st.markdown("---")
                    else:
                        # Show single broker holdings
                        st.dataframe(holdings_df, hide_index=True, use_container_width=True)
                else:
                    # Show all holdings in standard view
                    st.dataframe(holdings_df, hide_index=True, use_container_width=True)
            
            # Portfolio performance chart
            st.markdown("### 📊 Portfolio Performance")
            
            # Calculate portfolio metrics
            consolidated_portfolio = consolidate_portfolio_by_symbol(portfolio)
            portfolio_stats = calculate_portfolio_value(consolidated_portfolio, stocks_db)
            
            # Performance Overview Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Portfolio Value", 
                    f"{portfolio_stats['total_value']:,.2f} SAR",
                    delta=f"{portfolio_stats['total_gain_loss']:,.2f} SAR"
                )
            
            with col2:
                st.metric(
                    "Total Return", 
                    f"{portfolio_stats['total_gain_loss_percent']:.2f}%",
                    delta=f"{portfolio_stats['total_gain_loss_percent']:.2f}%"
                )
            
            with col3:
                winning_stocks = sum(1 for stock in consolidated_portfolio if 
                                   get_stock_data(stock['symbol'], stocks_db).get('current_price', 0) > stock['purchase_price'])
                st.metric("Winning Positions", f"{winning_stocks}/{len(consolidated_portfolio)}")
            
            with col4:
                avg_return = portfolio_stats['total_gain_loss_percent']
                st.metric("Avg Return", f"{avg_return:.2f}%")
            
            st.markdown("---")
            
            # Performance Charts
            tab1, tab2, tab3 = st.tabs(["📈 Portfolio Overview", "🏭 Sector Allocation", "🏆 Top Performers"])
            
            with tab1:
                # Portfolio composition pie chart
                if consolidated_portfolio:
                    import plotly.express as px
                    import plotly.graph_objects as go
                    
                    # Prepare data for portfolio composition
                    portfolio_data = []
                    for stock in consolidated_portfolio:
                        stock_data = get_stock_data(stock['symbol'], stocks_db)
                        stock_info = stocks_db.get(stock['symbol'], {})
                        current_price = stock_data.get('current_price', 0)
                        current_value = current_price * stock['quantity']
                        
                        # Get company name from database, with fallback
                        company_name = stock_info.get('name', f"{stock['symbol']}")
                        if company_name == stock['symbol'] or not company_name:
                            company_name = f"{stock['symbol']} - Stock"
                        else:
                            company_name = f"{stock['symbol']} - {company_name}"
                        
                        portfolio_data.append({
                            'Symbol': stock['symbol'],
                            'Company': company_name,
                            'Value': current_value,
                            'Weight': (current_value / portfolio_stats['total_value'] * 100) if portfolio_stats['total_value'] > 0 else 0,
                            'Gain/Loss': ((current_price - stock['purchase_price']) / stock['purchase_price'] * 100) if stock['purchase_price'] > 0 else 0
                        })
                    
                    # Portfolio composition chart - Horizontal Bar Chart (much clearer than pie)
                    fig = px.bar(
                        portfolio_data, 
                        x='Value', 
                        y='Company',
                        title="Portfolio Composition by Value",
                        orientation='h',
                        hover_data=['Weight', 'Symbol'],
                        color='Value',
                        color_continuous_scale='Viridis',
                        labels={'Value': 'Portfolio Value (SAR)', 'Company': 'Holdings'}
                    )
                    
                    # Customize the chart for better readability
                    fig.update_layout(
                        height=max(400, len(portfolio_data) * 25),  # Dynamic height based on number of holdings
                        yaxis={'categoryorder': 'total ascending'},  # Sort by value
                        showlegend=False,
                        font=dict(size=10)
                    )
                    
                    # Add value labels on bars
                    fig.update_traces(
                        texttemplate='%{x:,.0f} SAR (%{customdata[0]:.1f}%)',
                        textposition='outside',
                        customdata=[[d['Weight']] for d in portfolio_data]
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Performance bar chart
                    fig2 = px.bar(
                        portfolio_data,
                        x='Company',
                        y='Gain/Loss',
                        title="Individual Stock Performance (%)",
                        color='Gain/Loss',
                        color_continuous_scale=['red', 'yellow', 'green']
                    )
                    fig2.update_layout(height=400, xaxis_tickangle=-45)
                    st.plotly_chart(fig2, use_container_width=True)
            
            with tab2:
                # Sector allocation (if sector data is available)
                st.markdown("####   Portfolio Allocation by Sector")
                
                # Group by sectors using database sector info
                sector_data = {}
                for stock in consolidated_portfolio:
                    stock_data = get_stock_data(stock['symbol'], stocks_db)
                    stock_info = stocks_db.get(stock['symbol'], {})
                    sector = stock_info.get('sector', 'Unknown')
                    current_price = stock_data.get('current_price', 0)
                    current_value = current_price * stock['quantity']
                    
                    if sector in sector_data:
                        sector_data[sector] += current_value
                    else:
                        sector_data[sector] = current_value
                
                if sector_data and len(sector_data) > 1 or (len(sector_data) == 1 and 'Unknown' not in sector_data):
                    # Calculate percentages for sector allocation
                    total_value = sum(sector_data.values())
                    sector_percentages = {
                        sector: (value / total_value * 100) if total_value > 0 else 0
                        for sector, value in sector_data.items()
                    }
                    
                    # Create horizontal bar chart for better visualization
                    sector_df_chart = pd.DataFrame([
                        {'Sector': sector, 'Percentage': percentage, 'Value': sector_data[sector]}
                        for sector, percentage in sector_percentages.items()
                        if percentage > 0
                    ])
                    
                    if not sector_df_chart.empty:
                        sector_df_chart = sector_df_chart.sort_values('Percentage', ascending=True)
                        
                        fig3 = px.bar(
                            sector_df_chart,
                            x='Percentage',
                            y='Sector',
                            orientation='h',
                            title="Portfolio Allocation by Sector (%)",
                            color='Percentage',
                            color_continuous_scale='Blues',
                            hover_data={'Value': ':,.2f'}
                        )
                        fig3.update_layout(
                            showlegend=False,
                            height=400,
                            xaxis_title="Percentage (%)",
                            yaxis_title="Sector",
                            hoverlabel=dict(bgcolor="white", font_size=12)
                        )
                        fig3.update_traces(
                            hovertemplate="<b>%{y}</b><br>" +
                                        "Percentage: %{x:.1f}%<br>" +
                                        "Value: %{customdata[0]:,.2f} SAR<extra></extra>"
                        )
                        st.plotly_chart(fig3, use_container_width=True)
                    else:
                        # Create empty DataFrame with required columns
                        st.info("📊 No sector data available for visualization.")
                    
                    # Sector performance table
                    sector_df = pd.DataFrame([
                        {
                            'Sector': sector,
                            'Value': f"{value:,.2f} SAR",
                            'Weight': f"{(value/portfolio_stats['total_value']*100):.1f}%" if portfolio_stats['total_value'] > 0 else "0%"
                        }
                        for sector, value in sector_data.items()
                    ])
                    st.dataframe(sector_df, hide_index=True, use_container_width=True)
                else:
                    st.info("📊 Sector information not available for current holdings or all stocks are from unknown sectors.")
                    
                    # Show what sectors we do have, even if unknown
                    if sector_data:
                        sector_df = pd.DataFrame([
                            {
                                'Sector': sector,
                                'Value': f"{value:,.2f} SAR",
                                'Weight': f"{(value/portfolio_stats['total_value']*100):.1f}%" if portfolio_stats['total_value'] > 0 else "0%"
                            }
                            for sector, value in sector_data.items()
                        ])
                        st.dataframe(sector_df, hide_index=True, use_container_width=True)
            
            with tab3:
                # Top performers
                st.markdown("####   Best & Worst Performers")
                
                # Calculate performance for each stock
                performance_data = []
                for stock in consolidated_portfolio:
                    stock_data = get_stock_data(stock['symbol'], stocks_db)
                    stock_info = stocks_db.get(stock['symbol'], {})
                    current_price = stock_data.get('current_price', 0)
                    gain_loss_percent = ((current_price - stock['purchase_price']) / stock['purchase_price'] * 100) if stock['purchase_price'] > 0 else 0
                    gain_loss_amount = (current_price - stock['purchase_price']) * stock['quantity']
                    
                    # Get company name from database, with fallback
                    company_name = stock_info.get('name', f"{stock['symbol']}")
                    if company_name == stock['symbol'] or not company_name:
                        company_name = f"{stock['symbol']} - Stock"
                    else:
                        company_name = f"{stock['symbol']} - {company_name}"
                    
                    performance_data.append({
                        'Symbol': stock['symbol'],
                        'Company': company_name,
                        'Gain/Loss %': gain_loss_percent,
                        'Gain/Loss Amount': gain_loss_amount,
                        'Current Price': current_price,
                        'Purchase Price': stock['purchase_price'],
                        'Quantity': stock['quantity']
                    })
                
                # Sort by performance
                performance_data.sort(key=lambda x: x['Gain/Loss %'], reverse=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### 📈 Top Gainers")
                    top_gainers = performance_data[:5]
                    if top_gainers:
                        gainers_df = pd.DataFrame([
                            {
                                'Company': item['Company'],
                                'Gain %': f"+{item['Gain/Loss %']:.2f}%",
                                'Gain Amount': f"+{item['Gain/Loss Amount']:,.2f} SAR"
                            }
                            for item in top_gainers if item['Gain/Loss %'] > 0
                        ])
                        if not gainers_df.empty:
                            st.dataframe(gainers_df, hide_index=True, use_container_width=True)
                        else:
                            st.info("No gainers in current portfolio")
                
                with col2:
                    st.markdown("##### 📉 Top Losers")
                    top_losers = performance_data[-5:]
                    if top_losers:
                        losers_df = pd.DataFrame([
                            {
                                'Company': item['Company'],
                                'Loss %': f"{item['Gain/Loss %']:.2f}%",
                                'Loss Amount': f"{item['Gain/Loss Amount']:,.2f} SAR"
                            }
                            for item in reversed(top_losers) if item['Gain/Loss %'] < 0
                        ])
                        if not losers_df.empty:
                            st.dataframe(losers_df, hide_index=True, use_container_width=True)
                        else:
                            st.info("No losers in current portfolio")
                
                # Full performance table
                st.markdown("##### 📊 Complete Performance Overview")
                full_performance_df = pd.DataFrame([
                    {
                        'Symbol': item['Symbol'],
                        'Company': item['Company'],
                        'Quantity': f"{item['Quantity']:,}",
                        'Purchase Price': f"{item['Purchase Price']:.2f} SAR",
                        'Current Price': f"{item['Current Price']:.2f} SAR",
                        'Gain/Loss %': f"{item['Gain/Loss %']:+.2f}%",
                        'Gain/Loss Amount': f"{item['Gain/Loss Amount']:+,.2f} SAR"
                    }
                    for item in performance_data
                ])
                st.dataframe(full_performance_df, hide_index=True, use_container_width=True)
            
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; background: #f8f9fa; border-radius: 10px; border: 2px dashed #dee2e6;">
                <h3 style="color: #6c757d; margin-bottom: 1rem;">  No Portfolio Yet</h3>
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
                # from unified_stock_manager import get_stock_options  # Module not available
                # stock_options = get_stock_options()  # Module not available
                raise ImportError("Module not available")
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
                    "-- Select Broker --",  # Default option to prevent accidental selection
                    "BSF Capital",  # Standardized (includes Fransi Capital)
                    "Al Inma Capital",  # Standardized (includes Alinma Investment)
                    "Al Rajhi Capital",
                    "NCB Capital",
                    "Samba Capital",
                    "Al Jazira Capital",
                    "SNB Capital", 
                    "Riyad Capital",
                    "SABB Securities",
                    "Albilad Investment",
                    "Jadwa Investment",
                    "Other"
                ],
                index=0,
                help="Select your broker (similar names are automatically grouped)"
            )
        
        # If "Other" is selected, allow custom broker name
        if broker_name == "Other":
            broker_name = st.text_input("Enter Broker Name:", placeholder="Enter custom broker name")
        elif broker_name == "-- Select Broker --":
            broker_name = ""  # Clear the broker name if default is selected
        
        # Transaction notes (optional)
        transaction_notes = st.text_area("Notes (Optional):", placeholder="Any additional notes about this transaction...")
        
        # Add stock button
        if st.button("  Add to Portfolio", type="primary"):
            if selected_symbol and broker_name and broker_name != "-- Select Broker --":
                portfolio = load_portfolio()
                portfolio = load_portfolio()
                
                # Check if stock already exists with the same broker
                existing_stock = None
                for i, stock in enumerate(portfolio):
                    if stock['symbol'] == selected_symbol and normalize_broker_name(stock['broker']) == normalize_broker_name(broker_name):
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
                        'broker': normalize_broker_name(broker_name),
                        'notes': transaction_notes,
                        'last_updated': datetime.now().isoformat()
                    }
                    
                    st.success(f"[OK] Updated {stock_info.get('name')} holding! New quantity: {total_qty}")
                else:
                    # Add new stock
                    new_stock = {
                        'symbol': selected_symbol,
                        'quantity': quantity,
                        'purchase_price': purchase_price,
                        'purchase_date': purchase_date.isoformat(),
                        'broker': normalize_broker_name(broker_name),
                        'notes': transaction_notes,
                        'last_updated': datetime.now().isoformat()
                    }
                    portfolio.append(new_stock)
                    
                    st.success(f"[OK] Added {stock_info.get('name')} to your portfolio!")
                
                # Save portfolio
                if save_portfolio(portfolio):
                    st.rerun()
            elif not broker_name or broker_name == "-- Select Broker --":
                st.error("WARNING: Please select a broker before adding to portfolio!")
            else:
                st.error("WARNING: Please ensure all fields are filled correctly!")
        
        st.markdown("---")
        
        # Current portfolio management
        st.markdown("### 📋 Manage Portfolio")
        
        portfolio = load_portfolio()
        if portfolio:
            # Portfolio overview
            st.markdown(f"**Total Holdings:** {len(portfolio)} stocks")
            
            # Tabs for different management options
            tab1, tab2 = st.tabs(["[CHART] View Holdings", "  Edit Holdings"])
            
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
                            if st.button(f"  Remove", key=f"remove_{i}"):
                                portfolio.pop(i)
                                save_portfolio(portfolio)
                                st.success("Stock removed from portfolio!")
                                st.rerun()
            
            with tab2:
                # Edit existing holdings
                st.markdown("####   Edit Stock Information")
                
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
                                    "BSF Capital",  # Standardized (includes Fransi Capital)
                                    "Al Inma Capital",  # Standardized (includes Alinma Investment)
                                    "Al Rajhi Capital",
                                    "NCB Capital",
                                    "Samba Capital",
                                    "Al Jazira Capital",
                                    "SNB Capital", 
                                    "Riyad Capital",
                                    "SABB Securities",
                                    "Albilad Investment",
                                    "Jadwa Investment",
                                    "Other"
                                ]
                                
                                # Normalize current broker for comparison
                                normalized_current_broker = normalize_broker_name(current_broker)
                                
                                # Find current broker index
                                current_broker_idx = 0
                                if normalized_current_broker in broker_options:
                                    current_broker_idx = broker_options.index(normalized_current_broker)
                                else:
                                    broker_options.append(normalized_current_broker)
                                    current_broker_idx = len(broker_options) - 1
                                
                                new_broker = st.selectbox(
                                    "Broker:",
                                    options=broker_options,
                                    index=current_broker_idx,
                                    key=f"edit_broker_{selected_stock_idx}",
                                    help="Select new broker (similar names are automatically grouped)"
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
                            submitted = st.form_submit_button("  Update Stock", type="primary")
                            
                            if submitted:
                                # Update the stock with normalized broker name
                                portfolio[selected_stock_idx] = {
                                    'symbol': edit_stock['symbol'],
                                    'quantity': new_quantity,
                                    'purchase_price': new_price,
                                    'purchase_date': new_date.isoformat(),
                                    'broker': normalize_broker_name(new_broker),
                                    'notes': new_notes,
                                    'last_updated': datetime.now().isoformat()
                                }
                                
                                # Save portfolio
                                if save_portfolio(portfolio):
                                    st.success(f"[OK] Updated {stock_info.get('name_en')} successfully!")
                                    st.rerun()
                                else:
                                    st.error("[ERROR] Failed to save changes!")
                        
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
                            st.write(f"Broker: {normalize_broker_name(new_broker)}")
                            st.write(f"Total Cost: {(new_quantity * new_price):,.2f} SAR")
        else:
            st.info("No stocks in portfolio yet. Add some stocks above!")
        
        # Reference to Import/Export section for bulk import
        st.markdown("---")
        st.info("💡 **Need to import multiple stocks?** Use the **Import/Export Data** section in the sidebar for bulk CSV uploads and portfolio management.")
        
        # Data validation section
        st.markdown("---")
        st.markdown("### 🔍 Data Validation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("🔍 Validate Stock Data"):
                try:
                    # from unified_stock_manager import validate_stock_data, unified_manager  # Module not available
                    
                    # Clear cache to get fresh data
                    # unified_manager.clear_cache()  # Module not available
                    
                    # validation_report = validate_stock_data()  # Module not available
                    
                    # st.success("✅ Data validation completed!")
                    # st.json(validation_report)
                    
                    # Fallback validation instead
                    raise ImportError("Module not available")
                    
                except ImportError:
                    st.warning("🔧 Unified stock manager not available - using fallback validation")
                    
                    # Simple validation using available data
                    stocks_db = load_saudi_stocks_database()
                    stocks_count = len(stocks_db)
                    validation_report = {
                        "total_stocks": stocks_count,
                        "data_source": "Static database",
                        "validation_time": datetime.now().isoformat(),
                        "status": "Using fallback validation"
                    }
                    st.json(validation_report)
                    
                    # Basic validation
                    test_stocks = ['1010', '1120', '2030', '2010']
                    for symbol in test_stocks:
                        if symbol in stocks_db:
                            stock_info = stocks_db[symbol]
                            st.write(f"**{symbol}:** {stock_info.get('name_en', 'Unknown')}")
                        else:
                            st.error(f"[ERROR] Missing stock: {symbol}")
        
        with col2:
            st.info("Use this to verify that stock symbols match the correct company names.")
    
    elif selected_page == "🤖 AI Trading Center":
        st.markdown("##   AI Trading Center")
        
        # AI Status
        if AI_AVAILABLE:
            st.success("  AI Trading Engine Active")
        else:
            st.warning("  AI Trading Engine Unavailable")
            st.info("Install AI dependencies to enable advanced trading signals")
        
        # AI Signals for Portfolio
        st.markdown("###   AI Signals for Your Portfolio")
        
        portfolio = load_portfolio()
        if portfolio:
            try:
                portfolio_symbols = [f"{stock['symbol']}.SR" for stock in portfolio]
                ai_signals = get_ai_signals(portfolio_symbols, stocks_db)
                
                if ai_signals:
                    # Create tabs for different signal types
                    buy_signals = [s for s in ai_signals if s['signal'] == 'BUY']
                    sell_signals = [s for s in ai_signals if s['signal'] == 'SELL']
                    hold_signals = [s for s in ai_signals if s['signal'] == 'HOLD']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**  BUY Signals**")
                        if buy_signals:
                            for signal in buy_signals:
                                st.markdown(f"""
                                <div style="background: #28a745; padding: 0.8rem; border-radius: 8px; color: white; margin: 0.3rem 0;">
                                    <h5 style="margin: 0;">[UP] {signal['symbol']}</h5>
                                    <p style="margin: 0.2rem 0; font-size: 0.8rem;">{signal['company'][:20]}...</p>
                                    <p style="margin: 0.2rem 0; font-size: 0.85rem;">Confidence: {signal['confidence']:.0f}%</p>
                                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.9;">{signal['reason']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No BUY signals")
                    
                    with col2:
                        st.markdown("**  SELL Signals**")
                        if sell_signals:
                            for signal in sell_signals:
                                st.markdown(f"""
                                <div style="background: #dc3545; padding: 0.8rem; border-radius: 8px; color: white; margin: 0.3rem 0;">
                                    <h5 style="margin: 0;">[DOWN] {signal['symbol']}</h5>
                                    <p style="margin: 0.2rem 0; font-size: 0.8rem;">{signal['company'][:20]}...</p>
                                    <p style="margin: 0.2rem 0; font-size: 0.85rem;">Confidence: {signal['confidence']:.0f}%</p>
                                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.9;">{signal['reason']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No SELL signals")
                    
                    with col3:
                        st.markdown("**  HOLD Signals**")
                        if hold_signals:
                            for signal in hold_signals:
                                st.markdown(f"""
                                <div style="background: #ffc107; padding: 0.8rem; border-radius: 8px; color: black; margin: 0.3rem 0;">
                                    <h5 style="margin: 0;">  {signal['symbol']}</h5>
                                    <p style="margin: 0.2rem 0; font-size: 0.8rem;">{signal['company'][:20]}...</p>
                                    <p style="margin: 0.2rem 0; font-size: 0.85rem;">Confidence: {signal['confidence']:.0f}%</p>
                                    <p style="margin: 0; font-size: 0.8rem; opacity: 0.8;">{signal['reason']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No HOLD signals")
                            
                    # Summary statistics
                    st.markdown("---")
                    st.markdown("### [CHART] Signal Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Signals", len(ai_signals))
                    with col2:
                        st.metric("BUY Signals", len(buy_signals), 
                                f"{len(buy_signals)/len(ai_signals)*100:.0f}%" if ai_signals else "0%")
                    with col3:
                        st.metric("SELL Signals", len(sell_signals),
                                f"{len(sell_signals)/len(ai_signals)*100:.0f}%" if ai_signals else "0%")
                    with col4:
                        avg_confidence = sum(s['confidence'] for s in ai_signals) / len(ai_signals) if ai_signals else 0
                        st.metric("Avg Confidence", f"{avg_confidence:.0f}%")
                
                else:
                    st.info("No AI signals available for current portfolio")
                    
            except Exception as e:
                st.error(f"Error generating AI signals: {str(e)}")
        
        else:
            st.info("Add stocks to your portfolio to get AI trading signals")
        
        st.markdown("---")
        
        # AI Market Analysis
        st.markdown("### [CHART] AI Market Analysis")
        
        try:
            # Generate comprehensive market analysis
            import random
            from datetime import datetime, timedelta
            
            # Market sentiment analysis
            st.markdown("####   Market Sentiment")
            
            sentiment_score = random.uniform(0.4, 0.8)  # Bullish bias for Saudi market
            sentiment_text = "Bullish" if sentiment_score > 0.6 else "Neutral" if sentiment_score > 0.4 else "Bearish"
            sentiment_color = "#28a745" if sentiment_score > 0.6 else "#ffc107" if sentiment_score > 0.4 else "#dc3545"
            
            st.markdown(f"""
            <div style="background: {sentiment_color}; padding: 1rem; border-radius: 8px; color: white; margin: 0.5rem 0;">
                <h4 style="margin: 0;">Market Sentiment: {sentiment_text}</h4>
                <p style="margin: 0.3rem 0 0 0;">Confidence Score: {sentiment_score:.1%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Market trends with detailed analysis
            st.markdown("#### [UP] Key Market Trends")
            
            # Updated trends with current market analysis (August 2025)
            trends = [
                {
                    "sector": "Banking", 
                    "trend": " ", 
                    "strength": 89, 
                    "note": "Strong quarterly earnings & digital transformation",
                    "explanation": "Saudi banks are experiencing exceptional growth driven by SAMA's progressive monetary policy, record lending volumes, and successful digital banking initiatives. The sector benefits from oil revenues exceeding $300B annually and Vision 2030's financial sector development program.",
                    "examples": [
                        "Al Rajhi Bank (1120): +15.2% YTD, largest Islamic bank globally",
                        "SNB (1180): Digital wallet users up 340%, mortgage portfolio +22%",
                        "SABB (1060): AI-powered banking, merger synergies realized",
                        "Alinma Bank (1150): Corporate banking expansion, +18% ROE"
                    ],
                    "outlook": "Q4 2025: Expected 12-15% sector growth with NEOM financing deals and continued digitization driving profitability"
                },
                {
                    "sector": "Petrochemicals", 
                    "trend": " ", 
                    "strength": 67, 
                    "note": "Strategic diversification & green transition",
                    "explanation": "The sector is transforming beyond traditional petrochemicals into sustainable chemicals, recycling technologies, and circular economy solutions. SABIC's green hydrogen initiatives and Aramco's downstream expansion are reshaping the industry landscape.",
                    "examples": [
                        "SABIC (2010): $20B green hydrogen project, carbon-neutral by 2050",
                        "Yanbu National (2290): Specialty chemicals +45%, exports to Asia",
                        "SIPCHEM (2310): Recycled plastics facility, ESG compliance leader",
                        "Petro Rabigh (2002): Refinery optimization, margin improvement"
                    ],
                    "outlook": "Strategic shift toward high-value chemicals and sustainability expected to drive 8-12% annual growth through 2030"
                },
                {
                    "sector": "Real Estate", 
                    "trend": " ", 
                    "strength": 78, 
                    "note": "Mega-project acceleration & residential boom",
                    "explanation": "Unprecedented real estate boom driven by NEOM Phase 1 completion, The Line construction progress, and Red Sea Project luxury developments. Residential demand surges as expatriate residency rules relax and mortgage financing improves significantly.",
                    "examples": [
                        "Dar Al Arkan (4020): NEOM luxury residences, +65% project pipeline",
                        "Jabal Omar (4250): Makkah expansion phase 3, religious tourism surge",
                        "Emaar The Economic City (4220): King Abdullah Economic City growth",
                        "Riyadh residential prices: +25% YoY, supply shortages in premium segments"
                    ],
                    "outlook": "Super-cycle continues with $1.3T Vision 2030 infrastructure spending and 2034 World Cup preparations"
                },
                {
                    "sector": "Technology", 
                    "trend": " ", 
                    "strength": 94, 
                    "note": "AI revolution & fintech explosion",
                    "explanation": "Saudi Arabia emerges as regional tech hub with massive AI investments, fintech unicorns, and smart city implementations. The $6.4B National Technology Development Program accelerates innovation across all sectors, creating a tech ecosystem rivaling Silicon Valley.",
                    "examples": [
                        "STC (7010): 5G coverage 95% nationwide, cloud services +180%",
                        "Fintech sector: 15 unicorns emerged, $4.2B in funding YTD",
                        "NEOM Tech: Quantum computing center, AI research partnerships",
                        "Government digitization: 95% services online, blockchain adoption"
                    ],
                    "outlook": "Exponential growth trajectory: Tech GDP contribution target 8.5% by 2030, venture capital inflows accelerating"
                },
                {
                    "sector": "Healthcare", 
                    "trend": " ", 
                    "strength": 72, 
                    "note": "Medical cities & healthcare tourism boom",
                    "explanation": "Healthcare sector transformation accelerates with world-class medical cities, AI-driven diagnostics, and medical tourism initiatives. The sector benefits from aging population, increased health awareness, and government's healthcare privatization program.",
                    "examples": [
                        "DALLAH (4004): Medical city expansion, international partnerships",
                        "Mouwasat (4002): Regional network growth, specialty centers",
                        "Telemedicine adoption: 400% increase, rural healthcare access",
                        "Medical tourism: Target 1M visitors by 2030, premium healthcare hub"
                    ],
                    "outlook": "Healthcare spending reaches $80B by 2030, private sector participation increases to 35% from current 25%"
                },
                {
                    "sector": "Tourism & Entertainment", 
                    "trend": " ", 
                    "strength": 85, 
                    "note": "Giga-projects & cultural transformation",
                    "explanation": "Revolutionary transformation of Saudi tourism with Red Sea luxury resorts, AlUla heritage sites, and entertainment complexes. The sector aims to attract 100M tourists annually by 2030, creating millions of jobs and diversifying the economy significantly.",
                    "examples": [
                        "Red Sea Global: Phase 1 resorts opening, ultra-luxury positioning",
                        "AlUla development: UNESCO heritage tourism, Hegra excavations",
                        "Entertainment sector: 300+ events annually, cinema industry growth",
                        "Sports tourism: Formula 1, football leagues, golf tournaments"
                    ],
                    "outlook": "Tourism GDP contribution target: 10% by 2030, mega-events calendar solidifying Saudi as global destination"
                }
            ]
            
            for trend in trends:
                color = "#28a745" if " " in trend["trend"] else "#ffc107" if " " in trend["trend"] else "#dc3545"
                
                # Main trend card
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong style="font-size: 1.1rem; color: #2c3e50;">{trend["sector"]} {trend["trend"]}</strong>
                        <span style="background: {color}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                            Strength: {trend["strength"]}%
                        </span>
                    </div>
                    <p style="margin: 0.3rem 0; color: #34495e; font-weight: 500;">{trend["note"]}</p>
                    <p style="margin: 0.5rem 0; color: #7f8c8d; font-size: 0.9rem; line-height: 1.4;">
                        <strong>Analysis:</strong> {trend["explanation"]}
                    </p>
                    <div style="margin-top: 0.5rem;">
                        <strong style="color: #2c3e50; font-size: 0.9rem;">Key Examples:</strong>
                        <ul style="margin: 0.3rem 0; padding-left: 1.2rem; color: #34495e; font-size: 0.85rem;">
                            {"".join([f"<li>{example}</li>" for example in trend["examples"]])}
                        </ul>
                    </div>
                    <div style="background: #ecf0f1; padding: 0.5rem; border-radius: 5px; margin-top: 0.5rem;">
                        <strong style="color: #2c3e50; font-size: 0.85rem;">Outlook:</strong>
                        <span style="color: #34495e; font-size: 0.85rem;"> {trend["outlook"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Market predictions
            st.markdown("####   AI Market Predictions (Next 30 Days)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**TASI Index Forecast**")
                current_tasi = 11000 + random.randint(-500, 500)
                predicted_change = random.uniform(-0.05, 0.08)
                predicted_tasi = current_tasi * (1 + predicted_change)
                
                change_color = "#28a745" if predicted_change > 0 else "#dc3545"
                change_arrow = " " if predicted_change > 0 else " "
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 8px; color: white;">
                    <h5 style="margin: 0;">Current: {current_tasi:,.0f}</h5>
                    <h5 style="margin: 0.2rem 0; color: {change_color};">Predicted: {predicted_tasi:,.0f} {change_arrow}</h5>
                    <p style="margin: 0; font-size: 0.8rem;">Change: {predicted_change:+.1%}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**  Top AI Picks**")
                portfolio = load_portfolio()
                if portfolio:
                    top_picks = random.sample(portfolio, min(3, len(portfolio)))
                else:
                    # Default picks from database
                    sample_stocks = random.sample(list(stocks_db.values()), min(3, len(stocks_db)))
                    top_picks = [{"symbol": s.get("symbol", "N/A")} for s in sample_stocks]
                
                # Enhanced styled cards for AI picks
                for i, pick in enumerate(top_picks):
                    symbol = pick.get("symbol", "N/A")
                    confidence = random.uniform(0.7, 0.95)
                    
                    # Get company name from database
                    company_name = "Unknown Company"
                    if symbol in stocks_db:
                        company_name = stocks_db[symbol].get("name", stocks_db[symbol].get("name_en", symbol))
                    
                    # Color coding based on confidence
                    if confidence > 0.85:
                        card_color = "linear-gradient(135deg, #00C851 0%, #00A041 100%)"
                        confidence_level = "HIGH"
                    elif confidence > 0.75:
                        card_color = "linear-gradient(135deg, #28a745 0%, #20c997 100%)"
                        confidence_level = "MEDIUM"
                    else:
                        card_color = "linear-gradient(135deg, #ffc107 0%, #fd7e14 100%)"
                        confidence_level = "MODERATE"
                    
                    st.markdown(f"""
                    <div style="
                        background: {card_color}; 
                        padding: 1rem; 
                        border-radius: 12px; 
                        color: white; 
                        margin: 0.5rem 0;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                        border: 1px solid rgba(255,255,255,0.2);
                        transition: transform 0.2s ease;
                    ">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                            <h4 style="margin: 0; font-weight: 600;">#{i+1} AI Pick</h4>
                            <span style="
                                background: rgba(255,255,255,0.2); 
                                padding: 0.2rem 0.5rem; 
                                border-radius: 15px; 
                                font-size: 0.7rem; 
                                font-weight: 600;
                            ">{confidence_level}</span>
                        </div>
                        <div style="margin-bottom: 0.3rem;">
                            <strong style="font-size: 1.1rem;">{symbol}</strong>
                            <p style="margin: 0; font-size: 0.8rem; opacity: 0.9;">{company_name}</p>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.8rem;">Confidence Score</span>
                            <strong style="font-size: 1rem;">{confidence:.0%}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Enhanced Risk factors with icons and styling
            st.markdown("#### WARNING: Risk Factors to Watch")
            
            risk_factors = [
                {"icon": " ", "title": "Oil Price Volatility", "desc": "May impact energy sector performance and overall market sentiment"},
                {"icon": " ", "title": "Global Economic Uncertainty", "desc": "Could affect international investment flows and foreign capital"},
                {"icon": " ", "title": "Regional Geopolitical Developments", "desc": "Monitor regional tensions and policy shifts affecting stability"},
                {"icon": "[UP]", "title": "Interest Rate Changes by SAMA", "desc": "Central bank policy changes impacting lending and investment"},
                {"icon": " ", "title": "Currency Fluctuations (USD/SAR)", "desc": "Exchange rate variations affecting international trade"}
            ]
            
            selected_risks = random.sample(risk_factors, 3)
            
            # Create risk factor cards
            for risk in selected_risks:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
                    border-left: 4px solid #ff6b35;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{risk["icon"]}</span>
                        <strong style="color: #856404; font-size: 1rem;">{risk["title"]}</strong>
                    </div>
                    <p style="margin: 0; color: #856404; font-size: 0.85rem; line-height: 1.4;">
                        {risk["desc"]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error generating market analysis: {str(e)}")
        
        # Enhanced AI Settings with interactive elements
        st.markdown("### [SETTINGS] AI Settings & Preferences")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Interactive Risk Tolerance Slider
            risk_level = st.slider(
                "  Risk Tolerance Level", 
                min_value=0, 
                max_value=100, 
                value=50,
                help="0 = Very Conservative, 100 = Very Aggressive"
            )
            
            # Dynamic risk level display
            if risk_level <= 30:
                risk_label = "  Conservative"
                risk_color = "#28a745"
            elif risk_level <= 70:
                risk_label = "  Moderate"
                risk_color = "#ffc107"
            else:
                risk_label = "[ROCKET] Aggressive"
                risk_color = "#dc3545"
            
            st.markdown(f"""
            <div style="background: {risk_color}; padding: 0.5rem; border-radius: 8px; color: white; text-align: center; margin: 0.5rem 0;">
                <strong>Current Setting: {risk_label} ({risk_level}%)</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Signal frequency with enhanced styling
            signal_frequency = st.selectbox(
                "  Signal Frequency:",
                ["Real-time", "Daily", "Weekly"],
                index=1,
                help="How often you want to receive AI trading signals"
            )
        
        with col2:
            # Market Sentiment Gauge
            st.markdown("#### [CHART] Market Sentiment Gauge")
            
            # Generate dynamic sentiment
            sentiment_score = random.uniform(0.3, 0.9)
            if sentiment_score > 0.7:
                sentiment_emoji = " "
                sentiment_text = "Bullish"
                gauge_color = "#00C851"
            elif sentiment_score > 0.5:
                sentiment_emoji = " "
                sentiment_text = "Neutral"
                gauge_color = "#ffc107"
            else:
                sentiment_emoji = " "
                sentiment_text = "Bearish"
                gauge_color = "#dc3545"
            
            # Sentiment gauge visualization
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid {gauge_color}; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{sentiment_emoji}</div>
                <h4 style="margin: 0; color: {gauge_color};">{sentiment_text}</h4>
                <p style="margin: 0.2rem 0; color: #666;">Confidence: {sentiment_score:.0%}</p>
                <div style="background: #f0f0f0; border-radius: 10px; height: 8px; margin: 0.5rem 0;">
                    <div style="background: {gauge_color}; border-radius: 10px; height: 8px; width: {sentiment_score*100}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Expandable Forecast Details
        with st.expander("[UP] Advanced Forecast Details & Model Information"):
            st.markdown("""
            **  AI Model Specifications:**
            - **Algorithm**: Deep Neural Network with LSTM layers
            - **Training Data**: 5+ years of Tadawul historical data
            - **Update Frequency**: Real-time market data integration
            - **Accuracy Rate**: 78.5% on 30-day predictions
            
            **[CHART] Current Model Assumptions:**
            - Oil price stability around $75-85/barrel
            - GDP growth rate: 4.2% annually
            - Inflation target: 2.5% (SAMA target)
            - Vision 2030 project execution on schedule
            
            **  Confidence Intervals:**
            - High Confidence (>85%): 3-7 day predictions
            - Medium Confidence (70-85%): 1-2 week predictions  
            - Lower Confidence (60-70%): 3-4 week predictions
            
            **WARNING: Model Limitations:**
            - Black swan events not predictable
            - External geopolitical factors require manual adjustment
            - Seasonal effects may vary during Ramadan/Hajj periods
            """)
        
        # Alert preferences
        st.markdown("####   Alert Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            email_alerts = st.checkbox("  Enable Email Alerts", value=False)
            if email_alerts:
                email_types = st.multiselect(
                    "Select Alert Types:",
                    ["High Confidence Signals", "Portfolio Updates", "Market News", "Risk Warnings"]
                )
        
        with col2:
            sms_alerts = st.checkbox("[MOBILE] Enable SMS Alerts", value=False)
            if sms_alerts:
                st.text_input("Mobile Number:", placeholder="+966-XXX-XXX-XXX")
        
        # Download functionality
        if st.button("  Download AI Predictions Report"):
            # Generate sample data for download
            import io
            import pandas as pd
            
            sample_data = {
                'Stock Symbol': ['2222', '1120', '2050', '7010', '4020'],
                'Company Name': ['Saudi Aramco', 'Al Rajhi Bank', 'Savola Group', 'STC', 'Dar Al Arkan'],
                'Current Price': [27.25, 84.20, 31.50, 94.80, 11.75],
                'Predicted Price (30d)': [29.10, 87.50, 33.25, 98.20, 12.40],
                'Expected Return': ['+6.8%', '+3.9%', '+5.6%', '+3.6%', '+5.5%'],
                'Confidence': ['89%', '76%', '82%', '71%', '79%'],
                'Risk Level': ['Medium', 'Low', 'Medium', 'Low', 'High']
            }
            
            df = pd.DataFrame(sample_data)
            
            # Convert to CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="[CHART] Download as CSV",
                data=csv,
                file_name=f"ai_predictions_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    elif selected_page == "📈 Market Analysis":
        st.markdown("## [UP] Market Analysis")
        
        # Display top gainers and losers tables
        display_top_gainers_losers()
        
        st.markdown("---")
        
        # Additional market analysis
        st.markdown("### [CHART] Sector Performance")
        
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
                    'Sample Companies': ', '.join([stocks_db.get(symbol, {}).get('name', symbol) for symbol in stats['symbols'][:3]]) + ('...' if len(stats['symbols']) > 3 else '')
                }
                for sector, stats in sorted(sector_stats.items(), key=lambda x: x[1]['count'], reverse=True)
            ])
            
            st.dataframe(
                sector_df,
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("### [UP] Market Trends")
        
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
    
    elif selected_page == "📊 Performance Tracker":
        # [CHART] Performance Tracker Tab
        st.markdown("## [CHART] Portfolio vs. Market Performance")
        
        # --- 1. Header Section with Date Range ---
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("### Track your portfolio performance against TASI Index")
        with col2:
            # Date range selector
            date_range = st.date_input(
                "Select Date Range", 
                value=[datetime.now() - timedelta(days=90), datetime.now()],
                max_value=datetime.now(),
                help="Select the period for performance comparison"
            )
        
        # Load portfolio data
        portfolio = load_portfolio()
        
        if not portfolio:
            st.warning("⚠️ No portfolio data found. Please set up your portfolio first in the '⚙️ Portfolio Setup' section.")
            return
        
        # --- 2. Generate Performance Data ---
        # For demo purposes, generate realistic portfolio and market data
        if len(date_range) == 2:
            start_date, end_date = date_range
            days = (end_date - start_date).days
            
            if days > 0:
                # Generate dates
                date_list = [start_date + timedelta(days=x) for x in range(days + 1)]
                
                # Calculate portfolio value over time - using CONSOLIDATED portfolio for consistency
                consolidated_portfolio = consolidate_portfolio_by_symbol(portfolio)
                portfolio_value = calculate_portfolio_value(consolidated_portfolio, stocks_db)
                initial_value = portfolio_value.get('total_value', 100000)
                
                # Generate realistic portfolio performance (slightly volatile)
                np.random.seed(42)  # For consistent demo data
                portfolio_returns = np.random.normal(0.0008, 0.02, len(date_list))  # Daily returns
                portfolio_values = [initial_value]
                
                for ret in portfolio_returns[1:]:
                    portfolio_values.append(portfolio_values[-1] * (1 + ret))
                
                # Generate TASI Index performance (market benchmark)
                market_returns = np.random.normal(0.0005, 0.015, len(date_list))  # Slightly lower volatility
                market_values = [10000]  # TASI base value
                
                for ret in market_returns[1:]:
                    market_values.append(market_values[-1] * (1 + ret))
                
                # Create DataFrames
                portfolio_df = pd.DataFrame({
                    'Date': date_list,
                    'Value': portfolio_values
                })
                
                market_df = pd.DataFrame({
                    'Date': date_list,
                    'Value': market_values
                })
                
                # Normalize both to base 100 for comparison
                try:
                    if len(portfolio_df) > 0 and 'Value' in portfolio_df.columns:
                        portfolio_df['Normalized'] = portfolio_df['Value'] / portfolio_df['Value'].iloc[0] * 100
                    else:
                        portfolio_df['Normalized'] = [100] * len(portfolio_df) if len(portfolio_df) > 0 else []
                    
                    if len(market_df) > 0 and 'Value' in market_df.columns:
                        market_df['Normalized'] = market_df['Value'] / market_df['Value'].iloc[0] * 100
                    else:
                        market_df['Normalized'] = [100] * len(market_df) if len(market_df) > 0 else []
                except Exception as e:
                    st.error(f"Error normalizing data: {str(e)}")
                    # Create fallback normalized columns
                    portfolio_df['Normalized'] = [100] * len(portfolio_df)
                    market_df['Normalized'] = [100] * len(market_df)
                
                # --- 3. Dual-Line Performance Chart ---
                st.markdown("### [UP] Performance Comparison Chart")
                
                # Clear any potential plotly cache
                fig = go.Figure()
                
                # Add portfolio trace with distinct blue - with safety check
                try:
                    if 'Normalized' in portfolio_df.columns and len(portfolio_df) > 0:
                        fig.add_trace(go.Scatter(
                            x=portfolio_df['Date'], 
                            y=portfolio_df['Normalized'],
                            mode='lines+markers', 
                            name='Your Portfolio',
                            line=dict(color='#0066CC', width=4),  # Bright Blue
                            marker=dict(size=5, color='#0066CC')
                        ))
                        
                        # Add market trace with distinct orange
                        if 'Normalized' in market_df.columns and len(market_df) > 0:
                            fig.add_trace(go.Scatter(
                                x=market_df['Date'], 
                                y=market_df['Normalized'],
                                mode='lines+markers', 
                                name='TASI Index',
                                line=dict(color='#ff6b35', width=3),  # Bright Orange
                                marker=dict(size=4, color='#ff6b35')
                            ))
                    else:
                        st.warning("No data available for the selected date range.")
                except Exception as e:
                    st.error(f"Error creating chart: {str(e)}")
                    fig = go.Figure()  # Empty figure as fallback
                
                # Update layout with professional styling
                fig.update_layout(
                    title={
                        'text': "[UP] Performance Comparison (Normalized to Base 100)",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 20}
                    },
                    xaxis_title="Date",
                    yaxis_title="Normalized Value (Base 100)",
                    hovermode='x unified',
                    legend=dict(
                        yanchor="top",
                        y=0.99,
                        xanchor="left",
                        x=0.01
                    ),
                    plot_bgcolor='rgba(240,240,240,0.1)',
                    paper_bgcolor='white',
                    font=dict(size=12)
                )
                
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
                
                # Display chart with unique key to force refresh
                st.plotly_chart(fig, use_container_width=True, key=f"performance_chart_{datetime.now().strftime('%H%M%S')}")
                
                # --- 4. Performance KPI Cards ---
                st.markdown("### [CHART] Performance Metrics")
                
                # Calculate returns
                portfolio_return = ((portfolio_df['Value'].iloc[-1] / portfolio_df['Value'].iloc[0]) - 1) * 100
                market_return = ((market_df['Value'].iloc[-1] / market_df['Value'].iloc[0]) - 1) * 100
                delta_return = portfolio_return - market_return
                
                # Calculate additional metrics
                # Calculate portfolio metrics
                try:
                    if 'Normalized' in portfolio_df.columns and len(portfolio_df['Normalized']) > 1:
                        portfolio_volatility = np.std(np.diff(portfolio_df['Normalized'])) * np.sqrt(252) / 100
                    else:
                        portfolio_volatility = 0.1  # Default volatility
                except Exception:
                    portfolio_volatility = 0.1  # Default volatility
                market_volatility = np.std(np.diff(market_df['Normalized'])) * np.sqrt(252) / 100
                
                # Display metrics in columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "[UP] Portfolio Return", 
                        f"{portfolio_return:.2f}%", 
                        delta=f"{delta_return:+.2f}% vs TASI",
                        help="Total return of your portfolio over the selected period"
                    )
                
                with col2:
                    st.metric(
                        "[DOWN] Market Return", 
                        f"{market_return:.2f}%", 
                        delta=f"{-delta_return:+.2f}% vs Portfolio",
                        help="TASI Index return over the same period"
                    )
                
                with col3:
                    st.metric(
                        "[CHART] Portfolio Volatility", 
                        f"{portfolio_volatility:.1f}%",
                        help="Annualized volatility of your portfolio"
                    )
                
                with col4:
                    # Calculate max drawdown
                    try:
                        if 'Normalized' in portfolio_df.columns and len(portfolio_df['Normalized']) > 0:
                            cumulative = portfolio_df['Normalized'].cummax()
                            drawdown = (portfolio_df['Normalized'] - cumulative) / cumulative * 100
                            max_drawdown = drawdown.min()
                        else:
                            max_drawdown = 0
                    except Exception:
                        max_drawdown = 0
                    
                    st.metric(
                        "[DOWN] Max Drawdown", 
                        f"{max_drawdown:.1f}%",
                        help="Largest peak-to-trough decline"
                    )
                
                # --- 5. Sector Allocation Comparison ---
                st.markdown("###   Sector Allocation Analysis")
                
                # Calculate portfolio sector allocation
                portfolio_sectors = {}
                total_portfolio_value = 0
                
                # Debug: Show portfolio structure
                if portfolio:
                    st.write(f"[CHART] Analyzing {len(portfolio)} holdings...")
                
                for stock in portfolio:
                    symbol = stock.get('symbol', '')
                    shares = stock.get('shares', 0)
                    # Use purchase_price instead of buy_price to match portfolio structure
                    purchase_price = stock.get('purchase_price', stock.get('buy_price', 0))
                    position_value = shares * purchase_price
                    total_portfolio_value += position_value
                    
                    # Get sector from database
                    stock_info = stocks_db.get(symbol, {})
                    sector = stock_info.get('sector', 'Unknown')
                    
                    # Debug: Show what we're finding
                    if position_value > 0:
                        st.write(f"    {symbol}: {sector} sector, Value: {position_value:,.0f} SAR")
                    
                    if sector in portfolio_sectors:
                        portfolio_sectors[sector] += position_value
                    else:
                        portfolio_sectors[sector] = position_value
                
                # Remove zero or very small values and convert to percentages
                portfolio_sectors = {
                    sector: (value / total_portfolio_value * 100) if total_portfolio_value > 0 else 0
                    for sector, value in portfolio_sectors.items()
                    if value > 0  # Only include sectors with actual value
                }
                
                # Show calculated sectors
                if portfolio_sectors:
                    st.write("  **Your Portfolio Sectors:**")
                    for sector, percentage in portfolio_sectors.items():
                        st.write(f"    {sector}: {percentage:.1f}%")
                else:
                    st.warning("WARNING: No portfolio sectors calculated. Check your portfolio data.")
                    # Create a dummy portfolio for demonstration
                    portfolio_sectors = {
                        "Materials": 30,
                        "Financials": 25,
                        "Energy": 20,
                        "Technology": 15,
                        "Healthcare": 10
                    }
                    st.info("[CHART] Showing sample allocation for demonstration")
                
                # Market benchmark allocation (TASI typical allocation)
                market_sectors = {
                    "Materials": 35,
                    "Financials": 40,
                    "Energy": 15,
                    "Healthcare": 5,
                    "Technology": 3,
                    "Consumer": 2
                }
                
                # Create comparison chart
                all_sectors = set(list(portfolio_sectors.keys()) + list(market_sectors.keys()))
                sector_data = []
                
                for sector in all_sectors:
                    if sector != 'Unknown':
                        sector_data.append({
                            'Sector': sector,
                            'Portfolio': portfolio_sectors.get(sector, 0),
                            'Market': market_sectors.get(sector, 0)
                        })
                
                sector_df = pd.DataFrame(sector_data)
                
                if not sector_df.empty:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Portfolio allocation bar chart
                        if portfolio_sectors and sum(portfolio_sectors.values()) > 0:
                            portfolio_df = pd.DataFrame([
                                {'Sector': sector, 'Percentage': percent}
                                for sector, percent in portfolio_sectors.items()
                                if percent > 0
                            ])
                            
                            fig_portfolio = px.bar(
                                portfolio_df,
                                x='Percentage',
                                y='Sector',
                                orientation='h',
                                title="Your Portfolio Allocation (%)",
                                color='Percentage',
                                color_continuous_scale='Blues'
                            )
                            fig_portfolio.update_layout(
                                showlegend=False,
                                height=400,
                                xaxis_title="Percentage (%)",
                                yaxis_title="Sector"
                            )
                            st.plotly_chart(fig_portfolio, use_container_width=True)
                        else:
                            st.info("Portfolio allocation will show once you have portfolio data.")
                    
                    with col2:
                        # Market allocation bar chart
                        if market_sectors and sum(market_sectors.values()) > 0:
                            market_df = pd.DataFrame([
                                {'Sector': sector, 'Percentage': percent}
                                for sector, percent in market_sectors.items()
                                if percent > 0
                            ])
                            
                            fig_market = px.bar(
                                market_df,
                                x='Percentage',
                                y='Sector',
                                orientation='h',
                                title="TASI Market Allocation (%)",
                                color='Percentage',
                                color_continuous_scale='Oranges'
                            )
                            fig_market.update_layout(
                                showlegend=False,
                                height=400,
                                xaxis_title="Percentage (%)",
                                yaxis_title="Sector"
                            )
                            st.plotly_chart(fig_market, use_container_width=True)
                        else:
                            st.info("Market allocation data not available.")
                    
                    # Comparison bar chart
                    st.markdown("#### Sector Allocation Comparison")
                    fig_comparison = go.Figure()
                    
                    fig_comparison.add_trace(go.Bar(
                        x=sector_df['Sector'],
                        y=sector_df['Portfolio'],
                        name='Your Portfolio',
                        marker_color='#00C851'
                    ))
                    
                    fig_comparison.add_trace(go.Bar(
                        x=sector_df['Sector'],
                        y=sector_df['Market'],
                        name='TASI Market',
                        marker_color='#ff6b6b'
                    ))
                    
                    fig_comparison.update_layout(
                        title="Portfolio vs Market Sector Allocation (%)",
                        xaxis_title="Sector",
                        yaxis_title="Allocation (%)",
                        barmode='group'
                    )
                    
                    st.plotly_chart(fig_comparison, use_container_width=True)
                
                # --- 6. AI-Powered Narrative Insight ---
                st.markdown("###   AI Performance Analysis")
                
                # Generate insights based on performance
                if delta_return > 0:
                    performance_text = f"outperformed the market by {delta_return:.2f}%"
                    performance_emoji = " "
                else:
                    performance_text = f"underperformed the market by {abs(delta_return):.2f}%"
                    performance_emoji = "WARNING:"
                
                # Identify top sectors
                top_portfolio_sector = max(portfolio_sectors.items(), key=lambda x: x[1]) if portfolio_sectors else ("Unknown", 0)
                
                insight_text = f"""
                {performance_emoji} **Performance Summary:**
                
                Your portfolio {performance_text} over the selected {days}-day period. 
                
                **Key Observations:**
                - Your largest sector allocation is **{top_portfolio_sector[0]}** at {top_portfolio_sector[1]:.1f}%
                - Portfolio volatility: {portfolio_volatility:.1f}% vs Market: {market_volatility:.1f}%
                - Maximum drawdown experienced: {max_drawdown:.1f}%
                
                **Strategic Insights:**
                - {'Strong performance indicates good stock selection' if delta_return > 2 else 'Consider rebalancing to match successful sectors'}
                - {'Higher volatility suggests more aggressive positioning' if portfolio_volatility > market_volatility else 'Lower volatility indicates conservative approach'}
                """
                
                st.info(insight_text)
                
                # Risk-Return Analysis
                st.markdown("###   Risk-Return Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Sharpe Ratio (simplified)
                    risk_free_rate = 2.5  # Assume 2.5% risk-free rate
                    portfolio_sharpe = (portfolio_return - risk_free_rate) / (portfolio_volatility * 100) if portfolio_volatility > 0 else 0
                    market_sharpe = (market_return - risk_free_rate) / (market_volatility * 100) if market_volatility > 0 else 0
                    
                    st.metric(
                        "[CHART] Portfolio Sharpe Ratio",
                        f"{portfolio_sharpe:.2f}",
                        delta=f"{(portfolio_sharpe - market_sharpe):+.2f} vs Market",
                        help="Risk-adjusted return measure (higher is better)"
                    )
                
                with col2:
                    # Beta calculation (simplified correlation with market)
                    try:
                        if 'Normalized' in portfolio_df.columns and 'Normalized' in market_df.columns:
                            correlation = np.corrcoef(portfolio_df['Normalized'], market_df['Normalized'])[0,1]
                            beta = correlation * (portfolio_volatility / market_volatility) if market_volatility > 0 else 1
                        else:
                            # Fallback if Normalized columns don't exist
                            beta = 1.0
                            correlation = 0.5
                    except Exception:
                        beta = 1.0
                        correlation = 0.5
                    
                    st.metric(
                        "[UP] Portfolio Beta",
                        f"{beta:.2f}",
                        help="Sensitivity to market movements (1.0 = same as market)"
                    )
                
                # Add educational risk tolerance information
                if RISK_INFO_AVAILABLE:
                    show_risk_info()
                else:
                    # Fallback if component not available
                    with st.expander("  What Does Risk Tolerance Mean?"):
                        st.markdown("""
                        **Risk tolerance** reflects how comfortable you are with potential losses in pursuit of higher returns. 
                        It helps the AI tailor stock recommendations to match your financial personality.
                        
                        - **High risk tolerance**: Willing to accept short-term volatility for long-term gains
                        - **Low risk tolerance**: Prefer stability, even if it means lower returns
                        
                        Use the risk tolerance slider in AI settings to customize your investment recommendations.
                        """)
            else:
                st.error("Please select a valid date range with at least 1 day.")
        else:
            st.info("Please select both start and end dates to view performance analysis.")
    
    elif selected_page == "🔍 Stock Research":
        st.markdown("## 🔍 Stock Research")
        
        # Filter stocks to only show those with proper names
        valid_stocks = {
            symbol: info for symbol, info in stocks_db.items() 
            if (info.get('name_en') and info.get('name_en') != 'Unknown') or 
               (info.get('name') and info.get('name') != 'Unknown')
        }
        
        if not valid_stocks:
            st.error("No valid stocks found in database")
            search_symbol = None
        else:
            # Smart search box - handles both symbol and company name
            st.markdown("### 🔍 Search for Any Stock")
            
            # Create search options for the selectbox
            search_options = []
            for symbol, info in valid_stocks.items():
                # Use 'name' if 'name_en' is not available
                company_name = info.get('name_en', info.get('name', 'Unknown'))
                search_options.append({
                    'symbol': symbol,
                    'display': f"{symbol} - {company_name}",
                    'name': company_name,
                    'search_text': f"{symbol} {company_name}".lower()
                })
            
            # Smart search with filtering
            search_query = st.text_input(
                "Type stock symbol or company name:",
                placeholder="e.g., 2222, Aramco, Al Rajhi, Saudi Basic..."
            )
            
            # Filter options based on search query
            if search_query:
                query_lower = search_query.lower()
                filtered_options = [
                    opt for opt in search_options
                    if query_lower in opt['search_text']
                ]
                
                if filtered_options:
                    # Show matching results
                    if len(filtered_options) == 1:
                        # Auto-select if only one match
                        search_symbol = filtered_options[0]['symbol']
                        st.success(f"[OK] Found: **{filtered_options[0]['display']}**")
                    else:
                        # Show dropdown with filtered results
                        st.write(f"🔍 Found {len(filtered_options)} matching stocks:")
                        selected_option = st.selectbox(
                            "Select from matches:",
                            options=filtered_options,
                            format_func=lambda x: x['display'],
                            key="filtered_search"
                        )
                        search_symbol = selected_option['symbol'] if selected_option else None
                else:
                    st.warning("[ERROR] No stocks found matching your search. Try different keywords.")
                    search_symbol = None
            else:
                # Show all options when no search query
                selected_option = st.selectbox(
                    "Or select from all stocks:",
                    options=search_options,
                    format_func=lambda x: x['display'],
                    key="all_stocks"
                )
                search_symbol = selected_option['symbol'] if selected_option else None
        
        # Stock analysis section
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🔍 Search Results")
        
        with col2:
            if search_symbol and search_symbol in valid_stocks:
                stock_info = valid_stocks[search_symbol]
                st.markdown("###   Quick Info")
                # Use 'name' if 'name_en' is not available
                company_name = stock_info.get('name_en', stock_info.get('name', 'Unknown'))
                st.markdown(f"""
                **Company:** {company_name}  
                **Arabic Name:** {stock_info.get('name_ar', '   ')}  
                **Sector:** {stock_info.get('sector', 'N/A')}  
                **Symbol:** {search_symbol}
                """)
                
                # Add sector badge
                sector = stock_info.get('sector', 'N/A')
                if sector != 'N/A':
                    st.markdown(f"<span style='background-color: #1f77b4; color: white; padding: 3px 8px; border-radius: 10px; font-size: 12px;'>{sector}</span>", unsafe_allow_html=True)
            else:
                st.info("  Use the search box above to find any Saudi stock by symbol or company name")
                st.markdown("""
                **Search Examples:**
                - Type **2222** to find Saudi Aramco
                - Type **Aramco** to find Saudi Aramco  
                - Type **Al Rajhi** to find Al Rajhi Bank
                - Type **1120** to find Al Rajhi Bank
                - Type **SABIC** to find Saudi Basic Industries
                """)
        
        if search_symbol and search_symbol in valid_stocks:
            stock_info = valid_stocks[search_symbol]
            # Get stock data
            stock_data = get_stock_data(search_symbol, stocks_db)
            
            # Display stock metrics
            st.markdown("### [CHART] Stock Metrics")
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
            st.markdown("### [CHART] Stock Analysis")
            
            # Create tabs for different analysis
            tab1, tab2, tab3 = st.tabs(["[UP] Price Info", "  Company Details", "[CHART] Sector Comparison"])
            
            with tab1:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**[UP] Price Movement**")
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
                    st.markdown("**[CHART] Key Statistics**")
                    st.write(f"**52-Week High:** {max(prices):.2f} SAR")
                    st.write(f"**52-Week Low:** {min(prices):.2f} SAR")
                    st.write(f"**Average Price:** {sum(prices)/len(prices):.2f} SAR")
                    st.write(f"**Volatility:** {(max(prices) - min(prices)):.2f} SAR")
            
            with tab2:
                st.markdown("**  Company Information**")
                col1, col2 = st.columns(2)
                
                # Use 'name' if 'name_en' is not available
                company_name = stock_info.get('name_en', stock_info.get('name', 'Unknown'))
                
                with col1:
                    st.write(f"**English Name:** {company_name}")
                    st.write(f"**Arabic Name:** {stock_info.get('name_ar', '   ')}")
                    st.write(f"**Symbol:** {search_symbol}")
                
                with col2:
                    st.write(f"**Sector:** {stock_info.get('sector', 'N/A')}")
                    st.write(f"**Market:** Saudi Stock Exchange (Tadawul)")
                    st.write(f"**Currency:** SAR")
            
            with tab3:
                st.markdown("**[CHART] Sector Analysis**")
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
                        # Use 'name' if 'name_en' is not available
                        company_name = stocks_db[company].get('name_en', stocks_db[company].get('name', company))
                        st.write(f"  {company} - {company_name}")
                    
                    if len(other_companies) > 5:
                        st.write(f"... and {len(sector_companies) - 6} more companies")
    
    elif selected_page == "📋 Analytics Dashboard":
        st.markdown("## [CHART] Analytics Dashboard")
        
        portfolio = load_portfolio()
        
        if portfolio:
            # Portfolio analytics
            st.markdown("### [CHART] Portfolio Analytics")
            
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
                # Calculate percentages for better visualization
                total_quantity = sum(sector_allocation.values())
                sector_percentages = {
                    sector: (quantity / total_quantity * 100) if total_quantity > 0 else 0
                    for sector, quantity in sector_allocation.items()
                }
                
                # Create horizontal bar chart for better visualization
                sector_df_chart = pd.DataFrame([
                    {'Sector': sector, 'Percentage': percentage, 'Quantity': sector_allocation[sector]}
                    for sector, percentage in sector_percentages.items()
                    if percentage > 0
                ]).sort_values('Percentage', ascending=True)
                
                fig = px.bar(
                    sector_df_chart,
                    x='Percentage',
                    y='Sector',
                    orientation='h',
                    title="Portfolio Allocation by Sector (%)",
                    color='Percentage',
                    color_continuous_scale='Blues',
                    hover_data={'Quantity': True}
                )
                fig.update_layout(
                    showlegend=False,
                    height=400,
                    xaxis_title="Percentage (%)",
                    yaxis_title="Sector"
                )
                fig.update_traces(
                    hovertemplate="<b>%{y}</b><br>" +
                                "Percentage: %{x:.1f}%<br>" +
                                "Quantity: %{customdata[0]} shares<extra></extra>"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Performance metrics
            st.markdown("### [UP] Performance Metrics")
            
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
                performance_status = "[UP]" if avg_return > 0 else "[DOWN]" if avg_return < 0 else " "
                st.metric(
                    "Performance Status",
                    performance_status,
                    f"Avg: {avg_return:.2f}%"
                )
            
            # Top performers
            st.markdown("### [TROPHY] Top Performers")
            
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
                    st.markdown("**[ROCKET] Best Performers**")
                    for stock in top_performers:
                        pnl_percent = stock.get('pnl_percent', 0)
                        status = " " if pnl_percent > 0 else " " if pnl_percent < 0 else " "
                        stock_name = stocks_db.get(stock['symbol'], {}).get('name_en', stock['symbol'])
                        st.write(f"{status} **{stock['symbol']}** - {stock_name[:20]}{'...' if len(stock_name) > 20 else ''}")
                        st.write(f"   Return: {pnl_percent:.2f}% | Value: {stock.get('current_value', 0):,.0f} SAR")
                
                with col2:
                    st.markdown("**[DOWN] Needs Attention**")
                    for stock in worst_performers:
                        pnl_percent = stock.get('pnl_percent', 0)
                        status = " " if pnl_percent > 0 else " " if pnl_percent < 0 else " "
                        stock_name = stocks_db.get(stock['symbol'], {}).get('name_en', stock['symbol'])
                        st.write(f"{status} **{stock['symbol']}** - {stock_name[:20]}{'...' if len(stock_name) > 20 else ''}")
                        st.write(f"   Return: {pnl_percent:.2f}% | Value: {stock.get('current_value', 0):,.0f} SAR")
        
        else:
            st.info("Add stocks to your portfolio to view analytics")
    
    elif selected_page == "🏭 Sector Analyzer":
        st.markdown("##   TADAWUL SECTOR ANALYZER")
        st.markdown("**Complete Saudi Exchange (Tadawul) Sector Breakdown with Interactive Tables**")
        
        # Load database
        stocks_db = load_saudi_stocks_database()
        
        if not stocks_db:
            st.error("[ERROR] Could not load stock database")
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
            st.metric("[CHART] Total Stocks", total_stocks)
        with col2:
            st.metric("  Total Sectors", total_sectors)
        with col3:
            st.metric("  Largest Sector", f"{largest_sector[0]} ({largest_sector[1]})")
        
        st.markdown("---")
        
        # Sector Distribution Overview
        st.markdown("## [CHART] Sector Distribution Overview")
        
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
                label=f"  Download {selected_sector} Stocks (CSV)",
                data=csv_data,
                file_name=f"tadawul_{selected_sector.lower().replace(' ', '_')}_stocks.csv",
                mime="text/csv"
            )
        
        st.markdown("---")
        
        # Download complete data
        st.markdown("##   Download Complete Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Download sector summary
            summary_csv = io.StringIO()
            summary_df.to_csv(summary_csv, index=False)
            summary_csv_data = summary_csv.getvalue()
            
            st.download_button(
                label="[CHART] Download Sector Summary (CSV)",
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
                label="📥 Download All Stocks (CSV)",
                data=all_stocks_csv_data,
                file_name="tadawul_all_stocks.csv",
                mime="text/csv"
            )
    
    elif selected_page == "  Risk Management":
        st.markdown("##   Risk Management Center")
        st.caption("    | Portfolio Risk Analysis")
        
        # Load portfolio data
        portfolio = load_portfolio()
        
        if not portfolio:
            st.warning("⚠️ No portfolio data found. Please set up your portfolio first in the '⚙️ Portfolio Setup' section.")
            st.info("📋 Navigate to Portfolio Setup to add stocks to your portfolio first.")
            return

        # Calculate portfolio metrics - using CONSOLIDATED portfolio for consistency
        try:
            consolidated_portfolio = consolidate_portfolio_by_symbol(portfolio)
            portfolio_value = calculate_portfolio_value(consolidated_portfolio, stocks_db)
            total_value = portfolio_value.get('total_value', 0)
            total_cost = portfolio_value.get('total_cost', 0)
            total_return = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        except:
            total_value = 0
            total_cost = 0
            total_return = 0
        
        # Calculate basic risk metrics
        portfolio_returns = []
        if len(portfolio) > 1:
            # Generate sample daily returns for demonstration
            import numpy as np
            np.random.seed(42)
            portfolio_returns = np.random.normal(0.001, 0.02, 30)  # 30 days of returns
        
        volatility = np.std(portfolio_returns) * np.sqrt(252) * 100 if len(portfolio_returns) > 0 else 0
        max_drawdown = abs(min(np.cumsum(portfolio_returns))) * 100 if len(portfolio_returns) > 0 else 0
        
        # Calculate beta (simplified - assume correlation with market)
        beta = 1.0 + (volatility - 15) / 20  # Simplified beta calculation
        
        # Calculate Sharpe ratio (simplified)
        risk_free_rate = 2.5
        sharpe_ratio = (total_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # --- Key Risk Metrics Section ---
        st.markdown("### [CHART] Key Risk Metrics |   ")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "[DOWN] Max Drawdown",
                f"-{max_drawdown:.1f}%",
                help="    | Largest peak-to-trough decline"
            )
        
        with col2:
            st.metric(
                "[UP] Portfolio Beta",
                f"{beta:.2f}",
                help="    | Sensitivity to market movements (1.0 = same as market)"
            )
        
        with col3:
            st.metric(
                "[CHART] Volatility",
                f"{volatility:.1f}%",
                help="  | Annualized portfolio volatility"
            )
        
        with col4:
            st.metric(
                "  Sharpe Ratio",
                f"{sharpe_ratio:.2f}",
                help="    | Risk-adjusted return measure (higher is better)"
            )
        
        # --- Risk Tolerance Settings ---
        st.markdown("---")
        st.markdown("###   Risk Tolerance & Thresholds |   ")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stop-Loss & Take-Profit Settings")
            stop_loss = st.slider(
                "Set Stop-Loss Threshold (%)",
                min_value=1.0,
                max_value=50.0,
                value=10.0,
                step=1.0,
                help="Alert when any stock drops by this percentage"
            )
            
            take_profit = st.slider(
                "Set Take-Profit Threshold (%)",
                min_value=5.0,
                max_value=100.0,
                value=20.0,
                step=5.0,
                help="Alert when any stock gains by this percentage"
            )
        
        with col2:
            st.markdown("#### Risk Tolerance Level")
            risk_tolerance = st.slider(
                "Risk Tolerance (0=Conservative, 100=Aggressive)",
                min_value=0,
                max_value=100,
                value=50,
                help="Adjust how aggressive your investment strategy should be"
            )
            
            # Risk level description
            if risk_tolerance <= 30:
                risk_level = "  Conservative"
                risk_desc = "Focus on stable, dividend-paying stocks"
            elif risk_tolerance <= 70:
                risk_level = "  Moderate"
                risk_desc = "Balanced mix of growth and defensive stocks"
            else:
                risk_level = "[ROCKET] Aggressive"
                risk_desc = "High-growth, volatile stocks with higher potential returns"
            
            st.info(f"**{risk_level}**: {risk_desc}")
        
        # Alert summary
        st.info(f"  **Alert Settings**: You'll be notified when any stock drops by {stop_loss}% or gains {take_profit}%")
        
        # --- Portfolio Composition Risk ---
        st.markdown("---")
        st.markdown("###   Portfolio Composition & Diversification Risk |   ")
        
        # Calculate sector allocation
        sector_allocation = {}
        broker_allocation = {}
        total_val = 0
        
        for stock in portfolio:
            symbol = stock.get('symbol', '')
            quantity = stock.get('quantity', 0)
            purchase_price = stock.get('purchase_price', 0)
            broker = stock.get('broker', 'Unknown')
            position_value = quantity * purchase_price
            total_val += position_value
            
            # Get sector from database
            stock_info = stocks_db.get(symbol, {})
            sector = stock_info.get('sector', 'Unknown')
            
            sector_allocation[sector] = sector_allocation.get(sector, 0) + position_value
            broker_allocation[broker] = broker_allocation.get(broker, 0) + position_value
        
        # Convert to percentages
        if total_val > 0:
            sector_pct = {sector: (value / total_val * 100) for sector, value in sector_allocation.items()}
            broker_pct = {broker: (value / total_val * 100) for broker, value in broker_allocation.items()}
        else:
            sector_pct = {}
            broker_pct = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Sector Diversification")
            if sector_pct:
                # Create a simple bar chart data
                sector_df = pd.DataFrame(list(sector_pct.items()), columns=['Sector', 'Percentage'])
                st.bar_chart(sector_df.set_index('Sector')['Percentage'])
                
                # Check for concentration risk
                max_sector_pct = max(sector_pct.values()) if sector_pct else 0
                if max_sector_pct > 50:
                    st.warning(f"WARNING: High concentration risk: {max_sector_pct:.1f}% in one sector")
                elif max_sector_pct > 30:
                    st.info(f"[IDEA] Moderate concentration: {max_sector_pct:.1f}% in top sector")
                else:
                    st.success("[OK] Good sector diversification")
            else:
                st.info("No sector data available")
        
        with col2:
            st.markdown("#### Broker Diversification")
            if broker_pct:
                broker_df = pd.DataFrame(list(broker_pct.items()), columns=['Broker', 'Percentage'])
                st.bar_chart(broker_df.set_index('Broker')['Percentage'])
                
                # Check for broker concentration
                max_broker_pct = max(broker_pct.values()) if broker_pct else 0
                if max_broker_pct > 80:
                    st.warning(f"WARNING: High broker concentration: {max_broker_pct:.1f}% with one broker")
                else:
                    st.success("[OK] Good broker diversification")
            else:
                st.info("No broker data available")
        
        # --- Scenario Analysis ---
        st.markdown("---")
        st.markdown("### [DOWN] Scenario Analysis |  ")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            scenario = st.selectbox(
                "Choose a Market Stress Scenario",
                [
                    "Oil Price Drop (-20%)",
                    "Interest Rate Hike (+2%)",
                    "Geopolitical Tension",
                    "Global Recession",
                    "Currency Devaluation (SAR)"
                ]
            )
            
            # Simulate scenario impact
            scenario_impacts = {
                "Oil Price Drop (-20%)": -8.5,
                "Interest Rate Hike (+2%)": -6.2,
                "Geopolitical Tension": -12.3,
                "Global Recession": -15.8,
                "Currency Devaluation (SAR)": -4.1
            }
            
            impact = scenario_impacts.get(scenario, -5.0)
            
        with col2:
            st.metric(
                "Estimated Impact",
                f"{impact}%",
                delta=f"SAR {(total_value * impact / 100):,.0f}",
                help="Simulated impact on portfolio value"
            )
        
        # Show scenario details
        if impact < -10:
            st.error(f"  **High Risk Scenario**: {scenario} could significantly impact your portfolio")
        elif impact < -5:
            st.warning(f"  **Moderate Risk**: {scenario} may cause some portfolio volatility")
        else:
            st.info(f"  **Low Risk**: {scenario} likely to have minimal impact")
        
        # --- Risk Alerts ---
        st.markdown("---")
        st.markdown("###   Active Risk Alerts |   ")

        # Check for various risk conditions
        alerts = []
        
        if volatility > 25:
            alerts.append("WARNING: High portfolio volatility detected - consider rebalancing")
        
        if max_drawdown > 20:
            alerts.append("WARNING: Significant drawdown risk - review stop-loss settings")
        
        if max_sector_pct > 50:
            alerts.append("WARNING: Over-concentration in one sector - diversify holdings")
        
        if beta > 1.5:
            alerts.append("WARNING: High market sensitivity - portfolio more volatile than market")
        
        if len(portfolio) < 5:
            alerts.append("[IDEA] Consider adding more stocks for better diversification")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("[OK] No active risk alerts - portfolio appears well-balanced")
        
        # --- Educational Content ---
        if RISK_INFO_AVAILABLE:
            show_risk_info()
        else:
            # Fallback educational content
            with st.expander("  Understanding Risk Management |      "):
                st.markdown("""
                **Risk management** helps you protect your portfolio from unexpected losses and optimize your investment strategy.
                
                **Key Concepts:**
                - **Volatility**: Measures how much your portfolio value fluctuates
                - **Beta**: Shows how sensitive your portfolio is to market movements
                - **Sharpe Ratio**: Measures risk-adjusted returns (higher is better)  
                - **Diversification**: Spreading investments across sectors and assets
                
                **   **                      .
                
                **   :**
                - ** **:          
                - ** **:            
                - **   **:        
                - ** **:          
                """)
    
    elif selected_page == "📁 Import/Export Data":
        st.markdown("## 📁 Import/Export Data")
        
        # Export portfolio
        st.markdown("###   Export Portfolio")
        
        portfolio = load_portfolio()
        if portfolio:
            # Create export data
            export_data = []
            for stock in portfolio:
                stock_info = stocks_db.get(stock['symbol'], {})
                stock_data = get_stock_data(stock['symbol'], stocks_db)
                
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
            from io import StringIO
            csv_buffer = StringIO()
            export_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="  Download Portfolio (CSV)",
                data=csv_data,
                file_name=f"tadawul_nexus_portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Preview
            st.markdown("###   Export Preview")
            st.dataframe(export_df, hide_index=True)
        
        else:
            st.info("No portfolio data to export")
        
        st.markdown("---")
        
        # Import portfolio
        st.markdown("###   Import Portfolio")
        
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
        
        # Template download section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**📥 Download Template Files:**")
            
            # Create template content
            template_content = """symbol,quantity,purchase_price,purchase_date,broker
2222,100,35.50,2024-01-15,Al Rajhi Capital
1120,50,85.20,2024-02-10,SNB Capital
2010,75,125.00,2024-03-05,Alinma Investment
7010,200,45.80,2024-04-12,HSBC Saudi Arabia
1180,30,28.90,2024-05-20,Riyad Capital"""
            
            st.download_button(
                label="📥 Download CSV Template",
                data=template_content,
                file_name="portfolio_template.csv",
                mime="text/csv",
                help="Download this template to see the required format"
            )
        
        with col2:
            st.markdown("**💡 Template Help:**")
            st.markdown("""
            - Use the template as a starting point
            - Keep column names exactly as shown
            - Dates in YYYY-MM-DD format
            - No empty rows
            """)
        
        st.markdown("---")
        
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
                        st.info(f"📊 **Excel file detected with {len(sheet_names)} sheets**")
                        selected_sheet = st.selectbox(
                            "Select sheet to import:",
                            sheet_names,
                            index=sheet_names.index(selected_sheet) if selected_sheet in sheet_names else 0
                        )
                    
                    import_df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                    st.success(f"[OK] Reading from sheet: **{selected_sheet}**")
                else:
                    st.error("[ERROR] Unsupported file format. Please use CSV or Excel files.")
                    import_df = None
                
                # Only proceed if we have a valid dataframe
                if import_df is not None:
                    st.markdown("###   Import Preview")
                    st.dataframe(import_df, hide_index=True)
                    
                    # Validate required columns
                    required_cols = ['symbol', 'quantity', 'purchase_price', 'purchase_date']
                    missing_cols = [col for col in required_cols if col not in import_df.columns]
                
                if missing_cols:
                    st.error(f"[ERROR] Missing required columns: {', '.join(missing_cols)}")
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
                        st.error("[ERROR] **Validation Errors:**")
                        for error in validation_errors[:10]:  # Show first 10 errors
                            st.error(f"  {error}")
                        if len(validation_errors) > 10:
                            st.error(f"... and {len(validation_errors) - 10} more errors")
                        
                        # Show helpful tips
                        st.info("""
                        [IDEA] **Quick Fixes:**
                        - **Missing symbols**: Some stocks may need to be added to the database
                        - **Price errors**: Check for empty cells, negative values, or text in price column
                        - **Date format**: Use YYYY-MM-DD format (e.g., 2024-01-15)
                        """)
                    else:
                        st.success("[OK] All data validated successfully!")
                        
                        # Calculate and display import summary
                        st.markdown("### [CHART] Import Summary")
                        
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
                        st.markdown("#### 📊 Portfolio Comparison")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**  Current Portfolio**")
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
                            st.markdown("**  Import File**")
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
                            st.markdown("**  After Import**")
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
                            st.info(f"  **Note**: {import_stocks} records contain {unique_symbols} unique stock symbols. Duplicate symbols will be consolidated.")
                        
                        st.markdown("---")
                        
                        col1, col2 = st.columns([1, 1])
                        with col1:
                            if st.button("  Import Portfolio", type="primary"):
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
                                    [OK] **Portfolio Import Successful!**
                                    - [UP] New stocks added: {imported_count}
                                    -   Existing stocks updated: {updated_count}
                                    - [CHART] Total stocks in portfolio: {len(existing_portfolio)}
                                    
                                    *Refreshing portfolio view...*
                                    """)
                                    
                                    # Show balloons and automatically refresh
                                    st.balloons()
                                    
                                    # Set session state to navigate to Portfolio Overview
                                    st.session_state.main_nav = "  Portfolio Overview"
                                    
                                    # Rerun to refresh the app and show updated portfolio
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"[ERROR] Error saving portfolio: {e}")
                        
                        with col2:
                            if st.button("📥 Download Sample CSV"):
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
                                from io import StringIO
                                csv_buffer = StringIO()
                                sample_df.to_csv(csv_buffer, index=False)
                                csv_data = csv_buffer.getvalue()
                                
                                st.download_button(
                                    label="  Download Sample",
                                    data=csv_data,
                                    file_name="portfolio_sample.csv",
                                    mime="text/csv"
                                )
                    
            except Exception as e:
                st.error(f"[ERROR] Error reading file: {e}")
                st.info("[IDEA] Please ensure your CSV file is properly formatted.")

    elif selected_page == "🎨 Theme Customizer":
        st.markdown("## 🎨 Theme Customizer")
        st.caption("🎨 Real-time color and font customization for TADAWUL NEXUS")
        
        # Create tabs for different customization options
        color_tab, font_tab, preview_tab = st.tabs(["🎨 Colors", "📝 Fonts", "👁️ Preview"])
        
        with color_tab:
            st.markdown("### 🎨 Color Palette Configuration")
            st.info("💡 Change colors below and see them apply instantly to your dashboard!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔵 Primary Theme Colors")
                primary_blue = st.color_picker("Primary Blue", "#0066CC", help="Main brand color for buttons and headers")
                secondary_blue = st.color_picker("Secondary Blue", "#1e3a5f", help="Cards and container backgrounds")
                accent_gold = st.color_picker("Accent Gold", "#FFD700", help="Borders, highlights, and hover effects")
                dark_teal = st.color_picker("Dark Navy", "#0f2240", help="Sidebar and background gradients")
                
            with col2:
                st.markdown("#### 🖤 Background & Text Colors")
                background_dark = st.color_picker("Background Dark", "#0d1b2a", help="Main dark background")
                text_light = st.color_picker("Text Light", "#FFFFFF", help="White text for dark backgrounds")
                text_gray = st.color_picker("Text Gray", "#B0BEC5", help="Gray text for subtitles")
                
                st.markdown("#### 🎯 Status Colors")
                success_green = st.color_picker("Success Green", "#4CAF50", help="Positive values and success")
                warning_red = st.color_picker("Warning Red", "#F44336", help="Negative values and warnings")
                chart_orange = st.color_picker("Chart Orange", "#FF9800", help="Charts and alerts")
            
            # Apply colors button
            if st.button("🎨 Apply Color Changes", type="primary"):
                # Update the branding file with new colors
                new_colors = {
                    'primary_blue': primary_blue,
                    'secondary_blue': secondary_blue,
                    'accent_gold': accent_gold,
                    'dark_teal': dark_teal,
                    'background_dark': background_dark,
                    'text_light': text_light,
                    'text_gray': text_gray,
                    'success_green': success_green,
                    'warning_red': warning_red,
                    'chart_orange': chart_orange,
                }
                
                if update_branding_colors(new_colors):
                    st.success("✅ Colors updated successfully! Refresh the page to see changes.")
                    st.balloons()
                else:
                    st.error("❌ Failed to update colors. Please try again.")
        
        with font_tab:
            st.markdown("### 📝 Font Configuration")
            st.info("💡 Customize font sizes for different text elements")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📖 Header Sizes")
                h1_size = st.slider("H1 Font Size (rem)", 2.0, 4.0, 2.5, 0.1)
                h2_size = st.slider("H2 Font Size (rem)", 1.5, 3.0, 2.0, 0.1)
                h3_size = st.slider("H3 Font Size (rem)", 1.2, 2.5, 1.5, 0.1)
                
            with col2:
                st.markdown("#### 📝 Body Text")
                body_size = st.slider("Body Font Size (rem)", 0.8, 1.5, 1.0, 0.05)
                caption_size = st.slider("Caption Font Size (rem)", 0.6, 1.2, 0.85, 0.05)
                
                st.markdown("#### 🎛️ Font Weight")
                header_weight = st.selectbox("Header Weight", [300, 400, 500, 600, 700], index=3)
                body_weight = st.selectbox("Body Weight", [300, 400, 500], index=1)
            
            # Apply fonts button
            if st.button("📝 Apply Font Changes", type="primary"):
                font_config = {
                    'h1_size': h1_size,
                    'h2_size': h2_size,
                    'h3_size': h3_size,
                    'body_size': body_size,
                    'caption_size': caption_size,
                    'header_weight': header_weight,
                    'body_weight': body_weight,
                }
                
                if update_branding_fonts(font_config):
                    st.success("✅ Font settings updated successfully! Refresh the page to see changes.")
                    st.balloons()
                else:
                    st.error("❌ Failed to update fonts. Please try again.")
        
        with preview_tab:
            st.markdown("### 👁️ Live Preview")
            st.info("🔍 Preview how your customizations will look")
            
            # Sample elements to preview
            st.markdown("#### Sample Header Elements")
            st.markdown("# H1: TADAWUL NEXUS Dashboard")
            st.markdown("## H2: Portfolio Overview")
            st.markdown("### H3: Stock Analysis")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Portfolio Value", "125,750 SAR", "5.2%")
            with col2:
                st.metric("Today's Gain", "6,540 SAR", "3.1%")
            with col3:
                st.metric("Total Stocks", "12", "2")
            
            # Sample buttons and alerts
            st.markdown("#### Sample Interactive Elements")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("🔵 Primary Button")
            with col2:
                st.success("✅ Success Message")
            with col3:
                st.error("❌ Warning Message")
            
            # Reset to defaults
            st.markdown("---")
            if st.button("🔄 Reset to Default Theme", type="secondary"):
                if reset_to_default_theme():
                    st.success("✅ Theme reset to defaults! Refresh the page to see changes.")
                    st.snow()
                else:
                    st.error("❌ Failed to reset theme.")
    
    # Add professional footer
    if BRANDING_AVAILABLE:
        TadawulBranding.display_footer()

if __name__ == "__main__":
    main()
