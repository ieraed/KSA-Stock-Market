"""
🇸🇦 Saudi Stock Exchange Portfolio Manager
Simple, clean portfolio management system for Tadawul stocks
Starting from scratch - Step by step approach
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, date
import io
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="🇸🇦 Saudi Portfolio Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean, professional CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.portfolio-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin: 1rem 0;
    border: 1px solid #e1e8ed;
}

.metric-card {
    background: linear-gradient(135deg, #00C851 0%, #007E33 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    box-shadow: 0 3px 15px rgba(0,0,0,0.1);
    margin: 0.5rem 0;
}

.stock-row {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 4px solid #00C851;
}

.profit { color: #00C851; font-weight: 600; }
.loss { color: #dc3545; font-weight: 600; }
.neutral { color: #ffc107; font-weight: 600; }

.upload-area {
    border: 2px dashed #00C851;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    background: linear-gradient(135deg, rgba(0,200,81,0.05), rgba(0,126,51,0.05));
    margin: 1rem 0;
}

.saudi-badge {
    background: linear-gradient(45deg, #00C851, #007E33);
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    color: white;
    font-weight: 500;
    font-size: 0.8rem;
    display: inline-block;
    margin: 0.2rem;
}

.section-title {
    color: #007E33;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    border-bottom: 2px solid #00C851;
    padding-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

class SaudiPortfolioManager:
    """Simple Saudi Stock Portfolio Manager"""
    
    def __init__(self):
        # Initialize session state for portfolio data
        if 'portfolio_stocks' not in st.session_state:
            st.session_state.portfolio_stocks = []
        if 'portfolio_data' not in st.session_state:
            st.session_state.portfolio_data = None
        
        # Load Saudi stocks database
        self.saudi_stocks_db = self.load_saudi_stocks_database()
    
    def load_saudi_stocks_database(self):
        """Load Saudi stocks database from JSON file"""
        try:
            with open('saudi_stocks_database.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return basic database if file not found
            return {
                "2222": {"symbol": "2222.SR", "name_en": "SABIC", "sector": "Petrochemicals"},
                "1010": {"symbol": "1010.SR", "name_en": "Saudi National Bank", "sector": "Banking"},
                "2030": {"symbol": "2030.SR", "name_en": "Saudi Aramco", "sector": "Energy"},
                "2380": {"symbol": "2380.SR", "name_en": "Saudi Electricity", "sector": "Utilities"},
                "1120": {"symbol": "1120.SR", "name_en": "Al Rajhi Bank", "sector": "Banking"},
                "2170": {"symbol": "2170.SR", "name_en": "Almarai", "sector": "Consumer Staples"},
                "4030": {"symbol": "4030.SR", "name_en": "United Electronics", "sector": "Consumer Discretionary"},
                "2050": {"symbol": "2050.SR", "name_en": "Jarir Marketing", "sector": "Consumer Discretionary"},
                "1180": {"symbol": "1180.SR", "name_en": "National Medical Care", "sector": "Healthcare"},
                "2060": {"symbol": "2060.SR", "name_en": "Saudi Telecom", "sector": "Communication Services"}
            }
        except Exception:
            return {}
    
    def search_saudi_stocks(self, query):
        """Search Saudi stocks by symbol or name"""
        if not query:
            return []
        
        query = query.lower()
        results = []
        
        for symbol, data in self.saudi_stocks_db.items():
            if (query in symbol.lower() or 
                query in data.get('name_en', '').lower() or
                query in data.get('sector', '').lower()):
                
                results.append({
                    'symbol': symbol,
                    'name': data.get('name_en', f'Stock {symbol}'),
                    'sector': data.get('sector', 'Unknown'),
                    'full_symbol': data.get('symbol', f'{symbol}.SR')
                })
        
        return results[:10]  # Return top 10 matches
    
    def get_saudi_stock_price(self, symbol):
        """Get real-time price for Saudi stock"""
        try:
            # Ensure .SR suffix
            if not symbol.endswith('.SR'):
                symbol += '.SR'
            
            ticker = yf.Ticker(symbol)
            history = ticker.history(period="5d")
            
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                previous_close = history['Close'].iloc[-2] if len(history) > 1 else current_price
                change = current_price - previous_close
                change_percent = (change / previous_close) * 100 if previous_close > 0 else 0
                
                return {
                    'current_price': current_price,
                    'change': change,
                    'change_percent': change_percent,
                    'status': 'success'
                }
            else:
                return {'status': 'error', 'message': 'No data found'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def calculate_portfolio_metrics(self):
        """Calculate portfolio performance metrics"""
        if not st.session_state.portfolio_stocks:
            return None
        
        total_value = 0
        total_cost = 0
        positions = []
        
        for stock in st.session_state.portfolio_stocks:
            symbol = stock['symbol']
            shares = stock['shares']
            avg_price = stock['avg_price']
            
            # Get current price
            price_data = self.get_saudi_stock_price(symbol)
            
            if price_data['status'] == 'success':
                current_price = price_data['current_price']
                current_value = shares * current_price
                cost_basis = shares * avg_price
                pnl = current_value - cost_basis
                pnl_percent = (pnl / cost_basis) * 100 if cost_basis > 0 else 0
                
                positions.append({
                    'symbol': symbol,
                    'company_name': stock.get('company_name', symbol),
                    'shares': shares,
                    'avg_price': avg_price,
                    'current_price': current_price,
                    'current_value': current_value,
                    'cost_basis': cost_basis,
                    'pnl': pnl,
                    'pnl_percent': pnl_percent,
                    'sector': stock.get('sector', 'Unknown'),
                    'change': price_data['change'],
                    'change_percent': price_data['change_percent']
                })
                
                total_value += current_value
                total_cost += cost_basis
        
        total_pnl = total_value - total_cost
        total_pnl_percent = (total_pnl / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            'positions': positions,
            'total_value': total_value,
            'total_cost': total_cost,
            'total_pnl': total_pnl,
            'total_pnl_percent': total_pnl_percent,
            'num_positions': len(positions)
        }
    
    def create_excel_template(self):
        """Create Excel template for portfolio upload"""
        template_data = {
            'Symbol': ['2222', '1010', '2030', '1180', '2380'],
            'Company_Name': ['SABIC', 'Saudi National Bank', 'Saudi Aramco', 'National Medical Care', 'Saudi Electricity'],
            'Shares': [100, 500, 200, 150, 300],
            'Average_Price': [120.50, 85.75, 35.25, 180.00, 25.80],
            'Purchase_Date': ['2024-01-15', '2024-02-01', '2024-03-15', '2024-01-30', '2024-02-20'],
            'Sector': ['Petrochemicals', 'Banking', 'Energy', 'Healthcare', 'Utilities'],
            'Notes': ['Basic Industries', 'Financial Services', 'Oil & Gas', 'Healthcare Provider', 'Electricity']
        }
        
        template_df = pd.DataFrame(template_data)
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            template_df.to_excel(writer, sheet_name='Saudi_Portfolio', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Saudi_Portfolio']
            
            # Header format
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#00C851',
                'font_color': 'white',
                'border': 1
            })
            
            # Write headers with format
            for col_num, value in enumerate(template_df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Auto-adjust column widths
            for i, col in enumerate(template_df.columns):
                column_len = max(template_df[col].astype(str).str.len().max(), len(col)) + 2
                worksheet.set_column(i, i, column_len)
        
        return output.getvalue()

def main():
    """Main Saudi Portfolio Manager App"""
    
    manager = SaudiPortfolioManager()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🇸🇦 Saudi Stock Exchange Portfolio Manager</h1>
        <p>Simple & Clean Portfolio Management for Tadawul Stocks</p>
        <div>
            <span class="saudi-badge">🏛️ TADAWUL</span>
            <span class="saudi-badge">💰 SAR CURRENCY</span>
            <span class="saudi-badge">📊 REAL-TIME</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## 🎯 Portfolio Actions")
        
        page = st.radio(
            "Select Action:",
            ["📊 View Portfolio", "➕ Add Stocks", "📁 Upload Excel", "📥 Download Template"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📈 Quick Stats")
        
        metrics = manager.calculate_portfolio_metrics()
        if metrics:
            st.metric("Total Positions", metrics['num_positions'])
            st.metric("Portfolio Value", f"{metrics['total_value']:,.0f} SAR")
            pnl_color = "🟢" if metrics['total_pnl'] >= 0 else "🔴"
            st.metric("Total P&L", f"{pnl_color} {metrics['total_pnl']:,.0f} SAR")
        else:
            st.info("No positions added yet")
    
    # Main Content Area
    if page == "📊 View Portfolio":
        render_portfolio_view(manager)
    elif page == "➕ Add Stocks":
        render_add_stocks(manager)
    elif page == "📁 Upload Excel":
        render_upload_excel(manager)
    elif page == "📥 Download Template":
        render_download_template(manager)

def render_portfolio_view(manager):
    """Display portfolio overview and positions"""
    
    st.markdown('<h2 class="section-title">📊 Portfolio Overview</h2>', unsafe_allow_html=True)
    
    metrics = manager.calculate_portfolio_metrics()
    
    if not metrics or metrics['num_positions'] == 0:
        st.markdown("""
        <div class="portfolio-card">
            <h3>👋 Welcome to Your Saudi Portfolio Manager!</h3>
            <p>You haven't added any stocks yet. Get started by:</p>
            <ul>
                <li>➕ <strong>Add Stocks</strong> - Manually enter your Saudi stocks</li>
                <li>📁 <strong>Upload Excel</strong> - Import your complete portfolio</li>
                <li>📥 <strong>Download Template</strong> - Get the Excel template to fill out</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Portfolio Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Total Value</h3>
            <h2>{metrics['total_value']:,.0f} SAR</h2>
            <p>Current Market Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💵 Total Cost</h3>
            <h2>{metrics['total_cost']:,.0f} SAR</h2>
            <p>Purchase Cost Basis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pnl_class = "profit" if metrics['total_pnl'] >= 0 else "loss"
        pnl_symbol = "+" if metrics['total_pnl'] >= 0 else ""
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Total P&L</h3>
            <h2 class="{pnl_class}">{pnl_symbol}{metrics['total_pnl']:,.0f} SAR</h2>
            <p>{metrics['total_pnl_percent']:+.2f}% Return</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Positions</h3>
            <h2>{metrics['num_positions']}</h2>
            <p>Saudi Stocks</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Positions
    st.markdown('<h3 class="section-title">📋 Stock Positions</h3>', unsafe_allow_html=True)
    
    for position in metrics['positions']:
        pnl_class = "profit" if position['pnl'] >= 0 else "loss"
        change_class = "profit" if position['change'] >= 0 else "loss"
        pnl_symbol = "+" if position['pnl'] >= 0 else ""
        change_symbol = "+" if position['change'] >= 0 else ""
        
        st.markdown(f"""
        <div class="stock-row">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #007E33;">{position['symbol']}.SR - {position['company_name']}</h4>
                    <p style="margin: 0; color: #666;">{position['sector']} • {position['shares']:,.0f} shares @ {position['avg_price']:.2f} SAR avg</p>
                </div>
                <div style="text-align: right;">
                    <h4 style="margin: 0;">Current: {position['current_price']:.2f} SAR <span class="{change_class}">({change_symbol}{position['change']:.2f})</span></h4>
                    <p style="margin: 0;" class="{pnl_class}">P&L: {pnl_symbol}{position['pnl']:,.0f} SAR ({position['pnl_percent']:+.2f}%)</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_add_stocks(manager):
    """Add stocks manually to portfolio"""
    
    st.markdown('<h2 class="section-title">➕ Add Saudi Stocks to Portfolio</h2>', unsafe_allow_html=True)
    
    # Stock Search Feature
    st.markdown("""
    <div class="portfolio-card">
        <h3>🔍 Stock Search & Selection</h3>
        <p>Search for Saudi stocks by symbol, company name, or sector</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search box
    search_query = st.text_input(
        "🔍 Search Saudi Stocks", 
        placeholder="Type stock symbol (e.g. 2222, 1010) or company name (e.g. SABIC, Aramco)",
        help="Search by symbol, company name, or sector"
    )
    
    # Show search results
    if search_query:
        search_results = manager.search_saudi_stocks(search_query)
        
        if search_results:
            st.markdown("### 📋 Search Results:")
            
            for result in search_results:
                col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
                
                with col1:
                    st.write(f"**{result['symbol']}.SR**")
                with col2:
                    st.write(result['name'])
                with col3:
                    st.write(f"*{result['sector']}*")
                with col4:
                    if st.button("➕", key=f"select_{result['symbol']}", help="Select this stock"):
                        st.session_state['selected_symbol'] = result['symbol']
                        st.session_state['selected_name'] = result['name']
                        st.rerun()
        else:
            st.info("No stocks found. Try searching with different terms.")
    
    # Manual Entry Form
    st.markdown("""
    <div class="portfolio-card">
        <h3>📝 Enter Stock Details</h3>
        <p>Add your Saudi stocks manually. Selected stock from search will auto-fill below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_stock_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Auto-fill from search if selected
            default_symbol = st.session_state.get('selected_symbol', '')
            default_name = st.session_state.get('selected_name', '')
            
            symbol = st.text_input(
                "Stock Symbol",
                value=default_symbol,
                placeholder="e.g., 2222, 1010, 2030",
                help="Enter the Tadawul stock symbol (numbers only)"
            )
            
            company_name = st.text_input(
                "Company Name",
                value=default_name,
                placeholder="e.g., SABIC, Saudi National Bank",
                help="Company name for easier identification"
            )
            
            shares = st.number_input(
                "Number of Shares",
                min_value=1,
                step=1,
                help="Total shares you own"
            )
        
        with col2:
            avg_price = st.number_input(
                "Average Purchase Price (SAR)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                help="Your average purchase price in Saudi Riyals"
            )
            
            # Auto-fill sector if stock is known
            default_sector = "Other"
            if symbol and symbol in manager.saudi_stocks_db:
                default_sector = manager.saudi_stocks_db[symbol].get('sector', 'Other')
            
            sector = st.selectbox(
                "Sector",
                [
                    "Banking", "Petrochemicals", "Energy", "Healthcare", 
                    "Telecommunications", "Utilities", "Real Estate", 
                    "Materials", "Industrials", "Consumer Staples", 
                    "Consumer Discretionary", "Communication Services", 
                    "Technology", "Financials", "Other"
                ],
                index=0 if default_sector == "Other" else [
                    "Banking", "Petrochemicals", "Energy", "Healthcare", 
                    "Telecommunications", "Utilities", "Real Estate", 
                    "Materials", "Industrials", "Consumer Staples", 
                    "Consumer Discretionary", "Communication Services", 
                    "Technology", "Financials", "Other"
                ].index(default_sector) if default_sector in [
                    "Banking", "Petrochemicals", "Energy", "Healthcare", 
                    "Telecommunications", "Utilities", "Real Estate", 
                    "Materials", "Industrials", "Consumer Staples", 
                    "Consumer Discretionary", "Communication Services", 
                    "Technology", "Financials", "Other"
                ] else 0,
                help="Select the company's business sector"
            )
            
            purchase_date = st.date_input(
                "Purchase Date",
                value=date.today(),
                help="When you purchased this stock"
            )
        
        notes = st.text_area(
            "Notes (Optional)",
            placeholder="Any additional notes about this investment...",
            height=80
        )
        
        submitted = st.form_submit_button(
            "🚀 Add Stock to Portfolio",
            use_container_width=True
        )
        
        if submitted:
            if symbol and shares > 0 and avg_price > 0:
                # Validate symbol format (should be numbers)
                if not symbol.isdigit():
                    st.error("❌ Saudi stock symbols should be numbers only (e.g., 2222, 1010)")
                else:
                    # Add to portfolio
                    new_stock = {
                        'symbol': symbol,
                        'company_name': company_name if company_name else f"Stock {symbol}",
                        'shares': shares,
                        'avg_price': avg_price,
                        'sector': sector,
                        'purchase_date': purchase_date.strftime('%Y-%m-%d'),
                        'notes': notes,
                        'added_date': datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    
                    st.session_state.portfolio_stocks.append(new_stock)
                    
                    # Clear selected stock
                    if 'selected_symbol' in st.session_state:
                        del st.session_state['selected_symbol']
                    if 'selected_name' in st.session_state:
                        del st.session_state['selected_name']
                    
                    st.success(f"✅ Successfully added {shares} shares of {symbol}.SR ({company_name}) to your portfolio!")
                    
                    # Show current price if available
                    price_data = manager.get_saudi_stock_price(symbol)
                    if price_data['status'] == 'success':
                        current_value = shares * price_data['current_price']
                        cost_basis = shares * avg_price
                        pnl = current_value - cost_basis
                        st.info(f"📊 Current value: {current_value:,.0f} SAR | P&L: {pnl:+,.0f} SAR")
                    
                    st.rerun()
            else:
                st.error("❌ Please fill in all required fields (Symbol, Shares, Average Price)")
    
    # Show available sectors
    if manager.saudi_stocks_db:
        st.markdown('<h3 class="section-title">📊 Popular Saudi Stocks by Sector</h3>', unsafe_allow_html=True)
        
        sectors_data = {}
        for symbol, data in manager.saudi_stocks_db.items():
            sector = data.get('sector', 'Other')
            if sector not in sectors_data:
                sectors_data[sector] = []
            sectors_data[sector].append({
                'symbol': symbol,
                'name': data.get('name_en', f'Stock {symbol}')
            })
        
        # Show top sectors with examples
        for sector, stocks in list(sectors_data.items())[:6]:  # Show 6 sectors
            with st.expander(f"📈 {sector} ({len(stocks)} stocks)"):
                for stock in stocks[:5]:  # Show 5 stocks per sector
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        st.write(f"**{stock['symbol']}**")
                    with col2:
                        st.write(stock['name'])
                    with col3:
                        if st.button("Select", key=f"quick_{stock['symbol']}", help="Quick select this stock"):
                            st.session_state['selected_symbol'] = stock['symbol']
                            st.session_state['selected_name'] = stock['name']
                            st.rerun()
    
    # Show current portfolio summary
    if st.session_state.portfolio_stocks:
        st.markdown('<h3 class="section-title">📊 Current Portfolio</h3>', unsafe_allow_html=True)
        
        for i, stock in enumerate(st.session_state.portfolio_stocks):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{stock['symbol']}.SR** - {stock['company_name']}")
                st.write(f"{stock['shares']:,.0f} shares @ {stock['avg_price']:.2f} SAR • {stock['sector']}")
            
            with col2:
                price_data = manager.get_saudi_stock_price(stock['symbol'])
                if price_data['status'] == 'success':
                    current_value = stock['shares'] * price_data['current_price']
                    st.metric("Current Value", f"{current_value:,.0f} SAR")
                else:
                    st.write("Price unavailable")
            
            with col3:
                if st.button(f"🗑️ Remove", key=f"remove_{i}"):
                    st.session_state.portfolio_stocks.pop(i)
                    st.rerun()
        
        # Clear all button
        if st.button("🗑️ Clear All Stocks", type="secondary"):
            st.session_state.portfolio_stocks = []
            st.rerun()

def render_upload_excel(manager):
    """Upload portfolio from Excel file"""
    
    st.markdown('<h2 class="section-title">📁 Upload Portfolio from Excel</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-area">
        <h3>📊 Upload Your Saudi Portfolio</h3>
        <p>Upload an Excel file with your Saudi stock positions</p>
        <p><strong>Required columns:</strong> Symbol, Shares, Average_Price</p>
        <p><strong>Optional columns:</strong> Company_Name, Sector, Purchase_Date, Notes</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose Excel file (.xlsx or .xls)",
        type=['xlsx', 'xls'],
        help="Upload your portfolio Excel file"
    )
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            st.markdown("### 👀 File Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Validate required columns
            required_cols = ['Symbol', 'Shares', 'Average_Price']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
                st.info("Required columns: Symbol, Shares, Average_Price")
                return
            
            # Validate data
            if df.empty:
                st.error("❌ The Excel file is empty")
                return
            
            # Process the data
            st.markdown("### ✅ Data Validation")
            
            valid_rows = 0
            errors = []
            
            for index, row in df.iterrows():
                # Basic validation
                if pd.isna(row['Symbol']) or pd.isna(row['Shares']) or pd.isna(row['Average_Price']):
                    errors.append(f"Row {index + 2}: Missing required data")
                    continue
                
                if not str(row['Symbol']).isdigit():
                    errors.append(f"Row {index + 2}: Symbol should be numbers only")
                    continue
                
                if row['Shares'] <= 0 or row['Average_Price'] <= 0:
                    errors.append(f"Row {index + 2}: Shares and price must be positive")
                    continue
                
                valid_rows += 1
            
            if errors:
                st.warning(f"⚠️ Found {len(errors)} errors:")
                for error in errors[:5]:  # Show first 5 errors
                    st.write(f"• {error}")
                if len(errors) > 5:
                    st.write(f"• ... and {len(errors) - 5} more errors")
            
            st.success(f"✅ {valid_rows} valid rows found")
            
            if valid_rows > 0:
                if st.button("🚀 Import Portfolio", type="primary", use_container_width=True):
                    # Clear existing portfolio
                    st.session_state.portfolio_stocks = []
                    
                    # Import valid rows
                    imported = 0
                    for index, row in df.iterrows():
                        # Skip invalid rows
                        if (pd.isna(row['Symbol']) or pd.isna(row['Shares']) or 
                            pd.isna(row['Average_Price']) or not str(row['Symbol']).isdigit() or
                            row['Shares'] <= 0 or row['Average_Price'] <= 0):
                            continue
                        
                        stock = {
                            'symbol': str(row['Symbol']),
                            'company_name': row.get('Company_Name', f"Stock {row['Symbol']}") if not pd.isna(row.get('Company_Name')) else f"Stock {row['Symbol']}",
                            'shares': float(row['Shares']),
                            'avg_price': float(row['Average_Price']),
                            'sector': row.get('Sector', 'Other') if not pd.isna(row.get('Sector')) else 'Other',
                            'purchase_date': str(row.get('Purchase_Date', '2024-01-01')) if not pd.isna(row.get('Purchase_Date')) else '2024-01-01',
                            'notes': str(row.get('Notes', '')) if not pd.isna(row.get('Notes')) else '',
                            'added_date': datetime.now().strftime('%Y-%m-%d %H:%M')
                        }
                        
                        st.session_state.portfolio_stocks.append(stock)
                        imported += 1
                    
                    st.success(f"🎉 Successfully imported {imported} stocks to your portfolio!")
                    
                    # Calculate total value
                    metrics = manager.calculate_portfolio_metrics()
                    if metrics:
                        st.info(f"📊 Portfolio value: {metrics['total_value']:,.0f} SAR | P&L: {metrics['total_pnl']:+,.0f} SAR")
                    
                    st.balloons()
        
        except Exception as e:
            st.error(f"❌ Error reading Excel file: {str(e)}")
            st.info("Please make sure your file is a valid Excel format (.xlsx or .xls)")

def render_download_template(manager):
    """Download Excel template"""
    
    st.markdown('<h2 class="section-title">📥 Download Excel Template</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="portfolio-card">
        <h3>📋 Portfolio Excel Template</h3>
        <p>Download our pre-formatted Excel template with sample Saudi stocks data.</p>
        <p><strong>Includes:</strong></p>
        <ul>
            <li>✅ Proper column headers and formatting</li>
            <li>✅ Sample data with popular Saudi stocks</li>
            <li>✅ Instructions and field descriptions</li>
            <li>✅ Ready-to-use format for upload</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate template
    template_data = manager.create_excel_template()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.download_button(
            label="📥 Download Saudi Portfolio Template",
            data=template_data,
            file_name=f"saudi_portfolio_template_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        st.info("💡 Fill out the template with your stocks and upload it back!")
    
    # Show template preview
    st.markdown("### 👀 Template Preview")
    
    preview_data = {
        'Symbol': ['2222', '1010', '2030', '1180', '2380'],
        'Company_Name': ['SABIC', 'Saudi National Bank', 'Saudi Aramco', 'National Medical Care', 'Saudi Electricity'],
        'Shares': [100, 500, 200, 150, 300],
        'Average_Price': [120.50, 85.75, 35.25, 180.00, 25.80],
        'Sector': ['Petrochemicals', 'Banking', 'Energy', 'Healthcare', 'Utilities']
    }
    
    preview_df = pd.DataFrame(preview_data)
    st.dataframe(preview_df, use_container_width=True)
    
    st.markdown("""
    <div class="portfolio-card">
        <h4>📝 Instructions:</h4>
        <ol>
            <li><strong>Symbol:</strong> Saudi stock symbol (numbers only, e.g., 2222, 1010)</li>
            <li><strong>Company_Name:</strong> Optional company name for identification</li>
            <li><strong>Shares:</strong> Number of shares you own</li>
            <li><strong>Average_Price:</strong> Your average purchase price in SAR</li>
            <li><strong>Sector:</strong> Company's business sector</li>
            <li><strong>Purchase_Date:</strong> When you bought the stock (optional)</li>
            <li><strong>Notes:</strong> Any additional notes (optional)</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
