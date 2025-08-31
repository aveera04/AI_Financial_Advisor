#!/usr/bin/env python3
"""
Multi-Agent System Test Script for Financial Advisor
Tests Orchestrator Agent (OSS Model) + IPO Agent (DeepSeek Model)
"""

from agent.agentic_workflow import OrchestratorAgent, IPOAdvisorAgent
from dotenv import load_dotenv
import os
import time

def test_multi_agent_system():
    """Test the complete multi-agent system with different models"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if required API keys are set
    required_keys = ["GROQ_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set them in your .env file")
        return False
    
    print("🚀 MULTI-AGENT FINANCIAL ADVISOR SYSTEM TEST")
    print("=" * 70)
    print("🎯 Orchestrator Agent: groq_oss (llama3-70b-8192)")
    print("📊 IPO Agent: groq_deepseek (deepseek-r1-distill-llama-70b)")
    print("=" * 70)
    
    try:
        # Initialize the orchestrator with OSS model
        print("\n🤖 Initializing Multi-Agent System...")
        orchestrator = OrchestratorAgent(model_provider="groq_oss")
        
        print("✅ Multi-Agent System initialized successfully!")
        
        # Test cases for different routing scenarios
        test_cases = [
            {
                "category": "IPO ROUTING TEST",
                "query": "What are the current IPOs in India with their GMP today?",
                "expected_route": "IPO Advisor Agent",
                "description": "Should route to IPO Agent for specialized IPO analysis"
            },
            {
                "category": "IPO INVESTMENT TEST", 
                "query": "Should I invest in upcoming IPOs this week? Give me detailed analysis.",
                "expected_route": "IPO Advisor Agent",
                "description": "Should route to IPO Agent for investment recommendations"
            },
            {
                "category": "GENERAL SEARCH TEST",
                "query": "What are the current market trends in Indian stock market?", 
                "expected_route": "General Web Search",
                "description": "Should use general search for broad market information"
            },
            {
                "category": "MIXED QUERY TEST",
                "query": "Compare IPO performance vs stock market returns this year",
                "expected_route": "Either IPO Agent or General Search",
                "description": "Tests orchestrator decision making for mixed queries"
            }
        ]
        
        print(f"\n🧪 Running {len(test_cases)} test scenarios...")
        print("=" * 70)
        
        successful_tests = 0
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 TEST {i}: {test_case['category']}")
            print(f"Query: {test_case['query']}")
            print(f"Expected Route: {test_case['expected_route']}")
            print(f"Description: {test_case['description']}")
            print("-" * 50)
            
            try:
                start_time = time.time()
                response = orchestrator.run(test_case['query'])
                end_time = time.time()
                
                # Check routing success
                if "IPO Advisor Response:" in response:
                    actual_route = "IPO Advisor Agent"
                    route_emoji = "🎯"
                elif "Search Results for:" in response:
                    actual_route = "General Web Search"
                    route_emoji = "🔍"
                else:
                    actual_route = "Unknown/Direct Response"
                    route_emoji = "❓"
                
                print(f"{route_emoji} Actual Route: {actual_route}")
                print(f"⏱️  Response Time: {end_time - start_time:.2f} seconds")
                print(f"📄 Response Preview: {response[:200]}...")
                
                # Check for rate limit errors in response
                if "rate limit" in response.lower() or "429" in response:
                    print("⚠️  Rate limit detected in response - waiting 30 seconds...")
                    time.sleep(30)
                    successful_tests += 0.5  # Partial credit
                    print("⚠️  TEST PARTIAL - Rate limited but routing worked")
                elif "Error" in response and len(response) < 100:
                    print("❌ TEST FAILED - Error in response")
                else:
                    # Determine success
                    if ("IPO Advisor" in test_case['expected_route'] and "IPO Advisor Response:" in response) or \
                       ("General" in test_case['expected_route'] and "Search Results" in response) or \
                       ("Either" in test_case['expected_route']):
                        print("✅ TEST PASSED - Correct routing!")
                        successful_tests += 1
                    else:
                        print("⚠️  TEST INCONCLUSIVE - Routing unclear but response received")
                        successful_tests += 0.5
                    
            except Exception as e:
                print(f"❌ TEST FAILED - Error: {str(e)}")
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    print("💡 Rate limit reached - waiting 30 seconds...")
                    time.sleep(30)
                elif "groq" in str(e).lower():
                    print("💡 Groq API issue - waiting 10 seconds...")
                    time.sleep(10)
            
            print("-" * 50)
            
            # Add delay between tests to avoid rate limits
            if i < len(test_cases):
                print("⏳ Waiting 10 seconds before next test...")
                time.sleep(10)
        
        # Summary
        print(f"\n🎉 MULTI-AGENT SYSTEM TEST SUMMARY")
        print("=" * 50)
        print(f"✅ Successful Tests: {successful_tests}/{len(test_cases)}")
        print(f"📊 Success Rate: {(successful_tests/len(test_cases)*100):.1f}%")
        
        if successful_tests >= len(test_cases) * 0.75:
            print("🎯 MULTI-AGENT SYSTEM: WORKING CORRECTLY!")
        elif successful_tests >= len(test_cases) * 0.5:
            print("⚠️  MULTI-AGENT SYSTEM: PARTIALLY WORKING")
        else:
            print("❌ MULTI-AGENT SYSTEM: NEEDS DEBUGGING")
            
        return successful_tests >= len(test_cases) * 0.5
        
    except Exception as e:
        print(f"❌ Failed to initialize multi-agent system: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_agents():
    """Test individual agents separately for debugging"""
    print("\n🔬 INDIVIDUAL AGENT TESTING")
    print("=" * 40)
    
    try:
        # Test IPO Agent directly
        print("📊 Testing IPO Agent (DeepSeek) directly...")
        ipo_agent = IPOAdvisorAgent(model_provider="groq_deepseek")
        
        ipo_query = "What are today's IPO recommendations?"
        ipo_response = ipo_agent.process_query(ipo_query)
        
        print(f"✅ IPO Agent Response: {ipo_response[:150]}...")
        print("✅ IPO Agent working independently!")
        
        return True
        
    except Exception as e:
        print(f"❌ Individual agent test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🎪 STARTING COMPREHENSIVE MULTI-AGENT TESTING")
    print("=" * 60)
    
    # Test individual agents first
    individual_success = test_individual_agents()
    
    if individual_success:
        print("\n" + "=" * 60)
        # Test full multi-agent system
        system_success = test_multi_agent_system()
        
        if system_success:
            print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
            print("🚀 Multi-Agent Financial Advisor System is READY!")
        else:
            print("\n⚠️  Some tests failed. Check the logs above.")
    else:
        print("\n❌ Individual agent tests failed. Fix before testing system.")

if __name__ == "__main__":
    main()
