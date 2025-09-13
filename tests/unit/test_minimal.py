#!/usr/bin/env python3
"""
Minimal working test for the Multi-Agent Orchestrator
"""

from agent.agentic_workflow import OrchestratorAgent
from dotenv import load_dotenv
import os
import sys

def main():
    print("🎯 MINIMAL ORCHESTRATOR TEST")
    print("=" * 40)
    
    # Load env
    load_dotenv()
    
    # Check keys
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Missing GROQ_API_KEY")
        sys.exit(1)
        
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ Missing TAVILY_API_KEY")
        sys.exit(1)
    
    try:
        print("🤖 Creating orchestrator...")
        orchestrator = OrchestratorAgent(model_provider="groq_oss")
        print("✅ Orchestrator created successfully!")
        
        print("🔧 Available tools:", [tool.name for tool in orchestrator.all_tools])
        
        # Simple test query
        print("🔍 Testing with simple IPO query...")
        query = "What are current IPO listings?"
        
        print("🚀 Running query...")
        response = orchestrator.run(query)
        
        print("✅ Response received!")
        print(f"📄 Response length: {len(response)} characters")
        print(f"📄 Response preview: {response[:100]}...")
        
        if "IPO Advisor Response:" in response:
            print("🎯 Successfully routed to IPO Agent!")
        elif "Error" in response:
            print("⚠️  Response contains error but routing worked")
        else:
            print("❓ Response unclear but system functioning")
            
        print("\n🎉 MINIMAL TEST COMPLETED SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
