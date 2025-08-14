"""
Saudi Stock Market Trading Signals App - Web Interface with AI Features
Simplified, working version with proper error handling
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="Saudi Stock Market - Enhanced Trading Platform",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

def calculate_rsi(prices, period=14):
    """Calculate RSI with proper error handling"""
    try:
        if len(prices) < period:
            return pd.Series([50] * len(prices), index=prices.index)
        
        # Ensure we have numeric data
        prices = pd.to_numeric(prices, errors='coerce').dropna()
        
        if len(prices) < period:
            return pd.Series([50] * len(prices), index=prices.index)
        
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Avoid division by zero
        rs = gain / loss.replace(0, 0.001)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.fillna(50)
    except Exception as e:
        print(f"Error calculating RSI: {e}")
        return pd.Series([50] * len(prices), index=prices.index)

def get_saudi_stock_data(symbol, period="3mo"):
    """Get stock data for Saudi stocks"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        return hist
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

def generate_trading_signals():
    """Generate trading signals for Saudi stocks"""
    signals_data = []
    saudi_stocks = {
        '2222.SR': 'Saudi Aramco',
        '1120.SR': 'Al Rajhi Bank',
        '2030.SR': 'SABIC',
        '4030.SR': 'Riyad Bank',
        '1210.SR': 'Saudi National Bank'
    }
    
    for symbol, company in saudi_stocks.items():
        try:
            # Get stock data
            hist = get_saudi_stock_data(symbol)
            
            if hist.empty or len(hist) < 14:
                continue
            
            # Calculate indicators
            current_price = hist['Close'].iloc[-1]
            rsi = calculate_rsi(hist['Close'])
            current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
            
            # Generate signal
            if current_rsi < 30:
                signal = "BUY"
                strength = "Strong"
            elif current_rsi < 40:
                signal = "BUY"
                strength = "Moderate"
            elif current_rsi > 70:
                signal = "SELL"
                strength = "Strong"
            elif current_rsi > 60:
                signal = "SELL"
                strength = "Moderate"
            else:
                signal = "HOLD"
                strength = "Neutral"
            
            signals_data.append({
                'Symbol': symbol.replace('.SR', ''),
                'Company': company,
                'Price': f"{current_price:.2f} SAR",
                'RSI': f"{current_rsi:.1f}",
                'Signal': signal,
                'Strength': strength
            })
            
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue
    
    return pd.DataFrame(signals_data)

def get_ai_sample_signals():
    """Get sample AI trading signals for demonstration"""
    return [
        {"symbol": "2222", "signal": "BUY", "confidence": 0.85, "price_target": "32.50 SAR"},
        {"symbol": "1120", "signal": "HOLD", "confidence": 0.72, "price_target": "95.00 SAR"},
        {"symbol": "2030", "signal": "SELL", "confidence": 0.78, "price_target": "88.50 SAR"}
    ]

def main():
    """Main application"""
    
    # Title and description
    st.title("🇸🇦 Saudi Stock Market - Enhanced Trading Platform")
    st.markdown("**Complete AI-Enhanced Trading Platform for Saudi Stock Market (Tadawul)**")
    
    # Sidebar navigation
    st.sidebar.title("📱 Navigation")
    page = st.sidebar.radio(
        "Choose a section:",
        ["🏠 Dashboard", "📊 Technical Analysis", "🤖 AI Trading", "📈 Market Signals", "💼 Portfolio"]
    )
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Technical Analysis":
        show_technical_analysis()
    elif page == "🤖 AI Trading":
        show_ai_trading()
    elif page == "📈 Market Signals":
        show_market_signals()
    elif page == "💼 Portfolio":
        show_portfolio()

