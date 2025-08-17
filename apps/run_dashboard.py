"""
Run the Streamlit dashboard for the Saudi Stock Market Trading Signals App
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the Streamlit dashboard"""
    dashboard_path = Path(__file__).parent / "src" / "dashboard" / "app.py"
    
    try:
        print("🚀 Starting Saudi Stock Market Trading Signals Dashboard...")
        print("📊 The dashboard will open in your default web browser")
        print("🔗 URL: http://localhost:8501")
        print("\n" + "="*50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(dashboard_path),
            "--server.port=8501",
            "--server.address=localhost"
        ])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

if __name__ == "__main__":
    main()
