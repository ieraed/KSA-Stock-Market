#!/usr/bin/env python3
"""
Script to fix the corrupted display_top_gainers_losers function
"""

def get_clean_function():
    return '''def display_top_gainers_losers():
    """Display top gainers and losers tables with optimized performance"""
    st.markdown("""
    <div class="section-header">
         Saudi Market Performance - Live Data from TASI (Saudi Exchange)
    </div>
    """, unsafe_allow_html=True)
    
    # Display data source information
    st.info("""
     **Optimized Mode**: Using instant market data with live fallbacks
     **Data Source**: TASI data with real-time updates
     **Status**: High-performance mode enabled for best user experience
    """)
    
    # Get market data using optimized approach
    with st.spinner(" Loading market data..."):
        market_data = get_instant_market_data()
        
        if market_data and market_data.get('success'):
            st.success(f" Market data loaded instantly! ({market_data.get('total_stocks_fetched', 'unknown')} stocks)")
            
            # Display the tables - Top Gainers and Losers
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("###  Top 10 Gainers (TASI)")
                if market_data.get('top_gainers'):
                    gainers_df = pd.DataFrame(market_data['top_gainers'])
                    if not gainers_df.empty:
                        # Take first 10 or show what we have
                        gainers_df = gainers_df.head(10)
                        
                        # Format the DataFrame for display
                        display_cols = ['symbol', 'name', 'current_price', 'change_pct']
                        if all(col in gainers_df.columns for col in display_cols):
                            gainers_display = gainers_df[display_cols].copy()
                            gainers_display['symbol'] = gainers_display['symbol'].astype(str).str.replace('.SR', '')
                            gainers_display['change_pct'] = gainers_display['change_pct'].apply(lambda x: f"+{x:.2f}%" if x >= 0 else f"{x:.2f}%")
                            gainers_display['current_price'] = gainers_display['current_price'].apply(lambda x: f"{x:.2f} SAR")
                            gainers_display.columns = ['Symbol', 'Company', 'Price', 'Change']
                            
                            st.dataframe(gainers_display, use_container_width=True, hide_index=True)
                        else:
                            st.dataframe(gainers_df.head(10), use_container_width=True, hide_index=True)
                    else:
                        st.warning("No gainers data available")
                else:
                    st.warning("No gainers data available from live sources")
            
            with col2:
                st.markdown("###  Top 10 Losers (TASI)")
                if market_data.get('top_losers'):
                    losers_df = pd.DataFrame(market_data['top_losers'])
                    if not losers_df.empty:
                        # Take first 10 or show what we have
                        losers_df = losers_df.head(10)
                        
                        # Format the DataFrame for display
                        display_cols = ['symbol', 'name', 'current_price', 'change_pct']
                        if all(col in losers_df.columns for col in display_cols):
                            losers_display = losers_df[display_cols].copy()
                            losers_display['symbol'] = losers_display['symbol'].astype(str).str.replace('.SR', '')
                            losers_display['change_pct'] = losers_display['change_pct'].apply(lambda x: f"{x:.2f}%")
                            losers_display['current_price'] = losers_display['current_price'].apply(lambda x: f"{x:.2f} SAR")
                            losers_display.columns = ['Symbol', 'Company', 'Price', 'Change']
                            
                            st.dataframe(losers_display, use_container_width=True, hide_index=True)
                        else:
                            st.dataframe(losers_df.head(10), use_container_width=True, hide_index=True)
                    else:
                        st.warning("No losers data available")
                else:
                    st.warning("No losers data available from live sources")
            
            st.markdown("---")
            
            # Market data source information
            st.success(f"""
            **Primary Source**: {market_data.get('data_source', 'Live Market Data')}
            **Reliability**: High - Real-time TASI market data
            **Stocks Processed**: {market_data.get('total_stocks_fetched', 'Unknown')} companies
            **Last Updated**: {market_data.get('timestamp', 'Unknown')}
            """)
            
        else:
            # Fallback to alternative data sources
            with st.spinner(" Trying alternative data sources..."):
                if SAUDI_EXCHANGE_AVAILABLE:
                    try:
                        market_data = get_market_summary()
                        if market_data and market_data.get('success'):
                            st.info(" Market data loaded from alternative source")
                            # Display basic tables
                            if market_data.get('top_gainers') or market_data.get('top_losers'):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("###  Top Gainers")
                                    if market_data.get('top_gainers'):
                                        st.dataframe(pd.DataFrame(market_data['top_gainers']).head(10), use_container_width=True)
                                    else:
                                        st.warning("No gainers data available")
                                
                                with col2:
                                    st.markdown("###  Top Losers") 
                                    if market_data.get('top_losers'):
                                        st.dataframe(pd.DataFrame(market_data['top_losers']).head(10), use_container_width=True)
                                    else:
                                        st.warning("No losers data available")
                        else:
                            st.error(" Could not fetch market data from any source")
                            st.warning(" Please check your internet connection")
                    except Exception as e:
                        st.error(f" Error fetching market data: {str(e)}")
                else:
                    st.error(" Saudi Exchange fetcher not available")
    
    # Manual stock price test section
    with st.expander(" Test Individual Stock Prices (Live Data)"):
        test_symbol = st.text_input("Enter Saudi stock symbol (e.g., 2222, 1120, 4190):", "2222")
        
        if st.button(" Fetch Live Price"):
            if test_symbol:
                with st.spinner(f" Fetching live data for {test_symbol}..."):
                    result = get_stock_price(test_symbol) if SAUDI_EXCHANGE_AVAILABLE else None
                    
                    if result and result.get('success'):
                        st.success(f"""
                         **Symbol**: {result.get('symbol', test_symbol)}
                         **Company**: {result.get('company_name', 'Unknown')}
                         **Current Price**: {result.get('current_price', 'N/A')} SAR
                         **Change**: {result.get('change_pct', 'N/A')}%
                         **Source**: {result.get('data_source', 'Unknown')}
                         **Time**: {result.get('timestamp', 'N/A')}
                        """)
                    else:
                        error_msg = result.get('error', 'Unknown error') if result else 'Fetcher not available'
                        st.error(f" Failed to fetch live data for {test_symbol}: {error_msg}")
            else:
                st.warning("Please enter a stock symbol")
'''

def fix_file():
    # Read the original file
    with open('apps/enhanced_saudi_app_v2.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the start and end of the corrupted function
    start_marker = "def display_top_gainers_losers():"
    end_marker = "def main():"
    
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        print("Could not find function markers")
        return False
    
    # Replace the corrupted function with the clean version
    before_function = content[:start_index]
    after_function = content[end_index:]
    
    clean_function = get_clean_function()
    
    new_content = before_function + clean_function + "\n\n" + after_function
    
    # Write the fixed file
    with open('apps/enhanced_saudi_app_v2.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Function fixed successfully!")
    return True

if __name__ == "__main__":
    fix_file()
