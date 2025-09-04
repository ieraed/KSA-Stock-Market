import pandas as pd

def summarize_user_dividends(df, user_symbols):
    user_df = df[df["Symbol"].isin(user_symbols)]
    today = pd.Timestamp.today()

    past = user_df[user_df["Distribution Date"] < today]
    upcoming = user_df[user_df["Distribution Date"] >= today]

    return {
        "past": past.sort_values("Distribution Date", ascending=False),
        "upcoming": upcoming.sort_values("Distribution Date")
    }

def summarize_market_upcoming(df):
    today = pd.Timestamp.today()
    return df[df["Distribution Date"] >= today].sort_values("Distribution Date")
