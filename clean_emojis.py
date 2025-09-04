import re

# Script to clean up corrupted emojis in enhanced_saudi_app_v2.py
def clean_emoji_corruption():
    file_path = r"c:\Users\raed1\OneDrive\Saudi Stock Market App\apps\enhanced_saudi_app_v2.py"
    
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Navigation options cleanup
    navigation_replacements = {
        '"📊 Portfolio Overview"': '"Portfolio Overview"',
        '"⚙️ Portfolio Setup"': '"Portfolio Setup"',
        '"🤖 AI Trading Center"': '"AI Trading Center"',
        '"📈 Market Analysis"': '"Market Analysis"',
        '"📊 Performance Tracker"': '"Performance Tracker"',
        '"🔍 Stock Research"': '"Stock Research"',
        '"📋 Analytics Dashboard"': '"Analytics Dashboard"',
        '"🏭 Sector Analyzer"': '"Sector Analyzer"',
        '"⚠️ Risk Management"': '"Risk Management"',
        '"🎨 Theme Customizer"': '"Theme Customizer"',
    }
    
    # Handle corrupted characters (� replacements)
    corruption_patterns = [
        (r'"[^"]*� Dividend Tracker[^"]*"', '"Dividend Tracker"'),
        (r'"[^"]*�📁 Import/Export Data[^"]*"', '"Import/Export Data"'),
        (r'"[^"]*� Import/Export Data[^"]*"', '"Import/Export Data"'),
    ]
    
    # Apply navigation replacements
    for old, new in navigation_replacements.items():
        content = content.replace(old, new)
    
    # Apply corruption pattern fixes using regex
    for pattern, replacement in corruption_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Fix conditional statements
    conditional_replacements = {
        'if selected_page == "📊 Portfolio Overview"': 'if selected_page == "Portfolio Overview"',
        'elif selected_page == "⚙️ Portfolio Setup"': 'elif selected_page == "Portfolio Setup"',
        'elif selected_page == "🤖 AI Trading Center"': 'elif selected_page == "AI Trading Center"',
        'elif selected_page == "📈 Market Analysis"': 'elif selected_page == "Market Analysis"',
        'elif selected_page == "📊 Performance Tracker"': 'elif selected_page == "Performance Tracker"',
        'elif selected_page == "🔍 Stock Research"': 'elif selected_page == "Stock Research"',
        'elif selected_page == "📋 Analytics Dashboard"': 'elif selected_page == "Analytics Dashboard"',
        'elif selected_page == "🏭 Sector Analyzer"': 'elif selected_page == "Sector Analyzer"',
        'elif selected_page == "⚠️ Risk Management"': 'elif selected_page == "Risk Management"',
        'elif selected_page == "🎨 Theme Customizer"': 'elif selected_page == "Theme Customizer"',
    }
    
    # Handle corrupted conditional statements
    conditional_corruption_patterns = [
        (r'elif selected_page == "[^"]*� Dividend Tracker[^"]*"', 'elif selected_page == "Dividend Tracker"'),
        (r'elif selected_page == "[^"]*�📁 Import/Export Data[^"]*"', 'elif selected_page == "Import/Export Data"'),
        (r'elif selected_page == "[^"]*� Import/Export Data[^"]*"', 'elif selected_page == "Import/Export Data"'),
    ]
    
    # Apply conditional replacements
    for old, new in conditional_replacements.items():
        content = content.replace(old, new)
    
    # Apply conditional corruption fixes
    for pattern, replacement in conditional_corruption_patterns:
        content = re.sub(pattern, replacement, content)
    
    # Clean up other UI elements with emojis (optional for performance)
    ui_cleanup = {
        '## 💰 Dividend Tracker': '## Dividend Tracker',
        '"📦 Dividend tracker modules': '"Dividend tracker modules',
        '"❌ Dividend Tracker Error': '"Dividend Tracker Error',
        '"💡 Make sure all dividend': '"Make sure all dividend',
        '"🏦 By Broker"': '"By Broker"',
        '"📊 Consolidated Holdings"': '"Consolidated Holdings"',
    }
    
    for old, new in ui_cleanup.items():
        content = content.replace(old, new)
    
    # Write cleaned content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Emoji corruption cleanup completed!")
    print("✅ All navigation options converted to clean text")
    print("✅ All conditional statements updated")
    print("✅ UI elements cleaned for performance")

if __name__ == "__main__":
    clean_emoji_corruption()
