#!/usr/bin/env python3
"""
Enhanced test script that shows tool invocation process clearly
"""

from agent.agentic_workflow import GraphBuilder
from dotenv import load_dotenv
import os

def test_agent_with_verbose_output():
    """Test agent with detailed output showing tool usage"""
    
    load_dotenv()
    
    print("🤖 Testing Financial Advisor Agent with Tool Invocation Visibility...")
    
    # Initialize the agent
    agent = GraphBuilder(model_provider="groq")
    graph = agent.build_graph()
    
    # Test query
    query = "What are the current IPOs in India with their GMP today?"
    
    print(f"\n📝 Query: {query}")
    print("=" * 60)
    
    from langchain_core.messages import HumanMessage
    initial_state = {"messages": [HumanMessage(content=query)]}
    
    # Run and track each step
    result = graph.invoke(initial_state)
    
    print("\n🔍 AGENT EXECUTION TRACE:")
    print("=" * 40)
    
    for i, message in enumerate(result['messages']):
        if message.content:  # Skip empty messages
            print(f"\n{i+1}. {type(message).__name__}:")
            
            if hasattr(message, 'tool_calls') and message.tool_calls:
                print("   🛠️  TOOL CALLS MADE:")
                for tool_call in message.tool_calls:
                    print(f"     - Tool: {tool_call['name']}")
                    print(f"     - Query: {tool_call['args']['query']}")
                    print(f"     - ID: {tool_call['id']}")
                
            if message.content:
                content = message.content
                if len(content) > 300:
                    content = content[:300] + "... [truncated]"
                print(f"   📝 Content: {content}")
            
            print("   " + "-" * 30)
    
    print(f"\n🎯 FINAL RESPONSE:")
    print("=" * 40)
    print(result["messages"][-1].content)

if __name__ == "__main__":
    test_agent_with_verbose_output()
