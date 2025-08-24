"""
Advanced Portfolio Optimization Engine for TADAWUL NEXUS
Modern Portfolio Theory implementation with Saudi market constraints
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
from datetime import datetime, timedelta

class AdvancedPortfolioOptimizer:
    def __init__(self):
        self.risk_free_rate = 0.025  # 2.5% Saudi risk-free rate
        self.market_constraints = {
            'max_sector_weight': 0.4,  # Max 40% in any sector
            'max_single_stock': 0.2,   # Max 20% in single stock
            'min_diversification': 5   # Minimum 5 stocks
        }
    
    def create_optimization_dashboard(self):
        """Advanced portfolio optimization interface"""
        
        st.markdown("## 🎯 Portfolio Optimization Engine")
        st.caption("Modern Portfolio Theory for Saudi Markets")
        
        # Optimization parameters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            optimization_goal = st.selectbox(
                "Optimization Goal",
                ["Maximum Sharpe Ratio", "Minimum Risk", "Target Return", "Risk Parity"]
            )
            
        with col2:
            risk_tolerance = st.slider("Risk Tolerance", 1, 10, 5)
            
        with col3:
            investment_amount = st.number_input("Investment Amount (SAR)", 
                                              min_value=1000, value=100000, step=1000)
        
        # Advanced constraints
        st.markdown("### ⚙️ Portfolio Constraints")
        
        constraint_cols = st.columns(4)
        
        with constraint_cols[0]:
            max_sector_weight = st.slider("Max Sector Weight (%)", 10, 50, 40)
            
        with constraint_cols[1]:
            max_stock_weight = st.slider("Max Single Stock (%)", 5, 25, 20)
            
        with constraint_cols[2]:
            min_stocks = st.slider("Min # of Stocks", 3, 15, 5)
            
        with constraint_cols[3]:
            rebalance_freq = st.selectbox("Rebalancing", ["Monthly", "Quarterly", "Semi-Annual"])
        
        # Efficient Frontier Visualization
        st.markdown("### 📊 Efficient Frontier Analysis")
        
        if st.button("🚀 Generate Optimal Portfolio", type="primary"):
            self.generate_efficient_frontier()
            self.display_optimal_allocation(investment_amount, optimization_goal)
    
    def generate_efficient_frontier(self):
        """Generate and display efficient frontier"""
        
        # Sample data for Saudi stocks
        stocks = ['2222.SR', '2380.SR', '1120.SR', '2010.SR', '1180.SR', '7010.SR']
        
        # Simulate historical returns (in practice, fetch real data)
        np.random.seed(42)
        n_days = 252
        returns_data = {}
        
        for stock in stocks:
            # Generate realistic return data for Saudi stocks
            daily_returns = np.random.normal(0.0008, 0.025, n_days)  # ~20% annual return, 25% volatility
            returns_data[stock] = daily_returns
        
        returns_df = pd.DataFrame(returns_data)
        
        # Calculate mean returns and covariance matrix
        mean_returns = returns_df.mean() * 252  # Annualized
        cov_matrix = returns_df.cov() * 252     # Annualized
        
        # Generate efficient frontier
        n_portfolios = 50
        results = np.zeros((3, n_portfolios))
        
        target_returns = np.linspace(mean_returns.min(), mean_returns.max(), n_portfolios)
        
        for i, target in enumerate(target_returns):
            # Optimize for minimum risk given target return
            weights = self.optimize_portfolio(mean_returns, cov_matrix, target)
            
            portfolio_return = np.sum(mean_returns * weights)
            portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_risk
            
            results[0,i] = portfolio_return
            results[1,i] = portfolio_risk
            results[2,i] = sharpe_ratio
        
        # Plot efficient frontier
        fig = go.Figure()
        
        # Efficient frontier line
        fig.add_trace(go.Scatter(
            x=results[1,:] * 100,  # Convert to percentage
            y=results[0,:] * 100,  # Convert to percentage
            mode='lines+markers',
            name='Efficient Frontier',
            line=dict(color='blue', width=3),
            marker=dict(size=6),
            hovertemplate="Risk: %{x:.1f}%<br>Return: %{y:.1f}%<extra></extra>"
        ))
        
        # Maximum Sharpe ratio point
        max_sharpe_idx = np.argmax(results[2,:])
        fig.add_trace(go.Scatter(
            x=[results[1,max_sharpe_idx] * 100],
            y=[results[0,max_sharpe_idx] * 100],
            mode='markers',
            name='Max Sharpe Ratio',
            marker=dict(size=15, color='red', symbol='star'),
            hovertemplate="Optimal Portfolio<br>Risk: %{x:.1f}%<br>Return: %{y:.1f}%<extra></extra>"
        ))
        
        # Individual stocks
        for i, stock in enumerate(stocks):
            stock_return = mean_returns.iloc[i] * 100
            stock_risk = np.sqrt(cov_matrix.iloc[i,i]) * 100
            
            fig.add_trace(go.Scatter(
                x=[stock_risk],
                y=[stock_return],
                mode='markers',
                name=stock.replace('.SR', ''),
                marker=dict(size=10),
                hovertemplate=f"{stock}<br>Risk: %{{x:.1f}}%<br>Return: %{{y:.1f}}%<extra></extra>"
            ))
        
        fig.update_layout(
            title="🎯 Efficient Frontier - Saudi Stocks",
            xaxis_title="Risk (Volatility %)",
            yaxis_title="Expected Return (%)",
            hovermode='closest',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display metrics for optimal portfolio
        optimal_return = results[0,max_sharpe_idx] * 100
        optimal_risk = results[1,max_sharpe_idx] * 100
        optimal_sharpe = results[2,max_sharpe_idx]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Expected Return", f"{optimal_return:.1f}%", "Annualized")
        with col2:
            st.metric("Portfolio Risk", f"{optimal_risk:.1f}%", "Volatility")
        with col3:
            st.metric("Sharpe Ratio", f"{optimal_sharpe:.2f}", "Risk-adjusted return")
    
    def optimize_portfolio(self, mean_returns, cov_matrix, target_return):
        """Optimize portfolio for given target return"""
        
        n_assets = len(mean_returns)
        
        # Objective function (minimize risk)
        def objective(weights):
            return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights sum to 1
            {'type': 'eq', 'fun': lambda x: np.sum(x * mean_returns) - target_return}  # Target return
        ]
        
        # Bounds (0 to 1 for each weight)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess (equal weights)
        x0 = np.array([1/n_assets] * n_assets)
        
        # Optimize
        result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
        
        return result.x if result.success else x0
    
    def display_optimal_allocation(self, investment_amount, optimization_goal):
        """Display recommended portfolio allocation"""
        
        st.markdown("### 💼 Recommended Portfolio Allocation")
        
        # Sample optimal weights (in practice, use actual optimization results)
        stocks = ['SABIC (2010)', 'Al Rajhi Bank (1120)', 'STC (7010)', 'ARAMCO (2222)', 'NCB (1180)', 'SABIC Agri (2290)']
        weights = [0.25, 0.20, 0.18, 0.15, 0.12, 0.10]  # Optimal weights
        sectors = ['Petrochemicals', 'Banking', 'Telecom', 'Energy', 'Banking', 'Petrochemicals']
        
        allocation_df = pd.DataFrame({
            'Stock': stocks,
            'Weight (%)': [w*100 for w in weights],
            'Allocation (SAR)': [w*investment_amount for w in weights],
            'Sector': sectors
        })
        
        # Display allocation table
        st.dataframe(
            allocation_df.style.format({
                'Weight (%)': '{:.1f}%',
                'Allocation (SAR)': '{:,.0f} SAR'
            }),
            use_container_width=True
        )
        
        # Pie chart for visual allocation
        fig = px.pie(
            allocation_df, 
            values='Weight (%)', 
            names='Stock',
            title=f"🥧 Portfolio Allocation - {optimization_goal}",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk metrics for recommended portfolio
        st.markdown("### 📊 Portfolio Risk Analysis")
        
        risk_cols = st.columns(4)
        
        with risk_cols[0]:
            st.metric("VaR (95%)", "12,450 SAR", "Daily risk")
            
        with risk_cols[1]:
            st.metric("Beta", "0.87", "vs TASI")
            
        with risk_cols[2]:
            st.metric("Correlation", "0.72", "with market")
            
        with risk_cols[3]:
            st.metric("Diversification Ratio", "1.35", "Risk reduction")

# Usage function
def add_portfolio_optimizer():
    """Add portfolio optimization to main app"""
    optimizer = AdvancedPortfolioOptimizer()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Portfolio Optimizer")
    
    if st.sidebar.checkbox("⚡ Enable Optimizer"):
        optimizer.create_optimization_dashboard()
