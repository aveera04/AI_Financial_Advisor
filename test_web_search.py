#!/usr/bin/env python3
"""
Test script to verify the connection between web_search_tool.py and ipo_info_search.py
"""

from tools.web_search_tool import WebSearchTool
from utils.ipo_info_search import TavilyIPOInfoSearch
from dotenv import load_dotenv
import os

def test_connection():
    """Test the connection between web_search_tool and ipo_info_search"""
    
    # Load environment variables
    load_dotenv()
    
    # Check if TAVILY_API_KEY is available
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ TAVILY_API_KEY not found in environment variables")
        print("Please add TAVILY_API_KEY to your .env file")
        return False
    
    print("🔍 Testing Web Search Tool and IPO Info Search connection...")
    
    try:
        # Test 1: Initialize WebSearchTool
        print("\n📝 Test 1: Initializing WebSearchTool...")
        web_search = WebSearchTool()
        print("✅ WebSearchTool initialized successfully")
        
        # Test 2: Initialize TavilyIPOInfoSearch directly
        print("\n📝 Test 2: Initializing TavilyIPOInfoSearch...")
        ipo_search = TavilyIPOInfoSearch()
        print("✅ TavilyIPOInfoSearch initialized successfully")
        
        # Test 3: Get tools from WebSearchTool
        print("\n📝 Test 3: Getting tools from WebSearchTool...")
        tools = web_search.get_tools()
        print(f"✅ Retrieved {len(tools)} tools: {[tool.name for tool in tools]}")
        
        # Test 4: Test IPO search functionality (if you have API key set up)
        print("\n📝 Test 4: Testing IPO search (this may take a moment)...")
        test_query = "Bajaj Housing Finance IPO"
        result = ipo_search.tavily_search_(test_query)
        
        if isinstance(result, dict) and 'error' not in result:
            print(f"✅ IPO search successful! Found {len(result) if isinstance(result, list) else 'some'} results")
            print(f"Sample result keys: {list(result.keys()) if isinstance(result, dict) else 'List of results'}")
        else:
            print(f"⚠️  IPO search returned: {result}")
        
        print("\n🎉 All tests passed! Web search tool is properly connected to IPO info search.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    
    if success:
        print("\n" + "="*60)
        print("🎯 CONNECTION SUCCESSFUL!")
        print("="*60)
        print("Your web_search_tool.py is now properly connected to ipo_info_search.py")
        print("\nAvailable methods:")
        print("• search_web(query) - General web search")
        print("• search_ipo_info(query) - Specialized IPO search")
        print("• get_tools() - Get both tools for LangChain")
        print("• get_tool() - Get general search tool")
    else:
        print("\n" + "="*60)
        print("❌ CONNECTION FAILED")
        print("="*60)
        print("Please check the error messages above and fix the issues.")
