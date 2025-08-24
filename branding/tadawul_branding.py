"""
TADAWUL NEXUS Branding Module
Professional branding implementation for Streamlit applications
"""

import streamlit as st
import base64
import os

class TadawulBranding:
    """Professional branding system for TADAWUL NEXUS applications"""
    
    # Brand Colors - Updated to match professional image
    COLORS = {
        'primary_blue': '#0066CC',
        'secondary_blue': '#2c5f41', 
        'accent_gold': '#FFD700',
        'dark_teal': '#1a472a',
        'background_dark': '#0d1b2a',
        'background_light': '#e8f4f8',
        'text_light': '#FFFFFF',
        'text_gray': '#B0BEC5',
        'success_green': '#4CAF50',
        'warning_red': '#F44336',
        'chart_orange': '#FF9800',
        'light_gray': '#f8f9fa'
    }
    
    # Taglines
    TAGLINES = {
        'primary': "Where Saudi Markets Meet Intelligence",
        'arabic': "حيث تلتقي الأسواق السعودية بالذكاء",
        'feature': "Intelligent Trading for the Saudi Market",
        'gateway': "Your Gateway to Tadawul Excellence",
        'technical': "Advanced Analytics for Saudi Stocks"
    }
    
    @staticmethod
    def load_css():
        """Load comprehensive CSS styling for TADAWUL NEXUS"""
        return f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {{
            font-family: 'Noto Sans Arabic', 'Cairo', Arial, sans-serif;
        }}
        
        # Sidebar Styling - Dark theme to match image
        [data-testid=stSidebar] {{
            background: linear-gradient(180deg, {TadawulBranding.COLORS['dark_teal']} 0%, {TadawulBranding.COLORS['secondary_blue']} 100%);
            border-right: 3px solid {TadawulBranding.COLORS['accent_gold']};
        }}
        
        [data-testid=stSidebar] .css-1d391kg {{
            padding: 1rem;
        }}
        
        /* Header Styling - Professional dark theme */
        h1, h2, h3 {{
            color: {TadawulBranding.COLORS['text_light']};
            font-family: 'Noto Sans Arabic', 'Cairo', sans-serif;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}
        
        h2 {{
            font-size: 2rem;
            margin-bottom: 1rem;
        }}
        
        h3 {{
            font-size: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        
        /* Logo Container - Dark theme styling */
        .logo-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            background: linear-gradient(135deg, {TadawulBranding.COLORS['background_dark']} 0%, {TadawulBranding.COLORS['dark_teal']} 100%);
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            border: 2px solid {TadawulBranding.COLORS['accent_gold']};
        }}
        
        .logo-container img {{
            max-width: 100%;
            height: auto;
            filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.5));
        }}
        
        /* Brand Header - Match the professional image style */
        .brand-header {{
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, {TadawulBranding.COLORS['background_dark']} 0%, {TadawulBranding.COLORS['dark_teal']} 50%, {TadawulBranding.COLORS['secondary_blue']} 100%);
            color: {TadawulBranding.COLORS['text_light']};
            border-radius: 15px;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }}
        
        .brand-header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cpath d='M0 0L100 100M100 0L0 100' stroke='%23FFD700' stroke-width='0.5' opacity='0.1'/%3E%3C/svg%3E");
            animation: subtle-move 20s linear infinite;
        }}
        
        @keyframes subtle-move {{
            0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
            100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
        }}
        
        .brand-title {{
            font-size: 3.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            background: linear-gradient(45deg, {TadawulBranding.COLORS['text_light']}, {TadawulBranding.COLORS['accent_gold']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .brand-tagline {{
            font-size: 1.2rem;
            opacity: 0.9;
            font-weight: 300;
            color: {TadawulBranding.COLORS['text_gray']};
        }}
        
        /* Navigation Styling - Dark theme */
        .stSelectbox > div > div {{
            background-color: {TadawulBranding.COLORS['secondary_blue']};
            border: 2px solid {TadawulBranding.COLORS['accent_gold']};
            border-radius: 8px;
            color: {TadawulBranding.COLORS['text_light']};
        }}
        
        /* Metric Cards - Enhanced dark theme */
        [data-testid=metric-container] {{
            background: linear-gradient(135deg, {TadawulBranding.COLORS['secondary_blue']} 0%, {TadawulBranding.COLORS['dark_teal']} 100%);
            border: 1px solid {TadawulBranding.COLORS['accent_gold']};
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            transition: all 0.3s ease-in-out;
            color: {TadawulBranding.COLORS['text_light']};
        }}
        
        [data-testid=metric-container]:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 16px rgba(255,215,0,0.2);
            border-color: {TadawulBranding.COLORS['text_light']};
        }}
        
        /* Chart Containers - Professional styling */
        .plotly-graph-div {{
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border: 1px solid {TadawulBranding.COLORS['accent_gold']};
            background: {TadawulBranding.COLORS['secondary_blue']};
        }}
        
        /* Buttons - Gold accent theme */
        .stButton > button {{
            background: linear-gradient(135deg, {TadawulBranding.COLORS['primary_blue']} 0%, {TadawulBranding.COLORS['secondary_blue']} 100%);
            color: {TadawulBranding.COLORS['text_light']};
            border: 2px solid {TadawulBranding.COLORS['accent_gold']};
            border-radius: 10px;
            padding: 0.7rem 1.8rem;
            font-weight: 600;
            transition: all 0.3s ease-in-out;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .stButton > button:hover {{
            background: linear-gradient(135deg, {TadawulBranding.COLORS['accent_gold']} 0%, {TadawulBranding.COLORS['chart_orange']} 100%);
            color: {TadawulBranding.COLORS['background_dark']};
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255,215,0,0.3);
        }}
        
        /* Success/Warning Colors - Enhanced */
        .success-text {{
            color: {TadawulBranding.COLORS['success_green']};
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .warning-text {{
            color: {TadawulBranding.COLORS['warning_red']};
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        /* Professional Tables - Dark theme */
        .stDataFrame {{
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border: 1px solid {TadawulBranding.COLORS['accent_gold']};
        }}
        
        /* Footer - Professional dark styling */
        .brand-footer {{
            text-align: center;
            padding: 2rem 1rem;
            background: linear-gradient(135deg, {TadawulBranding.COLORS['background_dark']} 0%, {TadawulBranding.COLORS['dark_teal']} 100%);
            color: {TadawulBranding.COLORS['text_gray']};
            font-size: 0.9rem;
            border-top: 3px solid {TadawulBranding.COLORS['accent_gold']};
            margin-top: 2rem;
            border-radius: 10px 10px 0 0;
        }}
        
        /* Arabic Text Support */
        .arabic-text {{
            font-family: 'Cairo', 'Noto Sans Arabic', sans-serif;
            direction: rtl;
            text-align: right;
        }}
        
        /* Loading Spinner */
        .stSpinner > div {{
            border-top-color: {TadawulBranding.COLORS['primary_blue']} !important;
        }}
        
        /* Progress Bar */
        .stProgress > div > div > div {{
            background-color: {TadawulBranding.COLORS['primary_blue']};
        }}
        </style>
        """
    
    @staticmethod
    def apply_branding():
        """Apply complete TADAWUL NEXUS branding to Streamlit app"""
        st.markdown(TadawulBranding.load_css(), unsafe_allow_html=True)
    
    @staticmethod
    def display_logo(logo_type="light", width=180):
        """Display TADAWUL NEXUS logo"""
        logo_files = {
            "light": "branding/logos/tadawul_nexus_logo.svg",
            "dark": "branding/logos/tadawul_nexus_logo_dark.svg", 
            "bilingual": "branding/logos/tadawul_nexus_bilingual.svg"
        }
        
        logo_path = logo_files.get(logo_type, logo_files["light"])
        
        # Try to load local file, fallback to embedded SVG
        try:
            if os.path.exists(logo_path):
                with open(logo_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                st.markdown(f'<div class="logo-container">{svg_content}</div>', 
                           unsafe_allow_html=True)
            else:
                # Fallback embedded logo
                TadawulBranding.display_embedded_logo(width)
        except:
            TadawulBranding.display_embedded_logo(width)
    
    @staticmethod
    def display_embedded_logo(width=180):
        """Display embedded SVG logo as fallback - Updated to match professional image"""
        embedded_logo = f"""
        <div class="logo-container">
            <svg width="{width}" height="{int(width*0.3)}" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
                <!-- Circular logo background matching professional image -->
                <circle cx="30" cy="30" r="28" fill="#1a472a" opacity="0.9"/>
                <circle cx="30" cy="30" r="25" fill="#2c5f41"/>
                
                <!-- Inner circular design with blue and gold -->
                <circle cx="30" cy="30" r="20" fill="#0066CC" opacity="0.8"/>
                <circle cx="30" cy="30" r="15" fill="none" stroke="#FFD700" stroke-width="2"/>
                
                <!-- Stylized "S" curve design -->
                <path d="M 20,22 Q 30,18 40,22 Q 30,26 20,22" fill="#FFD700"/>
                <path d="M 20,38 Q 30,34 40,38 Q 30,42 20,38" fill="#FFD700"/>
                
                <!-- Central connecting element -->
                <circle cx="30" cy="30" r="5" fill="#FFFFFF"/>
                <circle cx="30" cy="30" r="3" fill="#0066CC"/>
                
                <!-- Professional text matching image style -->
                <text x="65" y="25" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#FFFFFF">TADAWUL</text>
                <text x="65" y="42" font-family="Arial, sans-serif" font-size="16" font-weight="normal" fill="#FFFFFF">NEXUS</text>
                <text x="65" y="52" font-family="Arial, sans-serif" font-size="8" fill="#B0BEC5">Where Saudi Markets Meet Intelligence</text>
            </svg>
        </div>
        """
        st.markdown(embedded_logo, unsafe_allow_html=True)
    
    @staticmethod
    def display_header(title="TADAWUL NEXUS", tagline="primary", include_logo=True):
        """Display branded header with logo and title"""
        if include_logo:
            TadawulBranding.display_logo()
        
        tagline_text = TadawulBranding.TAGLINES.get(tagline, TadawulBranding.TAGLINES["primary"])
        
        header_html = f"""
        <div class="brand-header">
            <div class="brand-title">{title}</div>
            <div class="brand-tagline">{tagline_text}</div>
        </div>
        """
        st.markdown(header_html, unsafe_allow_html=True)
    
    @staticmethod
    def display_footer():
        """Display branded footer"""
        footer_html = f"""
        <div class="brand-footer">
            <p>TADAWUL NEXUS © 2025 | {TadawulBranding.TAGLINES['primary']}</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                Professional Saudi Stock Market Intelligence Platform
            </p>
        </div>
        """
        st.markdown(footer_html, unsafe_allow_html=True)
    
    @staticmethod
    def success_metric(label, value, delta=None):
        """Display success-styled metric"""
        if delta:
            st.markdown(f'<p class="success-text">{label}: {value} ({delta})</p>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="success-text">{label}: {value}</p>', 
                       unsafe_allow_html=True)
    
    @staticmethod
    def warning_metric(label, value, delta=None):
        """Display warning-styled metric"""
        if delta:
            st.markdown(f'<p class="warning-text">{label}: {value} ({delta})</p>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<p class="warning-text">{label}: {value}</p>', 
                       unsafe_allow_html=True)
