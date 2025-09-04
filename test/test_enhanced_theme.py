# Theme Customizer Test - Enhanced Table Color Updates

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
from components.hyper_themes import (
    get_hyper_themes, 
    apply_complete_css,
    apply_theme_with_preview,
    force_theme_refresh
)

st.set_page_config(page_title="Enhanced Theme Test", layout="wide")

st.title("🎨 Enhanced Theme Customizer Test")

# Apply complete CSS base
apply_complete_css()

# Initialize theme
if 'current_theme' not in st.session_state:
    st.session_state.current_theme = "dark_charcoal"

st.markdown("### Test Theme Changes on Portfolio Table")

# Theme selector buttons
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("⚫ Dark Charcoal", type="primary"):
        apply_theme_with_preview("dark_charcoal")
        st.rerun()

with col2:
    if st.button("🔵 Professional Blue"):
        apply_theme_with_preview("professional_blue")
        st.rerun()

with col3:
    if st.button("🟢 Financial Green"):
        apply_theme_with_preview("financial_green")
        st.rerun()

with col4:
    if st.button("🟡 Saudi Gold"):
        apply_theme_with_preview("saudi_gold")
        st.rerun()

st.markdown("---")

# Sample portfolio table
st.markdown("### 📊 Portfolio Table (Live Theme Test)")

# Create sample data
portfolio_data = {
    "Symbol": ["2222", "1120", "1180", "7010", "2030"],
    "Company": ["Saudi Aramco", "Al Rajhi Bank", "SHR", "Falcom", "SABIC"],
    "Quantity": [100, 50, 200, 75, 150],
    "Price": [28.50, 85.00, 35.20, 42.10, 57.80],
    "Value": [2850.00, 4250.00, 7040.00, 3157.50, 8670.00]
}

df = pd.DataFrame(portfolio_data)
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.info("👆 Click the theme buttons above and watch the table colors change instantly!")

# Force refresh to ensure themes are applied
force_theme_refresh()
