"""
Saudi Stock Market Trading Signals App - Dashboard Launcher
Launches the main Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Saudi Stock Market Dashboard"""
    # Get the path to the main app
    current_dir = Path(__file__).parent
    app_path = current_dir / "apps" / "enhanced_saudi_app_v2.py"
    
    if not app_path.exists():
        print("❌ Error: Main app file not found!")
        print(f"Expected location: {app_path}")
        return 1
    
    try:
        print("🚀 Starting TADAWUL NEXUS - Enhanced Saudi Intelligence Platform...")
        print("📊 Loading complete database with 700+ Tadawul stocks...")
        print("🔗 Dashboard will open at: http://localhost:8501")
        print("🛑 Press Ctrl+C to stop the dashboard")
        print("\n" + "="*60)
        
        # Change to the correct directory and run streamlit
        os.chdir(current_dir)
        
        # Run streamlit with the main app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
