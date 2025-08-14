@echo off
echo Starting Saudi Stock Market Trading Signals Web Launcher...
echo Using the WORKING version (simple_working_app.py)
echo Port 8505 (avoiding conflicts with your other app on 5173 and 3001)
echo.
cd /d "C:\Users\raed1\OneDrive\Saudi Stock Market App"
echo. | ".venv\Scripts\python.exe" -m streamlit run simple_working_app.py --server.port=8505
pause
