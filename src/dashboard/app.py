"""
Streamlit dashboard for Saudi Stock Market Trading Signals App
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from ..data.market_data import MarketDataFetcher
from ..signals.signal_generator import SignalGenerator
from ..analysis.technical_indicators import TechnicalIndicators
from ..utils.config import Config

# Page configuration
st.set_page_config(
    page_title="Saudi Stock Market Signals",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
    }
    .signal-buy {
        background-color: #d4edda;
        color: #155724;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .signal-sell {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .signal-hold {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'config' not in st.session_state:
    st.session_state.config = Config()
if 'data_fetcher' not in st.session_state:
    st.session_state.data_fetcher = MarketDataFetcher(st.session_state.config)
if 'signal_generator' not in st.session_state:
    st.session_state.signal_generator = SignalGenerator(st.session_state.data_fetcher, st.session_state.config)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🇸🇦 Saudi Stock Market Trading Signals</h1>', unsafe_allow_html=True)
    
    # Sidebar
    create_sidebar()
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Signals", "📈 Stock Analysis", "⚙️ Settings", "📋 About"])
    
    with tab1:
        show_live_signals()
    
    with tab2:
        show_stock_analysis()
    
    with tab3:
        show_settings()
    
    with tab4:
        show_about()

def create_sidebar():
    """Create sidebar with controls"""
    
    st.sidebar.title("🎯 Control Panel")
    
    # Popular Saudi stocks
    popular_stocks = st.session_state.data_fetcher.get_popular_saudi_stocks()
    stock_names = {
        "2222.SR": "Saudi Aramco",
        "1120.SR": "Al Rajhi Bank",
        "2030.SR": "SABIC",
        "4030.SR": "Riyad Bank",
        "1210.SR": "The Saudi National Bank"
    }
    
    # Stock selection
    st.sidebar.subheader("📈 Select Stock")
    selected_stock = st.sidebar.selectbox(
        "Choose a stock:",
        options=popular_stocks[:5],
        format_func=lambda x: f"{stock_names.get(x, x)} ({x})",
        key="selected_stock"
    )
    
    # Timeframe selection
    st.sidebar.subheader("⏰ Timeframe")
    timeframe = st.sidebar.selectbox(
        "Select timeframe:",
        options=["1d", "1wk", "1mo"],
        index=0,
        key="timeframe"
    )
    
    # Period selection
    st.sidebar.subheader("📅 Period")
    period = st.sidebar.selectbox(
        "Select period:",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        index=2,
        key="period"
    )
    
    # Auto-refresh
    st.sidebar.subheader("🔄 Auto Refresh")
    auto_refresh = st.sidebar.checkbox("Enable auto-refresh (30s)", value=False)
    
    if auto_refresh:
        st.rerun()

def show_live_signals():
    """Show live trading signals for all Saudi stocks"""
    
    st.header("📊 Live Trading Signals")
    
    # Add refresh button
    if st.button("🔄 Refresh All Signals", type="primary"):
        # Clear any cached data
        if 'signals_data' in st.session_state:
            del st.session_state['signals_data']
    
    try:
        # Saudi stocks with Arabic names
        saudi_stocks = {
            "2222.SR": "أرامكو السعودية",
            "1120.SR": "الراجحي", 
            "2030.SR": "سافكو",
            "7020.SR": "أسواق العثيم",
            "4030.SR": "الحكير",
            "2020.SR": "سابك",
            "1180.SR": "الأهلي",
            "4001.SR": "زين السعودية"
        }
        
        # Generate signals for all stocks
        with st.spinner("Analyzing Saudi stocks..."):
            signals_data = []
            progress_bar = st.progress(0)
            
            for i, (symbol, arabic_name) in enumerate(saudi_stocks.items()):
                try:
                    signals = st.session_state.signal_generator.generate_signals(symbol)
                    
                    if signals:
                        latest_signal = signals[-1]  # Get the most recent signal
                        signals_data.append({
                            "Stock Code": symbol.replace('.SR', ''),
                            "Company": arabic_name,
                            "Signal": latest_signal.signal_type,
                            "Price (SAR)": f"{latest_signal.price:.2f}",
                            "Confidence": f"{latest_signal.confidence:.1%}",
                            "Reason": latest_signal.reason[:40] + "..." if len(latest_signal.reason) > 40 else latest_signal.reason,
                            "Time": latest_signal.timestamp.strftime("%H:%M")
                        })
                    else:
                        signals_data.append({
                            "Stock Code": symbol.replace('.SR', ''),
                            "Company": arabic_name,
                            "Signal": "NO DATA",
                            "Price (SAR)": "N/A",
                            "Confidence": "N/A",
                            "Reason": "Insufficient data",
                            "Time": "N/A"
                        })
                        
                except Exception as e:
                    signals_data.append({
                        "Stock Code": symbol.replace('.SR', ''),
                        "Company": arabic_name,
                        "Signal": "ERROR",
                        "Price (SAR)": "N/A",
                        "Confidence": "N/A",
                        "Reason": f"Error: {str(e)[:30]}...",
                        "Time": "N/A"
                    })
                
                progress_bar.progress((i + 1) / len(saudi_stocks))
            
            # Display results in table format
            if signals_data:
                st.success(f"✅ Analysis completed for {len(signals_data)} stocks!")
                
                # Create DataFrame for better display
                import pandas as pd
                df = pd.DataFrame(signals_data)
                
                # Style the table based on signals
                def highlight_signals(row):
                    if row['Signal'] == 'BUY':
                        return ['background-color: #90EE90'] * len(row)  # Light green
                    elif row['Signal'] == 'SELL':
                        return ['background-color: #FFB6C1'] * len(row)  # Light red  
                    elif row['Signal'] == 'HOLD':
                        return ['background-color: #FFFFE0'] * len(row)  # Light yellow
                    else:
                        return ['background-color: #F0F0F0'] * len(row)  # Gray
                
                # Display styled table
                st.dataframe(df.style.apply(highlight_signals, axis=1), use_container_width=True, hide_index=True)
                
                # Summary metrics
                buy_count = len([s for s in signals_data if s['Signal'] == 'BUY'])
                sell_count = len([s for s in signals_data if s['Signal'] == 'SELL'])
                hold_count = len([s for s in signals_data if s['Signal'] == 'HOLD'])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🟢 BUY Signals", buy_count)
                with col2:
                    st.metric("🔴 SELL Signals", sell_count) 
                with col3:
                    st.metric("🟡 HOLD Signals", hold_count)
            else:
                st.warning("❌ No signals generated")
    
    except Exception as e:
        st.error(f"Error generating signals: {e}")
        import traceback
        st.code(traceback.format_exc())
    
    # Market status
    st.subheader("🕐 Market Status")
    market_open = st.session_state.data_fetcher.is_market_open()
    status_color = "🟢" if market_open else "🔴"
    status_text = "Open" if market_open else "Closed"
    st.write(f"{status_color} Saudi Market is currently **{status_text}**")
    
    # Trading hours info
    market_hours = st.session_state.config.get_saudi_market_hours()
    st.write(f"Trading Hours: {market_hours['start_time']} - {market_hours['end_time']} ({market_hours['timezone']})")
    st.write(f"Trading Days: {', '.join(market_hours['trading_days'])}")

def show_stock_analysis():
    """Show detailed stock analysis"""
    
    st.header("📈 Stock Analysis")
    
    selected_stock = st.session_state.get("selected_stock", "2222.SR")
    period = st.session_state.get("period", "6mo")
    timeframe = st.session_state.get("timeframe", "1d")
    
    try:
        # Fetch stock data
        with st.spinner(f"Loading data for {selected_stock}..."):
            data = st.session_state.data_fetcher.get_stock_data(selected_stock, period=period, interval=timeframe)
        
        if data is not None and not data.empty:
            # Basic metrics
            show_stock_metrics(data, selected_stock)
            
            # Price chart with technical indicators
            show_price_chart(data, selected_stock)
            
            # Technical indicators
            show_technical_indicators(data)
            
        else:
            st.error(f"No data available for {selected_stock}")
    
    except Exception as e:
        st.error(f"Error loading stock analysis: {e}")

def show_stock_metrics(data: pd.DataFrame, symbol: str):
    """Show basic stock metrics"""
    
    latest_data = data.iloc[-1]
    prev_data = data.iloc[-2] if len(data) > 1 else latest_data
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Current Price",
            value=f"{latest_data['Close']:.2f} SAR",
            delta=f"{latest_data['Close'] - prev_data['Close']:.2f}"
        )
    
    with col2:
        change_pct = ((latest_data['Close'] - prev_data['Close']) / prev_data['Close']) * 100
        st.metric(
            label="Change %",
            value=f"{change_pct:.2f}%"
        )
    
    with col3:
        st.metric(
            label="Volume",
            value=f"{latest_data['Volume']:,.0f}"
        )
    
    with col4:
        st.metric(
            label="High",
            value=f"{latest_data['High']:.2f} SAR"
        )
    
    with col5:
        st.metric(
            label="Low",
            value=f"{latest_data['Low']:.2f} SAR"
        )

def show_price_chart(data: pd.DataFrame, symbol: str):
    """Show price chart with technical indicators"""
    
    st.subheader("📊 Price Chart with Technical Indicators")
    
    # Calculate technical indicators
    indicators = TechnicalIndicators()
    
    close_prices = data['Close']
    rsi = indicators.rsi(close_prices)
    macd_line, macd_signal, macd_hist = indicators.macd(close_prices)
    bb_upper, bb_middle, bb_lower = indicators.bollinger_bands(close_prices)
    sma_20 = indicators.sma(close_prices, 20)
    sma_50 = indicators.sma(close_prices, 50)
    
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Price & Bollinger Bands', 'MACD', 'RSI'),
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price"
        ),
        row=1, col=1
    )
    
    # Bollinger Bands
    fig.add_trace(go.Scatter(x=data.index, y=bb_upper, name="BB Upper", line=dict(color='red', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=bb_middle, name="BB Middle", line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=bb_lower, name="BB Lower", line=dict(color='red', dash='dash')), row=1, col=1)
    
    # Moving averages
    fig.add_trace(go.Scatter(x=data.index, y=sma_20, name="SMA 20", line=dict(color='orange')), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=sma_50, name="SMA 50", line=dict(color='purple')), row=1, col=1)
    
    # MACD
    fig.add_trace(go.Scatter(x=data.index, y=macd_line, name="MACD", line=dict(color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=macd_signal, name="Signal", line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Bar(x=data.index, y=macd_hist, name="Histogram"), row=2, col=1)
    
    # RSI
    fig.add_trace(go.Scatter(x=data.index, y=rsi, name="RSI", line=dict(color='purple')), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # Update layout
    fig.update_layout(
        title=f"{symbol} Technical Analysis",
        xaxis_title="Date",
        height=800,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_technical_indicators(data: pd.DataFrame):
    """Show technical indicators table"""
    
    st.subheader("🔍 Technical Indicators")
    
    indicators = TechnicalIndicators()
    close_prices = data['Close']
    high_prices = data['High']
    low_prices = data['Low']
    
    # Calculate latest values
    latest_rsi = indicators.rsi(close_prices).iloc[-1]
    macd_line, macd_signal, _ = indicators.macd(close_prices)
    latest_macd = macd_line.iloc[-1]
    latest_macd_signal = macd_signal.iloc[-1]
    
    stoch_k, stoch_d = indicators.stochastic(high_prices, low_prices, close_prices)
    latest_stoch_k = stoch_k.iloc[-1]
    latest_stoch_d = stoch_d.iloc[-1]
    
    latest_williams_r = indicators.williams_r(high_prices, low_prices, close_prices).iloc[-1]
    latest_atr = indicators.atr(high_prices, low_prices, close_prices).iloc[-1]
    
    # Create indicators DataFrame
    indicators_df = pd.DataFrame({
        'Indicator': ['RSI', 'MACD', 'MACD Signal', 'Stochastic %K', 'Stochastic %D', 'Williams %R', 'ATR'],
        'Value': [
            f"{latest_rsi:.2f}",
            f"{latest_macd:.4f}",
            f"{latest_macd_signal:.4f}",
            f"{latest_stoch_k:.2f}",
            f"{latest_stoch_d:.2f}",
            f"{latest_williams_r:.2f}",
            f"{latest_atr:.2f}"
        ],
        'Interpretation': [
            "Overbought" if latest_rsi > 70 else "Oversold" if latest_rsi < 30 else "Neutral",
            "Bullish" if latest_macd > latest_macd_signal else "Bearish",
            "Signal Line",
            "Overbought" if latest_stoch_k > 80 else "Oversold" if latest_stoch_k < 20 else "Neutral",
            "Overbought" if latest_stoch_d > 80 else "Oversold" if latest_stoch_d < 20 else "Neutral",
            "Overbought" if latest_williams_r > -20 else "Oversold" if latest_williams_r < -80 else "Neutral",
            "Volatility Measure"
        ]
    })
    
    st.dataframe(indicators_df, use_container_width=True)

def show_settings():
    """Show application settings"""
    
    st.header("⚙️ Settings")
    
    st.subheader("📊 Technical Indicator Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**RSI Settings**")
        rsi_period = st.number_input("RSI Period", value=st.session_state.config.rsi_period, min_value=5, max_value=50)
        rsi_oversold = st.number_input("RSI Oversold Level", value=st.session_state.config.rsi_oversold, min_value=10.0, max_value=40.0)
        rsi_overbought = st.number_input("RSI Overbought Level", value=st.session_state.config.rsi_overbought, min_value=60.0, max_value=90.0)
        
        st.write("**MACD Settings**")
        macd_fast = st.number_input("MACD Fast Period", value=st.session_state.config.macd_fast, min_value=5, max_value=20)
        macd_slow = st.number_input("MACD Slow Period", value=st.session_state.config.macd_slow, min_value=20, max_value=50)
        macd_signal = st.number_input("MACD Signal Period", value=st.session_state.config.macd_signal, min_value=5, max_value=15)
    
    with col2:
        st.write("**Bollinger Bands Settings**")
        bb_period = st.number_input("BB Period", value=st.session_state.config.bb_period, min_value=10, max_value=50)
        bb_std_dev = st.number_input("BB Standard Deviation", value=st.session_state.config.bb_std_dev, min_value=1.0, max_value=3.0, step=0.1)
        
        st.write("**Moving Average Settings**")
        sma_short = st.number_input("Short MA Period", value=st.session_state.config.sma_short, min_value=5, max_value=30)
        sma_long = st.number_input("Long MA Period", value=st.session_state.config.sma_long, min_value=30, max_value=100)
    
    if st.button("💾 Save Settings"):
        # Update configuration
        st.session_state.config.rsi_period = rsi_period
        st.session_state.config.rsi_oversold = rsi_oversold
        st.session_state.config.rsi_overbought = rsi_overbought
        st.session_state.config.macd_fast = macd_fast
        st.session_state.config.macd_slow = macd_slow
        st.session_state.config.macd_signal = macd_signal
        st.session_state.config.bb_period = bb_period
        st.session_state.config.bb_std_dev = bb_std_dev
        st.session_state.config.sma_short = sma_short
        st.session_state.config.sma_long = sma_long
        
        st.success("Settings saved successfully!")

def show_about():
    """Show about information"""
    
    st.header("📋 About")
    
    st.markdown("""
    ## 🇸🇦 Saudi Stock Market Trading Signals App
    
    This application provides automated trading signals for the Saudi stock market (Tadawul) using technical analysis.
    
    ### 🎯 Features
    - **Real-time Signals**: Get buy/sell signals based on multiple technical indicators
    - **Technical Analysis**: RSI, MACD, Bollinger Bands, Moving Averages, and more
    - **Interactive Charts**: Visualize price movements and technical indicators
    - **Saudi Market Focus**: Specifically designed for Tadawul stocks
    - **Customizable Parameters**: Adjust indicator settings to match your trading style
    
    ### 📊 Supported Indicators
    - **RSI (Relative Strength Index)**: Identifies overbought/oversold conditions
    - **MACD**: Trend-following momentum indicator
    - **Bollinger Bands**: Volatility indicator
    - **Moving Averages**: Trend identification
    - **Stochastic Oscillator**: Momentum indicator
    - **Williams %R**: Momentum indicator
    - **ATR (Average True Range)**: Volatility measure
    
    ### 🏦 Popular Saudi Stocks
    - **2222.SR**: Saudi Aramco
    - **1120.SR**: Al Rajhi Bank
    - **2030.SR**: SABIC
    - **4030.SR**: Riyad Bank
    - **1210.SR**: The Saudi National Bank
    
    ### ⚠️ Disclaimer
    This application is for educational purposes only. Trading signals should not be considered as financial advice. 
    Always do your own research and consult with a qualified financial advisor before making investment decisions.
    
    ### 🕐 Saudi Market Hours
    - **Trading Days**: Sunday to Thursday
    - **Trading Hours**: 10:00 AM - 3:00 PM (Saudi Time)
    - **Currency**: SAR (Saudi Riyal)
    """)

if __name__ == "__main__":
    main()
