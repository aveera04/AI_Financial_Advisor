#!/usr/bin/env python3
"""
Quick test to identify the stock agent routing issue
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def test_stock_agent_directly():
    """Test StockAdvisorAgent directly with orchestrator configuration"""
    print("🧪 Testing StockAdvisorAgent directly...")
    
    try:
        from agent.agentic_workflow import StockAdvisorAgent
        
        # Initialize the stock agent with orchestrator's configuration
        print("📊 Initializing StockAdvisorAgent with Gemini...")
        stock_agent = StockAdvisorAgent(model_provider="gemini_2.5_pro", api_key_name="GEMINI_API_KEY")
        
        # Test a simple query
        test_query = "Analyze Angel One stock performance"
        print(f"📝 Testing query: {test_query}")
        
        result = stock_agent.process_query(test_query)
        print(f"✅ StockAdvisorAgent Response: {result[:500]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ StockAdvisorAgent Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_orchestrator_routing():
    """Test orchestrator routing for stock queries"""
    print("\n🎛️  Testing Orchestrator routing...")
    
    try:
        from agent.agentic_workflow import OrchestratorAgent
        
        # Initialize orchestrator
        print("📋 Initializing OrchestratorAgent...")
        orchestrator = OrchestratorAgent(model_provider="groq_oss")
        
        # Test stock query routing
        test_query = "Analyze Angel One stock for investment"
        print(f"📝 Testing query: {test_query}")
        
        result = orchestrator.run(test_query)
        print(f"🎯 Orchestrator Response: {result[:500]}...")
        
        # Check if it mentions stock advisor
        if "Stock Advisor" in result or "stock_advisor_agent" in result:
            print("✅ Query appears to be routed to Stock Advisor")
        else:
            print("⚠️  Query may not be routed to Stock Advisor")
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run routing diagnosis"""
    print("🔍 DIAGNOSING STOCK AGENT ROUTING ISSUE")
    print("="*60)
    
    # Test 1: Direct stock agent
    success1 = test_stock_agent_directly()
    
    # Test 2: Orchestrator routing
    success2 = test_orchestrator_routing()
    
    print("\n" + "="*60)
    print("📊 DIAGNOSIS RESULTS")
    print("="*60)
    
    if success1 and success2:
        print("🎉 Both tests passed - issue might be in web interface")
    elif success1 and not success2:
        print("⚠️  StockAgent works but Orchestrator routing failed")
    elif not success1 and success2:
        print("⚠️  Orchestrator works but StockAgent has issues")
    else:
        print("❌ Both components have issues")

if __name__ == "__main__":
    main()
