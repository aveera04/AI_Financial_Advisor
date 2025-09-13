#!/usr/bin/env python3
"""
Test script for the Orchestrator Agent with specialized agents
"""

from agent.agentic_workflow import OrchestratorAgent
from dotenv import load_dotenv
import os

def test_orchestrator():
    """Test the orchestrator agent with different types of queries"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if required API keys are set
    required_keys = ["GROQ_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set them in your .env file")
        return
    
    print("🎯 Initializing Orchestrator Agent...")
    
    try:
        # Initialize the orchestrator
        orchestrator = OrchestratorAgent(model_provider="groq")
        graph = orchestrator.build_graph()
        
        print("✅ Orchestrator initialized successfully!")
        print("\n" + "="*80)
        print("🎛️  FINANCIAL ADVISOR ORCHESTRATOR")
        print("="*80)
        
        # Test queries for different scenarios
        test_queries = [
            {
                "query": "Tell me about upcoming IPOs in India with their GMP",
                "expected_agent": "IPO Advisor"
            },
            {
                "query": "What are the current market trends in Indian stock market?",
                "expected_agent": "General Search"
            },
            {
                "query": "Should I invest in Tata Motors IPO? What's the GMP?",
                "expected_agent": "IPO Advisor"
            }
        ]
        
        print("\n🔍 Testing orchestrator routing...")
        
        for i, test_case in enumerate(test_queries, 1):
            query = test_case["query"]
            expected = test_case["expected_agent"]
            
            print(f"\n📝 Test {i}: {query}")
            print(f"📋 Expected routing to: {expected}")
            print("-" * 70)
            
            try:
                response = orchestrator.run(query)
                print(f"🤖 Orchestrator Response: {response[:500]}...")
                
                # Check if response indicates correct routing
                if "IPO Advisor Response:" in response:
                    print("✅ Successfully routed to IPO Advisor Agent")
                elif "Search Results for:" in response:
                    print("✅ Successfully used general search tool")
                else:
                    print("ℹ️  Response received (routing method unclear)")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print("-" * 70)
        
        print(f"\n🎉 Orchestrator testing completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {str(e)}")
        import traceback
        traceback.print_exc()

def test_direct_ipo_agent():
    """Test the IPO agent directly"""
    print("\n" + "="*60)
    print("🧪 TESTING IPO AGENT DIRECTLY")
    print("="*60)
    
    from agent.agentic_workflow import IPOAdvisorAgent
    
    try:
        ipo_agent = IPOAdvisorAgent()
        query = "What are the top IPO opportunities this week?"
        
        print(f"📝 Direct IPO Query: {query}")
        response = ipo_agent.process_query(query)
        print(f"🎯 IPO Agent Response: {response[:300]}...")
        print("✅ Direct IPO agent test successful!")
        
    except Exception as e:
        print(f"❌ Direct IPO agent test failed: {str(e)}")

if __name__ == "__main__":
    test_orchestrator()
    test_direct_ipo_agent()