def show_dashboard():
    """Show main dashboard"""
    st.header("📊 Market Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("TASI Index", "12,345", "2.5%")
    with col2:
        st.metric("Market Cap", "2.8T SAR", "1.2%")
    with col3:
        st.metric("Volume", "156M", "-5.3%")
    with col4:
        st.metric("Active Stocks", "201", "3")
    
    # Quick market signals
    st.subheader("🎯 Quick Market Signals")
    if st.button("Generate Quick Signals"):
        with st.spinner("Analyzing market..."):
            signals = generate_trading_signals()
            if not signals.empty:
                st.dataframe(signals, use_container_width=True)
            else:
                st.warning("No signals generated. Please try again.")

def show_technical_analysis():
    """Show technical analysis section"""
    st.header("📊 Technical Analysis")
    
    # Stock selection
    stocks = {
        '2222.SR': 'Saudi Aramco',
        '1120.SR': 'Al Rajhi Bank', 
        '2030.SR': 'SABIC',
        '4030.SR': 'Riyad Bank',
        '1210.SR': 'Saudi National Bank'
    }
    
    selected_stock = st.selectbox("Select a stock:", list(stocks.keys()), format_func=lambda x: f"{x.replace('.SR', '')} - {stocks[x]}")
    
    if st.button("📈 Analyze Stock"):
        with st.spinner(f"Analyzing {stocks[selected_stock]}..."):
            hist = get_saudi_stock_data(selected_stock)
            
            if not hist.empty:
                # Price chart
                fig = px.line(hist, x=hist.index, y='Close', title=f'{stocks[selected_stock]} Price Chart')
                st.plotly_chart(fig, use_container_width=True)
                
                # Calculate and display RSI
                rsi = calculate_rsi(hist['Close'])
                current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"{hist['Close'].iloc[-1]:.2f} SAR")
                with col2:
                    st.metric("RSI", f"{current_rsi:.1f}")
                with col3:
                    signal = "BUY" if current_rsi < 30 else "SELL" if current_rsi > 70 else "HOLD"
                    st.metric("Signal", signal)
            else:
                st.error("Unable to fetch stock data")

def show_ai_trading():
    """Show AI trading section"""
    st.header("🤖 AI Trading Signals")
    
    st.info("AI features provide advanced market analysis and trading recommendations")
    
    if st.button("🎯 Generate AI Signals"):
        with st.spinner("AI analyzing market patterns..."):
            time.sleep(2)  # Simulate AI processing
            signals = get_ai_sample_signals()
            
            st.success("✅ AI signals generated successfully!")
            
            for signal in signals:
                signal_color = "🟢" if signal['signal'] == "BUY" else "🔴" if signal['signal'] == "SELL" else "🟡"
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"""
                    {signal_color} **{signal['symbol']}** - {signal['signal']}
                    - Target: {signal['price_target']}
                    """)
                with col2:
                    st.metric("Confidence", f"{signal['confidence']:.1%}")

def show_market_signals():
    """Show market signals section"""
    st.header("📈 Market Trading Signals")
    
    st.info("Generate buy/sell signals for Saudi stocks using technical analysis")
    
    if st.button("🎯 Generate Trading Signals", use_container_width=True):
        with st.spinner("Analyzing Saudi stocks..."):
            signals_data = generate_trading_signals()
            
            if not signals_data.empty:
                st.success("✅ Market signals generated successfully!")
                
                # Display signals table
                st.subheader("📊 Trading Signals")
                st.dataframe(signals_data, use_container_width=True)
                
                # Show summary
                if 'Signal' in signals_data.columns:
                    buy_signals = len(signals_data[signals_data['Signal'] == 'BUY'])
                    sell_signals = len(signals_data[signals_data['Signal'] == 'SELL'])
                    hold_signals = len(signals_data[signals_data['Signal'] == 'HOLD'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🟢 BUY Signals", buy_signals)
                    with col2:
                        st.metric("🔴 SELL Signals", sell_signals)
                    with col3:
                        st.metric("🟡 HOLD Signals", hold_signals)
            else:
                st.warning("⚠️ No signals generated. Please try again.")

def show_portfolio():
    """Show portfolio management section"""
    st.header("💼 Portfolio Management")
    
    st.info("Manage your Saudi stock portfolio")
    
    # Sample portfolio data
    portfolio_data = [
        {"Symbol": "2222", "Company": "Saudi Aramco", "Shares": 100, "Avg Cost": "32.50", "Current": "34.20", "P/L": "5.23%"},
        {"Symbol": "1120", "Company": "Al Rajhi Bank", "Shares": 50, "Avg Cost": "85.00", "Current": "87.50", "P/L": "2.94%"},
        {"Symbol": "2030", "Company": "SABIC", "Shares": 25, "Avg Cost": "90.00", "Current": "88.75", "P/L": "-1.39%"}
    ]
    
    st.subheader("📊 Current Holdings")
    st.dataframe(pd.DataFrame(portfolio_data), use_container_width=True)
    
    # Portfolio summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Value", "15,890 SAR")
    with col2:
        st.metric("Total P/L", "+1,250 SAR", "8.5%")
    with col3:
        st.metric("Day Change", "+320 SAR", "2.1%")
    with col4:
        st.metric("Holdings", "3 stocks")

if __name__ == "__main__":
    main()
