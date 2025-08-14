"""
Setup script for the Saudi Stock Market Trading Signals App
"""

import subprocess
import sys
import os
from pathlib import Path

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        try:
            with open(".env.example", "r") as example:
                content = example.read()
            
            with open(".env", "w") as env:
                env.write(content)
            
            print("✅ .env file created from .env.example")
            print("⚠️  Please edit .env file with your API keys and settings")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Some packages may have failed to install. Common issues:")
        print("   - TA-Lib requires additional system dependencies")
        print("   - Try: pip install --only-binary=all -r requirements.txt")
        return False
    
    return True

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    try:
        # Test basic imports
        import pandas as pd
        import numpy as np
        import yfinance as yf
        import streamlit as st
        import plotly.graph_objects as go
        
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Some dependencies may not be installed correctly")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "logs",
        "data_cache",
        "backtest_results"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")
    return True

def main():
    """Main setup function"""
    print("[SA] Saudi Stock Market Trading Signals App Setup")
    print("=" * 55)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Create directories
    create_directories()
    print()
    
    # Create .env file
    create_env_file()
    print()
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Dependency installation had issues. You may need to install some packages manually.")
    print()
    
    # Test installation
    test_success = test_installation()
    print()
    
    if test_success:
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 55)
        print()
        print("📝 Next Steps:")
        print("  1. Edit your .env file with API keys and email settings")
        print("  2. Run the test suite: python test_app.py")
        print("  3. Generate signals: python run_signals.py")
        print("  4. Start dashboard: python run_dashboard.py")
        print()
        print("📚 Documentation:")
        print("  - README.md: Complete project documentation")
        print("  - src/: Source code with detailed comments")
        print("  - .github/copilot-instructions.md: AI coding guidelines")
        print()
        print("🔧 Configuration:")
        print("  - Edit .env for API keys and email alerts")
        print("  - Modify src/utils/config.py for trading parameters")
        print()
        print("⚠️  IMPORTANT:")
        print("  - This is for educational purposes only")
        print("  - Always do your own research before trading")
        print("  - Consider consulting a financial advisor")
        print()
    else:
        print("❌ SETUP INCOMPLETE")
        print("Some issues were encountered during setup. Please check the errors above.")
        print("You may need to install some dependencies manually.")

if __name__ == "__main__":
    main()
