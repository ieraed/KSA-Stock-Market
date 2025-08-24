"""
Advanced News & Sentiment Analysis for TADAWUL NEXUS
Real-time news aggregation with AI-powered sentiment analysis
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import re
from textblob import TextBlob
import requests

class NewsAndSentimentAnalyzer:
    def __init__(self):
        self.news_sources = [
            "Argaam", "Mubasher", "Saudi Gazette", "Arab News", 
            "Al Arabiya", "CNBC Arabia", "Bloomberg Saudi"
        ]
        
    def create_news_dashboard(self):
        """Advanced news and sentiment analysis dashboard"""
        
        st.markdown("## 📰 News & Market Sentiment")
        st.caption("Real-time news aggregation with AI sentiment analysis")
        
        # News filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            news_category = st.selectbox(
                "News Category",
                ["All", "Market Updates", "Company News", "Economic", "Regulatory", "Earnings"]
            )
            
        with col2:
            sentiment_filter = st.selectbox(
                "Sentiment Filter", 
                ["All", "Positive", "Neutral", "Negative"]
            )
            
        with col3:
            time_range = st.selectbox(
                "Time Range",
                ["Last Hour", "Today", "This Week", "This Month"]
            )
            
        with col4:
            source_filter = st.multiselect(
                "News Sources",
                self.news_sources,
                default=self.news_sources[:3]
            )
        
        # Real-time sentiment gauge
        self.display_market_sentiment_gauge()
        
        # News feed with sentiment
        self.display_news_feed_with_sentiment()
        
        # Sentiment trends
        self.display_sentiment_trends()
        
        # Impact analysis
        self.display_news_impact_analysis()
    
    def display_market_sentiment_gauge(self):
        """Real-time market sentiment gauge"""
        
        st.markdown("### 🌡️ Market Sentiment Gauge")
        
        # Calculate overall market sentiment (mock data)
        sentiment_score = 0.65  # 0 = Very Negative, 1 = Very Positive
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = sentiment_score * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Market Sentiment"},
            delta = {'reference': 50, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 25], 'color': "red"},
                    {'range': [25, 50], 'color': "orange"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Sentiment breakdown
            sentiment_data = {
                'Sentiment': ['Very Positive', 'Positive', 'Neutral', 'Negative', 'Very Negative'],
                'Count': [45, 78, 32, 23, 12],
                'Percentage': [23.7, 41.1, 16.8, 12.1, 6.3]
            }
            
            sentiment_df = pd.DataFrame(sentiment_data)
            
            fig2 = px.bar(
                sentiment_df,
                x='Sentiment',
                y='Count',
                color='Sentiment',
                color_discrete_map={
                    'Very Positive': '#28a745',
                    'Positive': '#6c757d',
                    'Neutral': '#ffc107',
                    'Negative': '#fd7e14',
                    'Very Negative': '#dc3545'
                },
                title="News Sentiment Distribution"
            )
            
            fig2.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig2, use_container_width=True)
    
    def display_news_feed_with_sentiment(self):
        """Display news feed with sentiment analysis"""
        
        st.markdown("### 📊 Latest News with Sentiment Analysis")
        
        # Sample news data with sentiment
        news_data = [
            {
                "time": "2 hours ago",
                "headline": "ARAMCO announces record quarterly profits, beating analysts expectations",
                "source": "Argaam",
                "sentiment": "Positive",
                "sentiment_score": 0.85,
                "impact": "High",
                "category": "Earnings",
                "stocks_mentioned": ["2222.SR"]
            },
            {
                "time": "4 hours ago", 
                "headline": "Saudi Central Bank raises interest rates by 0.25%",
                "source": "Arab News",
                "sentiment": "Neutral",
                "sentiment_score": 0.45,
                "impact": "Medium", 
                "category": "Economic",
                "stocks_mentioned": ["1120.SR", "1180.SR"]
            },
            {
                "time": "6 hours ago",
                "headline": "SABIC faces regulatory investigation over environmental compliance",
                "source": "Bloomberg Saudi",
                "sentiment": "Negative",
                "sentiment_score": 0.25,
                "impact": "Medium",
                "category": "Regulatory",
                "stocks_mentioned": ["2010.SR"]
            },
            {
                "time": "8 hours ago",
                "headline": "Saudi Vision 2030 drives massive infrastructure investments",
                "source": "Saudi Gazette",
                "sentiment": "Positive",
                "sentiment_score": 0.78,
                "impact": "High",
                "category": "Economic",
                "stocks_mentioned": ["multiple"]
            }
        ]
        
        # Display news cards
        for news in news_data:
            # Determine sentiment color and emoji
            if news["sentiment"] == "Positive":
                sentiment_color = "#28a745"
                sentiment_emoji = "📈"
            elif news["sentiment"] == "Negative":
                sentiment_color = "#dc3545"
                sentiment_emoji = "📉"
            else:
                sentiment_color = "#6c757d"
                sentiment_emoji = "➡️"
            
            # Impact badge
            impact_colors = {"High": "#dc3545", "Medium": "#ffc107", "Low": "#28a745"}
            impact_color = impact_colors.get(news["impact"], "#6c757d")
            
            st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 12px; padding: 1.2rem; margin: 1rem 0;
                       background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                       box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <span style="background: {sentiment_color}; color: white; padding: 0.3rem 0.6rem; 
                                   border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                            {sentiment_emoji} {news["sentiment"]}
                        </span>
                        <span style="background: {impact_color}; color: white; padding: 0.3rem 0.6rem; 
                                   border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                            {news["impact"]} Impact
                        </span>
                        <span style="color: #6c757d; font-size: 0.8rem;">{news["time"]}</span>
                    </div>
                </div>
                
                <h4 style="margin: 0 0 0.5rem 0; color: #333; line-height: 1.4;">
                    {news["headline"]}
                </h4>
                
                <div style="display: flex; justify-content: between; align-items: center; margin-top: 0.8rem;">
                    <div style="color: #6c757d; font-size: 0.9rem;">
                        📰 {news["source"]} | 📂 {news["category"]}
                        {" | 🏢 " + ", ".join(news["stocks_mentioned"]) if news["stocks_mentioned"][0] != "multiple" else " | 🏢 Multiple stocks"}
                    </div>
                    <div style="background: #e9ecef; padding: 0.3rem 0.6rem; border-radius: 8px; font-size: 0.8rem;">
                        Sentiment Score: {news["sentiment_score"]:.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def display_sentiment_trends(self):
        """Display sentiment trends over time"""
        
        st.markdown("### 📈 Sentiment Trends Analysis")
        
        # Generate sample time series data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        
        # Sample sentiment data
        np.random.seed(42)
        sentiment_scores = np.random.normal(0.55, 0.15, len(dates))
        sentiment_scores = np.clip(sentiment_scores, 0, 1)  # Keep between 0 and 1
        
        market_returns = np.random.normal(0.002, 0.025, len(dates))
        
        sentiment_df = pd.DataFrame({
            'Date': dates,
            'Sentiment': sentiment_scores,
            'Market_Return': market_returns
        })
        
        # Create dual-axis chart
        fig = go.Figure()
        
        # Sentiment line
        fig.add_trace(go.Scatter(
            x=sentiment_df['Date'],
            y=sentiment_df['Sentiment'],
            mode='lines',
            name='Market Sentiment',
            line=dict(color='blue', width=2),
            yaxis='y1'
        ))
        
        # Market returns bars
        colors = ['green' if x > 0 else 'red' for x in sentiment_df['Market_Return']]
        fig.add_trace(go.Bar(
            x=sentiment_df['Date'],
            y=sentiment_df['Market_Return'] * 100,  # Convert to percentage
            name='Daily Market Return (%)',
            marker_color=colors,
            yaxis='y2',
            opacity=0.6
        ))
        
        # Update layout for dual axis
        fig.update_layout(
            title="💭 Market Sentiment vs Performance",
            xaxis_title="Date",
            yaxis=dict(
                title="Sentiment Score",
                side="left",
                range=[0, 1]
            ),
            yaxis2=dict(
                title="Daily Return (%)",
                side="right",
                overlaying="y",
                range=[-5, 5]
            ),
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        correlation = np.corrcoef(sentiment_df['Sentiment'], sentiment_df['Market_Return'])[0,1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sentiment-Return Correlation", f"{correlation:.2f}")
        with col2:
            avg_sentiment = sentiment_df['Sentiment'].mean()
            st.metric("Average Sentiment (30d)", f"{avg_sentiment:.2f}")
        with col3:
            sentiment_volatility = sentiment_df['Sentiment'].std()
            st.metric("Sentiment Volatility", f"{sentiment_volatility:.2f}")
    
    def display_news_impact_analysis(self):
        """Analyze news impact on stock prices"""
        
        st.markdown("### 🎯 News Impact Analysis")
        
        # Sample data showing news impact on stock prices
        impact_data = {
            'Stock': ['ARAMCO (2222)', 'Al Rajhi (1120)', 'SABIC (2010)', 'STC (7010)'],
            'Pre_News_Price': [35.50, 85.20, 125.00, 45.80],
            'Post_News_Price': [37.25, 84.15, 122.50, 46.90],
            'Price_Change_%': [4.93, -1.23, -2.00, 2.40],
            'News_Sentiment': [0.85, 0.35, 0.25, 0.68],
            'Volume_Change_%': [125, 45, 89, 67]
        }
        
        impact_df = pd.DataFrame(impact_data)
        
        # Scatter plot: Sentiment vs Price Change
        fig = px.scatter(
            impact_df,
            x='News_Sentiment',
            y='Price_Change_%',
            size='Volume_Change_%',
            color='Price_Change_%',
            hover_name='Stock',
            title="📊 News Sentiment vs Price Impact",
            labels={
                'News_Sentiment': 'News Sentiment Score',
                'Price_Change_%': 'Price Change (%)',
                'Volume_Change_%': 'Volume Change (%)'
            },
            color_continuous_scale='RdYlGn'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Impact summary table
        st.markdown("#### 📋 News Impact Summary")
        
        styled_df = impact_df.style.format({
            'Pre_News_Price': '{:.2f} SAR',
            'Post_News_Price': '{:.2f} SAR',
            'Price_Change_%': '{:+.1f}%',
            'News_Sentiment': '{:.2f}',
            'Volume_Change_%': '{:+.0f}%'
        }).background_gradient(subset=['Price_Change_%'], cmap='RdYlGn')
        
        st.dataframe(styled_df, use_container_width=True)

# Usage function
def add_news_sentiment_analysis():
    """Add news and sentiment analysis to main app"""
    analyzer = NewsAndSentimentAnalyzer()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📰 News Analysis")
    
    if st.sidebar.checkbox("📊 Enable News Analytics"):
        analyzer.create_news_dashboard()
