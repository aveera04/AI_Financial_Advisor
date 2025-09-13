#!/usr/bin/env python3
"""
Test script for the new SYSTEM_PROMPT_STOCK to ensure it works correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_stock_prompt():
    """Test the new stock analysis prompt"""
    print("🧪 Testing SYSTEM_PROMPT_STOCK...")
    
    try:
        from prompt_library.prompt import SYSTEM_PROMPT_STOCK
        
        print("✅ SYSTEM_PROMPT_STOCK imported successfully")
        print(f"📝 Prompt type: {type(SYSTEM_PROMPT_STOCK)}")
        print(f"📊 Content length: {len(SYSTEM_PROMPT_STOCK.content)} characters")
        
        # Check if the prompt contains key stock analysis sections
        content = SYSTEM_PROMPT_STOCK.content
        key_sections = [
            "Stock Overview",
            "Fundamental Analysis", 
            "Technical Analysis",
            "Investment Recommendation",
            "Risk Assessment",
            "Financial Health",
            "Valuation Metrics",
            "Price Targets"
        ]
        
        print("\n🔍 Checking key sections:")
        for section in key_sections:
            if section in content:
                print(f"   ✅ {section} - Found")
            else:
                print(f"   ❌ {section} - Missing")
        
        # Check for specific stock-related terms
        stock_terms = ["NSE", "BSE", "P/E Ratio", "RSI", "MACD", "Market Cap", "SEBI"]
        print("\n📈 Checking stock-specific terms:")
        for term in stock_terms:
            if term in content:
                print(f"   ✅ {term} - Found")
            else:
                print(f"   ❌ {term} - Missing")
        
        print(f"\n📝 Sample of prompt content (first 200 chars):")
        print(f"   {content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Stock prompt test failed: {e}")
        return False

def test_all_prompts():
    """Test all prompt imports"""
    print("\n🧪 Testing All Prompts...")
    
    try:
        from prompt_library.prompt import (
            SYSTEM_PROMPT_IPO,
            SYSTEM_PROMPT_STOCK, 
            SYSTEM_PROMPT_ORCHESTRATOR
        )
        
        prompts = [
            ("IPO Prompt", SYSTEM_PROMPT_IPO),
            ("Stock Prompt", SYSTEM_PROMPT_STOCK),
            ("Orchestrator Prompt", SYSTEM_PROMPT_ORCHESTRATOR)
        ]
        
        print("✅ All prompts imported successfully:")
        for name, prompt in prompts:
            print(f"   📝 {name}: {len(prompt.content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt imports test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Stock Prompt Tests")
    print("="*50)
    
    tests = [
        test_stock_prompt,
        test_all_prompts
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"❌ Tests Failed: {total-passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Stock analysis prompt is ready!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
