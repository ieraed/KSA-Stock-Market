"""
Minimal dividend fetcher that imports dependencies only when needed
"""

def fetch_dividend_table():
    """
    Fetch dividend data from Saudi Exchange website
    Returns a pandas DataFrame with dividend information
    
    Note: This function makes live web requests and may fail if the website
    blocks automated access or if there are network issues.
    """
    # Import dependencies only when function is called
    try:
        import pandas as pd
        import requests
        from bs4 import BeautifulSoup
    except ImportError as e:
        raise Exception(f"Required dependencies not installed: {e}")
    
    url = "https://www.saudiexchange.sa/wps/portal/saudiexchange/newsandreports/issuer-financial-calendars/dividends?locale=en"
    
    # Enhanced headers to avoid blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    try:
        # Add delay and retry logic
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 403:
            raise Exception("Access blocked by website. The Saudi Exchange website is restricting automated access. Please try again later or contact support for API access.")
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: Unable to fetch data from Saudi Exchange website")
        
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")
        
        if not table:
            raise Exception("No dividend table found on the website. The page structure may have changed.")
        
        rows = table.find_all("tr")[1:]  # Skip header
        
        if not rows:
            raise Exception("No dividend data found in the table.")
        
        data = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                data.append({
                    "Symbol": cols[0].text.strip(),
                    "Company": cols[1].text.strip(),
                    "Announcement Date": cols[2].text.strip(),
                    "Eligibility Date": cols[3].text.strip(),
                    "Distribution Method": cols[4].text.strip(),
                    "Distribution Date": cols[5].text.strip(),
                    "Dividend Amount": cols[6].text.strip() if len(cols) > 6 else "N/A"
                })
        
        if not data:
            raise Exception("No dividend records extracted from the website.")
        
        df = pd.DataFrame(data)
        df["Distribution Date"] = pd.to_datetime(df["Distribution Date"], errors="coerce")
        df["Announcement Date"] = pd.to_datetime(df["Announcement Date"], errors="coerce")
        df["Eligibility Date"] = pd.to_datetime(df["Eligibility Date"], errors="coerce")
        
        return df
        
    except requests.exceptions.Timeout:
        raise Exception("Request timeout. The Saudi Exchange website is not responding. Please try again later.")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection error. Please check your internet connection.")
    except Exception as e:
        raise Exception(f"Error fetching dividend data: {str(e)}")

# Test function to verify module can be imported
def test_import():
    return "fetch_dividends module imported successfully"
