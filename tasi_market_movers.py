import pandas as pd
import requests

# ✅ Replace with actual Tadawul API or scraping logic
def fetch_tasi_data():
    # Simulated full market data
data = [
    {"Symbol": "1120", "Company": "ALRAJHI", "Price": 93.55, "Change": 1.2},
    {"Symbol": "2222", "Company": "ARAMCO", "Price": 31.95, "Change": -0.4},
    {"Symbol": "7010", "Company": "STC", "Price": 43.95, "Change": 0.2},
    {"Symbol": "1050", "Company": "ALINMA", "Price": 29.10, "Change": 0.8},
    {"Symbol": "1060", "Company": "SAAB", "Price": 36.75, "Change": -1.1},
    {"Symbol": "1211", "Company": "MAADEN", "Price": 56.30, "Change": 2.3},
    {"Symbol": "2010", "Company": "SABIC", "Price": 88.40, "Change": -0.9},
    {"Symbol": "2020", "Company": "SAVOLA", "Price": 32.20, "Change": 1.5},
    {"Symbol": "2040", "Company": "TASNEE", "Price": 15.80, "Change": -0.6},
    {"Symbol": "2080", "Company": "SIPCHEM", "Price": 18.90, "Change": 0.4},
    {"Symbol": "2350", "Company": "SAUDI CABLE", "Price": 6.75, "Change": -2.1},
    {"Symbol": "3002", "Company": "ALMARAI", "Price": 55.60, "Change": 1.0},
    {"Symbol": "4003", "Company": "ASEEL", "Price": 22.10, "Change": 0.7},
    {"Symbol": "4190", "Company": "JARIR", "Price": 180.00, "Change": -0.3},
    {"Symbol": "4200", "Company": "ALDREES", "Price": 88.90, "Change": 1.8},
    {"Symbol": "4260", "Company": "SAUDI GERMAN HEALTH", "Price": 34.20, "Change": -1.4},
    {"Symbol": "4290", "Company": "ALHOKAIR", "Price": 17.50, "Change": 0.9},
    {"Symbol": "4330", "Company": "RIYAD REIT", "Price": 10.20, "Change": 0.2},
    {"Symbol": "6010", "Company": "NADIC", "Price": 23.40, "Change": -0.5},
    {"Symbol": "6050", "Company": "SAUDI FISHERIES", "Price": 18.75, "Change": 2.0},
]

// Tips for Scaling
//You can automate this using Tadawul’s Market Data Feed or scrape the full list using BeautifulSoup or Selenium.

// Add fields like Volume, Value, Sector, and MarketCap if you plan to build deeper analytics or committee filters.

//Consider storing this in a CSV or database for easier updates and dashboard integration.



def fetch_tasi_data():
    return pd.DataFrame(data)

def get_top_gainers(df, n=10):
    return df.sort_values(by="Change", ascending=False).head(n)

def get_top_losers(df, n=10):
    return df.sort_values(by="Change").head(n)

def get_movers_by_volume(df, n=10):
    return df.sort_values(by="Volume", ascending=False).head(n)

def get_movers_by_value(df, n=10):
    return df.sort_values(by="Value", ascending=False).head(n)

def main():
    df = fetch_tasi_data()

    print("📈 Top Gainers:")
    print(get_top_gainers(df))

    print("\n📉 Top Losers:")
    print(get_top_losers(df))

    print("\n📊 Movers by Volume:")
    print(get_movers_by_volume(df))

    print("\n💰 Movers by Value:")
    print(get_movers_by_value(df))

if __name__ == "__main__":
    main()
