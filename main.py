#!/usr/bin/env python3
"""
Launch script for the AI Financial Advisor Web UI
Launches the React frontend with FastAPI backend
"""

import subprocess
import sys
import os
import time
import atexit

processes = []

def cleanup():
    """Cleanup all spawned processes"""
    print("\n👋 Shutting down AI Financial Advisor...")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass

def main():
    """Launch the React frontend with FastAPI backend"""
    atexit.register(cleanup)
    
    print("🚀 Launching AI Financial Advisor Web UI...")
    print("📱 The app will be available at http://localhost:8080")
    print("🔗 Backend API: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Start the FastAPI backend
        print("🔧 Starting backend server...")
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
            print("Please check that all dependencies are installed:")
            print("  pip install -r requirements.txt")
            return
        
        print("✅ Backend server started")
        print("-" * 50)
        
        # Start the frontend development server
        print("🎨 Starting frontend server...")
        frontend_dir = os.path.join(project_dir, "frontend")
        
        # Check if node_modules exists
        if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
            print("📦 Installing frontend dependencies...")
            print("   This may take a few minutes on first run...")
            subprocess.run(
                ["npm", "install"],
                cwd=frontend_dir,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Frontend dependencies installed")
        
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        processes.append(frontend_process)
        
        print("✅ Frontend server started")
        print("-" * 50)
        print("🎉 AI Financial Advisor is now running!")
        print("   Open http://localhost:8080 in your browser")
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
        print("\n⏹️  Shutting down...")
    except FileNotFoundError as e:
        print(f"❌ Error: {str(e)}")
        print("Please ensure Node.js and npm are installed:")
        print("  https://nodejs.org/")
    except Exception as e:
        print(f"❌ Error launching app: {str(e)}")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
