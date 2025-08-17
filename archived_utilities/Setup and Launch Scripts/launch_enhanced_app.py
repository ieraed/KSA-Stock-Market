"""
🚀 Enhanced Saudi Stock Market App Launcher
Automatically sets up environment and launches the enhanced app
"""

import subprocess
import sys
import os
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing dependencies...")
    
    try:
        # Install core dependencies first
        core_deps = [
            "streamlit>=1.28.0",
            "pandas>=1.5.0", 
            "numpy>=1.24.0",
            "yfinance>=0.2.0",
            "plotly>=5.15.0",
            "openpyxl>=3.1.0",
            "xlsxwriter>=3.1.0"
        ]
        
        for dep in core_deps:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
        
        # Try to install AI dependencies (optional)
        ai_deps = [
            "scikit-learn>=1.3.0"
        ]
        
        print("🤖 Installing AI dependencies (optional)...")
        for dep in ai_deps:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ {dep} installed successfully")
            except:
                print(f"⚠️ {dep} installation failed - AI features may be limited")
        
        print("✅ Dependencies installation completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_files():
    """Check if required files exist"""
    required_files = [
        "saudi_stocks_database.json",
        "enhanced_saudi_app.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    return True

def create_sample_portfolio():
    """Create sample user portfolio if it doesn't exist"""
    portfolio_file = Path("user_portfolio.json")
    
    if not portfolio_file.exists():
        print("📁 Creating sample portfolio...")
        import json
        
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
            }
        ]
        
        with open("user_portfolio.json", "w") as f:
            json.dump(sample_portfolio, f, indent=2)
        
        print("✅ Sample portfolio created with Aramco and Al Rajhi Bank")

def launch_app():
    """Launch the Streamlit app"""
    print("🚀 Launching Enhanced Saudi Stock Market App...")
    print("🌐 App will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "enhanced_saudi_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

def main():
    """Main launcher function"""
    print("🇸🇦 Enhanced Saudi Stock Market App Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("saudi_stocks_database.json").exists():
        print("❌ Please run this script from the app directory")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Check required files
    if not check_files():
        print("❌ Missing required files")
        return
    
    # Create sample portfolio if needed
    create_sample_portfolio()
    
    print("\n🎉 Setup completed successfully!")
    print("\nApp Features:")
    print("📊 Portfolio Management")
    print("🔍 Saudi Stock Search") 
    print("🤖 AI Trading Signals")
    print("📈 Real-time Data")
    print("📁 Excel Import/Export")
    print("🎯 User-friendly Interface")
    
    input("\nPress Enter to launch the app...")
    
    # Launch the app
    launch_app()

if __name__ == "__main__":
    main()
