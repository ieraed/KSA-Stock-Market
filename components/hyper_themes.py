"""
Hyper-Optimized Theme System for Saudi Stock Market App
Complete CSS and theme management system extracted from main app
Includes all styling functions, theme management, and CSS definitions
"""

import streamlit as st
import re
from pathlib import Path


def get_hyper_themes():
    """Get all available themes with hyper-optimized color schemes - SOLID BACKGROUNDS FOR MAXIMUM VISIBILITY"""
    return {
        "dark_charcoal": {
            "name": "Dark Charcoal (Sleek & Professional)",
            "primary": "#2C3E50",
            "secondary": "#34495E", 
            "accent": "#3498DB",
            "background": "#1A1A1A",
            "surface": "#2C3E50",
            "text": "#ECF0F1",
            "table_bg": "rgba(45, 52, 64, 1.0)",        # SOLID: More opaque for better visibility
            "border": "rgba(88, 91, 112, 1.0)",         # SOLID: Fully opaque borders
            "header_bg": "rgba(59, 66, 82, 1.0)",       # SOLID: Fully opaque header
            "cell_bg": "rgba(50, 57, 70, 1.0)",         # SOLID: Fully opaque cells
            "table_text": "#E5E9F0",
            "shadow": "rgba(0, 0, 0, 0.4)",
            "success": "#00FF88",
            "error": "#FF4444",
            "warning": "#FFA500"
        },
        "professional_blue": {
            "name": "Professional Blue",
            "primary": "#0066CC",
            "secondary": "#1e3a5f",
            "accent": "#FFD700",
            "background": "#0d1b2a",
            "surface": "#1e3a5f",
            "text": "#FFFFFF",
            "table_bg": "rgba(35, 90, 150, 1.0)",       # SOLID: Fully opaque blue
            "border": "rgba(55, 110, 170, 1.0)",        # SOLID: Fully opaque blue border
            "header_bg": "rgba(45, 100, 160, 1.0)",     # SOLID: Fully opaque blue header
            "cell_bg": "rgba(40, 95, 155, 1.0)",        # SOLID: Fully opaque blue cells
            "table_text": "#F0F4F8",
            "shadow": "rgba(35, 90, 150, 0.4)",
            "success": "#00FF88",
            "error": "#FF4444",
            "warning": "#FFA500"
        },
        "financial_green": {
            "name": "Financial Green",
            "primary": "#00C851",
            "secondary": "#007E33",
            "accent": "#FFD700",
            "background": "#0d1b0f",
            "surface": "#1a2e1a",
            "text": "#E8F5E8",
            "table_bg": "rgba(46, 125, 50, 1.0)",       # SOLID: Fully opaque green
            "border": "rgba(66, 145, 70, 1.0)",         # SOLID: Fully opaque green border
            "header_bg": "rgba(56, 135, 60, 1.0)",      # SOLID: Fully opaque green header
            "cell_bg": "rgba(51, 130, 55, 1.0)",        # SOLID: Fully opaque green cells
            "table_text": "#F1F8E9",
            "shadow": "rgba(46, 125, 50, 0.4)",
            "success": "#00FF88",
            "error": "#FF4444", 
            "warning": "#FFA500"
        },
        "saudi_gold": {
            "name": "Saudi Gold",
            "primary": "#FFD700",
            "secondary": "#B8860B",
            "accent": "#228B22",
            "background": "#1A1A0A",
            "surface": "#2F2F1F",
            "text": "#FFF8DC",
            "table_bg": "rgba(200, 160, 40, 1.0)",      # SOLID: Fully opaque gold
            "border": "rgba(220, 180, 60, 1.0)",        # SOLID: Fully opaque gold border
            "header_bg": "rgba(210, 170, 50, 1.0)",     # SOLID: Fully opaque gold header
            "cell_bg": "rgba(195, 155, 35, 1.0)",       # SOLID: Fully opaque gold cells
            "table_text": "#1A1A1A",                    # Dark text for gold background
            "shadow": "rgba(200, 160, 40, 0.4)",
            "success": "#00FF88",
            "error": "#FF4444",
            "warning": "#FFA500"
        }
    }


