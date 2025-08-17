"""
🇸🇦 Enhanced Saudi Stock Market App with Continuous Data Fetching
Enhanced version of the main application with real-time data updates
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json
import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the continuous data integration
try:
    from saudi_data_integration import get_data_manager, get_all_saudi_stocks, get_market_summary
    CONTINUOUS_DATA_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Continuous data fetching not available: {e}")
    CONTINUOUS_DATA_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="TADAWUL NEXUS - Real-time Saudi Stock Market",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .gain-text { color: #00ff88; font-weight: bold; }
    .loss-text { color: #ff4444; font-weight: bold; }
    .neutral-text { color: #888888; }
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #00ff00;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>🇸🇦 TADAWUL NEXUS</h1>
        <h3>Real-time Saudi Stock Market Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    
    # Sidebar for controls and information
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        
        # Data source status
        if CONTINUOUS_DATA_AVAILABLE:
            manager = get_data_manager()
            is_fresh = manager.is_data_fresh(max_age_minutes=2)
            
            if is_fresh:
                st.markdown('<div class="live-indicator"></div> **Live Data Connected**', unsafe_allow_html=True)
                st.success("🟢 Real-time updates active")
            else:
                st.warning("🟡 Data may be stale")
            
            if manager.last_update:
                st.info(f"🕐 Last update: {manager.last_update.strftime('%H:%M:%S')}")
        else:
            st.error("❌ Continuous data not available")
        
        # Auto-refresh controls
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
        if auto_refresh:
            refresh_interval = st.slider("Refresh interval (seconds)", 10, 300, 30)
        
        # Export controls
        st.markdown("### 📤 Export Data")
        if st.button("📄 Export JSON"):
            if CONTINUOUS_DATA_AVAILABLE:
                filename = manager.export_current_data("json")
                st.success(f"✅ Exported to {filename}")
            else:
                st.error("❌ Export not available")
        
        if st.button("📊 Export CSV"):
            if CONTINUOUS_DATA_AVAILABLE:
                filename = manager.export_current_data("csv")
                st.success(f"✅ Exported to {filename}")
            else:
                st.error("❌ Export not available")
    
    # Main content area
    if not CONTINUOUS_DATA_AVAILABLE:
        st.error("❌ Continuous data fetching is not available. Please check the installation.")
        st.info("💡 You can still use the basic functionality with cached data.")
        return
    
    # Get latest data
    stocks_data = get_all_saudi_stocks()
    market_summary = get_market_summary()
    
    if not stocks_data:
        st.warning("⚠️ No stock data available. Please wait for the system to fetch data...")
        st.stop()
    
    # Market overview cards
    st.markdown("### 📊 Market Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Stocks",
            f"{market_summary.get('total_stocks', len(stocks_data))}",
            delta=None
        )
    
    with col2:
        gainers = market_summary.get('gainers', 0)
        st.metric(
            "Gainers",
            f"{gainers}",
            delta=None
        )
    
    with col3:
        losers = market_summary.get('losers', 0)
        st.metric(
            "Losers",
            f"{losers}",
            delta=None
        )
    
    with col4:
        avg_change = market_summary.get('avg_change', 0)
        delta_color = "normal" if avg_change >= 0 else "inverse"
        st.metric(
            "Avg Change",
            f"{avg_change:.2f}%",
            delta=None
        )
    
    with col5:
        market_status = market_summary.get('market_status', 'unknown')
        status_emoji = "🟢" if market_status == "open" else "🔴"
        st.metric(
            "Market Status",
            f"{status_emoji} {market_status.title()}",
            delta=None
        )
    
    # Top movers section
    st.markdown("### 🔥 Top Movers")
    
    manager = get_data_manager()
    movers = manager.get_top_movers(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Top Gainers")
        gainers_df = pd.DataFrame(movers['gainers'])
        if not gainers_df.empty:
            gainers_df['change_percent'] = gainers_df['change_percent'].apply(lambda x: f"+{x:.2f}%")
            st.dataframe(
                gainers_df[['symbol', 'name', 'price', 'change_percent']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No gainers data available")
    
    with col2:
        st.markdown("#### 📉 Top Losers")
        losers_df = pd.DataFrame(movers['losers'])
        if not losers_df.empty:
            losers_df['change_percent'] = losers_df['change_percent'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(
                losers_df[['symbol', 'name', 'price', 'change_percent']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No losers data available")
    
    # Market performance chart
    st.markdown("### 📊 Market Performance Distribution")
    
    # Create distribution chart
    changes = []
    for stock in stocks_data.values():
        if stock.get('change_percent') is not None:
            changes.append(stock['change_percent'])
    
    if changes:
        fig = px.histogram(
            x=changes,
            nbins=50,
            title="Distribution of Stock Price Changes",
            labels={'x': 'Change (%)', 'y': 'Number of Stocks'},
            color_discrete_sequence=['#1f77b4']
        )
        
        fig.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="No Change")
        fig.update_layout(
            xaxis_title="Price Change (%)",
            yaxis_title="Number of Stocks",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed stock table
    st.markdown("### 📋 All Stocks")
    
    # Convert to DataFrame for better display
    stocks_list = []
    for symbol, data in stocks_data.items():
        stocks_list.append({
            'Symbol': symbol,
            'Name': data.get('name_en', 'N/A'),
            'Price (SAR)': data.get('price', 0),
            'Change': data.get('change', 0),
            'Change (%)': data.get('change_percent', 0),
            'Last Update': data.get('last_update', 'N/A')
        })
    
    df = pd.DataFrame(stocks_list)
    
    # Add search functionality
    search_term = st.text_input("🔍 Search stocks by symbol or name:")
    if search_term:
        mask = (
            df['Symbol'].str.contains(search_term, case=False, na=False) |
            df['Name'].str.contains(search_term, case=False, na=False)
        )
        df = df[mask]
    
    # Sort options
    sort_by = st.selectbox(
        "📊 Sort by:",
        ['Symbol', 'Name', 'Price (SAR)', 'Change (%)', 'Last Update'],
        index=3  # Default to Change (%)
    )
    
    ascending = st.checkbox("⬆️ Ascending order", value=False)
    df_sorted = df.sort_values(by=sort_by, ascending=ascending)
    
    # Display the dataframe with styling
    st.dataframe(
        df_sorted,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Price (SAR)': st.column_config.NumberColumn(
                'Price (SAR)',
                format="%.2f"
            ),
            'Change': st.column_config.NumberColumn(
                'Change',
                format="%.2f"
            ),
            'Change (%)': st.column_config.NumberColumn(
                'Change (%)',
                format="%.2f%%"
            )
        }
    )
    
    # Footer with statistics
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        📊 Displaying {len(df_sorted)} stocks | 
        🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
        💹 TADAWUL NEXUS Real-time Data System
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh mechanism
    if auto_refresh and CONTINUOUS_DATA_AVAILABLE:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application error: {e}")
        st.info("🔄 Please refresh the page and try again.")
