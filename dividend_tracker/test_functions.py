"""
Test version of dividend tracker that doesn't make web requests during import
"""

import pandas as pd

def fetch_dividend_table_test():
    """Test version that returns sample data instead of making web requests"""
    # Return sample dividend data for testing
    sample_data = {
        'Symbol': ['1234', '2222', '1180'],
        'Company Name': ['Test Company A', 'Test Company B', 'Test Company C'],
        'Announcement Date': ['2024-01-01', '2024-01-15', '2024-02-01'],
        'Ex-Date': ['2024-01-15', '2024-02-01', '2024-02-15'],
        'Distribution Method': ['Cash', 'Cash', 'Cash'],
        'Distribution Date': ['2024-01-20', '2024-02-05', '2024-02-20'],
        'Dividend Yield (%)': [5.2, 3.8, 4.5]
    }
    
    df = pd.DataFrame(sample_data)
    df['Ex-Date'] = pd.to_datetime(df['Ex-Date'])
    df['Distribution Date'] = pd.to_datetime(df['Distribution Date'])
    df['Announcement Date'] = pd.to_datetime(df['Announcement Date'])
    
    return df

def style_dividend_table_test(df):
    """Test version of styling function"""
    return df.style.set_properties(**{
        'background-color': '#f9f9f9',
        'color': '#333',
        'border-color': '#ccc'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#004c97'), ('color', 'white')]
    }])

def summarize_user_dividends_test(df, user_symbols):
    """Test version of summarize function"""
    user_df = df[df["Symbol"].isin(user_symbols)]
    today = pd.Timestamp.today()

    past = user_df[user_df["Distribution Date"] < today]
    upcoming = user_df[user_df["Distribution Date"] >= today]

    return {
        "past": past.sort_values("Distribution Date", ascending=False),
        "upcoming": upcoming.sort_values("Distribution Date")
    }
