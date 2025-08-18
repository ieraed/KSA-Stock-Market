#!/usr/bin/env python3
"""
📊 TADAWUL SECTOR ANALYZER
Interactive Sector Analysis with Clickable Interface

Creates a comprehensive sector breakdown with clickable tables
showing all stocks within each sector.
"""

import streamlit as st
import pandas as pd
import json
from collections import defaultdict
import plotly.express as px
import plotly.graph_objects as go

def load_stock_database():
    """Load the Saudi stocks database"""
    try:
        with open('data/saudi_stocks_database.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("❌ Database file not found!")
        return {}

def create_sector_summary(stocks_db):
    """Create sector summary statistics"""
    sector_stats = defaultdict(list)
    
    for symbol, data in stocks_db.items():
        sector = data.get('sector', 'Unknown')
        stock_info = {
            'Symbol': symbol,
            'Company Name (EN)': data.get('name_en', 'Unknown'),
            'Company Name (AR)': data.get('name_ar', 'غير محدد'),
            'Sector': sector
        }
        sector_stats[sector].append(stock_info)
    
    return dict(sector_stats)

def main():
    st.set_page_config(
        page_title="📊 Tadawul Sector Analyzer",
        page_icon="📊",
        layout="wide"
    )
    
    # Header
    st.markdown("""
    # 📊 **TADAWUL SECTOR ANALYZER**
    ### Complete Saudi Exchange (Tadawul) Sector Breakdown with Interactive Tables
    
    ---
    """)
    
    # Load data
    stocks_db = load_stock_database()
    if not stocks_db:
        return
    
    sector_data = create_sector_summary(stocks_db)
    
    # Summary Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📈 Total Stocks", len(stocks_db))
    
    with col2:
        st.metric("🏢 Total Sectors", len(sector_data))
    
    with col3:
        largest_sector = max(sector_data.items(), key=lambda x: len(x[1]))
        st.metric("🥇 Largest Sector", f"{largest_sector[0]} ({len(largest_sector[1])})")
    
    # Sector Overview Chart
    st.markdown("## 📊 **Sector Distribution Overview**")
    
    sector_counts = {sector: len(stocks) for sector, stocks in sector_data.items()}
    
    # Create pie chart
    fig_pie = px.pie(
        values=list(sector_counts.values()),
        names=list(sector_counts.keys()),
        title="Stock Distribution by Sector",
        height=500
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    # Create bar chart
    fig_bar = px.bar(
        x=list(sector_counts.keys()),
        y=list(sector_counts.values()),
        title="Number of Stocks per Sector",
        labels={'x': 'Sector', 'y': 'Number of Stocks'},
        height=500
    )
    fig_bar.update_xaxes(tickangle=45)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Clickable Sector Summary Table
    st.markdown("## 🔍 **Clickable Sector Summary**")
    st.markdown("*Click on any sector below to see all stocks in that sector*")
    
    # Create summary dataframe
    summary_data = []
    for sector, stocks in sorted(sector_data.items()):
        summary_data.append({
            'Sector': sector,
            'Number of Stocks': len(stocks),
            'Sample Companies': ', '.join([stock['Company Name (EN)'] for stock in stocks[:3]]) + 
                              (f' ... and {len(stocks) - 3} more' if len(stocks) > 3 else '')
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Display summary table with selection
    event = st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Handle sector selection
    if event.selection and event.selection['rows']:
        selected_row = event.selection['rows'][0]
        selected_sector = summary_df.iloc[selected_row]['Sector']
        
        st.markdown(f"## 🏢 **{selected_sector} Sector Details**")
        st.markdown(f"**Total Stocks: {len(sector_data[selected_sector])}**")
        
        # Create detailed dataframe for selected sector
        sector_stocks = sector_data[selected_sector]
        detailed_df = pd.DataFrame(sector_stocks)
        
        # Display detailed table
        st.dataframe(
            detailed_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Symbol': st.column_config.TextColumn('Stock Symbol', width='small'),
                'Company Name (EN)': st.column_config.TextColumn('Company Name (English)', width='large'),
                'Company Name (AR)': st.column_config.TextColumn('Company Name (Arabic)', width='large'),
                'Sector': st.column_config.TextColumn('Sector', width='medium')
            }
        )
        
        # Download button for sector data
        csv = detailed_df.to_csv(index=False)
        st.download_button(
            label=f"📥 Download {selected_sector} Sector Data (CSV)",
            data=csv,
            file_name=f"tadawul_{selected_sector.lower().replace(' ', '_')}_stocks.csv",
            mime="text/csv"
        )
    
    # Special Issues Section
    st.markdown("## ⚠️ **Identified Issues & Recommendations**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 **Stock 9642 Analysis**")
        if '9642' in stocks_db:
            stock_9642 = stocks_db['9642']
            st.success(f"✅ **Found:** {stock_9642.get('name_en', 'Unknown')}")
            st.info(f"📊 **Sector:** {stock_9642.get('sector', 'Unknown')}")
            st.info(f"🏷️ **Arabic Name:** {stock_9642.get('name_ar', 'غير محدد')}")
        else:
            st.error("❌ Stock 9642 not found in database")
    
    with col2:
        st.markdown("### 🏢 **BAWAN (1302) Sector Issue**")
        if '1302' in stocks_db:
            bawan_data = stocks_db['1302']
            st.warning(f"⚠️ **Current Sector:** {bawan_data.get('sector', 'Unknown')}")
            st.info(f"🏷️ **Company:** {bawan_data.get('name_en', 'Unknown')}")
            st.markdown("**Official TASI may classify this differently**")
        else:
            st.error("❌ BAWAN (1302) not found in database")
    
    # Data Source Information
    st.markdown("## 📋 **Data Source & Update Recommendations**")
    
    st.info("""
    **Current Issues Identified:**
    1. **Sector Classification Discrepancies** - Some stocks may have outdated sector classifications
    2. **Missing Official TASI Mapping** - Need to update with official Saudi Exchange sector data
    3. **Data Source Inconsistency** - Multiple sources may have different classifications
    
    **Recommended Actions:**
    1. 📄 **Upload your official TASI sector file** to update classifications
    2. 🔄 **Cross-reference with saudiexchange.sa** for latest sector data  
    3. 🏷️ **Standardize sector naming** to match official TASI classifications
    """)
    
    # File upload section
    st.markdown("### 📤 **Upload Official TASI Sector Data**")
    uploaded_file = st.file_uploader(
        "Upload your CSV/Excel file with Symbol, Company Name, and Sector columns",
        type=['csv', 'xlsx', 'xls'],
        help="Please ensure your file has columns for Symbol, Company Name, and Sector"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success("✅ File uploaded successfully!")
            st.markdown("**Preview of uploaded data:**")
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("🔄 Update Database with New Sector Data"):
                st.info("This would update the database - implement update logic here")
                
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
    
    # Export All Data
    st.markdown("## 📥 **Export Options**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Export complete sector analysis
        all_data = []
        for sector, stocks in sector_data.items():
            for stock in stocks:
                all_data.append(stock)
        
        complete_df = pd.DataFrame(all_data)
        csv_all = complete_df.to_csv(index=False)
        
        st.download_button(
            label="📊 Complete Sector Analysis (CSV)",
            data=csv_all,
            file_name="tadawul_complete_sector_analysis.csv",
            mime="text/csv"
        )
    
    with col2:
        # Export sector summary
        summary_csv = summary_df.to_csv(index=False)
        st.download_button(
            label="📋 Sector Summary (CSV)",
            data=summary_csv,
            file_name="tadawul_sector_summary.csv",
            mime="text/csv"
        )
    
    with col3:
        # Export issues report
        issues_data = []
        
        # Check for potential issues
        for symbol, data in stocks_db.items():
            if data.get('sector') == 'Unknown' or not data.get('sector'):
                issues_data.append({
                    'Symbol': symbol,
                    'Company': data.get('name_en', 'Unknown'),
                    'Issue': 'Missing or Unknown Sector',
                    'Current Sector': data.get('sector', 'Unknown')
                })
        
        if issues_data:
            issues_df = pd.DataFrame(issues_data)
            issues_csv = issues_df.to_csv(index=False)
            
            st.download_button(
                label="⚠️ Issues Report (CSV)",
                data=issues_csv,
                file_name="tadawul_sector_issues.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No sector issues detected!")

if __name__ == "__main__":
    main()
