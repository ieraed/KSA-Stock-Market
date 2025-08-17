"""
🇸🇦 Enhanced Saudi Stock Portfolio Manager with Unified Data
Addresses data consistency issues with unified data sourcing
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="🇸🇦 Saudi Stock Portfolio | TADAWUL NEXUS",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #006c35 0%, #00a650 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #006c35;
    }
    
    .stock-card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1rem;
    }
    
    .data-source-indicator {
        background: #e3f2fd;
        padding: 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        color: #1565c0;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Data Loading Functions
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_unified_stock_database():
    """Load stock database with unified data management"""
    try:
        # Try unified manager first
        from unified_stock_manager import get_unified_stocks_database
        stocks_db = get_unified_stocks_database()
        st.success("📊 Using unified data manager - all sources synchronized!")
        return stocks_db, "unified"
    except ImportError:
        st.warning("⚠️ Unified manager not available - using fallback database")
        try:
            with open('saudi_stocks_database_corrected.json', 'r', encoding='utf-8') as f:
                return json.load(f), "corrected"
        except FileNotFoundError:
            with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
                return json.load(f), "main"

def load_portfolio():
    """Load user portfolio"""
    try:
        with open('user_portfolio.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_portfolio(portfolio):
    """Save user portfolio"""
    try:
        with open('user_portfolio.json', 'w') as f:
            json.dump(portfolio, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving portfolio: {e}")
        return False

def validate_data_consistency():
    """Validate data consistency"""
    stocks_db, source = load_unified_stock_database()
    
    validation_results = {
        'source': source,
        'total_stocks': len(stocks_db),
        'test_stocks': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Test critical stocks
    test_cases = [
        ('1010', 'Saudi National Bank'),
        ('1120', 'Al Rajhi Bank'),
        ('2030', 'Saudi Arabian Oil Company'),
        ('2010', 'Saudi Basic Industries Corporation')
    ]
    
    for symbol, expected in test_cases:
        stock_info = stocks_db.get(symbol, {})
        actual = stock_info.get('name_en', 'NOT FOUND')
        validation_results['test_stocks'][symbol] = {
            'expected': expected,
            'actual': actual,
            'match': expected.lower() in actual.lower(),
            'sector': stock_info.get('sector', 'Unknown')
        }
    
    return validation_results

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇸🇦 TADAWUL NEXUS | Saudi Stock Portfolio Manager</h1>
        <p>Enhanced with Unified Data Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    stocks_db, data_source = load_unified_stock_database()
    portfolio = load_portfolio()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📊 Market Overview")
        
        # Data source indicator
        source_color = {
            'unified': '#4caf50',
            'corrected': '#ff9800', 
            'main': '#2196f3'
        }
        
        st.markdown(f"""
        <div style="background: {source_color.get(data_source, '#gray')}; color: white; padding: 0.5rem; border-radius: 4px; text-align: center;">
            📡 Data Source: {data_source.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        # Market metrics
        st.metric("🏢 Total Stocks", len(stocks_db))
        st.metric("📈 Portfolio Stocks", len(portfolio))
        
        if portfolio:
            total_investment = sum(stock['quantity'] * stock['purchase_price'] for stock in portfolio)
            st.metric("💰 Total Investment", f"{total_investment:,.2f} SAR")
        
        # Quick data validation
        st.markdown("---")
        st.markdown("### 🔍 Data Validation")
        
        if st.button("🔄 Validate Data"):
            validation = validate_data_consistency()
            
            st.markdown("**Test Results:**")
            for symbol, result in validation['test_stocks'].items():
                status = "✅" if result['match'] else "❌"
                st.write(f"{status} {symbol}: {result['actual']}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Dashboard", 
        "⚙️ Portfolio Setup", 
        "📊 Analysis", 
        "🔧 System Status"
    ])
    
    with tab1:
        st.markdown("## 🏠 Portfolio Dashboard")
        
        if portfolio:
            # Portfolio overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_stocks = len(portfolio)
                st.metric("📊 Portfolio Stocks", total_stocks)
            
            with col2:
                total_quantity = sum(stock['quantity'] for stock in portfolio)
                st.metric("📈 Total Shares", f"{total_quantity:,}")
            
            with col3:
                total_investment = sum(stock['quantity'] * stock['purchase_price'] for stock in portfolio)
                st.metric("💰 Total Investment", f"{total_investment:,.2f} SAR")
            
            # Portfolio details
            st.markdown("### 📋 Portfolio Holdings")
            
            portfolio_data = []
            for stock in portfolio:
                stock_info = stocks_db.get(stock['symbol'], {})
                
                portfolio_data.append({
                    'Symbol': stock['symbol'],
                    'Company': stock_info.get('name_en', 'Unknown Company'),
                    'Sector': stock_info.get('sector', 'Unknown'),
                    'Quantity': stock['quantity'],
                    'Purchase Price': f"{stock['purchase_price']:.2f}",
                    'Total Value': f"{stock['quantity'] * stock['purchase_price']:.2f}",
                    'Purchase Date': stock['purchase_date']
                })
            
            if portfolio_data:
                df = pd.DataFrame(portfolio_data)
                st.dataframe(df, use_container_width=True)
            
        else:
            st.info("📝 No stocks in portfolio yet. Go to Portfolio Setup to add stocks.")
    
    with tab2:
        st.markdown("## ⚙️ Portfolio Setup")
        
        st.markdown("### ➕ Add New Stock")
        
        # Stock selection with unified data
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create stock options
            stock_options = []
            for symbol, data in stocks_db.items():
                name_en = data.get('name_en', 'Unknown Company')
                sector = data.get('sector', '')
                
                option_text = f"{symbol} - {name_en}"
                if sector and sector != 'Unknown':
                    option_text += f" ({sector})"
                
                stock_options.append((option_text, symbol))
            
            stock_options.sort()
            
            selected_option = st.selectbox(
                "Choose a Saudi stock:",
                options=[opt[0] for opt in stock_options],
                index=0,
                help=f"Select from {len(stocks_db)} available Saudi stocks"
            )
            
            # Get selected symbol
            selected_symbol = None
            for opt_text, symbol in stock_options:
                if opt_text == selected_option:
                    selected_symbol = symbol
                    break
        
        with col2:
            if selected_symbol:
                stock_info = stocks_db[selected_symbol]
                
                st.markdown(f"""
                <div class="stock-card">
                    <h4 style="color: #006c35; margin: 0;">{stock_info.get('name_en', 'Unknown')}</h4>
                    <p style="margin: 0.5rem 0;"><strong>Symbol:</strong> {selected_symbol}</p>
                    <p style="margin: 0.5rem 0;"><strong>Sector:</strong> {stock_info.get('sector', 'N/A')}</p>
                    {f'<p style="margin: 0.5rem 0;"><strong>Current Price:</strong> {stock_info.get("current_price", "N/A")} SAR</p>' if stock_info.get('current_price') else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Data source indicator
                if stock_info.get('last_updated'):
                    st.markdown(f"""
                    <div class="data-source-indicator">
                        📊 Updated: {stock_info.get('last_updated', 'Unknown')[:19].replace('T', ' ')}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Stock details input
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quantity = st.number_input("Quantity:", min_value=1, value=100, step=1)
        
        with col2:
            purchase_price = st.number_input("Purchase Price (SAR):", min_value=0.01, value=50.0, step=0.01)
        
        with col3:
            purchase_date = st.date_input("Purchase Date:", value=datetime.now().date())
        
        # Add to portfolio
        if st.button("➕ Add to Portfolio", type="primary"):
            if selected_symbol:
                portfolio = load_portfolio()
                
                # Check for existing stock
                existing_index = None
                for i, stock in enumerate(portfolio):
                    if stock['symbol'] == selected_symbol:
                        existing_index = i
                        break
                
                stock_info = stocks_db[selected_symbol]
                
                if existing_index is not None:
                    # Update existing
                    old_stock = portfolio[existing_index]
                    old_qty = old_stock['quantity']
                    old_price = old_stock['purchase_price']
                    
                    total_qty = old_qty + quantity
                    total_cost = (old_qty * old_price) + (quantity * purchase_price)
                    avg_price = total_cost / total_qty
                    
                    portfolio[existing_index] = {
                        'symbol': selected_symbol,
                        'quantity': total_qty,
                        'purchase_price': avg_price,
                        'purchase_date': purchase_date.isoformat(),
                        'last_updated': datetime.now().isoformat()
                    }
                    
                    st.success(f"✅ Updated {stock_info.get('name_en')} holding! New quantity: {total_qty}")
                else:
                    # Add new
                    new_stock = {
                        'symbol': selected_symbol,
                        'quantity': quantity,
                        'purchase_price': purchase_price,
                        'purchase_date': purchase_date.isoformat(),
                        'last_updated': datetime.now().isoformat()
                    }
                    portfolio.append(new_stock)
                    
                    st.success(f"✅ Added {stock_info.get('name_en')} to your portfolio!")
                
                if save_portfolio(portfolio):
                    st.rerun()
        
        # Portfolio management
        st.markdown("---")
        st.markdown("### 📋 Current Portfolio")
        
        if portfolio:
            for i, stock in enumerate(portfolio):
                stock_info = stocks_db.get(stock['symbol'], {})
                
                with st.expander(f"{stock['symbol']} - {stock_info.get('name_en', 'Unknown')} ({stock['quantity']} shares)"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Company:** {stock_info.get('name_en', 'Unknown')}")
                        st.write(f"**Sector:** {stock_info.get('sector', 'Unknown')}")
                        st.write(f"**Purchase Price:** {stock['purchase_price']:.2f} SAR")
                        st.write(f"**Quantity:** {stock['quantity']} shares")
                        st.write(f"**Total Value:** {stock['quantity'] * stock['purchase_price']:.2f} SAR")
                        st.write(f"**Purchase Date:** {stock['purchase_date']}")
                    
                    with col2:
                        if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                            portfolio.pop(i)
                            save_portfolio(portfolio)
                            st.success("Stock removed!")
                            st.rerun()
        else:
            st.info("No stocks in portfolio yet.")
    
    with tab3:
        st.markdown("## 📊 Portfolio Analysis")
        
        if portfolio:
            # Sector distribution
            sector_data = {}
            for stock in portfolio:
                stock_info = stocks_db.get(stock['symbol'], {})
                sector = stock_info.get('sector', 'Unknown')
                value = stock['quantity'] * stock['purchase_price']
                
                if sector in sector_data:
                    sector_data[sector] += value
                else:
                    sector_data[sector] = value
            
            if sector_data:
                fig = px.pie(
                    values=list(sector_data.values()),
                    names=list(sector_data.keys()),
                    title="Portfolio by Sector"
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add stocks to your portfolio to see analysis.")
    
    with tab4:
        st.markdown("## 🔧 System Status")
        
        # Data validation
        validation = validate_data_consistency()
        
        st.markdown("### 📊 Data Source Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Data Source", validation['source'].upper())
            st.metric("Total Stocks", validation['total_stocks'])
        
        with col2:
            st.metric("Validation Time", validation['timestamp'][:19].replace('T', ' '))
        
        # Validation results
        st.markdown("### 🔍 Data Validation Results")
        
        validation_df = []
        for symbol, result in validation['test_stocks'].items():
            validation_df.append({
                'Symbol': symbol,
                'Expected': result['expected'],
                'Actual': result['actual'],
                'Status': '✅ Match' if result['match'] else '❌ Mismatch',
                'Sector': result['sector']
            })
        
        if validation_df:
            df = pd.DataFrame(validation_df)
            st.dataframe(df, use_container_width=True)
        
        # System recommendations
        st.markdown("### 💡 Recommendations")
        
        all_match = all(result['match'] for result in validation['test_stocks'].values())
        
        if all_match:
            st.success("✅ All stock data is consistent! The Portfolio Setup page should show correct symbol-name pairs.")
        else:
            st.warning("⚠️ Some data inconsistencies detected. Consider refreshing the data source.")
        
        if validation['source'] != 'unified':
            st.info("💡 Install dependencies for the continuous data fetcher to enable unified data management.")

if __name__ == "__main__":
    main()
