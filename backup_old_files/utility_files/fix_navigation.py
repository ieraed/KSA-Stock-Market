#!/usr/bin/env python3
"""
Quick script to fix navigation menu character encoding issues
"""

def fix_navigation_menu():
    """Fix the navigation menu by replacing corrupted characters"""
    
    # Read the file
    with open('web_launcher_new.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define the correct navigation menu
    correct_navigation = '''    # Navigation
    pages = {
        "🌟 Register/Welcome": "User Registration",
        "🎯 Quick Actions": "Quick Actions",
        "🔍 Signal Generation": "Signal Generation",
        "📺 My Live Dashboard": "Live Dashboard", 
        "🔍 Stock Screener": "Stock Screener",
        "🎯 Market Screening": "Market Screening",
        "💼 Portfolio Analysis": "Portfolio Analysis",
        "📝 Portfolio Management": "Portfolio Management",
        "💰 Corporate Actions": "Corporate Actions",
        "📈 Technical Analysis": "Technical Analysis",
        "📊 Market Data": "Market Data",
        "🎛️ Original Dashboard": "Original Dashboard"
    }'''
    
    # Find and replace the navigation section
    import re
    
    # Pattern to match the pages dictionary
    pattern = r'    # Navigation\s*\n\s*pages = \{[^}]+\}'
    
    # Replace with correct navigation
    new_content = re.sub(pattern, correct_navigation, content, flags=re.DOTALL)
    
    # Write back to file
    with open('web_launcher_new.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Navigation menu fixed successfully!")
    print("🎯 Market Screening option has been added to the menu")

if __name__ == "__main__":
    fix_navigation_menu()
