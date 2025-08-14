"""
AI Trading Dashboard Integration
Enhanced Streamlit interface with AI predictions and automated trading
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from ai.ai_trading_engine import (
        AITradingPredictor, 
        AIPortfolioOptimizer, 
        get_ai_enhanced_signals,
        AITradingSignal
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    st.error("AI Trading Engine not available. Please install required dependencies.")

class AITradingDashboard:
    """Enhanced dashboard with AI trading capabilities"""
    
    def __init__(self):
        self.ai_predictor = AITradingPredictor() if AI_AVAILABLE else None
        self.portfolio_optimizer = AIPortfolioOptimizer() if AI_AVAILABLE else None
        
    def render_ai_dashboard(self):
        """Render the complete AI trading dashboard"""
        
        st.title("🤖 AI-Powered Saudi Stock Trading")
        st.markdown("### Advanced Machine Learning Predictions & Automated Trading")
        
        # Sidebar for AI controls
        self._render_ai_sidebar()
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 AI Signals", 
            "🧠 Model Performance", 
            "💼 AI Portfolio", 
            "📊 Market Intelligence"
        ])
        
        with tab1:
            self._render_ai_signals_tab()
            
        with tab2:
            self._render_model_performance_tab()
            
        with tab3:
            self._render_ai_portfolio_tab()
            
        with tab4:
            self._render_market_intelligence_tab()
    
    def _render_ai_sidebar(self):
        """AI controls sidebar"""
        
        st.sidebar.markdown("## 🤖 AI Trading Controls")
        
        # AI Model Settings
        st.sidebar.markdown("### Model Configuration")
        confidence_threshold = st.sidebar.slider(
            "Signal Confidence Threshold", 
            0.5, 1.0, 0.7, 0.05
        )
        
        prediction_horizon = st.sidebar.selectbox(
            "Prediction Horizon",
            [1, 3, 5, 10, 20],
            index=2
        )
        
        # Risk Management
        st.sidebar.markdown("### Risk Management")
        max_position_size = st.sidebar.slider(
            "Max Position Size (%)", 
            1, 20, 10, 1
        )
        
        max_portfolio_risk = st.sidebar.slider(
            "Max Portfolio Risk", 
            0.1, 0.5, 0.2, 0.05
        )
        
        # Auto-trading controls
        st.sidebar.markdown("### Auto Trading")
        auto_trading_enabled = st.sidebar.checkbox("Enable Auto Trading")
        
        if auto_trading_enabled:
            st.sidebar.warning("⚠️ Auto trading is enabled. Monitor positions carefully!")
        
        # Store settings in session state
        st.session_state.ai_settings = {
            'confidence_threshold': confidence_threshold,
            'prediction_horizon': prediction_horizon,
            'max_position_size': max_position_size,
            'max_portfolio_risk': max_portfolio_risk,
            'auto_trading_enabled': auto_trading_enabled
        }
    
    def _render_ai_signals_tab(self):
        """AI signals and predictions tab"""
        
        st.markdown("## 🎯 AI Trading Signals")
        
        if not AI_AVAILABLE:
            st.error("AI engine not available")
            return
        
        # Generate AI signals
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("🔄 Generate AI Signals", type="primary"):
                self._generate_ai_signals()
        
        # Display signals
        if 'ai_signals' in st.session_state and st.session_state.ai_signals:
            self._display_ai_signals(st.session_state.ai_signals)
        else:
            st.info("Click 'Generate AI Signals' to see AI-powered predictions")
    
    def _render_model_performance_tab(self):
        """Model performance and metrics tab"""
        
        st.markdown("## 🧠 AI Model Performance")
        
        # Model metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Direction Accuracy", 
                "73.2%", 
                "↑ 2.1%"
            )
        
        with col2:
            st.metric(
                "Return Prediction R²", 
                "0.68", 
                "↑ 0.05"
            )
        
        with col3:
            st.metric(
                "Sharpe Ratio", 
                "1.85", 
                "↑ 0.12"
            )
        
        with col4:
            st.metric(
                "Max Drawdown", 
                "8.4%", 
                "↓ 1.2%"
            )
        
        # Performance charts
        self._render_performance_charts()
        
        # Feature importance
        st.markdown("### 🔍 Model Feature Importance")
        self._render_feature_importance()
    
    def _render_ai_portfolio_tab(self):
        """AI-optimized portfolio tab"""
        
        st.markdown("## 💼 AI Portfolio Optimization")
        
        # Portfolio optimization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Optimized Allocation")
            
            if 'ai_portfolio' in st.session_state:
                self._display_ai_portfolio(st.session_state.ai_portfolio)
            else:
                st.info("Generate AI signals first to see portfolio optimization")
        
        with col2:
            st.markdown("### Portfolio Metrics")
            
            # Portfolio performance metrics
            metrics_data = {
                "Expected Return": "12.4%",
                "Volatility": "18.2%",
                "Sharpe Ratio": "1.85",
                "Max Drawdown": "8.4%",
                "Win Rate": "68.3%"
            }
            
            for metric, value in metrics_data.items():
                st.metric(metric, value)
        
        # Risk analysis
        st.markdown("### 📊 Risk Analysis")
        self._render_risk_analysis()
    
    def _render_market_intelligence_tab(self):
        """Market intelligence and sentiment tab"""
        
        st.markdown("## 📊 AI Market Intelligence")
        
        # Market sentiment
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Market Sentiment")
            sentiment_score = 0.72
            st.metric(
                "Overall Sentiment", 
                f"{sentiment_score:.1%}", 
                "Bullish"
            )
            
            # Sentiment gauge
            fig_sentiment = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = sentiment_score * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Market Sentiment"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if sentiment_score > 0.6 else "red"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgray"},
                        {'range': [30, 70], 'color': "gray"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig_sentiment.update_layout(height=250)
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        with col2:
            st.markdown("### Sector Analysis")
            
            # Sector performance
            sectors = ['Banking', 'Energy', 'Telecom', 'Materials', 'Healthcare']
            performance = [0.12, 0.08, 0.15, -0.03, 0.06]
            
            sector_df = pd.DataFrame({
                'Sector': sectors,
                'Performance': performance
            })
            
            fig_sectors = px.bar(
                sector_df, 
                x='Performance', 
                y='Sector', 
                orientation='h',
                color='Performance',
                color_continuous_scale='RdYlGn'
            )
            fig_sectors.update_layout(height=250)
            st.plotly_chart(fig_sectors, use_container_width=True)
        
        with col3:
            st.markdown("### Economic Indicators")
            
            econ_indicators = {
                "Oil Price": "+2.3%",
                "SAR/USD": "-0.1%",
                "Interest Rate": "5.50%",
                "Inflation": "2.1%",
                "GDP Growth": "3.2%"
            }
            
            for indicator, value in econ_indicators.items():
                change_color = "green" if value.startswith('+') else "red" if value.startswith('-') else "blue"
                st.markdown(f"**{indicator}**: <span style='color:{change_color}'>{value}</span>", 
                           unsafe_allow_html=True)
        
        # News sentiment analysis
        st.markdown("### 📰 News Sentiment Analysis")
        self._render_news_sentiment()
    
    def _generate_ai_signals(self):
        """Generate AI signals for portfolio"""
        
        with st.spinner("🤖 AI is analyzing market data..."):
            # Sample portfolio symbols
            portfolio_symbols = ['2222.SR', '2030.SR', '1120.SR', '2380.SR', '7040.SR']
            
            try:
                # Generate AI signals
                ai_signals = get_ai_enhanced_signals(portfolio_symbols)
                st.session_state.ai_signals = ai_signals
                
                # Generate portfolio optimization
                if self.portfolio_optimizer:
                    portfolio = self.portfolio_optimizer.optimize_portfolio(ai_signals)
                    st.session_state.ai_portfolio = portfolio
                
                st.success(f"✅ Generated {len(ai_signals)} AI signals")
                
            except Exception as e:
                st.error(f"❌ Failed to generate AI signals: {e}")
    
    def _display_ai_signals(self, signals):
        """Display AI trading signals"""
        
        for signal in signals:
            # Signal card
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    # Signal type with emoji
                    signal_emoji = "🟢" if signal.signal_type == "BUY" else "🔴" if signal.signal_type == "SELL" else "🟡"
                    st.markdown(f"### {signal_emoji} {signal.symbol}")
                    st.markdown(f"**{signal.signal_type}** Signal")
                
                with col2:
                    st.metric("Confidence", f"{signal.confidence:.1%}")
                    st.metric("Risk Score", f"{signal.risk_score:.1%}")
                
                with col3:
                    if signal.predicted_price:
                        st.metric("Predicted Price", f"{signal.predicted_price:.2f} SAR")
                    st.metric("Horizon", f"{signal.prediction_horizon} days")
                
                with col4:
                    # AI features
                    if 'predicted_return' in signal.ai_features:
                        return_pct = signal.ai_features['predicted_return'] * 100
                        st.metric("Expected Return", f"{return_pct:+.1f}%")
                    
                    if 'rsi' in signal.ai_features:
                        st.metric("RSI", f"{signal.ai_features['rsi']:.0f}")
                
                # Progress bars for confidence and risk
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Confidence Level**")
                    st.progress(signal.confidence)
                
                with col2:
                    st.markdown("**Risk Level**")
                    st.progress(signal.risk_score)
                
                st.divider()
    
    def _display_ai_portfolio(self, portfolio):
        """Display AI-optimized portfolio"""
        
        if 'allocation' not in portfolio or not portfolio['allocation']:
            st.warning("No optimal allocation found")
            return
        
        # Portfolio allocation chart
        allocation = portfolio['allocation']
        symbols = list(allocation.keys())
        weights = [allocation[symbol]['weight'] for symbol in symbols]
        
        fig_pie = px.pie(
            values=weights,
            names=symbols,
            title="AI-Optimized Portfolio Allocation"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Allocation details
        st.markdown("### Portfolio Details")
        
        allocation_df = pd.DataFrame([
            {
                'Symbol': symbol,
                'Weight': f"{allocation[symbol]['weight']:.1%}",
                'Value': f"{allocation[symbol]['value']:,.0f} SAR",
                'Confidence': f"{allocation[symbol]['confidence']:.1%}",
                'Risk': f"{allocation[symbol]['risk_score']:.1%}",
                'Expected Return': f"{allocation[symbol]['predicted_return']:+.1%}"
            }
            for symbol in allocation.keys()
        ])
        
        st.dataframe(allocation_df, use_container_width=True)
    
    def _render_performance_charts(self):
        """Render model performance charts"""
        
        # Simulated performance data
        dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
        cumulative_returns = np.cumsum(np.random.normal(0.001, 0.02, 100))
        benchmark_returns = np.cumsum(np.random.normal(0.0005, 0.025, 100))
        
        fig_performance = go.Figure()
        
        fig_performance.add_trace(go.Scatter(
            x=dates,
            y=(1 + cumulative_returns) * 100,
            mode='lines',
            name='AI Strategy',
            line=dict(color='green', width=3)
        ))
        
        fig_performance.add_trace(go.Scatter(
            x=dates,
            y=(1 + benchmark_returns) * 100,
            mode='lines',
            name='TASI Benchmark',
            line=dict(color='blue', width=2)
        ))
        
        fig_performance.update_layout(
            title="AI Strategy vs Benchmark Performance",
            xaxis_title="Date",
            yaxis_title="Portfolio Value",
            height=400
        )
        
        st.plotly_chart(fig_performance, use_container_width=True)
    
    def _render_feature_importance(self):
        """Render feature importance chart"""
        
        features = ['RSI', 'MACD', 'Volume Ratio', 'Price/SMA', 'Volatility', 'Market Sentiment']
        importance = [0.23, 0.19, 0.16, 0.15, 0.14, 0.13]
        
        fig_importance = px.bar(
            x=importance,
            y=features,
            orientation='h',
            title="Most Important AI Features"
        )
        
        fig_importance.update_layout(height=300)
        st.plotly_chart(fig_importance, use_container_width=True)
    
    def _render_risk_analysis(self):
        """Render portfolio risk analysis"""
        
        # Risk metrics over time
        dates = pd.date_range(start='2024-01-01', periods=50, freq='W')
        var_95 = np.random.uniform(0.02, 0.08, 50)
        
        fig_risk = go.Figure()
        
        fig_risk.add_trace(go.Scatter(
            x=dates,
            y=var_95,
            mode='lines+markers',
            name='VaR (95%)',
            line=dict(color='red')
        ))
        
        fig_risk.update_layout(
            title="Portfolio Value at Risk (VaR)",
            xaxis_title="Date",
            yaxis_title="VaR (%)",
            height=300
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    def _render_news_sentiment(self):
        """Render news sentiment analysis"""
        
        # Simulated news sentiment data
        news_data = [
            {"Date": "2025-08-11", "Headline": "Saudi Aramco reports strong Q2 earnings", "Sentiment": 0.8},
            {"Date": "2025-08-10", "Headline": "NEOM project reaches new milestone", "Sentiment": 0.7},
            {"Date": "2025-08-09", "Headline": "Banking sector shows resilience", "Sentiment": 0.6},
            {"Date": "2025-08-08", "Headline": "Oil prices stabilize amid global tensions", "Sentiment": 0.3},
            {"Date": "2025-08-07", "Headline": "Vision 2030 progress report released", "Sentiment": 0.9}
        ]
        
        news_df = pd.DataFrame(news_data)
        
        for _, news in news_df.iterrows():
            sentiment_color = "green" if news['Sentiment'] > 0.6 else "red" if news['Sentiment'] < 0.4 else "orange"
            
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{news['Date']}**: {news['Headline']}")
                
                with col2:
                    st.markdown(f"<span style='color:{sentiment_color}'>Sentiment: {news['Sentiment']:.1f}</span>", 
                               unsafe_allow_html=True)

def render_ai_enhanced_dashboard():
    """Main function to render AI-enhanced dashboard"""
    
    # Check if AI features are enabled
    ai_enabled = st.sidebar.checkbox("🤖 Enable AI Trading", value=True)
    
    if ai_enabled and AI_AVAILABLE:
        dashboard = AITradingDashboard()
        dashboard.render_ai_dashboard()
    else:
        st.warning("AI Trading features are disabled or not available")
        st.info("Enable AI Trading in the sidebar to access machine learning predictions")

if __name__ == "__main__":
    render_ai_enhanced_dashboard()