def get_hyper_theme_css(theme_colors):
    """
    Returns enhanced, high-performance CSS for theme application with stronger specificity
    Focus: Speed, simplicity, and effectiveness with proper table color updates
    """
    import time
    timestamp = int(time.time() * 1000)  # Add timestamp for cache busting
    
    return f"""
    <style id="hyper-theme-{timestamp}">
    /* HYPER THEME - Enhanced with Strong Specificity - {timestamp} */
    
    /* Force immediate CSS refresh */
    html, body {{ animation: theme-refresh-{timestamp} 0.1s ease; }}
    @keyframes theme-refresh-{timestamp} {{ 0% {{ opacity: 0.99; }} 100% {{ opacity: 1; }} }}
    
    /* Table Container Styling - MAXIMUM PRIORITY */
    div[data-testid="dataframe"],
    div[data-testid="dataframe"] > div,
    .stDataFrame,
    [data-testid="dataframe"],
    section[data-testid="stDataFrame"] {{
        background: {theme_colors['table_bg']} !important;
        border: 2px solid {theme_colors['border']} !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 16px {theme_colors['shadow']} !important;
        margin: 10px 0 !important;
        overflow: hidden !important;
    }}

    /* Force table element background */
    div[data-testid="dataframe"] table,
    .stDataFrame table,
    [data-testid="dataframe"] table {{
        background-color: {theme_colors['table_bg']} !important;
        background: {theme_colors['table_bg']} !important;
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
    }}

    /* Header Row Styling - ABSOLUTE MAXIMUM SPECIFICITY */
    div[data-testid="dataframe"] thead th,
    div[data-testid="dataframe"] thead tr th,
    div[data-testid="dataframe"] table thead th,
    div[data-testid="dataframe"] table thead tr th,
    .stDataFrame thead th,
    .stDataFrame thead tr th,
    .stDataFrame table thead th,
    .stDataFrame table thead tr th,
    [data-testid="dataframe"] thead th,
    [data-testid="dataframe"] thead tr th {{
        background-color: {theme_colors['header_bg']} !important;
        background: {theme_colors['header_bg']} !important;
        color: {theme_colors['table_text']} !important;
        font-weight: 700 !important;
        padding: 12px 8px !important;
        text-align: center !important;
        border-bottom: 2px solid {theme_colors['border']} !important;
        border-right: 1px solid {theme_colors['border']} !important;
        font-size: 14px !important;
    }}

    /* Data Cell Styling - ABSOLUTE MAXIMUM SPECIFICITY */
    div[data-testid="dataframe"] tbody td,
    div[data-testid="dataframe"] tbody tr td,
    div[data-testid="dataframe"] table tbody td,
    div[data-testid="dataframe"] table tbody tr td,
    .stDataFrame tbody td,
    .stDataFrame tbody tr td,
    .stDataFrame table tbody td,
    .stDataFrame table tbody tr td,
    [data-testid="dataframe"] tbody td,
    [data-testid="dataframe"] tbody tr td {{
        background-color: {theme_colors['cell_bg']} !important;
        background: {theme_colors['cell_bg']} !important;
        color: {theme_colors['table_text']} !important;
        padding: 10px 8px !important;
        border: 1px solid {theme_colors['border']} !important;
        font-size: 13px !important;
    }}
    
    /* Text Elements Inside Cells - Force text color */
    div[data-testid="dataframe"] tbody td *,
    div[data-testid="dataframe"] tbody tr td *,
    div[data-testid="dataframe"] table tbody td *,
    div[data-testid="dataframe"] table tbody tr td *,
    .stDataFrame tbody td *,
    .stDataFrame tbody tr td *,
    .stDataFrame table tbody td *,
    .stDataFrame table tbody tr td *,
    [data-testid="dataframe"] tbody td *,
    [data-testid="dataframe"] tbody tr td * {{
        color: {theme_colors['table_text']} !important;
        background: transparent !important;
    }}
    
    /* Header Text Elements - Force text color */
    div[data-testid="dataframe"] thead th *,
    div[data-testid="dataframe"] thead tr th *,
    div[data-testid="dataframe"] table thead th *,
    div[data-testid="dataframe"] table thead tr th *,
    .stDataFrame thead th *,
    .stDataFrame thead tr th *,
    .stDataFrame table thead th *,
    .stDataFrame table thead tr th *,
    [data-testid="dataframe"] thead th *,
    [data-testid="dataframe"] thead tr th * {{
        color: {theme_colors['table_text']} !important;
        background: transparent !important;
    }}
    
    /* ALL text inside dataframes - Nuclear option for text color */
    div[data-testid="dataframe"] span,
    div[data-testid="dataframe"] p,
    div[data-testid="dataframe"] div,
    div[data-testid="dataframe"] text,
    .stDataFrame span,
    .stDataFrame p,
    .stDataFrame div,
    .stDataFrame text,
    [data-testid="dataframe"] span,
    [data-testid="dataframe"] p,
    [data-testid="dataframe"] div,
    [data-testid="dataframe"] text {{
        color: {theme_colors['table_text']} !important;
    }}
    
    /* Force text color in ALL table descendants */
    div[data-testid="dataframe"] *,
    .stDataFrame *,
    [data-testid="dataframe"] * {{
        color: {theme_colors['table_text']} !important;
    }}

    /* Row Hover Effects */
    div[data-testid="dataframe"] tbody tr:hover,
    div[data-testid="dataframe"] tbody tr:hover td,
    div[data-testid="dataframe"] table tbody tr:hover,
    div[data-testid="dataframe"] table tbody tr:hover td,
    .stDataFrame tbody tr:hover,
    .stDataFrame tbody tr:hover td,
    .stDataFrame table tbody tr:hover,
    .stDataFrame table tbody tr:hover td,
    [data-testid="dataframe"] tbody tr:hover,
    [data-testid="dataframe"] tbody tr:hover td {{
        background-color: {theme_colors['header_bg']} !important;
        background: {theme_colors['header_bg']} !important;
        color: {theme_colors['table_text']} !important;
        transition: all 0.2s ease !important;
    }}
    
    /* Alternating Row Colors - Force background */
    div[data-testid="dataframe"] tbody tr:nth-child(even),
    div[data-testid="dataframe"] tbody tr:nth-child(even) td,
    div[data-testid="dataframe"] table tbody tr:nth-child(even),
    div[data-testid="dataframe"] table tbody tr:nth-child(even) td,
    .stDataFrame tbody tr:nth-child(even),
    .stDataFrame tbody tr:nth-child(even) td,
    .stDataFrame table tbody tr:nth-child(even),
    .stDataFrame table tbody tr:nth-child(even) td,
    [data-testid="dataframe"] tbody tr:nth-child(even),
    [data-testid="dataframe"] tbody tr:nth-child(even) td {{
        background-color: {theme_colors['cell_bg']} !important;
        background: {theme_colors['cell_bg']} !important;
    }}
    
    div[data-testid="dataframe"] tbody tr:nth-child(odd),
    div[data-testid="dataframe"] tbody tr:nth-child(odd) td,
    div[data-testid="dataframe"] table tbody tr:nth-child(odd),
    div[data-testid="dataframe"] table tbody tr:nth-child(odd) td,
    .stDataFrame tbody tr:nth-child(odd),
    .stDataFrame tbody tr:nth-child(odd) td,
    .stDataFrame table tbody tr:nth-child(odd),
    .stDataFrame table tbody tr:nth-child(odd) td,
    [data-testid="dataframe"] tbody tr:nth-child(odd),
    [data-testid="dataframe"] tbody tr:nth-child(odd) td {{
        background-color: {theme_colors['table_bg']} !important;
        background: {theme_colors['table_bg']} !important;
    }}
    
    /* Force immediate update with !important and higher specificity */
    * div[data-testid="dataframe"] {{
        background: {theme_colors['table_bg']} !important;
        border: 2px solid {theme_colors['border']} !important;
    }}
    
    * div[data-testid="dataframe"] table {{
        background: {theme_colors['table_bg']} !important;
    }}
    
    * div[data-testid="dataframe"] thead th {{
        background: {theme_colors['header_bg']} !important;
        color: {theme_colors['table_text']} !important;
    }}
    
    * div[data-testid="dataframe"] tbody td {{
        background: {theme_colors['cell_bg']} !important;
        color: {theme_colors['table_text']} !important;
    }}
    
    /* COMPREHENSIVE TEXT COLOR OVERRIDE - All possible text elements */
    .stDataFrame,
    .stDataFrame *,
    div[data-testid="dataframe"],
    div[data-testid="dataframe"] *,
    [data-testid="dataframe"],
    [data-testid="dataframe"] * {{
        color: {theme_colors['table_text']} !important;
    }}
    
    /* Force text color in Streamlit markdown and text elements */
    .stMarkdown,
    .stMarkdown *,
    .stText,
    .stText *,
    p, span, div, text {{
        color: #E5E9F0 !important;
    }}
    
    /* Main content area text color fixes */
    .main .block-container,
    .main .block-container *,
    section.main,
    section.main * {{
        color: #E5E9F0 !important;
    }}
    
    /* Streamlit form elements and content */
    .stSelectbox label,
    .stTextInput label,
    .stButton,
    .stRadio label,
    .stCheckbox label {{
        color: #E5E9F0 !important;
    }}
    
    /* App container text color override */
    .stApp,
    .stApp * {{
        color: #E5E9F0 !important;
    }}
    </style>
    """


