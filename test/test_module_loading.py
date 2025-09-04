#!/usr/bin/env python3
"""
Test script to verify that our module changes are being loaded correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys
import importlib
import inspect

# Force reload the module
if 'saudi_exchange_fetcher' in sys.modules:
    importlib.reload(sys.modules['saudi_exchange_fetcher'])

from saudi_exchange_fetcher import load_official_database

# Get the source code of the function to verify our changes are there
source = inspect.getsource(load_official_database)
print("=== FUNCTION SOURCE CODE ===")
print(source[:1000])  # First 1000 characters
print("...")

# Look for our specific debug patterns
if "cleaned_parts={cleaned_parts}" in source:
    print("✅ NEW CODE FOUND: Our updated parsing logic is in the source")
else:
    print("❌ OLD CODE: Still using old parsing logic")

# Now test the actual function
print("\n=== TESTING FUNCTION EXECUTION ===")
result = load_official_database()
print(f"Function returned {len(result)} stocks")
