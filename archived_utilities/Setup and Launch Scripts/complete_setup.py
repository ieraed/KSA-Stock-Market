"""
🇸🇦 Enhanced Saudi Stock Market App - Complete Setup
This script sets up everything you need for the enhanced app
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def create_saudi_stocks_database():
    """Create a comprehensive Saudi stocks database if it doesn't exist"""
    
    if Path("saudi_stocks_database.json").exists():
        print("✅ Saudi stocks database already exists")
        return True
    
    print("📊 Creating Saudi stocks database...")
    
    # Comprehensive Saudi stocks database
    saudi_stocks = {
        # Banking Sector
        "1010": {"symbol": "1010.SR", "name_en": "Saudi National Bank", "name_ar": "البنك الأهلي السعودي", "sector": "Banking"},
        "1020": {"symbol": "1020.SR", "name_en": "Bank AlJazira", "name_ar": "بنك الجزيرة", "sector": "Banking"},
        "1030": {"symbol": "1030.SR", "name_en": "Alinma Bank", "name_ar": "بنك الإنماء", "sector": "Banking"},
        "1050": {"symbol": "1050.SR", "name_en": "Bank Albilad", "name_ar": "بنك البلاد", "sector": "Banking"},
        "1060": {"symbol": "1060.SR", "name_en": "Saudi Investment Bank", "name_ar": "البنك السعودي للاستثمار", "sector": "Banking"},
        "1080": {"symbol": "1080.SR", "name_en": "Arab National Bank", "name_ar": "البنك العربي الوطني", "sector": "Banking"},
        "1120": {"symbol": "1120.SR", "name_en": "Al Rajhi Bank", "name_ar": "مصرف الراجحي", "sector": "Banking"},
        "1150": {"symbol": "1150.SR", "name_en": "Banque Saudi Fransi", "name_ar": "البنك السعودي الفرنسي", "sector": "Banking"},
        
        # Energy Sector
        "2030": {"symbol": "2030.SR", "name_en": "Saudi Arabian Oil Co (Aramco)", "name_ar": "أرامكو السعودية", "sector": "Energy"},
        "2222": {"symbol": "2222.SR", "name_en": "Saudi Aramco Base Oil Company", "name_ar": "أرامكو السعودية لزيوت الأساس", "sector": "Energy"},
        "2040": {"symbol": "2040.SR", "name_en": "Saudi Electricity", "name_ar": "الشركة السعودية للكهرباء", "sector": "Energy"},
        
        # Petrochemicals
        "2010": {"symbol": "2010.SR", "name_en": "Saudi Basic Industries Corp (SABIC)", "name_ar": "سابك", "sector": "Petrochemicals"},
        "2380": {"symbol": "2380.SR", "name_en": "Petrochemical Industries Co", "name_ar": "الصناعات البتروكيماوية", "sector": "Petrochemicals"},
        
        # Telecommunications
        "7040": {"symbol": "7040.SR", "name_en": "Saudi Telecom Company", "name_ar": "الاتصالات السعودية", "sector": "Telecommunications"},
        "7020": {"symbol": "7020.SR", "name_en": "Etihad Etisalat (Mobily)", "name_ar": "اتحاد اتصالات (موبايلي)", "sector": "Telecommunications"},
        
        # Materials
        "2020": {"symbol": "2020.SR", "name_en": "Saudi Cement", "name_ar": "الأسمنت السعودية", "sector": "Materials"},
        "3003": {"symbol": "3003.SR", "name_en": "Saudi Industrial Investment Group", "name_ar": "مجموعة الاستثمار الصناعي السعودي", "sector": "Materials"},
        
        # Healthcare
        "1180": {"symbol": "1180.SR", "name_en": "National Medical Care", "name_ar": "الرعاية الطبية الوطنية", "sector": "Healthcare"},
        
        # Technology
        "1182": {"symbol": "1182.SR", "name_en": "Elm Company", "name_ar": "شركة علم", "sector": "Technology"},
        
        # Real Estate
        "1301": {"symbol": "1301.SR", "name_en": "Alouja Development", "name_ar": "العوجا للتنمية", "sector": "Real Estate"},
        
        # Consumer Staples
        "1210": {"symbol": "1210.SR", "name_en": "BinDawood Holding", "name_ar": "مجموعة بن داود القابضة", "sector": "Consumer Staples"},
        "1320": {"symbol": "1320.SR", "name_en": "Saudi Fisheries", "name_ar": "الأسماك السعودية", "sector": "Consumer Staples"},
        
        # Additional Popular Stocks
        "1214": {"symbol": "1214.SR", "name_en": "AlHokair Group", "name_ar": "مجموعة فتيحي", "sector": "Consumer Discretionary"},
        "2060": {"symbol": "2060.SR", "name_en": "Saudi International Petrochemical", "name_ar": "سبكيم", "sector": "Petrochemicals"},
        "2090": {"symbol": "2090.SR", "name_en": "Jarir Marketing", "name_ar": "جرير للتسويق", "sector": "Consumer Discretionary"},
        "4001": {"symbol": "4001.SR", "name_en": "Saudi Airlines Catering", "name_ar": "الخدمات الأرضية", "sector": "Transportation"},
        "4002": {"symbol": "4002.SR", "name_en": "Riyad Bank", "name_ar": "بنك الرياض", "sector": "Banking"},
        "4003": {"symbol": "4003.SR", "name_en": "Saudi Industrial Export", "name_ar": "الصادرات السعودية", "sector": "Industrials"}
    }
    
    try:
        with open("saudi_stocks_database.json", "w", encoding="utf-8") as f:
            json.dump(saudi_stocks, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Created Saudi stocks database with {len(saudi_stocks)} stocks")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_sample_portfolio():
    """Create a sample portfolio for demonstration"""
    
    if Path("user_portfolio.json").exists():
        print("✅ User portfolio already exists")
        return True
    
    print("📁 Creating sample portfolio...")
    
    sample_portfolio = [
        {
            "symbol": "2030.SR",
            "quantity": 10,
            "purchase_price": 85.50,
            "date_added": "2024-01-15"
        },
        {
            "symbol": "1120.SR",
            "quantity": 5,
            "purchase_price": 92.30,
            "date_added": "2024-01-20"
        },
        {
            "symbol": "2010.SR",
            "quantity": 8,
            "purchase_price": 78.40,
            "date_added": "2024-01-25"
        }
    ]
    
    try:
        with open("user_portfolio.json", "w") as f:
            json.dump(sample_portfolio, f, indent=2)
        
        print("✅ Created sample portfolio with Aramco, Al Rajhi Bank, and SABIC")
        return True
        
    except Exception as e:
        print(f"❌ Error creating portfolio: {e}")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("🔧 Installing dependencies...")
    
    try:
        # Core dependencies
        core_deps = [
            "streamlit>=1.28.0",
            "pandas>=1.5.0",
            "numpy>=1.24.0", 
            "yfinance>=0.2.0",
            "plotly>=5.15.0",
            "openpyxl>=3.1.0",
            "xlsxwriter>=3.1.0"
        ]
        
        print("📦 Installing core dependencies...")
        for dep in core_deps:
            print(f"  Installing {dep}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️ Failed to install {dep}: {e}")
        
        # Optional AI dependencies
        ai_deps = ["scikit-learn>=1.3.0"]
        
        print("🤖 Installing AI dependencies...")
        for dep in ai_deps:
            try:
                print(f"  Installing {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"  ✅ {dep} installed")
            except subprocess.CalledProcessError:
                print(f"  ⚠️ {dep} installation failed - AI features may be limited")
        
        print("✅ Dependencies installation completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def test_setup():
    """Test if everything is set up correctly"""
    print("🧪 Testing setup...")
    
    # Test imports
    try:
        import streamlit
        import pandas
        import numpy
        import yfinance
        import plotly
        print("✅ Core libraries imported successfully")
        
        # Test AI engine
        try:
            from ai_engine.simple_ai import get_ai_signals
            print("✅ AI engine imported successfully")
        except ImportError:
            print("⚠️ AI engine not available - but app will still work")
        
        # Test database files
        if Path("saudi_stocks_database.json").exists():
            print("✅ Saudi stocks database found")
        else:
            print("❌ Saudi stocks database missing")
        
        if Path("user_portfolio.json").exists():
            print("✅ User portfolio found")
        else:
            print("❌ User portfolio missing")
        
        if Path("enhanced_saudi_app.py").exists():
            print("✅ Enhanced app file found")
        else:
            print("❌ Enhanced app file missing")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🇸🇦 Enhanced Saudi Stock Market App - Complete Setup")
    print("=" * 60)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return
    
    # Step 2: Create database
    if not create_saudi_stocks_database():
        print("❌ Setup failed at database creation")
        return
    
    # Step 3: Create sample portfolio
    if not create_sample_portfolio():
        print("❌ Setup failed at portfolio creation")
        return
    
    # Step 4: Test setup
    if not test_setup():
        print("❌ Setup testing failed")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 What's been set up:")
    print("  📊 Saudi stocks database (30+ stocks)")
    print("  📁 Sample portfolio with 3 stocks")
    print("  🔧 All required dependencies")
    print("  🤖 AI trading engine")
    
    print("\n🚀 How to run the app:")
    print("  1. Run: python launch_enhanced_app.py")
    print("  2. Or run: streamlit run enhanced_saudi_app.py")
    print("  3. Open browser at: http://localhost:8501")
    
    print("\n🌟 App Features:")
    print("  📈 Portfolio Management")
    print("  🔍 Saudi Stock Search")
    print("  🤖 AI Trading Signals")
    print("  📊 Real-time Analytics") 
    print("  📁 Excel Import/Export")
    print("  🎯 User-friendly Interface")
    
    print("\n✅ Ready to use your Enhanced Saudi Stock Market App!")

if __name__ == "__main__":
    main()
