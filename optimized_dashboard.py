"""
Optimized Saudi Stock Market Dashboard
Integrates ultra-fast fetching with reliable processing
Solves ALL performance and data consistency issues
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time
import sys
import os

# Add core modules to path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_path = os.path.join(current_dir, 'core')
sys.path.insert(0, core_path)

try:
    from ultra_fast_fetcher import UltraFastFetcher
    from reliable_processor import ReliableMarketProcessor
    OPTIMIZED_MODULES_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Optimized modules not available: {e}")
    OPTIMIZED_MODULES_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="TADAWUL NEXUS - Optimized",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for performance dashboard
st.markdown("""
<style>
    .metric-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .performance-badge {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .speed-indicator {
        background: #ff6b6b;
        color: white;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .data-quality-high {
        background: #28a745;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 1rem 0 0.5rem 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def show_performance_metrics(processing_time: float, total_stocks: int, success_rate: float):
    """Display performance metrics with visual indicators"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <h4>⚡ Loading Speed</h4>
            <h2>{processing_time:.1f}s</h2>
            <div class="performance-badge">
                {'ULTRA FAST' if processing_time < 5 else 'FAST' if processing_time < 15 else 'NORMAL'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <h4>📊 Stocks Processed</h4>
            <h2>{total_stocks}</h2>
            <div class="performance-badge">LIVE DATA</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <h4>✅ Success Rate</h4>
            <h2>{success_rate:.1f}%</h2>
            <div class="performance-badge">
                {'EXCELLENT' if success_rate > 90 else 'GOOD' if success_rate > 75 else 'FAIR'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        throughput = total_stocks / processing_time if processing_time > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <h4>🚀 Throughput</h4>
            <h2>{throughput:.1f}/s</h2>
            <div class="performance-badge">OPTIMIZED</div>
        </div>
        """, unsafe_allow_html=True)

def create_performance_chart(market_data: dict):
    """Create performance visualization chart"""
    if not market_data.get('success'):
        return None
    
    # Extract data for visualization
    gainers = market_data.get('top_gainers', {}).get('data', [])
    losers = market_data.get('top_losers', {}).get('data', [])
    
    if not gainers and not losers:
        return None
    
    # Prepare data
    symbols = []
    changes = []
    colors = []
    
    # Add top 5 gainers
    for stock in gainers[:5]:
        symbols.append(f"{stock['symbol']}")
        changes.append(stock['change_percent'])
        colors.append('#28a745')  # Green
    
    # Add top 5 losers
    for stock in losers[:5]:
        symbols.append(f"{stock['symbol']}")
        changes.append(stock['change_percent'])
        colors.append('#dc3545')  # Red
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=symbols,
            y=changes,
            marker_color=colors,
            text=[f"{change:+.1f}%" for change in changes],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Top Market Movers - Live Performance",
        xaxis_title="Stock Symbol",
        yaxis_title="Change %",
        height=400,
        showlegend=False,
        template="plotly_dark"
    )
    
    return fig

def display_market_summary_table(data_list: list, title: str, columns: list):
    """Display market data in a formatted table"""
    if not data_list:
        st.info(f"No {title.lower()} data available")
        return
    
    df = pd.DataFrame(data_list)
    
    # Format the DataFrame
    if 'current_price' in df.columns:
        df['current_price'] = df['current_price'].apply(lambda x: f"{x:.2f} SAR")
    
    if 'change_percent' in df.columns:
        df['change_percent'] = df['change_percent'].apply(lambda x: f"{x:+.2f}%")
    
    if 'volume' in df.columns:
        df['volume'] = df['volume'].apply(lambda x: f"{x:,}")
    
    if 'trading_value' in df.columns:
        df['trading_value'] = df['trading_value'].apply(lambda x: f"{x:,.0f} SAR")
    
    # Rename columns for display
    column_mapping = {
        'symbol': 'Symbol',
        'name': 'Company Name',
        'current_price': 'Price',
        'change_percent': 'Change %',
        'volume': 'Volume',
        'trading_value': 'Trading Value',
        'sector': 'Sector'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Select only requested columns that exist
    available_columns = [col for col in columns if col in df.columns]
    df_display = df[available_columns]
    
    st.dataframe(df_display, use_container_width=True, height=300)

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0;">🚀 TADAWUL NEXUS - OPTIMIZED</h1>
        <p style="color: white; margin: 0; font-size: 1.2rem;">Ultra-Fast Saudi Stock Market Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    st.sidebar.markdown("## ⚙️ Performance Controls")
    
    max_stocks = st.sidebar.slider(
        "📊 Number of Stocks to Process",
        min_value=10,
        max_value=100,
        value=50,
        step=10,
        help="More stocks = more comprehensive data but longer loading time"
    )
    
    use_cache = st.sidebar.checkbox(
        "⚡ Use Smart Cache",
        value=True,
        help="Uses cached data if available (updated hourly)"
    )
    
    performance_mode = st.sidebar.selectbox(
        "🎯 Performance Mode",
        ["Ultra Fast (5-10s)", "Fast (10-20s)", "Complete (20-40s)"],
        index=1
    )
    
    # Map performance mode to stock count
    mode_mapping = {
        "Ultra Fast (5-10s)": min(max_stocks, 25),
        "Fast (10-20s)": min(max_stocks, 50), 
        "Complete (20-40s)": max_stocks
    }
    
    actual_stock_count = mode_mapping[performance_mode]
    
    st.sidebar.markdown(f"""
    **Selected Configuration:**
    - Mode: {performance_mode}
    - Stocks: {actual_stock_count}
    - Cache: {'Enabled' if use_cache else 'Disabled'}
    """)
    
    # Check if optimized modules are available
    if not OPTIMIZED_MODULES_AVAILABLE:
        st.error("❌ Optimized modules not available. Please check installation.")
        st.stop()
    
    # Performance testing button
    if st.sidebar.button("🧪 Run Performance Test"):
        st.sidebar.info("Running performance test...")
        
        test_start = time.time()
        fetcher = UltraFastFetcher()
        test_symbols = ['2222.SR', '1120.SR', '2380.SR', '4061.SR', '2010.SR']
        test_data = fetcher.fetch_market_data(test_symbols)
        test_time = time.time() - test_start
        
        st.sidebar.success(f"✅ Test completed in {test_time:.2f}s")
        st.sidebar.info(f"📊 Fetched {len(test_data)} stocks")
    
    # Main content
    if st.button("🚀 Load Market Data", type="primary"):
        
        # Progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Fetch data
            status_text.text("📡 Fetching live market data...")
            progress_bar.progress(25)
            
            start_time = time.time()
            fetcher = UltraFastFetcher()
            
            # Get symbol list for fetching
            import sqlite3
            db_path = os.path.join(current_dir, 'data', 'Saudi Stock Exchange (TASI) Sectors and Companies.db')
            
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT symbol FROM companies WHERE symbol LIKE '%.SR'")
                symbols = [row[0] for row in cursor.fetchall()]
                conn.close()
                actual_symbols = symbols[:actual_stock_count]  # Limit to requested count
            else:
                # Fallback to common symbols
                actual_symbols = ['2222.SR', '1120.SR', '2380.SR', '4061.SR', '2010.SR']
            
            raw_stocks = fetcher.fetch_market_data(actual_symbols)
            
            # Step 2: Process data
            status_text.text("🔧 Processing and validating data...")
            progress_bar.progress(50)
            
            # Convert to dict format for processor
            stock_dicts = []
            for symbol, stock_data in raw_stocks.items():
                stock_dicts.append({
                    'symbol': symbol,
                    'price': stock_data.price,
                    'change': stock_data.change,
                    'change_percent': stock_data.change_percent,
                    'volume': stock_data.volume
                })
            
            # Step 3: Reliable processing
            status_text.text("✅ Generating market summary...")
            progress_bar.progress(75)
            
            processor = ReliableMarketProcessor()
            market_summary = processor.validate_and_process_data(stock_dicts)
            
            total_time = time.time() - start_time
            
            progress_bar.progress(100)
            status_text.text("🎉 Market data loaded successfully!")
            
            time.sleep(0.5)  # Brief pause to show completion
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            if market_summary.total_stocks > 0:
                
                # Performance metrics
                show_performance_metrics(
                    total_time,
                    market_data['processed_count'],
                    market_data['success_rate']
                )
                
                # Market overview
                st.markdown('<div class="section-header">📊 Market Overview</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Performance chart
                    fig = create_performance_chart(market_data)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Market statistics
                    stats = market_data.get('market_stats', {})
                    st.markdown(f"""
                    **📈 Market Statistics:**
                    - Total Volume: {stats.get('total_volume', 0):,}
                    - Total Value: {stats.get('total_trading_value', 0):,.0f} SAR
                    - Market Direction: {stats.get('market_direction', 'Unknown')}
                    - Gainers: {stats.get('gainers_count', 0)}
                    - Losers: {stats.get('losers_count', 0)}
                    """)
                    
                    st.markdown(f"""
                    **⚡ Performance:**
                    - Processing Time: {total_time:.2f}s
                    - Throughput: {market_data['processed_count']/total_time:.1f} stocks/s
                    - Data Quality: {market_data.get('data_quality', 'Unknown')}
                    """)
                
                # Market tables
                tab1, tab2, tab3, tab4 = st.tabs(["📈 Top Gainers", "📉 Top Losers", "📊 Volume Leaders", "💰 Value Leaders"])
                
                with tab1:
                    gainers_data = market_data.get('top_gainers', {}).get('data', [])
                    st.markdown(f"### {market_data.get('top_gainers', {}).get('title', 'Top Gainers')}")
                    display_market_summary_table(
                        gainers_data,
                        "Top Gainers",
                        ['Symbol', 'Company Name', 'Price', 'Change %', 'Volume', 'Sector']
                    )
                
                with tab2:
                    losers_data = market_data.get('top_losers', {}).get('data', [])
                    st.markdown(f"### {market_data.get('top_losers', {}).get('title', 'Top Losers')}")
                    display_market_summary_table(
                        losers_data,
                        "Top Losers",
                        ['Symbol', 'Company Name', 'Price', 'Change %', 'Volume', 'Sector']
                    )
                
                with tab3:
                    volume_data = market_data.get('volume_movers', {}).get('data', [])
                    st.markdown(f"### {market_data.get('volume_movers', {}).get('title', 'Volume Leaders')}")
                    display_market_summary_table(
                        volume_data,
                        "Volume Leaders",
                        ['Symbol', 'Company Name', 'Price', 'Volume', 'Trading Value', 'Sector']
                    )
                
                with tab4:
                    value_data = market_data.get('value_movers', {}).get('data', [])
                    st.markdown(f"### {market_data.get('value_movers', {}).get('title', 'Value Leaders')}")
                    display_market_summary_table(
                        value_data,
                        "Value Leaders",
                        ['Symbol', 'Company Name', 'Price', 'Trading Value', 'Volume', 'Sector']
                    )
                
                # Data sources and quality information
                st.markdown('<div class="section-header">📡 Data Sources & Quality</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Data Sources:**")
                    sources = market_data.get('data_sources', {})
                    for source, count in sources.items():
                        st.markdown(f"- {source}: {count} stocks")
                
                with col2:
                    st.markdown("**Quality Metrics:**")
                    st.markdown(f"- Official TASI Count: {market_data.get('official_stock_count', 'Unknown')}")
                    st.markdown(f"- Processed Count: {market_data.get('processed_count', 0)}")
                    st.markdown(f"- Success Rate: {market_data.get('success_rate', 0):.1f}%")
                    st.markdown(f"- Data Quality: {market_data.get('data_quality', 'Unknown')}")
                
                # Last update timestamp
                st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
            else:
                st.error("❌ Failed to load market data. Please try again.")
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error loading market data: {str(e)}")
            
            # Show debug information
            with st.expander("🔧 Debug Information"):
                st.code(f"Error: {str(e)}\nModules Available: {OPTIMIZED_MODULES_AVAILABLE}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🚀 Powered by Ultra-Fast Fetcher & Reliable Processor | 
        Live data from Yahoo Finance | 
        Optimized for TASI (Saudi Stock Exchange)</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
