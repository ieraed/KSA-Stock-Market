#!/usr/bin/env python3
"""
Fix import paths in test files
"""

import os
from pathlib import Path

def fix_test_imports():
    """Fix import paths in all test files"""
    
    test_dir = Path("C:/Users/raed1/OneDrive/Saudi Stock Market App/test")
    
    # Import fix to add at the beginning of test files
    import_fix = """import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
    
    # Process all test files
    for test_file in test_dir.glob("test_*.py"):
        print(f"🔧 Fixing imports in {test_file.name}")
        
        # Read the file
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already fixed
        if "sys.path.insert" in content:
            print(f"  ✅ Already fixed")
            continue
        
        # Find the first import line
        lines = content.split('\n')
        insert_index = 0
        
        for i, line in enumerate(lines):
            if line.strip().startswith('from ') or line.strip().startswith('import '):
                insert_index = i
                break
        
        # Insert the path fix before the first import
        lines.insert(insert_index, import_fix.strip())
        
        # Write the fixed file
        fixed_content = '\n'.join(lines)
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"  ✅ Fixed imports")

if __name__ == "__main__":
    fix_test_imports()
    print("✅ All test imports fixed!")
