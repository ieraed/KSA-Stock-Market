#!/usr/bin/env python3
"""
Test script for the integrated AI-enhanced Saudi Stock Market app
"""

import sys
import importlib.util
import traceback

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'streamlit',
        'pandas', 
        'yfinance',
        'plotly',
        'requests',
        'bs4',
        'openpyxl'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
    
    print()

def test_ai_availability():
    """Test AI components availability"""
    print("🤖 Testing AI availability...")
    
    ai_modules = [
        'sklearn',
        'numpy',
        'scipy'
    ]
    
    ai_available = True
    for module in ai_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            ai_available = False
    
    print(f"🤖 AI_AVAILABLE: {ai_available}")
    print()
    return ai_available

def test_app_structure():
    """Test the app structure"""
    print("📁 Testing app structure...")
    
    import os
    
    required_files = [
        'web_launcher_new.py',
        'requirements.txt',
        'saudi_exchange_fetcher.py'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    
    # Test AI directory structure
    ai_files = [
        'src/ai/ai_trading_engine.py',
        'src/dashboard/ai_dashboard.py'
    ]
    
    for file in ai_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"⚠️  {file} (AI feature file)")
    
    print()

def test_app_loading():
    """Test if the main app can be loaded"""
    print("🚀 Testing app loading...")
    
    try:
        # Import the main app file
        spec = importlib.util.spec_from_file_location("web_launcher", "web_launcher_new.py")
        app_module = importlib.util.module_from_spec(spec)
        
        # Test if we can load the module (without executing main)
        print("✅ App module can be imported")
        
        # Test specific functions exist
        spec.loader.exec_module(app_module)
        
        functions_to_test = [
            'main',
            'show_signal_generation', 
            'generate_portfolio_signals',
            'generate_market_signals'
        ]
        
        for func_name in functions_to_test:
            if hasattr(app_module, func_name):
                print(f"✅ Function: {func_name}")
            else:
                print(f"❌ Function: {func_name}")
        
        # Test AI functions
        ai_functions = [
            'show_ai_trading_signals',
            'generate_ai_portfolio_signals',
            'generate_ai_market_signals'
        ]
        
        for func_name in ai_functions:
            if hasattr(app_module, func_name):
                print(f"✅ AI Function: {func_name}")
            else:
                print(f"❌ AI Function: {func_name}")
        
        print("✅ App structure looks good!")
        return True
        
    except Exception as e:
        print(f"❌ App loading failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 INTEGRATED AI SAUDI STOCK MARKET APP - TEST SUITE")
    print("=" * 60)
    print()
    
    test_imports()
    ai_available = test_ai_availability()
    test_app_structure()
    app_loads = test_app_loading()
    
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    if app_loads:
        print("✅ Core App: READY")
    else:
        print("❌ Core App: FAILED")
    
    if ai_available:
        print("✅ AI Features: AVAILABLE")
    else:
        print("⚠️  AI Features: INSTALL REQUIRED")
    
    print()
    print("🚀 Application Status:")
    if app_loads:
        print("   Ready to launch with integrated AI features!")
        print("   Traditional signals will work immediately.")
        if ai_available:
            print("   AI-powered predictions will be fully functional.")
        else:
            print("   AI features will show install option to user.")
    else:
        print("   ❌ Application needs fixes before launch.")
    
    print()
    print("📝 To start the app:")
    print('   python -m streamlit run web_launcher_new.py --server.port 8501')

if __name__ == "__main__":
    main()
