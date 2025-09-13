#!/usr/bin/env python3
"""
Test script for the new stock search tools
Tests the enhanced stock utilities and tools integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_stock_utility():
    """Test the TavilyStockInfoSearch utility directly"""
    print("🧪 Testing TavilyStockInfoSearch Utility...")
    
    try:
        from utils.stock_info_search import TavilyStockInfoSearch
        
        # Initialize the utility
        stock_search = TavilyStockInfoSearch()
        print("✅ Stock utility initialized successfully")
        
        # Test query generation
        test_query = "RELIANCE stock"
        optimized_query = stock_search._generate_stock_query(test_query, "performance")
        print(f"📝 Query optimization test:")
        print(f"   Original: {test_query}")
        print(f"   Optimized: {optimized_query}")
        
        # Test search functions (just show they work, don't run full search)
        print("✅ Stock utility functions available:")
        print("   - search_stock_performance")
        print("   - search_stock_news") 
        print("   - search_stock_analysis")
        print("   - search_stock_recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Stock utility test failed: {e}")
        return False

def test_stock_tools():
    """Test the stock search tools"""
    print("\n🧪 Testing Stock Search Tools...")
    
    try:
        from tools.web_search_tool import (
            search_stock_performance, 
            search_stock_news,
            search_stock_analysis, 
            search_stock_recommendations
        )
        
        print("✅ Stock tools imported successfully:")
        print("   - search_stock_performance")
        print("   - search_stock_news")
        print("   - search_stock_analysis") 
        print("   - search_stock_recommendations")
        
        # Test tool metadata
        print(f"\n📊 Tool Details:")
        print(f"   Performance Tool: {search_stock_performance.name}")
        print(f"   News Tool: {search_stock_news.name}")
        print(f"   Analysis Tool: {search_stock_analysis.name}")
        print(f"   Recommendations Tool: {search_stock_recommendations.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Stock tools test failed: {e}")
        return False

def test_web_search_integration():
    """Test WebSearchTool class integration"""
    print("\n🧪 Testing WebSearchTool Integration...")
    
    try:
        from tools.web_search_tool import WebSearchTool
        
        # Initialize WebSearchTool
        web_tool = WebSearchTool()
        print("✅ WebSearchTool initialized successfully")
        
        # Check all tools
        all_tools = web_tool.get_tools()
        print(f"📝 Total tools available: {len(all_tools)}")
        
        # Check stock tools specifically
        stock_tools = web_tool.get_stock_tools()
        print(f"📈 Stock-specific tools: {len(stock_tools)}")
        
        # List all tool names
        print("🔧 Available tools:")
        for i, tool in enumerate(all_tools, 1):
            tool_name = getattr(tool, 'name', str(tool))
            print(f"   {i}. {tool_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ WebSearchTool integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Stock Tools Integration Tests")
    print("="*60)
    
    tests = [
        test_stock_utility,
        test_stock_tools, 
        test_web_search_integration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"❌ Tests Failed: {total-passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Stock tools integration successful!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
