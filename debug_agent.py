#!/usr/bin/env python3
"""
Debug script to test if the agent is actually invoking tools
"""

from agent.agentic_workflow import GraphBuilder
from dotenv import load_dotenv
import os

def debug_agent_tools():
    """Debug the agent's tool invocation"""
    
    # Load environment variables
    load_dotenv()
    
    print("🐛 DEBUG: Testing agent tool invocation...")
    
    # Initialize the agent
    agent = GraphBuilder(model_provider="groq")
    graph = agent.build_graph()
    
    # Create a simple query that should definitely trigger a tool
    test_query = "Search for current IPO information in India today"
    
    print(f"\n📝 Test Query: {test_query}")
    print("🔍 Invoking agent...")
    
    # Create initial state
    from langchain_core.messages import HumanMessage
    initial_state = {
        "messages": [HumanMessage(content=test_query)]
    }
    
    # Run the graph with debug information
    try:
        result = graph.invoke(initial_state, {"debug": True})
        
        print("\n📊 Debug Results:")
        print(f"Number of messages: {len(result['messages'])}")
        
        for i, message in enumerate(result['messages']):
            print(f"\nMessage {i+1}:")
            print(f"  Type: {type(message).__name__}")
            print(f"  Content: {message.content[:200]}...")
            
            # Check for tool calls
            if hasattr(message, 'tool_calls'):
                print(f"  Tool calls: {message.tool_calls}")
            
        return result["messages"][-1].content
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_agent_tools()
