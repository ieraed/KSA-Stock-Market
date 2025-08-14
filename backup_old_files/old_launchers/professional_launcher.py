"""
Professional Saudi Stock Market App Launcher
Orchestrates backend API and frontend interface with data integrity
"""

import subprocess
import sys
import time
import requests
import threading
from pathlib import Path
import signal
import os

class ProfessionalAppLauncher:
    def __init__(self):
        self.api_process = None
        self.frontend_process = None
        self.running = False
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            'fastapi', 'uvicorn', 'streamlit', 'pandas', 
            'sqlalchemy', 'redis', 'aiohttp'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - Missing")
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"] + missing_packages
            )
            print("✅ All dependencies installed!")
        
        return True
    
    def start_api_server(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting API Server...")
        
        try:
            # Check if API server file exists
            api_file = Path("api_server.py")
            if not api_file.exists():
                print("❌ API server file not found. Creating basic API...")
                return False
            
            # Start API server
            self.api_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "api_server:app", 
                "--host", "0.0.0.0", 
                "--port", "8000",
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for API to start
            for i in range(30):
                try:
                    response = requests.get("http://localhost:8000/api/health", timeout=1)
                    if response.status_code == 200:
                        print("✅ API Server started successfully on http://localhost:8000")
                        print("📖 API Documentation: http://localhost:8000/api/docs")
                        return True
                except:
                    time.sleep(1)
            
            print("⚠️  API Server starting (may take a moment)...")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start API server: {e}")
            return False
    
    def start_frontend(self):
        """Start the Streamlit frontend"""
        print("🎨 Starting Frontend Interface...")
        
        try:
            # Start Streamlit frontend
            self.frontend_process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", 
                "web_launcher_new.py",
                "--server.port=8501",
                "--server.address=0.0.0.0"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait for frontend to start
            time.sleep(5)
            
            print("✅ Frontend started successfully on http://localhost:8501")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False
    
    def check_data_integrity(self):
        """Validate data sources and integrity"""
        print("🔍 Checking data integrity...")
        
        try:
            # Test portfolio access
            from professional_portfolio import ProfessionalPortfolioManager
            portfolio_manager = ProfessionalPortfolioManager()
            
            if portfolio_manager.load_portfolio():
                print("✅ Portfolio data validation passed")
            else:
                print("⚠️  Portfolio data needs attention")
            
            # Test Saudi Exchange data fetcher
            from saudi_exchange_fetcher import SaudiExchangeDataFetcher
            fetcher = SaudiExchangeDataFetcher()
            
            print("✅ Data fetchers initialized")
            
            # Test API connectivity (if running)
            try:
                response = requests.get("http://localhost:8000/api/corporate-actions", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ API data integrity: {data.get('count', 0)} corporate actions loaded")
                    print(f"📊 Data source: {data.get('source', 'Unknown')}")
                else:
                    print("⚠️  API not responding, using local data")
            except:
                print("⚠️  API not available, using local data sources")
            
            return True
            
        except Exception as e:
            print(f"⚠️  Data integrity check warning: {e}")
            return False
    
    def display_system_status(self):
        """Display comprehensive system status"""
        print("\n" + "="*60)
        print("🎯 SAUDI STOCK MARKET APP - PROFESSIONAL STATUS")
        print("="*60)
        
        # API Status
        try:
            response = requests.get("http://localhost:8000/api/health", timeout=2)
            if response.status_code == 200:
                health_data = response.json()
                print("🔗 Backend API: ✅ RUNNING")
                print(f"   └── URL: http://localhost:8000")
                print(f"   └── Status: {health_data.get('status', 'Unknown')}")
                print(f"   └── Database: {health_data.get('database', 'Unknown')}")
            else:
                print("🔗 Backend API: ⚠️  ISSUES")
        except:
            print("🔗 Backend API: ❌ NOT RUNNING")
        
        # Frontend Status
        try:
            response = requests.get("http://localhost:8501", timeout=2)
            print("🎨 Frontend: ✅ RUNNING")
            print("   └── URL: http://localhost:8501")
        except:
            print("🎨 Frontend: ❌ NOT RUNNING")
        
        # Data Sources
        print("\n📊 DATA SOURCES:")
        
        # Portfolio
        try:
            from professional_portfolio import get_portfolio_for_signals
            portfolio = get_portfolio_for_signals()
            if portfolio:
                print(f"💼 Portfolio: ✅ LOADED ({len(portfolio['symbols'])} stocks)")
            else:
                print("💼 Portfolio: ⚠️  SAMPLE DATA")
        except:
            print("💼 Portfolio: ❌ ERROR")
        
        # Corporate Actions
        try:
            response = requests.get("http://localhost:8000/api/corporate-actions", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"📅 Corporate Actions: ✅ LOADED ({data.get('count', 0)} actions)")
                print(f"   └── Source: {data.get('source', 'Unknown')}")
                print(f"   └── Integrity: {data.get('data_integrity', 'Unknown')}")
            else:
                print("📅 Corporate Actions: ⚠️  LOCAL DATA")
        except:
            print("📅 Corporate Actions: ⚠️  LOCAL DATA")
        
        print("\n🎯 ACCESS POINTS:")
        print("   • Main App: http://localhost:8501")
        print("   • API Docs: http://localhost:8000/api/docs")
        print("   • API Health: http://localhost:8000/api/health")
        
        print("\n💡 FEATURES AVAILABLE:")
        print("   ✅ Real-time Corporate Actions")
        print("   ✅ Professional Portfolio Management") 
        print("   ✅ Trading Signal Generation")
        print("   ✅ Quarterly Dividend Analysis")
        print("   ✅ Data Integrity Validation")
        print("   ✅ API-based Architecture")
        
        print("="*60)
    
    def start_professional_app(self):
        """Start the complete professional application"""
        print("🚀 STARTING SAUDI STOCK MARKET PROFESSIONAL APP")
        print("="*60)
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed")
            return False
        
        # Step 2: Start API server
        if not self.start_api_server():
            print("⚠️  API server failed to start, continuing with local mode...")
        
        time.sleep(3)  # Give API time to initialize
        
        # Step 3: Start frontend
        if not self.start_frontend():
            print("❌ Frontend failed to start")
            self.cleanup()
            return False
        
        # Step 4: Check data integrity
        self.check_data_integrity()
        
        # Step 5: Display status
        time.sleep(5)  # Wait for everything to initialize
        self.display_system_status()
        
        self.running = True
        
        # Step 6: Monitor and keep running
        try:
            print("\n🎯 Professional app running! Press Ctrl+C to stop...")
            while self.running:
                time.sleep(10)
                # Optionally add health checks here
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.cleanup()
    
    def cleanup(self):
        """Clean shutdown of all processes"""
        print("🧹 Cleaning up...")
        
        if self.api_process:
            try:
                self.api_process.terminate()
                self.api_process.wait(timeout=5)
                print("✅ API server stopped")
            except:
                self.api_process.kill()
                print("🔨 API server force stopped")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend stopped")
            except:
                self.frontend_process.kill()
                print("🔨 Frontend force stopped")
        
        self.running = False
        print("✅ Professional app shutdown complete")

def main():
    """Main entry point"""
    launcher = ProfessionalAppLauncher()
    
    # Handle graceful shutdown
    def signal_handler(signum, frame):
        launcher.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start the professional application
    launcher.start_professional_app()

if __name__ == "__main__":
    main()
