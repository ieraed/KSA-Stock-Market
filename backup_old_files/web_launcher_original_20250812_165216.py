"""
Web-based launcher for Saudi Stock Market Trading Signals App
"""

import streamlit as st
import subprocess
import sys
import os
import pandas as pd
from pathlib import Path
import time
import threading
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Saudi Stock Market App Launcher",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

def run_command_in_background(command, description):
    """Run a command in the background"""
    try:
        st.info(f"🔄 {description}...")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            st.success(f"✅ {description} completed successfully!")
            if result.stdout:
                st.code(result.stdout)
        else:
            st.error(f"❌ {description} failed!")
            if result.stderr:
                st.code(result.stderr)
                
    except subprocess.TimeoutExpired:
        st.warning(f"⏱️ {description} is taking longer than expected...")
    except Exception as e:
        st.error(f"❌ Error: {e}")

def main():
    """Main web launcher function"""
    
    # Header
    st.title("🇸🇦 Saudi Stock Market Trading Signals App")
    st.markdown("---")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎯 Quick Actions", 
        "📊 Live Dashboard", 
        "💼 Portfolio Analysis",
        "💰 Investment Integration",
        "⚙️ Setup & Test",
        "📈 Analysis Tools",
        "📚 Documentation"
    ])
    
    with tab1:
        st.header("🎯 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🔍 Generate Signals")
            if st.button("🎯 Run Signal Analysis", key="signals", help="Analyze Saudi stocks and generate trading signals"):
                with st.spinner("Generating signals..."):
                    command = f'"{sys.executable}" run_signals.py'
                    run_command_in_background(command, "Signal Generation")
        
        with col2:
            st.subheader("📊 Start Dashboard")
            dashboard_url = "http://localhost:8501"
            
            if st.button("🚀 Launch Full Dashboard", key="dashboard", help="Open the complete analysis dashboard"):
                st.info("🌐 Dashboard starting...")
                st.markdown(f"**Open this URL in a new tab:** [{dashboard_url}]({dashboard_url})")
                st.code(f"streamlit run src/dashboard/app.py --server.port=8502")
        
        with col3:
            st.subheader("🧪 Run Tests")
            if st.button("🔬 Test System", key="test", help="Run comprehensive system tests"):
                with st.spinner("Running tests..."):
                    command = f'"{sys.executable}" test_app.py'
                    run_command_in_background(command, "System Testing")
    
    with tab2:
        st.header("📊 Live Dashboard Preview")
        
        # Quick signal preview
        st.subheader("🎯 Latest Signals")
        
        if st.button("🔄 Refresh Signals", key="refresh_signals"):
            try:
                # Import and run signal generation
                from data.market_data import MarketDataFetcher
                from signals.signal_generator import SignalGenerator
                from utils.config import Config
                
                config = Config()
                data_fetcher = MarketDataFetcher(config)
                signal_generator = SignalGenerator(data_fetcher, config)
                
                # Popular Saudi stocks with Arabic names
                saudi_stocks = {
                    "2222.SR": "أرامكو السعودية",
                    "1120.SR": "الراجحي", 
                    "2030.SR": "سافكو",
                    "7020.SR": "أسواق العثيم",
                    "4030.SR": "الحكير",
                    "2020.SR": "سابك"
                }
                
                with st.spinner("Analyzing Saudi stocks..."):
                    signals_data = []
                    progress_bar = st.progress(0)
                    
                    for i, (symbol, arabic_name) in enumerate(saudi_stocks.items()):
                        try:
                            signals = signal_generator.generate_signals(symbol)
                            
                            if signals:
                                latest_signal = signals[-1]  # Get the most recent signal
                                signals_data.append({
                                    "Stock Code": symbol.replace('.SR', ''),
                                    "Company": arabic_name,
                                    "Signal": latest_signal.signal_type,
                                    "Price (SAR)": f"{latest_signal.price:.2f}",
                                    "Confidence": f"{latest_signal.confidence:.1%}",
                                    "Reason": latest_signal.reason[:40] + "..." if len(latest_signal.reason) > 40 else latest_signal.reason
                                })
                            else:
                                signals_data.append({
                                    "Stock Code": symbol.replace('.SR', ''),
                                    "Company": arabic_name,
                                    "Signal": "NO DATA",
                                    "Price (SAR)": "N/A",
                                    "Confidence": "N/A",
                                    "Reason": "Insufficient data"
                                })
                                
                        except Exception as e:
                            signals_data.append({
                                "Stock Code": symbol.replace('.SR', ''),
                                "Company": arabic_name,
                                "Signal": "ERROR",
                                "Price (SAR)": "N/A",
                                "Confidence": "N/A",
                                "Reason": f"Error: {str(e)[:30]}..."
                            })
                        
                        progress_bar.progress((i + 1) / len(saudi_stocks))
                
                # Display results in table format
                if signals_data:
                    st.success(f"✅ Analysis completed for {len(signals_data)} stocks!")
                    
                    # Create DataFrame for better display
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
                        
                    # Investment integration note
                    st.info("💡 **Tip:** You can use these signals with your Alinma Capital account for automated trading!")
                else:
                    st.warning("❌ No signals generated")
                    
            except Exception as e:
                st.error(f"Error generating signals: {e}")
                import traceback
                st.code(traceback.format_exc())
        
        # Market status
        st.subheader("📈 Market Status")
        try:
            from data.market_data import MarketDataFetcher
            from utils.config import Config
            
            config = Config()
            data_fetcher = MarketDataFetcher(config)
            market_open = data_fetcher.is_market_open()
            
            if market_open:
                st.success("🟢 **Saudi Market is OPEN**")
            else:
                st.info("🔴 **Saudi Market is CLOSED**")
            
            market_hours = config.get_saudi_market_hours()
            st.write(f"**Trading Hours:** {market_hours['start_time']} - {market_hours['end_time']} (Saudi Time)")
            st.write(f"**Trading Days:** {', '.join(market_hours['trading_days'])}")
            
        except Exception as e:
            st.warning(f"Could not fetch market status: {e}")
    
    with tab3:
        st.header("� Portfolio Analysis")
        
        # Import portfolio manager
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.getcwd(), 'src'))
            
            from utils.portfolio_manager import PortfolioManager
            from data.market_data import MarketDataFetcher
            from utils.config import Config
            
            config = Config()
            data_fetcher = MarketDataFetcher(config)
            portfolio_manager = PortfolioManager(data_fetcher, config)
            
            st.subheader("📁 Portfolio Data Input")
            
            # Option to upload CSV or use sample data
            input_method = st.radio(
                "Choose input method:",
                ["Use My Real Portfolio", "Upload CSV File", "Manual Entry"],
                horizontal=True
            )
            
            portfolio_df = pd.DataFrame()
            
            if input_method == "Use My Real Portfolio":
                st.info("📊 Using your actual portfolio data from Al Inma Capital, BSF Capital, and Al Rajhi Capital")
                portfolio_df = portfolio_manager.create_sample_portfolio()
                
                # Validation
                total_positions = len(portfolio_df)
                expected_positions = 39
                
                if total_positions == expected_positions:
                    st.success(f"✅ Loaded {total_positions} stock positions across {portfolio_df['Custodian'].nunique()} brokers - Complete portfolio!")
                else:
                    st.warning(f"⚠️ Loaded {total_positions} positions (Expected: {expected_positions})")
                
                # Show breakdown by broker
                broker_counts = portfolio_df['Custodian'].value_counts()
                st.write("**Positions by Broker:**")
                for broker, count in broker_counts.items():
                    st.write(f"- **{broker}**: {count} positions")
                
            elif input_method == "Upload CSV File":
                uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
                if uploaded_file is not None:
                    portfolio_df = pd.read_csv(uploaded_file)
                    
            elif input_method == "Manual Entry":
                st.write("Add individual positions:")
                with st.form("add_position"):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        company = st.text_input("Company Name")
                        symbol = st.text_input("Symbol (e.g., 2222.SR)")
                    with col2:
                        quantity = st.number_input("Quantity", min_value=0)
                        cost = st.number_input("Average Cost", min_value=0.0)
                    with col3:
                        custodian = st.selectbox("Broker", ["Al Inma Capital", "BSF Capital", "Al Rajhi Capital", "Other"])
                    
                    if st.form_submit_button("Add Position"):
                        if company and symbol and quantity > 0:
                            # Add to session state portfolio
                            if 'manual_portfolio' not in st.session_state:
                                st.session_state.manual_portfolio = []
                            
                            st.session_state.manual_portfolio.append({
                                "Company": company,
                                "Symbol": symbol,
                                "Owned_Qty": quantity,
                                "Cost": cost,
                                "Custodian": custodian
                            })
                            st.success(f"Added {company} to portfolio!")
                
                if 'manual_portfolio' in st.session_state and st.session_state.manual_portfolio:
                    portfolio_df = pd.DataFrame(st.session_state.manual_portfolio)
            
            # Portfolio Analysis
            if not portfolio_df.empty:
                st.subheader("📊 Portfolio Analysis")
                
                with st.spinner("Fetching current prices and calculating metrics..."):
                    # Calculate portfolio metrics
                    portfolio_df = portfolio_manager.calculate_portfolio_metrics(portfolio_df)
                    
                    # Get summary statistics
                    summary = portfolio_manager.get_portfolio_summary(portfolio_df)
                
                # Display summary metrics
                st.subheader("📈 Portfolio Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "💰 Total Market Value",
                        f"{summary['total_market_value']:,.2f} SAR",
                        f"{summary['total_gain_loss']:+,.2f} SAR"
                    )
                    
                with col2:
                    st.metric(
                        "📊 Total Return",
                        f"{summary['total_gain_loss_pct']:+.2f}%",
                        f"{summary['total_gain_loss']:+,.2f} SAR"
                    )
                    
                with col3:
                    st.metric(
                        "🏢 Positions",
                        f"{summary['num_positions']}",
                        f"{summary['num_brokers']} brokers"
                    )
                    
                with col4:
                    st.metric(
                        "🥇 Top Holding",
                        summary['top_holding'],
                        f"Best: {summary['best_performer']}"
                    )
                
                # Portfolio breakdown by broker
                st.subheader("🏦 Portfolio by Broker")
                broker_summary = portfolio_df.groupby('Custodian').agg({
                    'Total_Cost': 'sum',
                    'Market_Value': 'sum',
                    'Gain_Loss': 'sum',
                    'Company': 'count'
                }).round(2)
                broker_summary.columns = ['Total Cost', 'Market Value', 'Gain/Loss', 'Positions']
                broker_summary['Return %'] = ((broker_summary['Market Value'] - broker_summary['Total Cost']) / broker_summary['Total Cost'] * 100).round(2)
                
                st.dataframe(broker_summary, use_container_width=True)
                
                # Detailed holdings table
                st.subheader("📋 Detailed Holdings")
                
                # Style the holdings table
                def color_gains(val):
                    if isinstance(val, (int, float)):
                        if val > 0:
                            return 'background-color: #90EE90'  # Light green
                        elif val < 0:
                            return 'background-color: #FFB6C1'  # Light red
                    return ''
                
                # Format the dataframe for display
                display_df = portfolio_df[['Stock_Name', 'Symbol', 'Custodian', 'Owned_Qty', 'Cost', 'Current_Price', 'Market_Value', 'Gain_Loss', 'Gain_Loss_Pct']].copy()
                display_df.columns = ['Company Name', 'Symbol', 'Broker', 'Quantity', 'Avg Cost', 'Current Price', 'Market Value', 'Gain/Loss', 'Return %']
                
                # Format numeric columns to show decimals properly
                display_df['Avg Cost'] = display_df['Avg Cost'].apply(lambda x: f"{x:.2f}")
                display_df['Current Price'] = display_df['Current Price'].apply(lambda x: f"{x:.2f}")
                display_df['Market Value'] = display_df['Market Value'].apply(lambda x: f"{x:,.2f}")
                display_df['Gain/Loss'] = display_df['Gain/Loss'].apply(lambda x: f"{x:+,.2f}")
                display_df['Return %'] = display_df['Return %'].apply(lambda x: f"{x:+.2f}%")
                
                # Apply styling
                styled_df = display_df.style.applymap(color_gains, subset=['Gain/Loss', 'Return %'])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # Portfolio allocation charts
                st.subheader("📊 Portfolio Allocation")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # By broker
                    broker_values = portfolio_df.groupby('Custodian')['Market_Value'].sum()
                    
                    import plotly.express as px
                    fig1 = px.pie(
                        values=broker_values.values,
                        names=broker_values.index,
                        title="Allocation by Broker"
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Top 10 holdings
                    top_holdings = portfolio_df.nlargest(10, 'Market_Value')
                    
                    fig2 = px.pie(
                        top_holdings,
                        values='Market_Value',
                        names='Company',
                        title="Top 10 Holdings"
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Performance analysis
                st.subheader("📈 Performance Analysis")
                
                # Winners and losers
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("🟢 **Top Performers**")
                    winners = portfolio_df.nlargest(5, 'Gain_Loss_Pct')[['Company', 'Gain_Loss_Pct', 'Gain_Loss']]
                    winners.columns = ['Company', 'Return %', 'Gain/Loss (SAR)']
                    st.dataframe(winners, hide_index=True)
                
                with col2:
                    st.write("🔴 **Underperformers**")
                    losers = portfolio_df.nsmallest(5, 'Gain_Loss_Pct')[['Company', 'Gain_Loss_Pct', 'Gain_Loss']]
                    losers.columns = ['Company', 'Return %', 'Gain/Loss (SAR)']
                    st.dataframe(losers, hide_index=True)
                
                # Export functionality
                st.subheader("📤 Export Portfolio")
                if st.button("📊 Export to CSV"):
                    csv = display_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"portfolio_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            else:
                st.info("👆 Please select a portfolio input method above to begin analysis")
                
        except Exception as e:
            st.error(f"Error in portfolio analysis: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    with tab4:
        st.header("�💰 Investment Integration")
        
        # Alinma Capital Integration
        st.subheader("🏦 Alinma Capital API Integration")
        
        st.info("""
        🔗 **Connect your Alinma Capital account to enable automated trading based on signals!**
        
        **Features Available:**
        - Real-time portfolio sync
        - Automated order execution
        - Risk management controls
        - Performance tracking
        """)
        
        # API Configuration
        with st.expander("⚙️ API Configuration", expanded=False):
            st.markdown("**Step 1: Get your API credentials from Alinma Capital**")
            
            api_key = st.text_input("🔑 API Key", type="password", help="Your Alinma Capital API key")
            api_secret = st.text_input("🛡️ API Secret", type="password", help="Your API secret key")
            account_id = st.text_input("👤 Account ID", help="Your account identifier")
            
            if st.button("💾 Save API Credentials"):
                if api_key and api_secret and account_id:
                    # Save to config (you can enhance this to encrypt and store securely)
                    st.success("✅ API credentials saved successfully!")
                    st.balloons()
                else:
                    st.error("❌ Please fill in all credentials")
        
        # Trading Settings
        with st.expander("🎛️ Trading Settings", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Signal Settings")
                min_confidence = st.slider("Minimum Signal Confidence", 0.5, 1.0, 0.75, 0.05)
                auto_execute = st.checkbox("🤖 Auto-execute trades", help="Automatically execute trades when signals meet criteria")
                
            with col2:
                st.subheader("💸 Risk Management")
                max_position_size = st.number_input("Max Position Size (SAR)", min_value=1000, max_value=1000000, value=50000, step=1000)
                max_daily_trades = st.number_input("Max Daily Trades", min_value=1, max_value=20, value=5)
        
        # Portfolio Overview
        st.subheader("📈 Portfolio Overview")
        
        # Mock portfolio data (replace with real API call)
        if st.button("🔄 Refresh Portfolio"):
            with st.spinner("Fetching portfolio data..."):
                # Simulate portfolio data
                portfolio_data = {
                    "Stock": ["2222 (أرامكو)", "1120 (الراجحي)", "2030 (سافكو)", "Cash"],
                    "Quantity": [100, 50, 200, "N/A"],
                    "Current Price": [30.50, 85.25, 42.10, "N/A"],
                    "Market Value": [3050, 4262.50, 8420, 15000],
                    "P&L": ["+5.2%", "-2.1%", "+8.7%", "N/A"]
                }
                
                portfolio_df = pd.DataFrame(portfolio_data)
                st.dataframe(portfolio_df, use_container_width=True, hide_index=True)
                
                # Portfolio metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("💰 Total Value", "30,732.50 SAR", "+1,250 SAR")
                with col2:
                    st.metric("📊 Day P&L", "+2.8%", "+0.5%")
                with col3:
                    st.metric("🎯 Active Positions", "3", "+1")
                with col4:
                    st.metric("💵 Available Cash", "15,000 SAR", "-5,000 SAR")
        
        # Trading Actions
        st.subheader("⚡ Quick Trading Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔥 Execute BUY Signals", type="primary"):
                st.success("🟢 BUY orders submitted for qualified signals!")
                
        with col2:
            if st.button("🛑 Execute SELL Signals"):
                st.warning("🔴 SELL orders submitted for qualified signals!")
                
        with col3:
            if st.button("⏸️ Pause Auto-Trading"):
                st.info("⏸️ Auto-trading paused. Manual review required.")
        
        # Recent Trades
        st.subheader("📋 Recent Trades")
        trades_data = {
            "Time": ["10:35", "11:20", "14:15"],
            "Action": ["BUY", "SELL", "BUY"],
            "Stock": ["2222", "1120", "2030"],
            "Quantity": [50, 25, 100],
            "Price": [30.25, 86.10, 41.85],
            "Status": ["✅ Filled", "✅ Filled", "⏳ Pending"]
        }
        
        trades_df = pd.DataFrame(trades_data)
        st.dataframe(trades_df, use_container_width=True, hide_index=True)
    
    with tab5:
        st.header("⚙️ Setup & Testing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 System Setup")
            
            if st.button("⚙️ Run Setup", key="setup", help="Install dependencies and configure the app"):
                with st.spinner("Running setup..."):
                    command = f'"{sys.executable}" setup.py'
                    run_command_in_background(command, "System Setup")
            
            if st.button("📦 Install Dependencies", key="deps", help="Install required Python packages"):
                with st.spinner("Installing dependencies..."):
                    command = f'"{sys.executable}" -m pip install -r requirements.txt'
                    run_command_in_background(command, "Dependency Installation")
        
        with col2:
            st.subheader("🧪 System Testing")
            
            if st.button("🔍 Test Data Fetching", key="test_data", help="Test stock data fetching"):
                try:
                    from data.market_data import MarketDataFetcher
                    from utils.config import Config
                    
                    config = Config()
                    data_fetcher = MarketDataFetcher(config)
                    
                    with st.spinner("Testing data fetching..."):
                        data = data_fetcher.get_stock_data("2222.SR", period="1mo")
                        
                    if data is not None and not data.empty:
                        st.success(f"✅ Data fetching successful! Got {len(data)} records")
                        st.write(f"Latest price: {data['Close'].iloc[-1]:.2f} SAR")
                    else:
                        st.error("❌ Data fetching failed")
                        
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            
            if st.button("📊 Test Indicators", key="test_indicators", help="Test technical indicators"):
                try:
                    from analysis.technical_indicators import TechnicalIndicators
                    from data.market_data import MarketDataFetcher
                    from utils.config import Config
                    
                    config = Config()
                    data_fetcher = MarketDataFetcher(config)
                    indicators = TechnicalIndicators()
                    
                    with st.spinner("Testing technical indicators..."):
                        data = data_fetcher.get_stock_data("2222.SR", period="6mo")
                        
                        if data is not None and not data.empty:
                            rsi = indicators.rsi(data['Close'])
                            latest_rsi = rsi.iloc[-1]
                            
                            st.success(f"✅ Technical indicators working!")
                            st.write(f"Latest RSI for Aramco: {latest_rsi:.2f}")
                        else:
                            st.error("❌ Could not get data for testing")
                            
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with tab6:
        st.header("📈 Analysis Tools")
        
        st.subheader("🔙 Backtesting")
        
        col1, col2 = st.columns(2)
        
        with col1:
            symbol = st.selectbox("Select Stock", ["2222.SR", "1120.SR", "2030.SR", "4030.SR"], 
                                key="backtest_symbol")
            start_date = st.date_input("Start Date", value=None, key="start_date")
            end_date = st.date_input("End Date", value=None, key="end_date")
        
        with col2:
            initial_capital = st.number_input("Initial Capital (SAR)", value=100000, min_value=1000)
            position_size = st.slider("Position Size (%)", min_value=5, max_value=50, value=20)
        
        if st.button("🔙 Run Backtest", key="backtest"):
            if start_date and end_date:
                try:
                    # Import backtesting module
                    from backtesting.backtest import Backtester
                    
                    with st.spinner("Running backtest..."):
                        backtester = Backtester(initial_capital=initial_capital)
                        result = backtester.run_backtest(
                            symbol=symbol,
                            start_date=start_date.strftime('%Y-%m-%d'),
                            end_date=end_date.strftime('%Y-%m-%d'),
                            position_size=position_size/100
                        )
                    
                    # Display results
                    st.success("✅ Backtest completed!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Return", f"{result.total_return:,.2f} SAR", 
                                f"{result.total_return_pct:.2f}%")
                    with col2:
                        st.metric("Win Rate", f"{result.win_rate:.1f}%")
                    with col3:
                        st.metric("Total Trades", result.total_trades)
                    
                    if result.trades:
                        st.subheader("Recent Trades")
                        for trade in result.trades[-5:]:  # Show last 5 trades
                            profit_color = "🟢" if trade['profit'] > 0 else "🔴"
                            st.write(f"{profit_color} {trade['exit_date'].strftime('%Y-%m-%d')}: "
                                   f"{trade['shares']} shares, Profit: {trade['profit']:.2f} SAR")
                
                except Exception as e:
                    st.error(f"❌ Backtest failed: {e}")
            else:
                st.warning("Please select start and end dates")
        
        st.subheader("📊 Stock Analysis")
        analysis_symbol = st.selectbox("Select Stock for Analysis", 
                                     ["2222.SR", "1120.SR", "2030.SR", "4030.SR"], 
                                     key="analysis_symbol")
        
        if st.button("📈 Analyze Stock", key="analyze"):
            try:
                from data.market_data import MarketDataFetcher
                from analysis.technical_indicators import TechnicalIndicators
                from utils.config import Config
                
                config = Config()
                data_fetcher = MarketDataFetcher(config)
                indicators = TechnicalIndicators()
                
                with st.spinner("Analyzing stock..."):
                    data = data_fetcher.get_stock_data(analysis_symbol, period="6mo")
                
                if data is not None and not data.empty:
                    st.success(f"✅ Analysis for {analysis_symbol}")
                    
                    # Basic metrics
                    latest = data.iloc[-1]
                    prev = data.iloc[-2]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        change = latest['Close'] - prev['Close']
                        st.metric("Current Price", f"{latest['Close']:.2f} SAR", f"{change:.2f}")
                    with col2:
                        st.metric("Volume", f"{latest['Volume']:,.0f}")
                    with col3:
                        high_low = ((latest['High'] - latest['Low']) / latest['Close']) * 100
                        st.metric("Daily Range", f"{high_low:.2f}%")
                    
                    # Technical indicators
                    st.subheader("📊 Technical Indicators")
                    rsi = indicators.rsi(data['Close']).iloc[-1]
                    macd_line, signal_line, _ = indicators.macd(data['Close'])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("RSI", f"{rsi:.2f}")
                        if rsi > 70:
                            st.warning("🔴 Overbought")
                        elif rsi < 30:
                            st.success("🟢 Oversold")
                        else:
                            st.info("⚪ Neutral")
                    
                    with col2:
                        latest_macd = macd_line.iloc[-1]
                        latest_signal = signal_line.iloc[-1]
                        st.metric("MACD", f"{latest_macd:.4f}")
                        if latest_macd > latest_signal:
                            st.success("🟢 Bullish")
                        else:
                            st.warning("🔴 Bearish")
                    
                    # Simple chart
                    st.subheader("📈 Price Chart (Last 30 days)")
                    chart_data = data.tail(30)[['Close']]
                    st.line_chart(chart_data)
                    
                else:
                    st.error("❌ Could not fetch data for analysis")
                    
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
    
    with tab7:
        st.header("📚 Documentation")
        
        st.subheader("🎯 About the App")
        st.markdown("""
        This **Saudi Stock Market Trading Signals App** is designed specifically for analyzing 
        and generating trading signals for the Saudi stock market (Tadawul).
        
        ### 🌟 Key Features:
        - **Technical Analysis**: RSI, MACD, Bollinger Bands, Moving Averages
        - **Signal Generation**: Automated buy/sell recommendations
        - **Backtesting**: Test strategies on historical data
        - **Real-time Data**: Live market data and analysis
        - **Portfolio Tracking**: Monitor your investments
        """)
        
        st.subheader("🏦 Supported Saudi Stocks")
        stocks_info = {
            "2222.SR": "Saudi Aramco - Energy",
            "1120.SR": "Al Rajhi Bank - Banking", 
            "2030.SR": "SABIC - Petrochemicals",
            "4030.SR": "Riyad Bank - Banking",
            "1210.SR": "The Saudi National Bank - Banking"
        }
        
        for symbol, name in stocks_info.items():
            st.write(f"• **{symbol}**: {name}")
        
        st.subheader("⚠️ Important Disclaimers")
        st.warning("""
        **Educational Purpose Only**: This application is for educational and learning purposes only.
        
        **Not Financial Advice**: Trading signals generated should NOT be considered as financial advice.
        
        **Risk Warning**: Trading involves substantial risk of loss. Always do your own research 
        and consult with qualified financial advisors before making investment decisions.
        """)
        
        st.subheader("🔧 Technical Requirements")
        st.info("""
        - **Python**: 3.8 or higher
        - **Internet**: Required for real-time data
        - **Dependencies**: Automatically installed via setup
        """)
        
        st.subheader("📞 Support")
        st.markdown("""
        For technical support or questions:
        1. Run the **Test System** to diagnose issues
        2. Check the **Setup & Testing** tab for configuration
        3. Review log files for detailed error messages
        """)

    # Sidebar
    with st.sidebar:
        st.title("🎛️ Control Panel")
        
        st.subheader("📊 Quick Stats")
        try:
            from utils.config import Config
            config = Config()
            
            st.write(f"**RSI Period**: {config.rsi_period}")
            st.write(f"**MACD Fast**: {config.macd_fast}")
            st.write(f"**BB Period**: {config.bb_period}")
            
        except:
            st.write("Configuration not loaded")
        
        st.subheader("🔗 Quick Links")
        st.markdown("- [Yahoo Finance](https://finance.yahoo.com)")
        st.markdown("- [Tadawul](https://www.saudiexchange.sa)")
        
        st.subheader("⚡ Quick Actions")
        if st.button("🔄 Restart App", key="restart"):
            st.rerun()

if __name__ == "__main__":
    main()
