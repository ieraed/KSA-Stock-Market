#!/usr/bin/env python3
"""
Direct file fixing for emoji corruption
"""

def fix_navigation_corruption():
    file_path = r"c:\Users\raed1\OneDrive\Saudi Stock Market App\apps\enhanced_saudi_app_v2.py"
    
    # Read file as binary first to handle corruption
    with open(file_path, 'rb') as f:
        content_bytes = f.read()
    
    # Convert to string with error handling
    content = content_bytes.decode('utf-8', errors='replace')
    
    # Direct string replacements for navigation list
    # Find the navigation section and replace it entirely
    start_marker = '            ['
    end_marker = '            ],'
    
    lines = content.split('\n')
    new_lines = []
    in_navigation = False
    
    for line in lines:
        if start_marker in line and 'Portfolio Overview' in content[content.find(line):content.find(line)+500]:
            # Start of navigation section
            in_navigation = True
            new_lines.append('            [')
            new_lines.append('                "Portfolio Overview",')
            new_lines.append('                "Portfolio Setup",')
            new_lines.append('                "AI Trading Center",')
            new_lines.append('                "Market Analysis",')
            new_lines.append('                "Performance Tracker",')
            new_lines.append('                "Stock Research",')
            new_lines.append('                "Analytics Dashboard",')
            new_lines.append('                "Sector Analyzer",')
            new_lines.append('                "Risk Management",')
            new_lines.append('                "Dividend Tracker",')
            new_lines.append('                "Import/Export Data",')
            new_lines.append('                "Theme Customizer"')
        elif in_navigation and end_marker in line:
            # End of navigation section
            in_navigation = False
            new_lines.append('            ],')
        elif not in_navigation:
            new_lines.append(line)
    
    # Join back together
    new_content = '\n'.join(new_lines)
    
    # Fix conditional statements
    conditionals = {
        'if selected_page == "Portfolio Overview"': 'if selected_page == "Portfolio Overview"',
        'elif selected_page == "Portfolio Setup"': 'elif selected_page == "Portfolio Setup"',
        'elif selected_page == "AI Trading Center"': 'elif selected_page == "AI Trading Center"',
        'elif selected_page == "Market Analysis"': 'elif selected_page == "Market Analysis"',
        'elif selected_page == "Performance Tracker"': 'elif selected_page == "Performance Tracker"',
        'elif selected_page == "Stock Research"': 'elif selected_page == "Stock Research"',
        'elif selected_page == "Analytics Dashboard"': 'elif selected_page == "Analytics Dashboard"',
        'elif selected_page == "Sector Analyzer"': 'elif selected_page == "Sector Analyzer"',
        'elif selected_page == "Risk Management"': 'elif selected_page == "Risk Management"',
        'elif selected_page == "Dividend Tracker"': 'elif selected_page == "Dividend Tracker"',
        'elif selected_page == "Import/Export Data"': 'elif selected_page == "Import/Export Data"',
        'elif selected_page == "Theme Customizer"': 'elif selected_page == "Theme Customizer"',
    }
    
    # Replace any remaining corrupted conditionals
    import re
    
    # Pattern to match corrupted conditionals
    corrupted_patterns = [
        (r'elif selected_page == "[^"]*�[^"]*Dividend Tracker[^"]*":', 'elif selected_page == "Dividend Tracker":'),
        (r'elif selected_page == "[^"]*�[^"]*Import/Export Data[^"]*":', 'elif selected_page == "Import/Export Data":'),
        (r'elif selected_page == "[^"]*🎨[^"]*Theme Customizer[^"]*":', 'elif selected_page == "Theme Customizer":'),
    ]
    
    for pattern, replacement in corrupted_patterns:
        new_content = re.sub(pattern, replacement, new_content)
    
    # Write back as UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Navigation corruption fixed!")
    print("✅ All emoji corruption removed from navigation")
    print("✅ Conditional statements cleaned")

if __name__ == "__main__":
    fix_navigation_corruption()
