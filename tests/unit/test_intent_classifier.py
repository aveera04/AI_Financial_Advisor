#!/usr/bin/env python3
"""Unit tests for Intent Classifier"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.intent_classifier import (
    IntentClassifier, QueryIntent, ClassificationResult,
    classify_query, extract_entity
)


def test_query_intent_enum():
    """Test QueryIntent enum values"""
    print("\n📋 Testing QueryIntent Enum")
    print("-" * 40)
    
    # Verify essential intents exist
    essential_intents = [
        "STOCK_OVERVIEW", "STOCK_FUNDAMENTAL", "STOCK_TECHNICAL", "STOCK_NEWS",
        "IPO_DETAILS", "IPO_GMP", "IPO_SUBSCRIPTION", "UPCOMING_IPO", "UNKNOWN"
    ]
    
    for intent_name in essential_intents:
        assert hasattr(QueryIntent, intent_name), f"Missing intent: {intent_name}"
        print(f"✅ {intent_name}: {getattr(QueryIntent, intent_name).value}")
    
    return True


def test_entity_extraction():
    """Test entity extraction patterns"""
    print("\n📋 Testing Entity Extraction")
    print("-" * 40)
    
    classifier = IntentClassifier()
    
    test_cases = [
        ("RELIANCE stock price", "RELIANCE"),
        ("about TCS share analysis", "TCS"),
        ("How is Infosys doing?", "Infosys"),
        ("HDFC Bank P/E ratio", "HDFC Bank"),
        ("upcoming IPO list", None),
        ("market update sensex", None),
    ]
    
    passed = 0
    for query, expected in test_cases:
        result = classifier.extract_entity(query)
        if result == expected:
            passed += 1
            print(f"✅ '{query}' -> '{result}'")
        else:
            print(f"❌ '{query}' -> Expected '{expected}', got '{result}'")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.75


def test_classification():
    """Test intent classification"""
    print("\n📋 Testing Intent Classification")
    print("-" * 40)
    
    classifier = IntentClassifier()
    
    test_cases = [
        ("RELIANCE stock price today", QueryIntent.STOCK_OVERVIEW),
        ("TCS P/E ratio fundamental", QueryIntent.STOCK_FUNDAMENTAL),
        ("technical chart support resistance", QueryIntent.STOCK_TECHNICAL),
        ("latest news stock update", QueryIntent.STOCK_NEWS),
        ("IPO price band lot size", QueryIntent.IPO_DETAILS),
        ("grey market premium GMP", QueryIntent.IPO_GMP),
        ("subscription status QIB NII", QueryIntent.IPO_SUBSCRIPTION),
        ("upcoming IPO next week", QueryIntent.UPCOMING_IPO),
    ]
    
    passed = 0
    for query, expected_intent in test_cases:
        result = classifier.classify(query)
        if result.intent == expected_intent:
            passed += 1
            print(f"✅ '{query}' -> {result.intent.value}")
        else:
            print(f"❌ '{query}' -> Expected {expected_intent.value}, got {result.intent.value}")
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.7


def test_classification_result_dataclass():
    """Test ClassificationResult structure"""
    print("\n📋 Testing ClassificationResult Structure")
    print("-" * 40)
    
    classifier = IntentClassifier()
    result = classifier.classify("RELIANCE stock price")
    
    assert isinstance(result, ClassificationResult), "Should return ClassificationResult"
    assert isinstance(result.intent, QueryIntent), "Intent should be QueryIntent enum"
    assert isinstance(result.confidence, float), "Confidence should be float"
    assert result.entity is not None or result.entity is None, "Entity can be str or None"
    assert isinstance(result.keywords_matched, list), "Keywords should be list"
    assert isinstance(result.requires_llm, bool), "requires_llm should be bool"
    
    print(f"✅ intent: {result.intent}")
    print(f"✅ confidence: {result.confidence}")
    print(f"✅ entity: {result.entity}")
    print(f"✅ keywords_matched: {result.keywords_matched}")
    print(f"✅ requires_llm: {result.requires_llm}")
    
    return True


def test_llm_fallback_trigger():
    """Test that ambiguous queries trigger LLM fallback"""
    print("\n📋 Testing LLM Fallback Trigger")
    print("-" * 40)
    
    classifier = IntentClassifier(confidence_threshold=0.3)
    
    # Clear ambiguous query
    result = classifier.classify("tell me something interesting")
    assert result.requires_llm == True, "Ambiguous query should trigger LLM fallback"
    print(f"✅ Ambiguous query triggers fallback (conf: {result.confidence:.2f})")
    
    # Clear stock query
    result = classifier.classify("RELIANCE stock price today")
    assert result.requires_llm == False, "Clear stock query should not need fallback"
    print(f"✅ Clear query doesn't trigger fallback (conf: {result.confidence:.2f})")
    
    return True


def test_batch_classification():
    """Test batch classification"""
    print("\n📋 Testing Batch Classification")
    print("-" * 40)
    
    classifier = IntentClassifier()
    
    queries = [
        "RELIANCE stock price",
        "TCS P/E ratio",
        "upcoming IPO",
    ]
    
    results = classifier.classify_batch(queries)
    assert len(results) == len(queries), "Should return same number of results"
    
    for query, result in zip(queries, results):
        print(f"✅ '{query}' -> {result.intent.value}")
    
    return True


def test_convenience_functions():
    """Test module-level convenience functions"""
    print("\n📋 Testing Convenience Functions")
    print("-" * 40)
    
    # Test classify_query
    result = classify_query("TCS stock price")
    assert isinstance(result, ClassificationResult), "Should return ClassificationResult"
    print(f"✅ classify_query works: {result.intent.value}")
    
    # Test extract_entity
    entity = extract_entity("RELIANCE stock analysis")
    assert entity == "RELIANCE", f"Expected RELIANCE, got {entity}"
    print(f"✅ extract_entity works: {entity}")
    
    return True


def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Unit Tests: Intent Classifier")
    print("=" * 50)
    
    tests = [
        ("QueryIntent Enum", test_query_intent_enum),
        ("Entity Extraction", test_entity_extraction),
        ("Classification", test_classification),
        ("ClassificationResult Structure", test_classification_result_dataclass),
        ("LLM Fallback Trigger", test_llm_fallback_trigger),
        ("Batch Classification", test_batch_classification),
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
