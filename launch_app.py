"""
🚀 SAUDI STOCK MARKET APP LAUNCHER
Professional launcher for the organized Saudi Stock Market application
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Saudi Stock Market App with proper paths"""
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    
    # Define app path
    app_path = current_dir / "apps" / "enhanced_saudi_app_v2.py"
    
    # Check if virtual environment exists
    venv_python = current_dir / ".venv" / "Scripts" / "python.exe"
    
    if venv_python.exists():
        python_cmd = str(venv_python)
        print("✅ Using virtual environment Python")
    else:
        python_cmd = "python"
        print("⚠️  Using system Python (virtual environment not found)")
    
    # Check if app exists
    if not app_path.exists():
        print(f"❌ App not found at: {app_path}")
        print("Please ensure the app is in the correct location")
        return
    
    print(f"🚀 Launching Saudi Stock Market App...")
    print(f"📍 App location: {app_path}")
    print(f"🐍 Python: {python_cmd}")
    print("📱 Starting Streamlit server...")
    
    # Launch the app
    try:
        cmd = [python_cmd, "-m", "streamlit", "run", str(app_path), "--server.port", "8501"]
        subprocess.run(cmd, cwd=current_dir)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main()
