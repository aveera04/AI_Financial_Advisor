#!/usr/bin/env python3
"""
Test script to verify the API server can start and respond
"""

import sys
import time
import subprocess
import requests

def test_api_server():
    """Test that the API server can start and respond"""
    print("🧪 Testing API Server Startup...")
    
    # Start the server
    print("  Starting server...")
    process = subprocess.Popen(
        [sys.executable, "api_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Check if server is running
        if process.poll() is not None:
            print("  ❌ Server failed to start")
            return False
        
        # Test health endpoint
        print("  Testing /health endpoint...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            print("  ✅ Health check passed")
        else:
            print(f"  ❌ Health check failed: {response.status_code}")
            return False
        
        # Test root endpoint
        print("  Testing / endpoint...")
        response = requests.get("http://localhost:8000/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Root endpoint passed: {data.get('message')}")
        else:
            print(f"  ❌ Root endpoint failed: {response.status_code}")
            return False
        
        print("✅ All API tests passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Error during testing: {str(e)}")
        return False
        
    finally:
        # Stop the server
        print("  Stopping server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    success = test_api_server()
    sys.exit(0 if success else 1)
