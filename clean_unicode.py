#!/usr/bin/env python3
# Unicode cleaner script
import re

def clean_unicode_file(filename):
    """Clean problematic Unicode characters from a Python file"""
    try:
        # Try to read with UTF-8 first
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fall back to reading as binary and cleaning
        with open(filename, 'rb') as f:
            data = f.read()
        
        # Replace problematic bytes
        data = data.replace(b'\x9d', b'')  # Remove specific problematic byte
        data = data.replace(b'\x81', b'')  # Remove other problematic bytes
        data = data.replace(b'\x8d', b'')
        data = data.replace(b'\x8f', b'')
        data = data.replace(b'\x90', b'')
        
        # Try to decode as UTF-8, replace errors
        content = data.decode('utf-8', errors='replace')
    
    # Remove any remaining Unicode replacement characters
    content = content.replace('\ufffd', '')  # Unicode replacement character
    
    # Clean up any remaining emoji or problematic characters
    # Remove various emoji patterns
    emoji_patterns = [
        r'[\u2600-\u26FF]',  # Miscellaneous Symbols
        r'[\u2700-\u27BF]',  # Dingbats
        r'[\U0001F600-\U0001F64F]',  # Emoticons
        r'[\U0001F300-\U0001F5FF]',  # Misc Symbols and Pictographs
        r'[\U0001F680-\U0001F6FF]',  # Transport and Map
        r'[\U0001F1E0-\U0001F1FF]',  # Regional indicator symbols
        r'[\u25A0-\u25FF]',  # Geometric Shapes
        r'[\u2190-\u21FF]',  # Arrows
        r'[\u23F0-\u23FF]',  # Misc Technical symbols
    ]
    
    for pattern in emoji_patterns:
        content = re.sub(pattern, '', content)
    
    # Write back the cleaned content
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Cleaned Unicode issues from {filename}")

if __name__ == "__main__":
    clean_unicode_file('apps/enhanced_saudi_app_v2.py')
