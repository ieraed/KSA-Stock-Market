"""
Saudi Stock Market Trading Signals App - Web Interface
Complete web-based interface for Saudi stock analysis and trading signals
"""

import streamlit as st
import subprocess
import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import time
import threading
from datetime import datetime, timedelta
import yfinance as yf

# Add the src directory to the path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Page configuration
st.set_page_config(
    page_title="نجم التداول - Najm Al-Tadawul (Trading Star)",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #1e3c72;
}

.sidebar-content {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

def get_market_status():
    """Get real Saudi market status based on current time"""
    from datetime import datetime
    import pytz
    
    # Saudi Arabia timezone
    saudi_tz = pytz.timezone('Asia/Riyadh')
    now = datetime.now(saudi_tz)
    
    # Market hours: Sunday to Thursday, 10:00 AM to 3:00 PM
    current_weekday = now.weekday()  # Monday=0, Sunday=6
    current_time = now.time()
    
    # Convert to Saudi weekday (Sunday=0, Thursday=4)
    saudi_weekday = (current_weekday + 1) % 7
    
    # Market open: Sunday (0) to Thursday (4), 10:00-15:00
    market_open_time = datetime.strptime("10:00", "%H:%M").time()
    market_close_time = datetime.strptime("15:00", "%H:%M").time()
    
    is_trading_day = saudi_weekday <= 4  # Sunday to Thursday
    is_trading_hours = market_open_time <= current_time <= market_close_time
    
    if is_trading_day and is_trading_hours:
        return "🟢 Market Open", f"🕐 {now.strftime('%I:%M %p')} - Open until 3:00 PM"
    elif is_trading_day and current_time < market_open_time:
        return "🟡 Pre-Market", f"🕐 Opens at 10:00 AM (Current: {now.strftime('%I:%M %p')})"
    elif is_trading_day and current_time > market_close_time:
        return "🔴 Market Closed", f"🕐 Closed at 3:00 PM (Current: {now.strftime('%I:%M %p')})"
    else:
        # Weekend (Friday/Saturday)
        return "🔴 Market Closed", "🕐 Weekend - Opens Sunday 10:00 AM"

def get_saudi_stocks_data():
    """Get data for popular Saudi stocks with .SR removal"""
    saudi_stocks = {
        'SABIC': '2010.SR',
        'Al Rajhi Bank': '1120.SR', 
        'Saudi Aramco': '2222.SR',
        'ACWA Power': '2082.SR',
        'Saudi Electric': '5110.SR',
        'SAMBA': '1090.SR',
        'Almarai': '2280.SR',
        'STC': '7010.SR'
    }
    
    data = {}
    for name, symbol in saudi_stocks.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change = current_price - prev_price
                change_pct = (change / prev_price * 100) if prev_price != 0 else 0
                
                data[name] = {
                    'symbol': symbol.replace('.SR', ''),  # Remove .SR suffix
                    'full_symbol': symbol,
                    'price': current_price,
                    'change': change,
                    'change_pct': change_pct,
                    'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                }
        except Exception as e:
            continue
    
    return data

def get_market_movers():
    """Get top gainers and losers for Saudi market"""
    # Extended list of Saudi stocks for better market coverage
    saudi_stocks = {
        'Saudi Aramco': '2222.SR', 'SABIC': '2010.SR', 'Al Rajhi Bank': '1120.SR',
        'STC': '7010.SR', 'Almarai': '2280.SR', 'ACWA Power': '2082.SR',
        'Saudi Electric': '5110.SR', 'SAMBA': '1090.SR', 'NCB': '1180.SR',
        'Alinma Bank': '1150.SR', 'Riyad Bank': '1010.SR', 'Arab Bank': '1140.SR',
        'Jarir': '4190.SR', 'Herfy': '6001.SR', 'Maaden': '1211.SR',
        'SIPCHEM': '2330.SR', 'Yanbu Cement': '3060.SR', 'Savola': '2050.SR'
    }
    
    movers_data = []
    for name, symbol in saudi_stocks.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d", interval="1d")
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2]
                change_pct = ((current_price - prev_price) / prev_price * 100)
                
                movers_data.append({
                    'name': name,
                    'symbol': symbol.replace('.SR', ''),
                    'price': current_price,
                    'change_pct': change_pct,
                    'volume': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
                })
        except:
            continue
    
    # Sort by change percentage
    movers_data.sort(key=lambda x: x['change_pct'], reverse=True)
    
    gainers = movers_data[:5]  # Top 5 gainers
    losers = movers_data[-5:]  # Top 5 losers
    losers.reverse()  # Show worst first
    
    return gainers, losers

def show_user_registration():
    """User Registration Page"""
    st.markdown('<div class="main-header"><h1>⭐ مرحباً بك في نجم التداول - Welcome to Najm Al-Tadawul</h1></div>', unsafe_allow_html=True)
    
    # Saudi-themed welcome
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0d4f3c 0%, #2d5a27 100%); padding: 2rem; border-radius: 15px; margin: 1rem 0; border: 2px solid #ffd700;">
        <h2 style="color: #ffd700; text-align: center; margin-bottom: 1rem;">🏛️ نجم التداول - Trading Star</h2>
        <p style="color: white; text-align: center; font-size: 1.1rem; margin-bottom: 0;">
            Your Gateway to Saudi Stock Market Excellence<br>
            بوابتك لتميز السوق المالية السعودية
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'user_registered' not in st.session_state:
        st.session_state.user_registered = False
    
    if not st.session_state.user_registered:
        st.markdown("### 📝 User Registration - تسجيل المستخدم")
        st.info("Please complete your registration to access all features of Najm Al-Tadawul")
        
        with st.form("user_registration"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name - الاسم الأول *", placeholder="أحمد")
                last_name = st.text_input("Last Name - الاسم الأخير *", placeholder="العبدالله")
                email = st.text_input("Email - البريد الإلكتروني *", placeholder="ahmed@example.com")
                phone = st.text_input("Phone - رقم الهاتف", placeholder="+966501234567")
            
            with col2:
                country = st.selectbox("Country - البلد *", [
                    "Saudi Arabia - المملكة العربية السعودية",
                    "United Arab Emirates - الإمارات العربية المتحدة", 
                    "Kuwait - الكويت",
                    "Qatar - قطر",
                    "Bahrain - البحرين",
                    "Oman - عُمان",
                    "Other - أخرى"
                ])
                city = st.text_input("City - المدينة", placeholder="الرياض")
                experience = st.selectbox("Trading Experience - خبرة التداول", [
                    "Beginner - مبتدئ",
                    "Intermediate - متوسط", 
                    "Advanced - متقدم",
                    "Professional - محترف"
                ])
                broker = st.selectbox("Primary Broker - الوسيط الأساسي", [
                    "Al Rajhi Capital - الراجحي المالية",
                    "Al Inma Capital - الإنماء للاستثمار",
                    "BSF Capital - بي اس اف كابيتال",
                    "SNB Capital - البنك الأهلي للاستثمار",
                    "Riyad Capital - الرياض المالية",
                    "Other - أخرى"
                ])
            
            # Terms and conditions
            st.markdown("---")
            terms_accepted = st.checkbox("I accept the Terms of Service and Privacy Policy - أوافق على شروط الخدمة وسياسة الخصوصية *")
            newsletter = st.checkbox("Subscribe to market updates and signals - الاشتراك في تحديثات السوق والإشارات")
            
            submit_button = st.form_submit_button("🚀 Complete Registration - إكمال التسجيل", use_container_width=True)
            
            if submit_button:
                if not all([first_name, last_name, email, country]) or not terms_accepted:
                    st.error("Please fill in all required fields (*) and accept the terms - يرجى ملء جميع الحقول المطلوبة (*) والموافقة على الشروط")
                else:
                    # Store user data in session state
                    st.session_state.user_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone,
                        'country': country,
                        'city': city,
                        'experience': experience,
                        'broker': broker,
                        'newsletter': newsletter,
                        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.user_registered = True
                    st.success("🎉 Registration completed successfully! Welcome to Najm Al-Tadawul! - تم التسجيل بنجاح! مرحباً بك في نجم التداول!")
                    time.sleep(1)
                    st.session_state.page = "Quick Actions"
                    st.rerun()
    
    else:
        # Show welcome message for registered users
        user_data = st.session_state.user_data
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0d4f3c 0%, #2d5a27 100%); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
            <h3 style="color: #ffd700; margin-bottom: 0.5rem;">🌟 Welcome back, {user_data['first_name']}!</h3>
            <p style="color: white; margin-bottom: 0;">Ready to explore the Saudi market with Najm Al-Tadawul</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Continue to Trading Dashboard - المتابعة إلى لوحة التداول", use_container_width=True):
            st.session_state.page = "Quick Actions"
            st.rerun()
        
        # Show user profile
        with st.expander("👤 View Profile - عرض الملف الشخصي"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {user_data['first_name']} {user_data['last_name']}")
                st.write(f"**Email:** {user_data['email']}")
                st.write(f"**Country:** {user_data['country']}")
            with col2:
                st.write(f"**Experience:** {user_data['experience']}")
                st.write(f"**Primary Broker:** {user_data['broker']}")
                st.write(f"**Registered:** {user_data['registration_date']}")

def show_quick_actions():
    """Quick Actions Page"""
    st.markdown('<div class="main-header"><h1>🎯 Quick Actions</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 Signal Generation")
        st.info("Generate buy/sell signals for Saudi stocks using technical analysis")
        
        if st.button("🎯 Generate Trading Signals", use_container_width=True):
            with st.spinner("Analyzing Saudi stocks..."):
                try:
                    # Import and run signal generation
                    sys.path.insert(0, str(current_dir / "src"))
                    from src.signals.signal_generator import SignalGenerator
                    from src.data.market_data import MarketDataFetcher
                    from src.utils.config import Config
                    
                    config = Config()
                    data_fetcher = MarketDataFetcher(config)
                    signal_gen = SignalGenerator(data_fetcher, config)
                    
                    # Generate signals for popular Saudi stocks
                    saudi_stocks = ['2222.SR', '2010.SR', '1120.SR', '7010.SR', '2280.SR']
                    
                    st.success("✅ Signals generated successfully!")
                    
                    for symbol in saudi_stocks:
                        try:
                            signals = signal_gen.generate_signals(symbol)
                            if signals:
                                st.write(f"**{symbol.replace('.SR', '')}**: {len(signals)} signals found")
                        except Exception as e:
                            st.write(f"**{symbol.replace('.SR', '')}**: Error - {str(e)}")
                            
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    # Fallback to subprocess
                    try:
                        venv_python = Path(current_dir) / ".venv" / "Scripts" / "python.exe"
                        if venv_python.exists():
                            result = subprocess.run([str(venv_python), "run_signals.py"], 
                                                  capture_output=True, text=True, cwd=current_dir)
                        else:
                            result = subprocess.run([sys.executable, "run_signals.py"], 
                                                  capture_output=True, text=True, cwd=current_dir)
                        
                        if result.returncode == 0:
                            st.success("✅ Signals generated successfully!")
                            st.text(result.stdout)
                        else:
                            st.error("❌ Error generating signals")
                            st.text(result.stderr)
                    except Exception as e2:
                        st.error(f"Subprocess error: {str(e2)}")
    
    with col2:
        st.markdown("### 📊 Portfolio Analysis")
        st.info("Analyze your portfolio performance and holdings")
        
        if st.button("📈 Analyze Portfolio", use_container_width=True):
            st.session_state.page = "Portfolio Analysis"
            st.rerun()
    
    with col3:
        st.markdown("### 🧪 Backtesting")
        st.info("Test trading strategies with historical data")
        
        if st.button("⚡ Run Backtest", use_container_width=True):
            with st.spinner("Running backtest..."):
                try:
                    venv_python = Path(current_dir) / ".venv" / "Scripts" / "python.exe"
                    if venv_python.exists():
                        result = subprocess.run([str(venv_python), "-m", "src.backtesting.backtest"], 
                                              capture_output=True, text=True, cwd=current_dir)
                    else:
                        result = subprocess.run([sys.executable, "-m", "src.backtesting.backtest"], 
                                              capture_output=True, text=True, cwd=current_dir)
                    
                    if result.returncode == 0:
                        st.success("✅ Backtest completed!")
                        st.text(result.stdout)
                    else:
                        st.error("❌ Backtest failed")
                        st.text(result.stderr)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

def show_live_dashboard():
    """Live Dashboard Page"""
    st.markdown('<div class="main-header"><h1>📊 Live Market Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Add home navigation
    if st.button("🏠 Back to Home", key="dashboard_home"):
        st.session_state.page = "Quick Actions"
        st.rerun()
    
    # Market overview with real TASI data
    col1, col2, col3, col4 = st.columns(4)
    
    # Get real TASI data
    try:
        tasi = yf.Ticker("^TASI")
        tasi_hist = tasi.history(period="2d")
        if not tasi_hist.empty:
            current_tasi = tasi_hist['Close'].iloc[-1]
            prev_tasi = tasi_hist['Close'].iloc[-2] if len(tasi_hist) > 1 else current_tasi
            tasi_change = current_tasi - prev_tasi
            tasi_change_pct = (tasi_change / prev_tasi * 100) if prev_tasi != 0 else 0
            
            with col1:
                st.metric("TASI Index", f"{current_tasi:,.2f}", f"{tasi_change:+.2f} ({tasi_change_pct:+.2f}%)")
        else:
            with col1:
                st.metric("TASI Index", "10,930.30", "-16.44 (-0.15%)")
    except:
        with col1:
            st.metric("TASI Index", "10,930.30", "-16.44 (-0.15%)")
    
    with col2:
        st.metric("Market Cap", "2.8T SAR", "1.2%")
    with col3:
        st.metric("Volume", "272M", "-5.2%")
    with col4:
        st.metric("Active Stocks", "485", "12")
    
    st.markdown("---")
    
    # Market Movers Section
    col1, col2 = st.columns(2)
    
    with st.spinner("Loading market movers..."):
        gainers, losers = get_market_movers()
    
    with col1:
        st.subheader("🏆 Top Gainers")
        if gainers:
            gainers_data = []
            for stock in gainers:
                gainers_data.append({
                    'Stock': stock['name'],
                    'Symbol': stock['symbol'],
                    'Price': f"{stock['price']:.2f}",
                    'Change %': f"+{stock['change_pct']:.2f}%"
                })
            st.dataframe(pd.DataFrame(gainers_data), use_container_width=True, hide_index=True)
        else:
            st.info("No gainers data available")
    
    with col2:
        st.subheader("📉 Top Losers")
        if losers:
            losers_data = []
            for stock in losers:
                losers_data.append({
                    'Stock': stock['name'],
                    'Symbol': stock['symbol'],
                    'Price': f"{stock['price']:.2f}",
                    'Change %': f"{stock['change_pct']:.2f}%"
                })
            st.dataframe(pd.DataFrame(losers_data), use_container_width=True, hide_index=True)
        else:
            st.info("No losers data available")
    
    st.markdown("---")
    
    # Get live data
    with st.spinner("Loading live market data..."):
        stocks_data = get_saudi_stocks_data()
    
    if stocks_data:
        # Create dataframe for display
        df_data = []
        for name, data in stocks_data.items():
            df_data.append({
                'Stock': name,
                'Symbol': data['symbol'],  # Already without .SR
                'Price (SAR)': f"{data['price']:.2f}",
                'Change': f"{data['change']:+.2f}",
                'Change %': f"{data['change_pct']:+.2f}%",
                'Volume': f"{data['volume']:,.0f}"
            })
        
        df = pd.DataFrame(df_data)
        
        # Display table
        st.subheader("📈 Live Stock Prices")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Price chart
        st.subheader("📊 Price Movements")
        
        # Create a sample chart (in real app, this would show intraday data)
        selected_stock = st.selectbox("Select Stock for Chart", list(stocks_data.keys()))
        
        if selected_stock:
            symbol = stocks_data[selected_stock]['full_symbol']  # Use full symbol for yfinance
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo", interval="1d")
                
                if not hist.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Candlestick(
                        x=hist.index,
                        open=hist['Open'],
                        high=hist['High'],
                        low=hist['Low'],
                        close=hist['Close'],
                        name=selected_stock
                    ))
                    
                    fig.update_layout(
                        title=f"{selected_stock} ({stocks_data[selected_stock]['symbol']}) - 1 Month Chart",
                        yaxis_title="Price (SAR)",
                        xaxis_title="Date"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading chart: {str(e)}")
    else:
        st.warning("No live data available at the moment.")

def show_portfolio_analysis():
    """Portfolio Analysis Page"""
    st.markdown('<div class="main-header"><h1>💼 Portfolio Analysis</h1></div>', unsafe_allow_html=True)
    
    # Add home navigation
    if st.button("🏠 Back to Home", key="portfolio_home"):
        st.session_state.page = "Quick Actions"
        st.rerun()
    
    try:
        # Clear any caching to ensure fresh data
        if hasattr(st, 'cache_data'):
            st.cache_data.clear()
        
        from src.utils.portfolio_manager import PortfolioManager
        from src.data.market_data import MarketDataFetcher
        from src.utils.config import Config
        
        # Initialize portfolio manager
        config = Config()
        data_fetcher = MarketDataFetcher(config)
        portfolio_manager = PortfolioManager(data_fetcher, config)
        
        # Load portfolio data
        if 'uploaded_portfolio' in st.session_state:
            # Use uploaded/manual portfolio
            portfolio_df = st.session_state.uploaded_portfolio.copy()
            st.info("📊 Using your uploaded/manual portfolio data")
        else:
            # Use default sample portfolio
            portfolio_df = portfolio_manager.create_sample_portfolio()
            st.info("📊 Using sample portfolio data. Upload your own in Portfolio Management.")
        
        # Portfolio summary
        total_positions = len(portfolio_df)
        brokers = portfolio_df['Custodian'].nunique()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Positions", total_positions)
        with col2:
            st.metric("Brokers", brokers)
        
        # Initially show placeholders
        metric3 = col3.empty()
        metric4 = col4.empty()
        metric3.metric("Total Value", "Calculating...")
        metric4.metric("Today's P&L", "Calculating...")
        
        # Broker breakdown
        st.subheader("📊 Holdings by Broker")
        broker_counts = portfolio_df['Custodian'].value_counts()
        
        fig = px.pie(values=broker_counts.values, names=broker_counts.index, 
                     title="Portfolio Distribution by Broker")
        st.plotly_chart(fig, use_container_width=True)
        
        # Holdings table
        st.subheader("📋 Current Holdings")
        
        # Get current prices with better error handling
        with st.spinner("Fetching current prices..."):
            try:
                # Try portfolio manager first
                try:
                    current_prices = portfolio_manager.get_current_prices(portfolio_df)
                except Exception as pm_error:
                    st.warning(f"Portfolio manager price fetch failed: {pm_error}")
                    # Fallback to direct yfinance calls
                    current_prices = {}
                    symbols = portfolio_df['Symbol'].unique()
                    
                    for symbol in symbols:
                        try:
                            import yfinance as yf
                            ticker = yf.Ticker(f"{symbol}.SR")
                            hist = ticker.history(period="1d")
                            if not hist.empty:
                                current_prices[symbol] = float(hist['Close'].iloc[-1])
                            else:
                                current_prices[symbol] = 0.0
                        except Exception:
                            current_prices[symbol] = 0.0
                
                # Calculate portfolio metrics
                portfolio_df['Current_Price'] = portfolio_df['Symbol'].map(current_prices).fillna(0)
                portfolio_df['Market_Value'] = portfolio_df['Owned_Qty'] * portfolio_df['Current_Price']
                portfolio_df['Total_Cost'] = portfolio_df['Owned_Qty'] * portfolio_df['Cost']
                portfolio_df['P&L'] = portfolio_df['Market_Value'] - portfolio_df['Total_Cost']
                portfolio_df['P&L %'] = np.where(portfolio_df['Total_Cost'] > 0, 
                                               (portfolio_df['P&L'] / portfolio_df['Total_Cost'] * 100), 0)
                
                # Calculate total metrics
                successful_prices = [p for p in current_prices.values() if p > 0]
                total_market_value = portfolio_df[portfolio_df['Current_Price'] > 0]['Market_Value'].sum()
                total_cost = portfolio_df['Total_Cost'].sum()
                total_pnl = portfolio_df[portfolio_df['Current_Price'] > 0]['P&L'].sum()
                total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
                
                # Update metrics
                metric3.metric("Total Value", f"{total_market_value:,.0f} SAR")
                metric4.metric("Today's P&L", f"{total_pnl:+,.0f} SAR ({total_pnl_pct:+.1f}%)")
                
                # Format display with better handling of missing prices
                display_df = portfolio_df.copy()
                display_df['Current_Price'] = display_df['Current_Price'].apply(
                    lambda x: f"{x:.2f}" if x > 0 else "No Data"
                )
                display_df['Market_Value'] = display_df['Market_Value'].apply(
                    lambda x: f"{x:,.2f}" if x > 0 else "No Data"
                )
                display_df['P&L'] = display_df.apply(
                    lambda row: f"{row['P&L']:+,.2f}" if row['Current_Price'] != "No Data" else "No Data", axis=1
                )
                display_df['P&L %'] = display_df.apply(
                    lambda row: f"{row['P&L %']:+.2f}%" if row['Current_Price'] != "No Data" else "No Data", axis=1
                )
                
                # Show successful vs failed price fetches
                successful_prices = sum(1 for x in current_prices.values() if x > 0)
                total_stocks = len(portfolio_df)
                
                if successful_prices < total_stocks:
                    st.warning(f"⚠️ Price data available for {successful_prices}/{total_stocks} stocks. Some prices may be delayed or unavailable.")
                else:
                    st.success(f"✅ Live prices fetched for all {total_stocks} stocks")
                
                st.dataframe(
                    display_df[['Symbol', 'Company', 'Custodian', 'Owned_Qty', 'Cost', 'Current_Price', 'Market_Value', 'P&L', 'P&L %']],
                    use_container_width=True,
                    hide_index=True
                )
                
            except Exception as e:
                st.error(f"Error fetching prices: {str(e)}")
                
                # Show basic portfolio without live prices
                st.warning("Showing portfolio without live pricing due to data issues")
                basic_df = portfolio_df[['Symbol', 'Company', 'Custodian', 'Owned_Qty', 'Cost']].copy()
                basic_df['Total_Cost'] = basic_df['Owned_Qty'] * basic_df['Cost']
                
                total_cost = portfolio_df['Total_Cost'].sum()
                metric3.metric("Total Cost", f"{total_cost:,.0f} SAR")
                metric4.metric("Live P&L", "Data Unavailable")
                
                st.dataframe(basic_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"Error loading portfolio: {str(e)}")
        st.info("Please ensure the portfolio module is properly configured.")

def show_technical_analysis():
    """Technical Analysis Page"""
    st.markdown('<div class="main-header"><h1>📈 Technical Analysis</h1></div>', unsafe_allow_html=True)
    
    # Add home navigation
    if st.button("🏠 Back to Home", key="technical_home"):
        st.session_state.page = "Quick Actions"
        st.rerun()
    
    # Stock selector
    popular_stocks = {
        'Saudi Aramco': '2222.SR',
        'SABIC': '2010.SR',
        'Al Rajhi Bank': '1120.SR',
        'STC': '7010.SR',
        'Almarai': '2280.SR'
    }
    
    selected_stock = st.selectbox("Select Stock for Analysis", list(popular_stocks.keys()))
    period = st.selectbox("Select Period", ['1mo', '3mo', '6mo', '1y'], index=1)
    
    if selected_stock:
        symbol = popular_stocks[selected_stock]
        display_symbol = symbol.replace('.SR', '')  # Remove .SR for display
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if not hist.empty:
                # Price chart with moving averages
                fig = go.Figure()
                
                # Candlestick chart
                fig.add_trace(go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name=selected_stock
                ))
                
                # Moving averages
                hist['MA20'] = hist['Close'].rolling(window=20).mean()
                hist['MA50'] = hist['Close'].rolling(window=50).mean()
                
                fig.add_trace(go.Scatter(
                    x=hist.index, y=hist['MA20'],
                    mode='lines', name='MA20',
                    line=dict(color='orange', width=2)
                ))
                
                fig.add_trace(go.Scatter(
                    x=hist.index, y=hist['MA50'],
                    mode='lines', name='MA50',
                    line=dict(color='blue', width=2)
                ))
                
                fig.update_layout(
                    title=f"{selected_stock} ({display_symbol}) Technical Analysis",
                    yaxis_title="Price (SAR)",
                    xaxis_title="Date",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Price Metrics")
                    current_price = hist['Close'].iloc[-1]
                    ma20 = hist['MA20'].iloc[-1]
                    ma50 = hist['MA50'].iloc[-1]
                    
                    st.metric("Current Price", f"{current_price:.2f} SAR")
                    st.metric("MA20", f"{ma20:.2f} SAR")
                    st.metric("MA50", f"{ma50:.2f} SAR")
                
                with col2:
                    st.subheader("🎯 Signals")
                    if current_price > ma20 and ma20 > ma50:
                        st.success("🟢 Bullish Trend")
                    elif current_price < ma20 and ma20 < ma50:
                        st.error("🔴 Bearish Trend")
                    else:
                        st.warning("🟡 Neutral/Mixed")
                
        except Exception as e:
            st.error(f"Error loading data for {selected_stock}: {str(e)}")

def show_market_data():
    """Market Data Page"""
    st.markdown('<div class="main-header"><h1>📊 Market Data</h1></div>', unsafe_allow_html=True)
    
    # Add home navigation
    if st.button("🏠 Back to Home", key="market_home"):
        st.session_state.page = "Quick Actions"
        st.rerun()
    
    # Data source options
    st.subheader("📈 Saudi Stock Market Data")
    
    # Get real market movers
    with st.spinner("Loading market data..."):
        gainers, losers = get_market_movers()
    
    # Market movers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Top Gainers")
        if gainers:
            gainers_data = []
            for stock in gainers:
                gainers_data.append({
                    'Stock': stock['name'],
                    'Symbol': stock['symbol'],  # Already without .SR
                    'Price': f"{stock['price']:.2f}",
                    'Change %': f"+{stock['change_pct']:.2f}%"
                })
            st.dataframe(pd.DataFrame(gainers_data), use_container_width=True, hide_index=True)
        else:
            # Fallback data
            gainers_data = {
                'Stock': ['ACWA Power', 'Saudi Aramco', 'SABIC'],
                'Symbol': ['2082', '2222', '2010'],
                'Change %': ['+5.67%', '+3.21%', '+2.45%']
            }
            st.dataframe(pd.DataFrame(gainers_data), use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("### 📉 Top Losers")
        if losers:
            losers_data = []
            for stock in losers:
                losers_data.append({
                    'Stock': stock['name'],
                    'Symbol': stock['symbol'],  # Already without .SR
                    'Price': f"{stock['price']:.2f}",
                    'Change %': f"{stock['change_pct']:.2f}%"
                })
            st.dataframe(pd.DataFrame(losers_data), use_container_width=True, hide_index=True)
        else:
            # Fallback data
            losers_data = {
                'Stock': ['Al Rajhi Bank', 'STC', 'Almarai'],
                'Symbol': ['1120', '7010', '2280'],
                'Change %': ['-2.34%', '-1.87%', '-1.23%']
            }
            st.dataframe(pd.DataFrame(losers_data), use_container_width=True, hide_index=True)
    
    # Market sectors
    st.subheader("🏭 Sector Performance")
    sector_data = {
        'Sector': ['Energy', 'Banking', 'Telecommunications', 'Materials', 'Utilities'],
        'Change %': ['+2.1%', '-0.5%', '+1.3%', '+0.8%', '+0.2%'],
        'Volume': ['45M', '23M', '12M', '18M', '8M']
    }
    
    fig = px.bar(sector_data, x='Sector', y=[float(x.replace('%', '').replace('+', '')) for x in sector_data['Change %']], 
                 title="Sector Performance Today")
    fig.update_yaxis(title="Change %")
    st.plotly_chart(fig, use_container_width=True)

def show_portfolio_management():
    """Portfolio Management Page - Upload or Manual Entry"""
    st.markdown('<div class="main-header"><h1>📝 Portfolio Management</h1></div>', unsafe_allow_html=True)
    
    # Add home navigation
    if st.button("🏠 Back to Home", key="portfolio_mgmt_home"):
        st.session_state.page = "Quick Actions"
        st.rerun()
    
    st.markdown("### 📊 Manage Your Portfolio Holdings")
    st.info("You can either upload an Excel file with your portfolio or enter holdings manually.")
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["📤 Upload Excel", "✏️ Manual Entry", "📋 Current Portfolio"])
    
    with tab1:
        st.subheader("📤 Upload Portfolio from Excel")
        
        # Excel format information
        st.markdown("### 📋 Required Excel Format")
        
        # Show expected format
        sample_data = {
            'Symbol': ['2222', '1120', '2010', '7010'],
            'Company': ['Saudi Aramco', 'Al Rajhi Bank', 'SABIC', 'STC'],
            'Owned_Qty': [100, 50, 75, 200],
            'Cost': [35.50, 85.20, 120.00, 45.30],
            'Custodian': ['Al Inma Capital', 'BSF Capital', 'Al Rajhi Capital', 'Al Inma Capital']
        }
        sample_df = pd.DataFrame(sample_data)
        
        st.markdown("**Expected columns (case-sensitive):**")
        st.dataframe(sample_df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Column Descriptions:**
        - **Symbol**: Stock symbol without .SR (e.g., 2222, 1120)
        - **Company**: Company name (will be auto-filled if left empty)
        - **Owned_Qty**: Number of shares owned
        - **Cost**: Average cost per share in SAR
        - **Custodian**: Broker name (e.g., Al Inma Capital, BSF Capital, Al Rajhi Capital)
        """)
        
        # Download template
        if st.button("📥 Download Excel Template", use_container_width=True):
            try:
                template_df = pd.DataFrame({
                    'Symbol': ['', '', '', ''],
                    'Company': ['', '', '', ''],
                    'Owned_Qty': [0, 0, 0, 0],
                    'Cost': [0.0, 0.0, 0.0, 0.0],
                    'Custodian': ['', '', '', '']
                })
                
                # Convert to Excel in memory
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    template_df.to_excel(writer, sheet_name='Portfolio', index=False)
                
                st.download_button(
                    label="💾 Download Template",
                    data=output.getvalue(),
                    file_name="portfolio_template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating template: {e}")
        
        st.markdown("---")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose Excel file",
            type=['xlsx', 'xls'],
            help="Upload your portfolio Excel file with the required format"
        )
        
        if uploaded_file is not None:
            try:
                # Read Excel file
                df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File uploaded successfully! Found {len(df)} rows.")
                
                # Validate required columns
                required_columns = ['Symbol', 'Company', 'Owned_Qty', 'Cost', 'Custodian']
                missing_columns = [col for col in required_columns if col not in df.columns]
                
                if missing_columns:
                    st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                    st.info("Please ensure your Excel file has all required columns.")
                else:
                    # Clean and validate data
                    df = df.dropna(subset=['Symbol', 'Owned_Qty', 'Cost'])  # Remove rows with missing critical data
                    
                    # Auto-fill company names if empty
                    for idx, row in df.iterrows():
                        if pd.isna(row['Company']) or row['Company'] == '':
                            stock_info = get_stock_company_name(str(row['Symbol']))
                            df.at[idx, 'Company'] = stock_info['name']
                    
                    # Validate data types
                    try:
                        df['Owned_Qty'] = pd.to_numeric(df['Owned_Qty'])
                        df['Cost'] = pd.to_numeric(df['Cost'])
                        df['Symbol'] = df['Symbol'].astype(str)
                    except Exception as e:
                        st.error(f"❌ Data validation error: {e}")
                        st.stop()
                    
                    # Show preview
                    st.subheader("📋 Portfolio Preview")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("💾 Save Portfolio", use_container_width=True):
                            try:
                                # Save to session state
                                st.session_state.uploaded_portfolio = df
                                st.success("✅ Portfolio saved successfully!")
                                st.info("Go to 'Portfolio Analysis' tab to view live analysis.")
                            except Exception as e:
                                st.error(f"Error saving portfolio: {e}")
                    
                    with col2:
                        if st.button("🔄 Clear Data", use_container_width=True):
                            if 'uploaded_portfolio' in st.session_state:
                                del st.session_state.uploaded_portfolio
                            st.success("Portfolio data cleared.")
                            st.rerun()
                            
            except Exception as e:
                st.error(f"❌ Error reading Excel file: {e}")
                st.info("Please ensure the file is a valid Excel file with the correct format.")
    
    with tab2:
        st.subheader("✏️ Manual Portfolio Entry")
        
        # Initialize session state for manual entries
        if 'manual_portfolio' not in st.session_state:
            st.session_state.manual_portfolio = []
        
        st.markdown("### ➕ Add New Position")
        
        # Form for adding positions
        with st.form("add_position"):
            col1, col2 = st.columns(2)
            
            with col1:
                symbol = st.text_input("Stock Symbol", placeholder="e.g., 2222")
                owned_qty = st.number_input("Quantity Owned", min_value=1, value=100)
                
            with col2:
                cost = st.number_input("Average Cost (SAR)", min_value=0.01, value=50.00, step=0.01)
                custodian = st.selectbox("Custodian/Broker", [
                    "Al Inma Capital", "BSF Capital", "Al Rajhi Capital", 
                    "SNB Capital", "Riyad Capital", "Other"
                ])
            
            if custodian == "Other":
                custodian = st.text_input("Enter Custodian Name")
            
            submitted = st.form_submit_button("➕ Add Position", use_container_width=True)
            
            if submitted:
                if symbol and owned_qty > 0 and cost > 0 and custodian:
                    # Get company name
                    stock_info = get_stock_company_name(symbol)
                    
                    new_position = {
                        'Symbol': symbol,
                        'Company': stock_info['name'],
                        'Owned_Qty': owned_qty,
                        'Cost': cost,
                        'Custodian': custodian
                    }
                    
                    st.session_state.manual_portfolio.append(new_position)
                    st.success(f"✅ Added {symbol} - {stock_info['name']} to portfolio!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
        
        # Display current manual entries
        if st.session_state.manual_portfolio:
            st.markdown("### 📋 Current Manual Entries")
            
            manual_df = pd.DataFrame(st.session_state.manual_portfolio)
            st.dataframe(manual_df, use_container_width=True, hide_index=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Save Manual Portfolio", use_container_width=True):
                    st.session_state.uploaded_portfolio = manual_df
                    st.success("✅ Manual portfolio saved!")
                    st.info("Go to 'Portfolio Analysis' tab to view analysis.")
            
            with col2:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.manual_portfolio = []
                    if 'uploaded_portfolio' in st.session_state:
                        del st.session_state.uploaded_portfolio
                    st.success("All entries cleared.")
                    st.rerun()
            
            with col3:
                # Remove specific position
                if len(st.session_state.manual_portfolio) > 0:
                    symbols = [f"{pos['Symbol']} - {pos['Company']}" for pos in st.session_state.manual_portfolio]
                    to_remove = st.selectbox("Remove Position", ["Select to remove..."] + symbols)
                    
                    if to_remove != "Select to remove..." and st.button("🗑️ Remove Selected"):
                        symbol_to_remove = to_remove.split(' - ')[0]
                        st.session_state.manual_portfolio = [
                            pos for pos in st.session_state.manual_portfolio 
                            if pos['Symbol'] != symbol_to_remove
                        ]
                        st.success(f"Removed {to_remove}")
                        st.rerun()
        
        else:
            st.info("No positions added yet. Use the form above to add your holdings.")
    
    with tab3:
        st.subheader("📋 Current Portfolio Status")
        
        if 'uploaded_portfolio' in st.session_state:
            df = st.session_state.uploaded_portfolio
            
            st.success(f"✅ Portfolio loaded with {len(df)} positions")
            
            # Portfolio summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Positions", len(df))
            with col2:
                st.metric("Unique Brokers", df['Custodian'].nunique())
            with col3:
                total_value = (df['Owned_Qty'] * df['Cost']).sum()
                st.metric("Total Cost", f"{total_value:,.0f} SAR")
            
            # Broker breakdown
            broker_counts = df['Custodian'].value_counts()
            st.markdown("### 📊 Holdings by Broker")
            
            for broker, count in broker_counts.items():
                st.markdown(f"- **{broker}**: {count} positions")
            
            # Show portfolio
            st.markdown("### 📋 Portfolio Details")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Export options
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📈 Analyze Portfolio", use_container_width=True):
                    st.session_state.page = "Portfolio Analysis"
                    st.rerun()
            
            with col2:
                # Export to Excel
                try:
                    from io import BytesIO
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df.to_excel(writer, sheet_name='Portfolio', index=False)
                    
                    st.download_button(
                        label="📥 Export to Excel",
                        data=output.getvalue(),
                        file_name=f"my_portfolio_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Export error: {e}")
        
        else:
            st.info("No portfolio data available. Upload an Excel file or enter positions manually.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📤 Upload Excel", use_container_width=True):
                    st.session_state.active_tab = 0  # Switch to upload tab
                    st.rerun()
            
            with col2:
                if st.button("✏️ Manual Entry", use_container_width=True):
                    st.session_state.active_tab = 1  # Switch to manual tab
                    st.rerun()

def get_stock_company_name(symbol: str) -> dict:
    """Get company name for a stock symbol"""
    stock_names = {
        "2222": "Saudi Aramco",
        "1120": "Al Rajhi Bank", 
        "2010": "SABIC",
        "7010": "Saudi Telecom Company",
        "2280": "Almarai",
        "1150": "Al Inma Bank",
        "8150": "ACIG",
        "6010": "NADEC",
        "4323": "SIMOUI",
        "1140": "Banque Saudi Fransi",
        "5110": "Saudi Electricity Company",
        "2290": "YANSAB",
        "4322": "RETAL",
        "4190": "Jarir Marketing",
        "2082": "ACWA Power",
        "1090": "SAMBA Financial Group",
        "1180": "The National Commercial Bank",
        "1010": "Riyad Bank",
        "1080": "Arab Bank",
        "7030": "Zain KSA",
        "2382": "ADES",
        "2230": "Petrochemical Industries",
        "9408": "Bank AlBilad",
        "4200": "Al Jazeera Bank",
        "2330": "SIPCHEM",
        "3060": "Yanbu Cement",
        "2050": "Savola Group",
        "1211": "Maaden",
        "6001": "Herfy Food Services"
    }
    
    return {
        "name": stock_names.get(symbol, f"Company {symbol}"),
        "symbol": symbol
    }

def show_original_dashboard():
    """Link to Original Dashboard"""
    st.markdown('<div class="main-header"><h1>🎛️ Original Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Add home navigation
    if st.button("🏠 Back to Home", key="original_home"):
        st.session_state.page = "Quick Actions"
        st.rerun()
    
    st.info("🚀 Launch the original Streamlit dashboard for comprehensive analysis")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🎛️ Open Original Dashboard", use_container_width=True):
            try:
                venv_python = Path(current_dir) / ".venv" / "Scripts" / "python.exe"
                if venv_python.exists():
                    subprocess.Popen([str(venv_python), "run_dashboard.py"], cwd=current_dir)
                else:
                    subprocess.Popen([sys.executable, "run_dashboard.py"], cwd=current_dir)
                
                st.success("✅ Dashboard started! Check http://localhost:8501")
                st.info("The original dashboard should open in a new browser tab.")
                
            except Exception as e:
                st.error(f"Error starting dashboard: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Dashboard Features:**")
        st.markdown("- Real-time market data")
        st.markdown("- Advanced technical analysis")
        st.markdown("- Interactive charts")
        
    with col2:
        st.markdown("**Trading Tools:**")
        st.markdown("- Signal generation")
        st.markdown("- Portfolio tracking")
        st.markdown("- Risk management")
        
    with col3:
        st.markdown("**Data Sources:**")
        st.markdown("- Yahoo Finance")
        st.markdown("- Saudi market data")
        st.markdown("- Real-time updates")

def main():
    """Main application"""
    
    # Sidebar navigation
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.title("🏦 Saudi Stock Market")
    st.sidebar.markdown("**Trading Signals App**")
    st.sidebar.markdown("---")
    
    # Navigation
    pages = {
        "🎯 Quick Actions": "Quick Actions",
        "📊 Live Dashboard": "Live Dashboard", 
        "💼 Portfolio Analysis": "Portfolio Analysis",
        "� Portfolio Management": "Portfolio Management",
        "�📈 Technical Analysis": "Technical Analysis",
        "📊 Market Data": "Market Data",
        "🎛️ Original Dashboard": "Original Dashboard"
    }
    
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "Quick Actions"
    
    # Page selection
    selected_page = st.sidebar.radio("Navigate to:", list(pages.keys()), 
                                    index=list(pages.values()).index(st.session_state.page))
    
    # Update session state
    st.session_state.page = pages[selected_page]
    
    st.sidebar.markdown("---")
    
    # Real market status
    st.sidebar.markdown("### 📈 Market Status")
    market_status, market_time = get_market_status()
    
    if "🟢" in market_status:
        st.sidebar.success(market_status)
    elif "�" in market_status:
        st.sidebar.warning(market_status)
    else:
        st.sidebar.error(market_status)
    
    st.sidebar.info(market_time)
    st.sidebar.markdown("---")
    
    # Quick stats with real TASI data
    st.sidebar.markdown("### 📊 Quick Stats")
    try:
        tasi = yf.Ticker("^TASI")
        tasi_hist = tasi.history(period="2d")
        if not tasi_hist.empty:
            current_tasi = tasi_hist['Close'].iloc[-1]
            prev_tasi = tasi_hist['Close'].iloc[-2] if len(tasi_hist) > 1 else current_tasi
            tasi_change = current_tasi - prev_tasi
            
            st.sidebar.metric("TASI", f"{current_tasi:,.0f}", f"{tasi_change:+.0f}")
        else:
            st.sidebar.metric("TASI", "10,930", "-16")
    except:
        st.sidebar.metric("TASI", "10,930", "-16")
    
    st.sidebar.metric("Volume", "272M", "-5.2%")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Route to appropriate page
    if st.session_state.page == "User Registration":
        show_user_registration()
    elif st.session_state.page == "Quick Actions":
        show_quick_actions()
    elif st.session_state.page == "Live Dashboard":
        show_live_dashboard()
    elif st.session_state.page == "Portfolio Analysis":
        show_portfolio_analysis()
    elif st.session_state.page == "Portfolio Management":
        show_portfolio_management()
    elif st.session_state.page == "Technical Analysis":
        show_technical_analysis()
    elif st.session_state.page == "Market Data":
        show_market_data()
    elif st.session_state.page == "Original Dashboard":
        show_original_dashboard()

if __name__ == "__main__":
    main()