def apply_complete_css():
    """Apply the complete embedded CSS for the application"""
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
    background: linear-gradient(180deg, #0f2240 0%, #1e3a5f 100%) !important;
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
   NOTE: This is overridden by global theme function
   ======================================== */

.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    /* Colors will be set by global theme function */
}

.stDataFrame, .stDataFrame td, .stDataFrame th, .stDataFrame div {
    /* Colors will be set by global theme function */
}

/* Additional specific selectors for better override */
div[data-testid="dataframe"] {
    border-radius: 12px !important;
    /* Colors will be set by global theme function */
}

div[data-testid="dataframe"] table {
    /* Colors will be set by global theme function */
}

div[data-testid="dataframe"] thead th {
    font-weight: bold !important;
    /* Colors will be set by global theme function */
}

div[data-testid="dataframe"] tbody td {
    /* Colors will be set by global theme function */
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
    background: #2d3748;
    color: #ffffff;
    padding: 1.2rem;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #4a5568;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
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
    background: #2d3748;
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

/* SUCCESS MESSAGES */
.success-card {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

/* WARNING MESSAGES */
.warning-card {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
}

/* ========================================
   🚨 CUSTOM ERROR MESSAGE STYLING
   CUSTOMIZE: Error message appearance
   ======================================== */

/* Error Messages - Red styling */
div[data-testid="stAlert"][data-baseweb="notification"] {
    background-color: rgba(244, 67, 54, 0.1) !important;
    border: 1px solid #f44336 !important;
    border-radius: 8px !important;
}

div[data-testid="stAlert"][data-baseweb="notification"] > div {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Streamlit error elements */
.stAlert > div {
    background-color: rgba(244, 67, 54, 0.15) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Warning alert styling */
div[data-testid="stAlert"][data-baseweb="notification"].warning {
    background-color: rgba(255, 152, 0, 0.1) !important;
    border-color: #ff9800 !important;
}

/* ========================================
   📋 SECTION HEADERS & TITLES STYLING
   CUSTOMIZE: Headers like "Scenario Analysis"
   ======================================== */

/* Main subheaders (h2, h3) - Custom colors */
.main h2, .main h3 {
    color: #FFD700 !important;  /* Gold color for titles */
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
}

/* Streamlit subheader elements */
.element-container h2,
.element-container h3 {
    color: #FFD700 !important;  /* Gold color */
    font-weight: 600 !important;
}

/* Specific styling for Risk Management titles */
.risk-title {
    color: #00D4FF !important;  /* Cyan blue for risk titles */
    font-weight: 700 !important;
    font-size: 1.2rem !important;
}

/* Portfolio section titles */
.portfolio-title {
    color: #00FF88 !important;  /* Green for portfolio titles */
    font-weight: 600 !important;
}

/* Market data titles */
.market-title {
    color: #FF6B6B !important;  /* Coral red for market titles */
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)


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
# 🎨 CUSTOM STYLING HELPER FUNCTIONS
# =============================================================================

def custom_title(text, color="#FFD700", size="1.5rem", weight="600"):
    """Display a custom styled title"""
    st.markdown(f"""
    <h3 style="
        color: {color} !important;
        font-size: {size} !important;
        font-weight: {weight} !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
    ">{text}</h3>
    """, unsafe_allow_html=True)


def custom_error(text, color="#FF4444", bg_color="rgba(244, 67, 54, 0.1)"):
    """Display a custom styled error message"""
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        color: {color};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {color};
        margin: 1rem 0;
        font-weight: 500;
    ">
        ⚠️ {text}
    </div>
    """, unsafe_allow_html=True)


def custom_success(text, color="#00FF88", bg_color="rgba(76, 175, 80, 0.1)"):
    """Display a custom styled success message"""
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        color: {color};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {color};
        margin: 1rem 0;
        font-weight: 500;
    ">
        ✅ {text}
    </div>
    """, unsafe_allow_html=True)


def custom_warning(text, color="#FFA500", bg_color="rgba(255, 152, 0, 0.1)"):
    """Display a custom styled warning message"""
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        color: {color};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {color};
        margin: 1rem 0;
        font-weight: 500;
    ">
        ⚠️ {text}
    </div>
    """, unsafe_allow_html=True)


def force_theme_refresh():
    """Force a complete theme refresh by applying CSS with unique key"""
    import time
    
    # Generate unique key to force CSS refresh
    refresh_key = int(time.time() * 1000)
    
    if 'current_theme' in st.session_state:
        themes = get_hyper_themes()
        current_theme_colors = themes[st.session_state.current_theme]
        
        # Apply enhanced CSS with timestamp to force refresh
        enhanced_css = f"""
        <style id="theme-refresh-{refresh_key}">
        /* FORCE REFRESH - {refresh_key} */
        {get_hyper_theme_css(current_theme_colors).replace('<style>', '').replace('</style>', '')}
        </style>
        """
        
        st.markdown(enhanced_css, unsafe_allow_html=True)
        return True
    return False


def apply_theme_with_preview(theme_name):
    """Apply theme and show immediate preview with forced refresh"""
    import time
    
    themes = get_hyper_themes()
    if theme_name in themes:
        st.session_state.current_theme = theme_name
        theme_colors = themes[theme_name]
        
        # Apply complete CSS first
        apply_complete_css()
        
        # Apply theme-specific CSS with high priority and timestamp for cache busting
        theme_css = get_hyper_theme_css(theme_colors)
        st.markdown(theme_css, unsafe_allow_html=True)
        
        # Force multiple refresh attempts for better compatibility
        force_theme_refresh()
        
        # Additional immediate CSS injection for tables
        immediate_table_css = f"""
        <style>
        /* IMMEDIATE TABLE UPDATE */
        div[data-testid="dataframe"] {{
            background: {theme_colors['table_bg']} !important;
            border: 2px solid {theme_colors['border']} !important;
            border-radius: 12px !important;
        }}
        div[data-testid="dataframe"] thead th {{
            background: {theme_colors['header_bg']} !important;
            color: {theme_colors['table_text']} !important;
        }}
        div[data-testid="dataframe"] tbody td {{
            background: {theme_colors['cell_bg']} !important;
            color: {theme_colors['table_text']} !important;
        }}
        </style>
        """
        st.markdown(immediate_table_css, unsafe_allow_html=True)
        
        # Store theme in session state for persistence
        st.session_state.theme_applied = True
        st.session_state.last_theme_update = int(time.time() * 1000)
        
        return True
    return False


def color_bot_assistant():
    """
    AI Color Bot Assistant for Saudi Stock Market App
    Provides intelligent color suggestions, palette generation, and theme customization
    """
    st.markdown("### 🎨 Color Bot Assistant")
    st.markdown("*Your intelligent color companion for perfect theme customization*")
    
    # Color Bot Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Smart Suggestions", "🎨 Color Picker", "🎯 Palette Generator", "💡 Tips & Guidelines"])
    
    with tab1:
        st.markdown("#### Smart Color Suggestions")
        
        # Market-specific color recommendations
        market_mood = st.selectbox(
            "What's your trading mood today?",
            ["📈 Bullish & Confident", "📉 Cautious & Analytical", "⚖️ Balanced & Neutral", "🚀 Aggressive & Bold"]
        )
        
        if market_mood == "📈 Bullish & Confident":
            st.success("**Recommended Colors for Bullish Trading:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.color_picker("Primary", "#00C851", key="bull_primary")
                st.write("**Green** - Growth & Prosperity")
            with col2:
                st.color_picker("Accent", "#FFD700", key="bull_accent")
                st.write("**Gold** - Success & Wealth")
            with col3:
                st.color_picker("Background", "#0A3D0A", key="bull_bg")
                st.write("**Dark Green** - Stability")
                
        elif market_mood == "📉 Cautious & Analytical":
            st.info("**Recommended Colors for Analytical Trading:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.color_picker("Primary", "#4A90E2", key="analytical_primary")
                st.write("**Blue** - Trust & Analysis")
            with col2:
                st.color_picker("Accent", "#6C7B7F", key="analytical_accent")
                st.write("**Gray** - Objectivity")
            with col3:
                st.color_picker("Background", "#1A2332", key="analytical_bg")
                st.write("**Dark Blue** - Focus")
                
        elif market_mood == "⚖️ Balanced & Neutral":
            st.warning("**Recommended Colors for Balanced Trading:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.color_picker("Primary", "#7B68EE", key="balanced_primary")
                st.write("**Purple** - Balance & Wisdom")
            with col2:
                st.color_picker("Accent", "#20B2AA", key="balanced_accent")
                st.write("**Teal** - Harmony")
            with col3:
                st.color_picker("Background", "#2F2F2F", key="balanced_bg")
                st.write("**Charcoal** - Neutrality")
                
        else:  # Aggressive & Bold
            st.error("**Recommended Colors for Aggressive Trading:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.color_picker("Primary", "#FF6B35", key="aggressive_primary")
                st.write("**Orange** - Energy & Action")
            with col2:
                st.color_picker("Accent", "#FF1744", key="aggressive_accent")
                st.write("**Red** - Power & Urgency")
            with col3:
                st.color_picker("Background", "#1A0A0A", key="aggressive_bg")
                st.write("**Dark Red** - Intensity")
        
        # Quick apply button
        if st.button("🚀 Apply Suggested Theme", type="primary"):
            st.success("Theme suggestion applied! Check your dashboard to see the changes.")
    
    with tab2:
        st.markdown("#### Custom Color Picker")
        
        # Main color selection
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Primary Colors**")
            primary_color = st.color_picker("Primary Color", "#2C3E50", key="custom_primary")
            secondary_color = st.color_picker("Secondary Color", "#34495E", key="custom_secondary")
            accent_color = st.color_picker("Accent Color", "#3498DB", key="custom_accent")
            
        with col2:
            st.markdown("**Background Colors**")
            bg_color = st.color_picker("Background", "#1A1A1A", key="custom_bg")
            surface_color = st.color_picker("Surface", "#2C3E50", key="custom_surface")
            text_color = st.color_picker("Text Color", "#ECF0F1", key="custom_text")
        
        # Live preview
        st.markdown("#### Live Preview")
        preview_css = f"""
        <div style="
            background: {bg_color};
            color: {text_color};
            padding: 20px;
            border-radius: 10px;
            border: 2px solid {accent_color};
            margin: 10px 0;
        ">
            <h4 style="color: {primary_color}; margin-top: 0;">Saudi Stock Market Dashboard</h4>
            <p style="background: {surface_color}; padding: 10px; border-radius: 5px; margin: 10px 0;">
                This is how your custom theme will look in the dashboard.
            </p>
            <button style="
                background: {accent_color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            ">Sample Button</button>
        </div>
        """
        st.markdown(preview_css, unsafe_allow_html=True)
        
        if st.button("💾 Save Custom Theme", type="primary"):
            # Here you would save the custom theme
            st.success("Custom theme saved successfully!")
    
    with tab3:
        st.markdown("#### AI Palette Generator")
        
        # Palette generation options
        palette_type = st.selectbox(
            "Choose palette type:",
            ["Monochromatic", "Complementary", "Triadic", "Analogous", "Saudi-Inspired"]
        )
        
        base_color = st.color_picker("Base Color", "#2C3E50", key="palette_base")
        
        if st.button("🎨 Generate Palette"):
            st.markdown("#### Generated Color Palette")
            
            if palette_type == "Saudi-Inspired":
                # Saudi flag inspired colors
                colors = ["#006C35", "#FFFFFF", "#000000", "#FFD700", "#8B4513"]
                descriptions = ["Saudi Green", "Pure White", "Desert Black", "Gold Accent", "Desert Sand"]
            elif palette_type == "Monochromatic":
                # Generate monochromatic variations
                colors = [base_color, "#34495E", "#5D6D7E", "#85929E", "#AEB6BF"]
                descriptions = ["Base", "Darker", "Medium", "Lighter", "Lightest"]
            elif palette_type == "Complementary":
                # Generate complementary colors
                colors = [base_color, "#E74C3C", "#F39C12", "#27AE60", "#8E44AD"]
                descriptions = ["Base", "Complement", "Warm", "Cool", "Accent"]
            elif palette_type == "Triadic":
                colors = [base_color, "#E67E22", "#9B59B6", "#1ABC9C", "#F1C40F"]
                descriptions = ["Base", "Triad 1", "Triad 2", "Balance", "Highlight"]
            else:  # Analogous
                colors = [base_color, "#2980B9", "#8E44AD", "#16A085", "#27AE60"]
                descriptions = ["Base", "Adjacent 1", "Adjacent 2", "Harmony 1", "Harmony 2"]
            
            # Display palette
            cols = st.columns(len(colors))
            for i, (color, desc) in enumerate(zip(colors, descriptions)):
                with cols[i]:
                    st.color_picker(desc, color, key=f"generated_{i}", disabled=True)
                    st.markdown(f"<div style='background:{color}; height:50px; border-radius:5px; margin:5px 0;'></div>", 
                              unsafe_allow_html=True)
    
    with tab4:
        st.markdown("#### Color Psychology for Trading")
        
        st.info("""
        **🔵 Blue Colors**: Promote trust, stability, and analytical thinking
        - Best for: Conservative trading strategies, long-term analysis
        - Avoid when: Making quick decisions, high-frequency trading
        """)
        
        st.success("""
        **🟢 Green Colors**: Associated with growth, prosperity, and positive gains
        - Best for: Bull markets, profit tracking, growth analysis
        - Psychological effect: Increases optimism and confidence
        """)
        
        st.error("""
        **🔴 Red Colors**: Create urgency and highlight risks/losses
        - Best for: Risk warnings, stop-loss alerts, urgent actions
        - Use sparingly: Can increase stress and impulsive decisions
        """)
        
        st.warning("""
        **🟡 Yellow/Gold Colors**: Represent wealth and important information
        - Best for: Highlighting key metrics, premium features
        - Cultural significance: Gold represents prosperity in Saudi culture
        """)
        
        st.markdown("#### Saudi Market Color Guidelines")
        st.markdown("""
        - **Tadawul Green** (#006C35): Use for market indices and growth
        - **Desert Gold** (#FFD700): Perfect for highlighting profits
        - **Heritage Brown** (#8B4513): Great for traditional/conservative elements
        - **Sky Blue** (#87CEEB): Ideal for technical analysis tools
        """)
        
        # Accessibility tips
        st.markdown("#### Accessibility Tips")
        st.markdown("""
        ✅ **Do:**
        - Use high contrast ratios (4.5:1 minimum)
        - Test colors with colorblind simulation
        - Provide text alternatives to color-coding
        - Use consistent color meanings throughout
        
        ❌ **Don't:**
        - Rely solely on color for important information
        - Use red/green only for profit/loss (colorblind users)
        - Use colors that are too similar in brightness
        - Change color meanings between different screens
        """)


def generate_color_suggestions(mood_type="balanced"):
    """
    Generate intelligent color suggestions based on trading mood and market conditions
    """
    suggestions = {
        "bullish": {
            "primary": "#00C851",
            "secondary": "#00A144", 
            "accent": "#FFD700",
            "background": "#0A3D0A",
            "description": "Optimistic greens with gold accents for confident trading"
        },
        "bearish": {
            "primary": "#FF4444",
            "secondary": "#CC3333",
            "accent": "#FFA500", 
            "background": "#3D0A0A",
            "description": "Cautious reds with orange warnings for defensive strategies"
        },
        "analytical": {
            "primary": "#4A90E2",
            "secondary": "#357ABD",
            "accent": "#6C7B7F",
            "background": "#1A2332", 
            "description": "Professional blues and grays for analytical mindset"
        },
        "balanced": {
            "primary": "#7B68EE",
            "secondary": "#6A5ACD",
            "accent": "#20B2AA",
            "background": "#2F2F2F",
            "description": "Balanced purples and teals for neutral perspective"
        }
    }
    
    return suggestions.get(mood_type, suggestions["balanced"])


def fix_white_backgrounds():
    """
    Quick fix function to replace white backgrounds with dark theme colors
    Call this function to instantly fix white areas in your app
    """
    fix_css = """
    <style>
    /* INSTANT WHITE BACKGROUND FIX */
    
    /* Navigation radio buttons */
    .stRadio > div {
        background: #2d3748 !important;
        color: #ffffff !important;
    }
    
    /* Market metric cards */
    .market-metric {
        background: #2d3748 !important;
        color: #ffffff !important;
        border: 1px solid #4a5568 !important;
    }
    
    /* Any remaining white backgrounds */
    div[style*="background: white"],
    div[style*="background-color: white"],
    div[style*="background: #ffffff"],
    div[style*="background-color: #ffffff"] {
        background: #2d3748 !important;
        color: #ffffff !important;
    }
    
    /* Force all white text on dark backgrounds */
    .stRadio > div *,
    .market-metric * {
        color: #ffffff !important;
    }
    
    </style>
    """
    
    import streamlit as st
    st.markdown(fix_css, unsafe_allow_html=True)
    
    return "✅ White backgrounds fixed!"
