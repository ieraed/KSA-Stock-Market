"""
Saudi Stock Market Trading Signals Generator
Generates and displays trading signals for Saudi stocks
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Signal Generator"""
    # Get the path to the signals app
    current_dir = Path(__file__).parent
    signals_path = current_dir / "apps" / "run_signals.py"
    
    if not signals_path.exists():
        print("❌ Error: Signals app file not found!")
        print(f"Expected location: {signals_path}")
        return 1
    
    try:
        print("📈 Starting Saudi Stock Market Signal Generator...")
        print("🔍 Analyzing 259 Tadawul stocks for trading opportunities...")
        print("\n" + "="*60)
        
        # Change to the correct directory and run the signals generator
        os.chdir(current_dir)
        
        # Run the signals generator
        subprocess.run([sys.executable, str(signals_path)])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Signal generator stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Error running signal generator: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
