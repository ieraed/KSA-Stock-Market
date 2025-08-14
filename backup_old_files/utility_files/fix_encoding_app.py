#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix encoding issues in web_launcher_new.py and add new features
"""

def fix_web_launcher():
    with open('web_launcher_new.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix title and page config
    content = content.replace(
        'page_title="Saudi Stock Market Trading Signals"',
        'page_title="نجم التداول - Najm Al-Tadawul (Trading Star)"'
    )
    content = content.replace('page_icon="📈"', 'page_icon="⭐"')
    
    # Fix sidebar title
    content = content.replace(
        'st.sidebar.title("🏦 Saudi Stock Market")',
        'st.sidebar.title("⭐ نجم التداول - Najm Al-Tadawul")'
    )
    content = content.replace(
        'st.sidebar.markdown("**Trading Signals App**")',
        'st.sidebar.markdown("**Trading Star Platform**")'
    )
    
    # Fix corrupted navigation entries
    content = content.replace('        "� Portfolio Management": "Portfolio Management",', '        "📝 Portfolio Management": "Portfolio Management",')
    content = content.replace('        "�📈 Technical Analysis": "Technical Analysis",', '        "📈 Technical Analysis": "Technical Analysis",')
    
    # Add User Registration to navigation
    content = content.replace(
        '    pages = {\n        "🎯 Quick Actions": "Quick Actions",',
        '    pages = {\n        "🌟 Register/Welcome": "User Registration",\n        "🎯 Quick Actions": "Quick Actions",'
    )
    
    # Change initial page to registration
    content = content.replace(
        'st.session_state.page = "Quick Actions"',
        'st.session_state.page = "User Registration"'
    )
    
    with open('web_launcher_new.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed encoding issues and updated navigation")

if __name__ == "__main__":
    fix_web_launcher()
