#!/usr/bin/env python3
"""
Simple launcher for Saudi Stock Market App - Bypasses import issues
"""

import streamlit as st
import sys
import os

def check_and_fix_imports():
    """Check and fix any import issues"""
    print("🔧 Checking application imports...")
    
    # Set page config first
    st.set_page_config(
        page_title="Saudi Stock Market App",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Basic imports that should always work
    try:
        import pandas as pd
        import yfinance as yf
        import plotly.express as px
        print("✅ Core libraries available")
    except ImportError as e:
        st.error(f"Missing core libraries: {e}")
        st.stop()
    
    # Show loading message
    st.markdown("# 🌟 Saudi Stock Market App")
    st.info("🚀 Loading application components...")
    
    # Try to import the main app
    try:
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import and run the main app functions directly
        exec(open('web_launcher_new.py').read())
        
    except Exception as e:
        st.error(f"Error loading application: {e}")
        st.markdown("## 🔧 Quick Fix Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Option 1: Basic Signal Generation")
            if st.button("🎯 Generate Basic Signals"):
                st.success("Basic signal generation would run here")
                
        with col2:
            st.markdown("### Option 2: Run Original Dashboard")
            if st.button("📊 Open Original Dashboard"):
                try:
                    import subprocess
                    subprocess.run([sys.executable, "run_dashboard.py"])
                    st.success("Dashboard started in separate process")
                except Exception as e:
                    st.error(f"Error: {e}")

def main():
    """Main function"""
    check_and_fix_imports()

if __name__ == "__main__":
    main()
