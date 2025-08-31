#!/usr/bin/env python3
"""
Launch script for the Streamlit Financial Advisor UI
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    print("🚀 Launching AI Financial Advisor Web UI...")
    print("📱 The app will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Launch Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ], check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Financial Advisor...")
    except Exception as e:
        print(f"❌ Error launching app: {str(e)}")

if __name__ == "__main__":
    main()
