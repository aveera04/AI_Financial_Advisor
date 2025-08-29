#!/usr/bin/env python3
"""
Test script for the Financial Advisor Agent with Web Search capabilities
"""

from agent.agentic_workflow import GraphBuilder
from dotenv import load_dotenv
import os

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if required API keys are set
    required_keys = ["GROQ_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f"❌ Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set them in your .env file")
        return
    
    print("🤖 Initializing Financial Advisor Agent...")
    
    try:
        # Initialize the agent
        agent = GraphBuilder(model_provider="groq")
        graph = agent.build_graph()
        
        print("✅ Agent initialized successfully!")
        print("\n" + "="*60)
        print("💰 FINANCIAL ADVISOR AGENT")
        print("="*60)
        
        # Test queries
        test_queries = [
            "Give me top 5 ipos in India",
            
        ]
        
        print("\n🔍 Running test queries...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Query {i}: {query}")
            print("-" * 50)
            
            try:
                response = agent.run(query)
                print(f"🤖 Response: {response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print("-" * 50)
    
    except Exception as e:
        print(f"❌ Failed to initialize agent: {str(e)}")

if __name__ == "__main__":
    main()
