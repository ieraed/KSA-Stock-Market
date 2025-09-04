# Clean Navigation System - No Emojis for Performance
# This will replace the corrupted emoji navigation

clean_navigation_options = [
    "Portfolio Overview",
    "Portfolio Setup", 
    "AI Trading Center",
    "Market Analysis",
    "Performance Tracker",
    "Stock Research",
    "Analytics Dashboard",
    "Sector Analyzer",
    "Risk Management",
    "Dividend Tracker",
    "Import/Export Data",
    "Theme Customizer"
]

# Clean page conditional logic
def get_clean_page_conditions():
    return {
        "Portfolio Overview": "Portfolio Overview",
        "Portfolio Setup": "Portfolio Setup",
        "AI Trading Center": "AI Trading Center", 
        "Market Analysis": "Market Analysis",
        "Performance Tracker": "Performance Tracker",
        "Stock Research": "Stock Research",
        "Analytics Dashboard": "Analytics Dashboard",
        "Sector Analyzer": "Sector Analyzer",
        "Risk Management": "Risk Management",
        "Dividend Tracker": "Dividend Tracker",
        "Import/Export Data": "Import/Export Data",
        "Theme Customizer": "Theme Customizer"
    }

def render_clean_navigation():
    """
    Clean navigation without emojis for maximum performance
    """
    import streamlit as st
    
    # Title Section with enhanced styling (no emojis)
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1rem; background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%); border-radius: 10px; color: white;">
        <h3 style="margin: 0; font-weight: 600; font-size: 1.2rem;">TADAWUL NEXUS</h3>
        <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; opacity: 0.9;">Portfolio & Trading Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Navigation Section
    st.markdown("**Main Navigation:**")
    
    # Add cache refresh button
    if st.button("Refresh Database", help="Clear cache and reload stock database"):
        st.cache_data.clear()
        st.rerun()
        
    selected_page = st.radio(
        "Navigation",
        clean_navigation_options,
        index=0,
        key="main_nav",
        label_visibility="collapsed"
    )
    
    return selected_page
