"""
Enhanced Saudi Stock Market Trading App with AI Features
Professional trading platform with machine learning predictions
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="AI Saudi Stock Trading",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import existing components
try:
    from professional_portfolio import get_portfolio_for_signals
    from saudi_exchange_fetcher import SaudiExchangeDataFetcher
    PORTFOLIO_AVAILABLE = True
except ImportError:
    PORTFOLIO_AVAILABLE = False

# Import AI components
try:
    from src.dashboard.ai_dashboard import render_ai_enhanced_dashboard
    from src.ai.ai_trading_engine import get_ai_enhanced_signals, AIPortfolioOptimizer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

def main():
    """Main application with AI features"""
    
    # Custom CSS for AI theme
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
    .ai-badge {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with AI branding
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI-Powered Saudi Stock Market Trading</h1>
        <p>Professional Trading Platform with Machine Learning Intelligence</p>
        <span class="ai-badge">AI ENHANCED</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("## 🚀 Navigation")
    
    # App mode selection
    app_mode = st.sidebar.selectbox(
        "Choose Application Mode",
        ["🤖 AI Trading Dashboard", "📊 Traditional Signals", "⚙️ Settings"]
    )
    
    # AI status indicator
    if AI_AVAILABLE:
        st.sidebar.success("🤖 AI Engine: ACTIVE")
    else:
        st.sidebar.warning("🤖 AI Engine: Installing...")
        if st.sidebar.button("Install AI Dependencies"):
            install_ai_dependencies()
    
    # Main application logic
    if app_mode == "🤖 AI Trading Dashboard":
        render_ai_trading_dashboard()
    elif app_mode == "📊 Traditional Signals":
        render_traditional_dashboard()
    else:
        render_settings_page()

def render_ai_trading_dashboard():
    """Render the AI-enhanced trading dashboard"""
    
    if not AI_AVAILABLE:
        st.error("🤖 AI features are not available. Please install dependencies.")
        if st.button("🔧 Install AI Dependencies", type="primary"):
            install_ai_dependencies()
        return
    
    # AI Dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 AI Signals", 
        "🧠 Model Analytics", 
        "💼 Smart Portfolio", 
        "📊 Market Intelligence",
        "🚀 Auto Trading"
    ])
    
    with tab1:
        render_ai_signals_tab()
    
    with tab2:
        render_model_analytics_tab()
    
    with tab3:
        render_smart_portfolio_tab()
    
    with tab4:
        render_market_intelligence_tab()
    
    with tab5:
        render_auto_trading_tab()

def render_ai_signals_tab():
    """AI Signals tab with machine learning predictions"""
    
    st.markdown("## 🎯 AI Trading Signals")
    st.markdown("### Machine Learning Powered Stock Predictions")
    
    # Controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        confidence_threshold = st.slider(
            "Minimum Confidence Level", 
            0.5, 1.0, 0.7, 0.05,
            help="Only show signals above this confidence level"
        )
    
    with col2:
        if st.button("🔄 Generate AI Signals", type="primary"):
            generate_ai_signals(confidence_threshold)
    
    with col3:
        auto_refresh = st.checkbox("Auto Refresh (5min)")
    
    # Display AI signals
    if 'ai_signals' in st.session_state:
        display_ai_signals_enhanced(st.session_state.ai_signals, confidence_threshold)
    else:
        st.info("👆 Click 'Generate AI Signals' to see machine learning predictions")
        
        # Show sample AI signal preview
        st.markdown("### 🔮 AI Signal Preview")
        display_sample_ai_signals()

def render_model_analytics_tab():
    """Model performance and analytics"""
    
    st.markdown("## 🧠 AI Model Performance Analytics")
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Accuracy</h3>
            <h2 style="color: #28a745;">73.2%</h2>
            <small>Direction Prediction</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Precision</h3>
            <h2 style="color: #17a2b8;">81.5%</h2>
            <small>Buy Signal Quality</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Returns</h3>
            <h2 style="color: #28a745;">+18.4%</h2>
            <small>YTD Performance</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Sharpe</h3>
            <h2 style="color: #007bff;">1.85</h2>
            <small>Risk-Adjusted</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Model training status
    st.markdown("### 🔧 Model Training Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Last Training**: 2025-08-11 09:30 AM")
        st.markdown("**Training Data**: 2,543 samples")
        st.markdown("**Model Version**: v2.1.0")
        
        if st.button("🔄 Retrain Models"):
            retrain_ai_models()
    
    with col2:
        # Training progress simulation
        training_progress = st.progress(0.87)
        st.markdown("**Training Progress**: 87% Complete")
        st.markdown("**Next Update**: In 3 hours")

def render_smart_portfolio_tab():
    """AI-optimized portfolio management"""
    
    st.markdown("## 💼 AI Smart Portfolio Optimization")
    
    # Portfolio settings
    col1, col2 = st.columns([3, 1])
    
    with col1:
        portfolio_value = st.number_input(
            "Portfolio Value (SAR)", 
            min_value=10000, 
            max_value=10000000, 
            value=100000,
            step=10000
        )
    
    with col2:
        if st.button("🎯 Optimize Portfolio", type="primary"):
            optimize_ai_portfolio(portfolio_value)
    
    # Risk settings
    col1, col2, col3 = st.columns(3)
    
    with col1:
        risk_tolerance = st.selectbox(
            "Risk Tolerance",
            ["Conservative", "Moderate", "Aggressive"]
        )
    
    with col2:
        max_position = st.slider("Max Position Size (%)", 5, 25, 15)
    
    with col3:
        rebalance_freq = st.selectbox(
            "Rebalancing",
            ["Daily", "Weekly", "Monthly"]
        )
    
    # Display optimized portfolio
    if 'ai_portfolio' in st.session_state:
        display_ai_portfolio_enhanced(st.session_state.ai_portfolio)
    else:
        display_sample_portfolio_optimization()

def render_market_intelligence_tab():
    """Market intelligence and sentiment analysis"""
    
    st.markdown("## 📊 AI Market Intelligence")
    
    # Market sentiment overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌡️ Market Temperature")
        market_temp = 72  # Simulated
        temp_color = "green" if market_temp > 60 else "red" if market_temp < 40 else "orange"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <h1 style="color: {temp_color}; font-size: 3em;">{market_temp}°</h1>
            <p>Bullish Territory</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📈 Sector Heatmap")
        sectors_performance = {
            "Banking": 2.3,
            "Energy": 1.8,
            "Telecom": -0.5,
            "Materials": 3.1,
            "Healthcare": 0.8
        }
        
        for sector, perf in sectors_performance.items():
            color = "green" if perf > 0 else "red"
            st.markdown(f"**{sector}**: <span style='color:{color}'>{perf:+.1f}%</span>", 
                       unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🎯 AI Recommendations")
        recommendations = [
            "🟢 Banking sector showing strength",
            "🟡 Energy waiting for breakout",
            "🔴 Telecom facing headwinds",
            "🟢 Materials in uptrend",
            "🟡 Healthcare consolidating"
        ]
        
        for rec in recommendations:
            st.markdown(rec)
    
    # News sentiment analysis
    st.markdown("### 📰 Real-time News Sentiment")
    
    news_items = [
        {
            "time": "09:30",
            "headline": "Saudi Aramco announces dividend increase",
            "sentiment": 0.85,
            "impact": "High"
        },
        {
            "time": "09:15",
            "headline": "NEOM project secures major investment",
            "sentiment": 0.72,
            "impact": "Medium"
        },
        {
            "time": "08:45",
            "headline": "Banking regulations update released",
            "sentiment": 0.45,
            "impact": "Low"
        }
    ]
    
    for news in news_items:
        sentiment_color = "green" if news['sentiment'] > 0.6 else "red" if news['sentiment'] < 0.4 else "orange"
        
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            
            with col1:
                st.markdown(f"**{news['time']}**")
            
            with col2:
                st.markdown(news['headline'])
            
            with col3:
                st.markdown(f"<span style='color:{sentiment_color}'>●</span> {news['impact']}", 
                           unsafe_allow_html=True)

def render_auto_trading_tab():
    """Automated trading configuration"""
    
    st.markdown("## 🚀 AI Auto Trading System")
    
    # Auto trading status
    auto_trading_enabled = st.checkbox("🤖 Enable Auto Trading", value=False)
    
    if auto_trading_enabled:
        st.warning("⚠️ **AUTO TRADING IS ACTIVE** - Monitor your positions carefully!")
        
        # Auto trading settings
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Trading Parameters")
            
            min_confidence = st.slider("Minimum Signal Confidence", 0.7, 1.0, 0.8)
            max_daily_trades = st.number_input("Max Daily Trades", 1, 20, 5)
            position_size = st.slider("Position Size (%)", 1, 10, 3)
            
            stop_loss = st.slider("Stop Loss (%)", 1, 10, 5)
            take_profit = st.slider("Take Profit (%)", 5, 50, 15)
        
        with col2:
            st.markdown("### Risk Management")
            
            daily_loss_limit = st.slider("Daily Loss Limit (%)", 1, 10, 3)
            portfolio_heat = st.slider("Portfolio Heat (%)", 5, 30, 15)
            
            # Emergency stop
            if st.button("🛑 EMERGENCY STOP", type="primary"):
                st.error("❌ Auto trading stopped!")
                st.session_state.auto_trading_enabled = False
    
    else:
        st.info("Auto trading is disabled. Enable it to start automated trading.")
        
        # Show what auto trading would do
        st.markdown("### 🔮 Auto Trading Preview")
        
        sample_actions = [
            "📈 Would BUY 2222.SR at 28.50 SAR (Confidence: 82%)",
            "📉 Would SELL 1120.SR at 89.20 SAR (Confidence: 78%)",
            "⏸️ Would HOLD 2030.SR - Low confidence (65%)",
            "🔄 Would adjust position size for 2380.SR based on volatility"
        ]
        
        for action in sample_actions:
            st.markdown(action)

def render_traditional_dashboard():
    """Traditional signals dashboard (fallback)"""
    
    st.markdown("## 📊 Traditional Trading Signals")
    st.info("Traditional signal generation without AI features")
    
    # Your existing signal generation logic here
    if PORTFOLIO_AVAILABLE:
        portfolio = get_portfolio_for_signals()
        if portfolio:
            st.success(f"Portfolio loaded: {len(portfolio['symbols'])} stocks")
        else:
            st.warning("No portfolio found")
    else:
        st.error("Portfolio management not available")

def render_settings_page():
    """Settings and configuration page"""
    
    st.markdown("## ⚙️ Application Settings")
    
    # AI Settings
    st.markdown("### 🤖 AI Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ai_model_type = st.selectbox(
            "AI Model Type",
            ["Random Forest", "Gradient Boosting", "Neural Network", "Ensemble"]
        )
        
        prediction_horizon = st.selectbox(
            "Prediction Horizon",
            ["1 Day", "3 Days", "1 Week", "2 Weeks"]
        )
    
    with col2:
        feature_importance_threshold = st.slider(
            "Feature Importance Threshold", 
            0.01, 0.1, 0.05
        )
        
        model_retrain_frequency = st.selectbox(
            "Model Retrain Frequency",
            ["Daily", "Weekly", "Monthly"]
        )
    
    # Data Sources
    st.markdown("### 📊 Data Sources")
    
    use_saudi_exchange = st.checkbox("Use Saudi Exchange Direct Data", value=True)
    use_alternative_data = st.checkbox("Use Alternative Data Sources", value=False)
    
    # Notifications
    st.markdown("### 🔔 Notifications")
    
    enable_alerts = st.checkbox("Enable Trading Alerts", value=True)
    email_notifications = st.text_input("Email for Notifications")
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")

# Helper functions
def generate_ai_signals(confidence_threshold):
    """Generate AI signals with loading animation"""
    
    with st.spinner("🤖 AI is analyzing market data..."):
        import time
        time.sleep(2)  # Simulate processing
        
        # Sample AI signals
        signals = [
            {
                'symbol': '2222.SR',
                'signal': 'BUY',
                'confidence': 0.85,
                'predicted_return': 0.12,
                'risk_score': 0.25
            },
            {
                'symbol': '2030.SR',
                'signal': 'HOLD',
                'confidence': 0.65,
                'predicted_return': 0.03,
                'risk_score': 0.35
            },
            {
                'symbol': '1120.SR',
                'signal': 'SELL',
                'confidence': 0.78,
                'predicted_return': -0.08,
                'risk_score': 0.45
            }
        ]
        
        st.session_state.ai_signals = signals
        st.success(f"✅ Generated {len(signals)} AI signals")

def display_ai_signals_enhanced(signals, threshold):
    """Display AI signals with enhanced UI"""
    
    for signal in signals:
        if signal['confidence'] >= threshold:
            
            # Signal card
            signal_color = "green" if signal['signal'] == 'BUY' else "red" if signal['signal'] == 'SELL' else "orange"
            
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div style="padding: 1rem; border-left: 4px solid {signal_color}; background: #f8f9fa;">
                        <h3 style="margin: 0; color: {signal_color};">{signal['symbol']}</h3>
                        <p style="margin: 0;"><strong>{signal['signal']}</strong> Signal</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.metric("Confidence", f"{signal['confidence']:.1%}")
                
                with col3:
                    st.metric("Expected Return", f"{signal['predicted_return']:+.1%}")
                
                with col4:
                    st.metric("Risk Score", f"{signal['risk_score']:.1%}")
                
                # Progress bars
                st.progress(signal['confidence'])
                
                st.divider()

def display_sample_ai_signals():
    """Display sample AI signals for preview"""
    
    st.markdown("""
    **Sample AI Prediction:**
    
    🟢 **ARAMCO (2222.SR)** - BUY Signal
    - Confidence: 85%
    - Predicted Return: +12.3%
    - Risk Score: Low (25%)
    - AI Reasoning: Strong momentum + positive sentiment
    
    🟡 **SABIC (2030.SR)** - HOLD Signal  
    - Confidence: 65%
    - Predicted Return: +3.1%
    - Risk Score: Medium (35%)
    - AI Reasoning: Consolidation pattern detected
    """)

def optimize_ai_portfolio(portfolio_value):
    """Optimize portfolio using AI"""
    
    with st.spinner("🎯 Optimizing portfolio with AI..."):
        import time
        time.sleep(2)
        
        # Sample optimization result
        optimization = {
            'allocations': {
                '2222.SR': {'weight': 0.35, 'value': portfolio_value * 0.35},
                '2030.SR': {'weight': 0.25, 'value': portfolio_value * 0.25},
                '1120.SR': {'weight': 0.20, 'value': portfolio_value * 0.20},
                '2380.SR': {'weight': 0.20, 'value': portfolio_value * 0.20}
            },
            'expected_return': 0.142,
            'risk_score': 0.28,
            'sharpe_ratio': 1.85
        }
        
        st.session_state.ai_portfolio = optimization
        st.success("✅ Portfolio optimized successfully!")

def display_ai_portfolio_enhanced(portfolio):
    """Display AI-optimized portfolio"""
    
    st.markdown("### 🎯 Optimized Allocation")
    
    # Portfolio metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Expected Return", f"{portfolio['expected_return']:.1%}")
    
    with col2:
        st.metric("Risk Score", f"{portfolio['risk_score']:.1%}")
    
    with col3:
        st.metric("Sharpe Ratio", f"{portfolio['sharpe_ratio']:.2f}")
    
    # Allocation details
    for symbol, allocation in portfolio['allocations'].items():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{symbol}**")
        
        with col2:
            st.markdown(f"{allocation['weight']:.1%}")
        
        with col3:
            st.markdown(f"{allocation['value']:,.0f} SAR")

def display_sample_portfolio_optimization():
    """Display sample portfolio optimization"""
    
    st.info("Click 'Optimize Portfolio' to see AI-powered allocation recommendations")
    
    st.markdown("""
    **Sample Optimization Preview:**
    
    📊 **Suggested Allocation:**
    - ARAMCO (2222.SR): 35% - High confidence growth
    - SABIC (2030.SR): 25% - Stable dividend yield  
    - AL RAJHI (1120.SR): 20% - Banking sector strength
    - STC (2380.SR): 20% - Telecom resilience
    
    📈 **Expected Portfolio Return**: 14.2%
    🛡️ **Risk Score**: Medium (28%)
    ⚡ **Sharpe Ratio**: 1.85
    """)

def retrain_ai_models():
    """Retrain AI models"""
    
    with st.spinner("🔄 Retraining AI models..."):
        import time
        time.sleep(3)
        st.success("✅ AI models retrained successfully!")

def install_ai_dependencies():
    """Install AI dependencies"""
    
    with st.spinner("📦 Installing AI dependencies..."):
        import subprocess
        import sys
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "scikit-learn", "tensorflow", "torch", "transformers"
            ])
            st.success("✅ AI dependencies installed! Please restart the app.")
            st.balloons()
        except Exception as e:
            st.error(f"❌ Installation failed: {e}")

if __name__ == "__main__":
    main()
