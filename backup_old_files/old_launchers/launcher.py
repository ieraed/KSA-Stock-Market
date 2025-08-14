"""
Saudi Stock Market Trading Signals App Launcher
"""

import sys
import subprocess
from pathlib import Path

# Fix encoding for Windows
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def show_menu():
    """Display the main menu"""
    print("\n[SA] Saudi Stock Market Trading Signals App")
    print("=" * 45)
    print("1. 🎯 Generate Trading Signals")
    print("2. 📊 Start Web Dashboard")
    print("3. 🧪 Run Test Suite")
    print("4. 🔙 Run Backtesting")
    print("5. ⚙️  Setup Application")
    print("6. 📚 View README")
    print("0. ❌ Exit")
    print("=" * 45)

def run_script(script_name, description):
    """Run a Python script"""
    print(f"\n🔄 {description}...")
    try:
        subprocess.run([sys.executable, script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}: {e}")
    except KeyboardInterrupt:
        print(f"\n🛑 {description} stopped by user")

def view_readme():
    """Display README content"""
    readme_path = Path("README.md")
    if readme_path.exists():
        print("\n📚 README.md Content:")
        print("=" * 50)
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Show first 2000 characters
            if len(content) > 2000:
                print(content[:2000])
                print("\n... (truncated, see README.md for full content)")
            else:
                print(content)
    else:
        print("❌ README.md not found")

def main():
    """Main launcher function"""
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "1":
                run_script("run_signals.py", "Generating Trading Signals")
            
            elif choice == "2":
                print("\n📊 Starting Web Dashboard...")
                print("🌐 Dashboard will open at: http://localhost:8501")
                print("🛑 Press Ctrl+C to stop the dashboard")
                run_script("run_dashboard.py", "Starting Web Dashboard")
            
            elif choice == "3":
                run_script("test_app.py", "Running Test Suite")
            
            elif choice == "4":
                run_script("src\\backtesting\\backtest.py", "Running Backtesting")
            
            elif choice == "5":
                run_script("setup.py", "Setting up Application")
            
            elif choice == "6":
                view_readme()
            
            elif choice == "0":
                print("\n👋 Goodbye! Happy trading!")
                break
            
            else:
                print("❌ Invalid choice. Please enter a number between 0-6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy trading!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
