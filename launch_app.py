#!/usr/bin/env python3
"""
Launch script for the AI Financial Advisor with React Frontend
Starts both the FastAPI backend and serves the frontend
"""

import subprocess
import sys
import os
import time
import signal
import atexit

processes = []

def cleanup():
    """Cleanup all spawned processes"""
    print("\n👋 Shutting down AI Financial Advisor...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        except (OSError, AttributeError):
            pass

def main():
    """Launch the application"""
    atexit.register(cleanup)
    
    print("🚀 Launching AI Financial Advisor...")
    print("-" * 50)
    
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Start the FastAPI backend
        print("🔧 Starting FastAPI backend server on http://localhost:8000...")
        backend_process = subprocess.Popen(
            [sys.executable, "api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(backend_process)
        
        # Give backend time to start
        time.sleep(3)
        
        # Check if backend started successfully
        if backend_process.poll() is not None:
            print("❌ Backend failed to start!")
            return
        
        print("✅ Backend server started successfully")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("-" * 50)
        
        # Start the frontend development server
        print("🎨 Starting React frontend on http://localhost:8080...")
        frontend_dir = os.path.join(project_dir, "frontend")
        
        # Check if node_modules exists
        if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
            print("📦 Installing frontend dependencies (this may take a moment)...")
            npm_install = subprocess.run(
                ["npm", "install"],
                cwd=frontend_dir,
                check=True
            )
        
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(frontend_process)
        
        print("✅ Frontend server starting...")
        print("🔗 Frontend URL: http://localhost:8080")
        print("⏹️  Press Ctrl+C to stop all servers")
        print("-" * 50)
        
        # Monitor both processes
        while True:
            # Check if either process has terminated
            if backend_process.poll() is not None:
                print("\n❌ Backend process terminated unexpectedly!")
                break
            if frontend_process.poll() is not None:
                print("\n❌ Frontend process terminated unexpectedly!")
                break
            
            time.sleep(1)
        
    except KeyboardInterrupt:
        print("\n⏹️  Received shutdown signal...")
    except Exception as e:
        print(f"❌ Error launching app: {str(e)}")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
