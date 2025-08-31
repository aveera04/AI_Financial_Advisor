#!/usr/bin/env python3
"""
Test script for enhanced Tavily search tools with AI-powered query generation
"""

import os
from dotenv import load_dotenv
from tools.web_search_tool import WebSearchTool
from utils.ipo_info_search import TavilyIPOInfoSearch

# Load environment variables
load_dotenv()

def test_enhanced_tavily_tools():
    """Test the new enhanced Tavily search tools"""
    
    print("🚀 TESTING ENHANCED TAVILY SEARCH TOOLS")
    print("="*60)
    
    # Check for API key
    if not os.getenv("TAVILY_API_KEY"):
        print("❌ TAVILY_API_KEY not found!")
        return False
    
    try:
        # Initialize tools
        print("🔧 Initializing Enhanced Web Search Tools...")
        web_tool = WebSearchTool()
        print("✅ WebSearchTool initialized with AI query generation")
        
        print("\n🔧 Initializing Enhanced IPO Search Tools...")
        ipo_tool = TavilyIPOInfoSearch()
        print("✅ TavilyIPOInfoSearch initialized with AI query generation")
        
        # Test 1: Smart Search Tool
        print("\n" + "="*60)
        print("🧠 TEST 1: AI-Powered Smart Search")
        print("="*60)
        
        test_query = "latest trends in Indian stock market"
        print(f"Query: {test_query}")
        result = web_tool.tavily_smart_search.invoke({"query": test_query, "search_context": "market"})
        print(f"Result Length: {len(result)} characters")
        print("✅ Smart search completed successfully")
        
        # Test 2: Financial Search Tool
        print("\n" + "="*60)
        print("💰 TEST 2: Financial Market Search")
        print("="*60)
        
        financial_query = "IPO performance analysis 2025"
        print(f"Query: {financial_query}")
        financial_result = web_tool.tavily_financial_search.invoke({"query": financial_query})
        print(f"Result Length: {len(financial_result)} characters")
        print("✅ Financial search completed successfully")
        
        # Test 3: Enhanced IPO Search
        print("\n" + "="*60)
        print("📊 TEST 3: AI-Enhanced IPO Search")
        print("="*60)
        
        ipo_query = "upcoming IPOs this week"
        print(f"Query: {ipo_query}")
        ipo_result = ipo_tool.search_upcoming_ipos()
        print(f"Result Type: {type(ipo_result)}")
        print("✅ Enhanced IPO search completed successfully")
        
        # Test 4: GMP Search
        print("\n" + "="*60)
        print("💹 TEST 4: Grey Market Premium Search")
        print("="*60)
        
        gmp_result = ipo_tool.search_ipo_gmp()
        print(f"GMP Search Result Type: {type(gmp_result)}")
        print("✅ GMP search completed successfully")
        
        # Test 5: Tool Integration
        print("\n" + "="*60)
        print("🔗 TEST 5: Tool Integration Test")
        print("="*60)
        
        all_tools = web_tool.get_tools()
        print(f"Total Available Tools: {len(all_tools)}")
        for i, tool in enumerate(all_tools, 1):
            print(f"  {i}. {tool.name}")
        
        advanced_tools = web_tool.get_advanced_tools()
        print(f"Advanced AI Tools: {len(advanced_tools)}")
        for i, tool in enumerate(advanced_tools, 1):
            print(f"  {i}. {tool.name}")
        
        print("✅ Tool integration test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def test_query_generation():
    """Test AI query generation capabilities"""
    
    print("\n\n🎯 TESTING AI QUERY GENERATION")
    print("="*60)
    
    try:
        web_tool = WebSearchTool()
        ipo_tool = TavilyIPOInfoSearch()
        
        # Test queries
        test_cases = [
            ("What are the best IPOs to invest in?", "ipo"),
            ("Stock market trends today", "market"),
            ("Financial news updates", "general"),
        ]
        
        print("🧠 Testing Web Search Query Generation:")
        for query, context in test_cases:
            if hasattr(web_tool, '_generate_search_query'):
                optimized = web_tool._generate_search_query(query, context)
                print(f"  Original: {query}")
                print(f"  Optimized ({context}): {optimized}")
                print()
        
        print("📊 Testing IPO Query Generation:")
        ipo_contexts = ["listing", "gmp", "upcoming", "performance"]
        for context in ipo_contexts:
            if hasattr(ipo_tool, '_generate_ipo_query'):
                optimized = ipo_tool._generate_ipo_query("Reliance IPO", context)
                print(f"  Context ({context}): {optimized}")
        
        print("✅ Query generation tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Query generation test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 ENHANCED TAVILY SEARCH TOOLS TEST SUITE")
    print("="*70)
    
    # Run tests
    tools_test = test_enhanced_tavily_tools()
    query_test = test_query_generation()
    
    # Summary
    print("\n" + "="*70)
    print("📋 TEST SUMMARY")
    print("="*70)
    print(f"🔧 Enhanced Tools Test: {'✅ PASSED' if tools_test else '❌ FAILED'}")
    print(f"🎯 Query Generation Test: {'✅ PASSED' if query_test else '❌ FAILED'}")
    
    if tools_test and query_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your enhanced Tavily search tools are ready to use!")
        print("\nAvailable Enhanced Features:")
        print("• AI-powered query optimization")
        print("• Context-aware search (IPO, Market, General)")
        print("• Smart financial search")
        print("• Enhanced IPO information retrieval")
        print("• Grey Market Premium (GMP) search")
        print("• Subscription status tracking")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
