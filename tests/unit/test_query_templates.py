#!/usr/bin/env python3
"""Unit tests for Query Template Manager"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.query_templates import (
    QueryTemplateManager, get_template_manager, QueryResult,
    reset_template_manager, optimize_query
)


def test_entity_extraction():
    """Test entity extraction from various query formats"""
    print("\n📋 Testing Entity Extraction")
    print("-" * 40)
    
    manager = QueryTemplateManager()
    
    test_cases = [
        ("Tell me about RELIANCE stock", "RELIANCE"),
        ("RELIANCE stock price today", "RELIANCE"),
        ("What is TCS share price?", "TCS"),
        ("HDFC Bank stock analysis", "HDFC Bank"),
        ("upcoming IPO", None),
        ("market news today", None),
        ("How is Infosys doing?", "Infosys"),
        ("Zomato IPO GMP", "Zomato"),
    ]
    
    passed = 0
    for query, expected in test_cases:
        result = manager.extract_entity(query)
        if result == expected:
            passed += 1
            print(f"✅ '{query}' -> '{result}'")
        else:
            print(f"❌ '{query}' -> Expected '{expected}', got '{result}'")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.75  # 75% threshold


def test_intent_classification():
    """Test intent classification accuracy"""
    print("\n📋 Testing Intent Classification")
    print("-" * 40)
    
    manager = QueryTemplateManager()
    
    test_cases = [
        ("RELIANCE stock price today", "stock_overview"),
        ("TCS P/E ratio analysis", "stock_fundamental"),
        ("technical chart analysis for HDFC", "stock_technical"),
        ("latest news about Infosys stock", "stock_news"),
        ("upcoming IPOs this week", "upcoming_ipo"),
        ("Zomato IPO grey market premium", "ipo_gmp"),
        ("subscription status of IPO", "ipo_subscription"),
    ]
    
    passed = 0
    for query, expected_intent in test_cases:
        intent, confidence = manager.classify_intent(query)
        if intent == expected_intent:
            passed += 1
            print(f"✅ '{query}' -> {intent} (conf: {confidence:.2f})")
        else:
            print(f"❌ '{query}' -> Expected '{expected_intent}', got '{intent}' (conf: {confidence:.2f})")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.7  # 70% threshold


def test_query_generation():
    """Test query generation from templates"""
    print("\n📋 Testing Query Generation")
    print("-" * 40)
    
    manager = QueryTemplateManager()
    
    # Test 1: Stock query with template
    result = manager.get_query("RELIANCE stock price")
    assert isinstance(result, QueryResult), "Should return QueryResult"
    assert "RELIANCE" in result.query, f"Query should contain entity: {result.query}"
    assert result.use_llm_fallback == False, "Should not need LLM fallback"
    print(f"✅ Stock query: '{result.query}' (template: {result.template_used})")
    
    # Test 2: Ambiguous query should trigger fallback
    result = manager.get_query("what should I invest in?")
    assert result.use_llm_fallback == True, "Ambiguous query should trigger fallback"
    print(f"✅ Fallback triggered for ambiguous query (conf: {result.confidence:.2f})")
    
    # Test 3: IPO query
    result = manager.get_query("Zomato IPO GMP")
    assert "Zomato" in result.query, f"Query should contain entity: {result.query}"
    print(f"✅ IPO query: '{result.query}' (template: {result.template_used})")
    
    return True


def test_composite_queries():
    """Test composite query generation"""
    print("\n📋 Testing Composite Queries")
    print("-" * 40)
    
    manager = QueryTemplateManager()
    
    # Test stock comprehensive queries
    queries = manager.get_composite_queries("Analyze RELIANCE stock", entity="RELIANCE")
    assert len(queries) > 1, f"Should generate multiple queries, got {len(queries)}"
    
    print(f"Generated {len(queries)} queries for comprehensive analysis:")
    for q in queries:
        print(f"  - {q.template_used}: {q.query[:50]}...")
    
    # Test IPO queries
    ipo_queries = manager.get_ipo_queries("Zomato")
    assert len(ipo_queries) > 0, "Should generate IPO queries"
    print(f"\nGenerated {len(ipo_queries)} IPO queries:")
    for q in ipo_queries:
        print(f"  - {q.template_used}: {q.query[:50]}...")
    
    return True


def test_singleton_pattern():
    """Test singleton template manager"""
    print("\n📋 Testing Singleton Pattern")
    print("-" * 40)
    
    reset_template_manager()
    
    manager1 = get_template_manager()
    manager2 = get_template_manager()
    
    assert manager1 is manager2, "Should return same instance"
    print("✅ Singleton pattern working correctly")
    
    return True


def test_convenience_functions():
    """Test convenience functions"""
    print("\n📋 Testing Convenience Functions")
    print("-" * 40)
    
    result = optimize_query("TCS stock price")
    assert isinstance(result, QueryResult), "Should return QueryResult"
    print(f"✅ optimize_query: '{result.query}'")
    
    return True


def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Unit Tests: Query Template Manager")
    print("=" * 50)
    
    tests = [
        ("Entity Extraction", test_entity_extraction),
        ("Intent Classification", test_intent_classification),
        ("Query Generation", test_query_generation),
        ("Composite Queries", test_composite_queries),
        ("Singleton Pattern", test_singleton_pattern),
        ("Convenience Functions", test_convenience_functions),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {name} PASSED")
            else:
                failed += 1
                print(f"\n❌ {name} FAILED")
        except Exception as e:
            failed += 1
            print(f"\n❌ {name} ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 50)
    print(f"Results: {passed}/{passed + failed} tests passed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
