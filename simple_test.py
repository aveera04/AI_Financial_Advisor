#!/usr/bin/env python3
"""
Simple test for orchestrator agent
"""

from agent.agentic_workflow import OrchestratorAgent
from dotenv import load_dotenv
import os

def simple_test():
    load_dotenv()
    
    print("🎯 Simple Orchestrator Test...")
    
    try:
        orchestrator = OrchestratorAgent(model_provider="groq")
        
        # Test 1: IPO query
        print("\n📝 Test 1: IPO Query")
        query = "Tell me about current IPOs in India"
        print(f"Query: {query}")
        
        response = orchestrator.run(query)
        print(f"Response: {response[:200]}...")
        
        if "IPO Advisor Response:" in response:
            print("✅ Successfully routed to IPO Advisor!")
        else:
            print("ℹ️  Response received (routing unclear)")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
