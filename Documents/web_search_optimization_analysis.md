# Web Search Query Optimization Analysis

## Financial Advisor Project - Search Strategy Evaluation

**Document Version:** 1.0  
**Date:** January 29, 2026  
**Author:** AI Analysis  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Approach Analysis](#current-approach-analysis)
3. [Hard-Coded vs Customized Search Queries](#hard-coded-vs-customized-search-queries)
4. [Detailed Comparison Matrix](#detailed-comparison-matrix)
5. [Token Consumption Analysis](#token-consumption-analysis)
6. [Performance & Latency Analysis](#performance--latency-analysis)
7. [Output Quality Analysis](#output-quality-analysis)
8. [Recommended Hybrid Approach](#recommended-hybrid-approach)
9. [Implementation Guidelines](#implementation-guidelines)
10. [Best Practices from Tavily Documentation](#best-practices-from-tavily-documentation)

---

## Executive Summary

After analyzing your Financial Advisor project's web search implementation, I've identified that you are currently using a **hybrid approach** with LLM-powered query generation. While this provides flexibility, it introduces significant overhead in terms of:

- **Token consumption** (extra LLM calls for query optimization)
- **Latency** (additional API round-trips)
- **Cost** (multiple model invocations)

**Recommendation:** Implement a **Template-Based Query System with Selective LLM Enhancement** - this provides the best balance of accuracy, speed, and cost efficiency.

---

## Current Approach Analysis

### Your Current Implementation

Based on the code analysis of your project:

#### 1. IPO Search (`utils/ipo_info_search.py`)
```python
# Current: Uses LLM to generate queries
def _generate_ipo_query(self, user_query: str, ipo_context: str = "general") -> str:
    if not self.query_generator:
        # Fallback to manual query enhancement
        if ipo_context == "listing":
            return f"{user_query} IPO listing date price subscription"
        # ... more fallback patterns
```

#### 2. Stock Search (`utils/stock_info_search.py`)
```python
# Current: Uses LLM with appended keywords
overview_query = self._generate_stock_query(
    user_query + " company overview sector market cap current price NSE BSE 52-week high low...",
    "overview"
)
```

#### 3. Web Search Tool (`tools/web_search_tool.py`)
```python
# Current: LLM-based query transformation
def _generate_search_query(self, user_query: str, search_type: str = "general") -> str:
    prompt = f"""Transform the following user query into an optimized search query..."""
    response = self.query_generator.invoke(prompt)
```

### Issues with Current Approach

| Issue | Impact | Severity |
|-------|--------|----------|
| **Double LLM invocation** | Each search requires LLM call for query generation + main agent LLM | 🔴 High |
| **Token overhead** | ~150-300 tokens per query generation prompt | 🔴 High |
| **Latency increase** | +500-1500ms per search operation | 🟠 Medium |
| **Inconsistent results** | LLM may generate varying queries for same input | 🟠 Medium |
| **Redundant keyword appending** | Pre-appending keywords before LLM optimization defeats purpose | 🟡 Low |

---

## Hard-Coded vs Customized Search Queries

### Approach 1: Hard-Coded Search Queries

**Definition:** Pre-defined query templates with variable substitution.

```python
# Example Hard-Coded Approach
QUERY_TEMPLATES = {
    "stock_overview": "{stock_name} stock price NSE BSE market cap 52-week range",
    "ipo_gmp": "{company} IPO grey market premium GMP today",
    "fundamental": "{stock_name} P/E ratio ROE financial ratios annual report",
}

def search_stock_overview(stock_name: str) -> str:
    query = QUERY_TEMPLATES["stock_overview"].format(stock_name=stock_name)
    return tavily_search(query)
```

#### Pros ✅
| Benefit | Description |
|---------|-------------|
| **Zero token overhead** | No LLM calls for query generation |
| **Fastest execution** | Direct string formatting, ~0ms overhead |
| **Consistent results** | Same query pattern every time |
| **Predictable costs** | Only Tavily API credits consumed |
| **Easy debugging** | Queries are transparent and traceable |

#### Cons ❌
| Drawback | Description |
|----------|-------------|
| **Limited flexibility** | Cannot adapt to unusual queries |
| **Maintenance burden** | Requires manual updates for new patterns |
| **May miss context** | Cannot understand nuanced user intent |

---

### Approach 2: LLM-Customized Search Queries

**Definition:** Using LLM to dynamically generate optimized search queries.

```python
# Example LLM-Customized Approach (Your Current Implementation)
def _generate_search_query(self, user_query: str, search_type: str) -> str:
    prompt = f"""Transform query into optimized search: {user_query}"""
    response = self.query_generator.invoke(prompt)
    return response.content.strip()
```

#### Pros ✅
| Benefit | Description |
|---------|-------------|
| **Maximum flexibility** | Adapts to any query type |
| **Context understanding** | Can interpret complex/ambiguous queries |
| **Natural language** | Handles conversational inputs well |

#### Cons ❌
| Drawback | Description |
|----------|-------------|
| **High token consumption** | 150-300 tokens per query generation |
| **Increased latency** | +500-1500ms per operation |
| **Inconsistent results** | Same input may produce different queries |
| **Higher costs** | Additional LLM API costs |
| **Failure points** | LLM errors can break search flow |

---

## Detailed Comparison Matrix

| Criteria | Hard-Coded | LLM-Customized | Hybrid (Recommended) |
|----------|------------|----------------|---------------------|
| **Token Consumption** | ⭐⭐⭐⭐⭐ (0 tokens) | ⭐⭐ (~200 tokens/query) | ⭐⭐⭐⭐ (~50 tokens avg) |
| **Execution Speed** | ⭐⭐⭐⭐⭐ (<10ms) | ⭐⭐ (500-1500ms) | ⭐⭐⭐⭐ (~100ms avg) |
| **Query Accuracy** | ⭐⭐⭐ (pattern-limited) | ⭐⭐⭐⭐ (context-aware) | ⭐⭐⭐⭐⭐ (best of both) |
| **Cost Efficiency** | ⭐⭐⭐⭐⭐ (lowest) | ⭐⭐ (highest) | ⭐⭐⭐⭐ (balanced) |
| **Flexibility** | ⭐⭐ (rigid) | ⭐⭐⭐⭐⭐ (maximum) | ⭐⭐⭐⭐ (selective) |
| **Reliability** | ⭐⭐⭐⭐⭐ (consistent) | ⭐⭐⭐ (variable) | ⭐⭐⭐⭐ (stable) |
| **Maintenance** | ⭐⭐⭐ (manual updates) | ⭐⭐⭐⭐ (self-adapting) | ⭐⭐⭐⭐ (low) |

---

## Token Consumption Analysis

### Current Implementation Token Usage

```
Per Stock Analysis Request:
┌─────────────────────────────────────────────────────────────────┐
│ Component                          │ Tokens  │ API Calls      │
├─────────────────────────────────────────────────────────────────┤
│ Main Agent (Orchestrator)          │ ~2000   │ 1 LLM call     │
│ Query Generation - Overview        │ ~200    │ 1 LLM call     │
│ Query Generation - Fundamental     │ ~200    │ 1 LLM call     │
│ Query Generation - Technical       │ ~200    │ 1 LLM call     │
│ Query Generation - News            │ ~200    │ 1 LLM call     │
├─────────────────────────────────────────────────────────────────┤
│ TOTAL                              │ ~2800   │ 5 LLM calls    │
└─────────────────────────────────────────────────────────────────┘
```

### Optimized Implementation (Recommended)

```
Per Stock Analysis Request:
┌─────────────────────────────────────────────────────────────────┐
│ Component                          │ Tokens  │ API Calls      │
├─────────────────────────────────────────────────────────────────┤
│ Main Agent (Orchestrator)          │ ~2000   │ 1 LLM call     │
│ Template-Based Query Generation    │ 0       │ 0 LLM calls    │
├─────────────────────────────────────────────────────────────────┤
│ TOTAL                              │ ~2000   │ 1 LLM call     │
└─────────────────────────────────────────────────────────────────┘

Token Savings: ~800 tokens per request (29% reduction)
API Call Savings: 4 LLM calls per request (80% reduction)
```

### Annual Cost Projection (1000 requests/day)

| Approach | Monthly Token Usage | Monthly Cost (Est.) |
|----------|---------------------|---------------------|
| Current (LLM-based) | 84M tokens | $168 - $252 |
| Optimized (Template) | 60M tokens | $120 - $180 |
| **Savings** | **24M tokens** | **$48 - $72/month** |

---

## Performance & Latency Analysis

### Current Latency Breakdown

```
User Query → Response Timeline (Current)
────────────────────────────────────────────────────────────────────
0ms         500ms       1000ms      1500ms      2000ms      2500ms
│           │           │           │           │           │
├───────────┼───────────┼───────────┼───────────┼───────────┤
│ Query Gen │ Tavily    │ Query Gen │ Tavily    │ Response  │
│ LLM Call  │ Search 1  │ LLM Call  │ Search 2  │ Process   │
│ (~500ms)  │ (~400ms)  │ (~500ms)  │ (~400ms)  │ (~200ms)  │
────────────────────────────────────────────────────────────────────
Total: ~2000ms for 2 searches
```

### Optimized Latency (Template-Based)

```
User Query → Response Timeline (Optimized)
────────────────────────────────────────────────────────────────────
0ms         500ms       1000ms      1500ms      2000ms
│           │           │           │           │
├───────────┼───────────┼───────────┼───────────┤
│ Template  │ Parallel  │ Response  │
│ Format    │ Tavily    │ Process   │
│ (~10ms)   │ Searches  │ (~200ms)  │
│           │ (~600ms)  │           │
────────────────────────────────────────────────────────────────────
Total: ~810ms for 2 parallel searches

Improvement: ~60% faster response time
```

---

## Output Quality Analysis

### Search Result Quality Comparison

Based on Tavily's best practices and your domain requirements:

| Query Type | Hard-Coded Quality | LLM-Generated Quality | Winner |
|------------|-------------------|----------------------|--------|
| **Stock Overview** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Hard-Coded |
| **IPO GMP** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Hard-Coded |
| **News Search** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Tie |
| **Complex Multi-Topic** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | LLM |
| **Ambiguous Queries** | ⭐⭐ | ⭐⭐⭐⭐⭐ | LLM |

### Key Insight from Tavily Documentation

> **"Keep queries concise—under 400 characters. Think of it as a query for an agent performing web search, not long-form prompts."**

Your current implementation appends many keywords which may actually **reduce** search quality:
```python
# Your current approach (potentially suboptimal)
overview_query = self._generate_stock_query(
    user_query + " company overview sector market cap current price NSE BSE 52-week high low trading volume beta dividend yield",
    "overview"
)
```

**Problem:** This creates queries that are:
- Too long (may exceed optimal 400 character limit)
- Over-specific (reduces search engine flexibility)
- Redundant (LLM then tries to "optimize" an already keyword-stuffed query)

---

## Recommended Hybrid Approach

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID QUERY SYSTEM                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │ User Query   │───▶│ Intent       │───▶│ Route to     │     │
│  │ Input        │    │ Classifier   │    │ Strategy     │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│                              │                   │              │
│                              ▼                   ▼              │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    ROUTING LOGIC                        │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                         │   │
│  │  ┌─────────────────┐        ┌─────────────────┐        │   │
│  │  │ TEMPLATE PATH   │        │ LLM PATH        │        │   │
│  │  │ (90% of cases)  │        │ (10% of cases)  │        │   │
│  │  ├─────────────────┤        ├─────────────────┤        │   │
│  │  │ • Stock queries │        │ • Ambiguous     │        │   │
│  │  │ • IPO queries   │        │ • Multi-topic   │        │   │
│  │  │ • News queries  │        │ • Comparative   │        │   │
│  │  │ • Price data    │        │ • Complex       │        │   │
│  │  └─────────────────┘        └─────────────────┘        │   │
│  │           │                          │                  │   │
│  │           ▼                          ▼                  │   │
│  │  ┌─────────────────┐        ┌─────────────────┐        │   │
│  │  │ Template Query  │        │ LLM Query       │        │   │
│  │  │ Generation      │        │ Generation      │        │   │
│  │  │ (~0 tokens)     │        │ (~100 tokens)   │        │   │
│  │  └─────────────────┘        └─────────────────┘        │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│                    ┌──────────────────┐                        │
│                    │ Tavily Search    │                        │
│                    │ with Optimized   │                        │
│                    │ Parameters       │                        │
│                    └──────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Query Template Library

```python
# Recommended Template Structure
FINANCIAL_QUERY_TEMPLATES = {
    # Stock Templates
    "stock_overview": {
        "template": "{entity} stock price current NSE BSE",
        "search_depth": "basic",
        "topic": "finance",
        "max_results": 5
    },
    "stock_fundamental": {
        "template": "{entity} stock P/E ratio financial analysis",
        "search_depth": "advanced",
        "topic": "finance",
        "max_results": 5
    },
    "stock_technical": {
        "template": "{entity} stock technical analysis support resistance",
        "search_depth": "basic",
        "topic": "finance",
        "max_results": 3
    },
    "stock_news": {
        "template": "{entity} stock news latest",
        "search_depth": "basic",
        "topic": "news",
        "time_range": "week",
        "max_results": 5
    },
    
    # IPO Templates
    "ipo_details": {
        "template": "{entity} IPO price band lot size dates",
        "search_depth": "advanced",
        "topic": "finance",
        "max_results": 5
    },
    "ipo_gmp": {
        "template": "{entity} IPO grey market premium GMP today",
        "search_depth": "basic",
        "topic": "finance",
        "time_range": "day",
        "max_results": 3
    },
    "ipo_subscription": {
        "template": "{entity} IPO subscription status QIB NII retail",
        "search_depth": "basic",
        "topic": "news",
        "max_results": 3
    },
    "upcoming_ipo": {
        "template": "upcoming IPO India 2026 January February",
        "search_depth": "basic",
        "topic": "news",
        "time_range": "week",
        "max_results": 10
    }
}
```

### Intent Classification (Lightweight)

```python
# Keyword-based intent classification (no LLM needed)
INTENT_PATTERNS = {
    "stock_overview": ["stock", "share", "price", "current", "today"],
    "stock_fundamental": ["pe ratio", "roe", "fundamental", "financial", "earnings", "revenue"],
    "stock_technical": ["technical", "chart", "support", "resistance", "rsi", "macd"],
    "stock_news": ["news", "latest", "update", "announcement"],
    "ipo_details": ["ipo", "issue", "price band", "lot size"],
    "ipo_gmp": ["gmp", "grey market", "premium"],
    "ipo_subscription": ["subscription", "allotment", "qib", "retail"],
    "upcoming_ipo": ["upcoming", "next", "new ipo"]
}

def classify_intent(query: str) -> str:
    query_lower = query.lower()
    scores = {}
    
    for intent, keywords in INTENT_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in query_lower)
        scores[intent] = score
    
    # If no clear intent, fall back to LLM
    max_score = max(scores.values())
    if max_score < 2:
        return "needs_llm"
    
    return max(scores, key=scores.get)
```

---

## Implementation Guidelines

### Step 1: Create Query Template Manager

```python
# utils/query_templates.py
class QueryTemplateManager:
    """Manages search query templates for optimal performance"""
    
    def __init__(self):
        self.templates = FINANCIAL_QUERY_TEMPLATES
        self.intent_patterns = INTENT_PATTERNS
    
    def get_query(self, user_input: str, entity: str = None) -> dict:
        """Returns optimized query and Tavily parameters"""
        intent = self._classify_intent(user_input)
        
        if intent == "needs_llm":
            return {"use_llm": True, "user_input": user_input}
        
        template_config = self.templates[intent]
        query = template_config["template"].format(
            entity=entity or self._extract_entity(user_input)
        )
        
        return {
            "use_llm": False,
            "query": query,
            "search_depth": template_config.get("search_depth", "basic"),
            "topic": template_config.get("topic", "general"),
            "time_range": template_config.get("time_range"),
            "max_results": template_config.get("max_results", 5)
        }
```

### Step 2: Optimize Tavily API Usage

Based on Tavily documentation best practices:

```python
# Optimized Tavily Search Configuration
TAVILY_OPTIMAL_CONFIG = {
    "stock_search": {
        "search_depth": "basic",      # 1 credit, balanced latency/relevance
        "topic": "finance",            # Use finance topic for financial queries
        "max_results": 5,              # Don't request too many
        "include_answer": True,        # Get LLM summary from Tavily
        "country": "india"             # Boost Indian market results
    },
    "ipo_search": {
        "search_depth": "advanced",    # 2 credits, highest relevance
        "topic": "finance",
        "max_results": 5,
        "include_answer": True,
        "time_range": "week"           # Recent IPO data
    },
    "news_search": {
        "search_depth": "fast",        # 1 credit, prioritize speed
        "topic": "news",
        "max_results": 5,
        "time_range": "day"
    }
}
```

### Step 3: Implement Parallel Search

```python
# Use async for parallel searches
import asyncio
from tavily import AsyncTavilyClient

async def parallel_stock_search(stock_name: str):
    """Execute multiple searches in parallel"""
    tavily = AsyncTavilyClient(api_key)
    
    queries = [
        {"query": f"{stock_name} stock price NSE", "topic": "finance"},
        {"query": f"{stock_name} stock news today", "topic": "news"},
        {"query": f"{stock_name} financial results", "topic": "finance"}
    ]
    
    results = await asyncio.gather(
        *[tavily.search(**q) for q in queries],
        return_exceptions=True
    )
    
    return results
```

---

## Best Practices from Tavily Documentation

### 1. Query Optimization Rules

| Rule | Description | Your Current Status |
|------|-------------|---------------------|
| **< 400 characters** | Keep queries concise | ❌ Some queries exceed this |
| **Break complex queries** | Split multi-topic into sub-queries | ⚠️ Partially implemented |
| **Avoid keyword stuffing** | Focus on key terms | ❌ Current approach appends many keywords |
| **Use topic parameter** | Set `finance` or `news` appropriately | ⚠️ Not consistently used |

### 2. Optimal Search Depth Selection

| Use Case | Recommended Depth | Credits |
|----------|-------------------|---------|
| Real-time stock prices | `fast` or `ultra-fast` | 1 |
| Company overview | `basic` | 1 |
| Detailed financial analysis | `advanced` | 2 |
| IPO detailed information | `advanced` | 2 |
| News updates | `fast` | 1 |

### 3. Leverage Tavily Features

**Use `include_answer: true`** - This gives you an LLM-generated answer directly from Tavily, reducing the need for post-processing:

```python
response = tavily.search(
    query="RELIANCE stock price today",
    include_answer=True,  # Tavily generates summary
    topic="finance"
)
# response.answer contains ready-to-use summary
```

**Use `auto_parameters: true`** for complex queries:

```python
response = tavily.search(
    query=complex_user_query,
    auto_parameters=True,
    search_depth="basic"  # Override to control cost
)
```

### 4. Domain Filtering for Finance

```python
# Include trusted financial sources
TRUSTED_FINANCIAL_DOMAINS = [
    "moneycontrol.com",
    "economictimes.indiatimes.com",
    "bseindia.com",
    "nseindia.com",
    "investorgain.com",
    "screener.in",
    "tickertape.in"
]

# Exclude irrelevant domains
EXCLUDED_DOMAINS = [
    "reddit.com",
    "quora.com",
    "facebook.com",
    "twitter.com"
]
```

---

## Summary & Recommendations

### Immediate Actions (High Impact, Low Effort)

1. **Remove LLM-based query generation for standard queries**
   - Use template-based approach for 90% of queries
   - Save ~800 tokens and 4 LLM calls per request

2. **Implement parallel Tavily searches**
   - Use `AsyncTavilyClient` for concurrent requests
   - Reduce total latency by 50-60%

3. **Stop appending excessive keywords before LLM optimization**
   - Current approach: `user_query + " company overview sector market cap..."`
   - Recommended: Use focused template or pass raw query

### Medium-Term Improvements

4. **Create comprehensive query template library**
   - Cover all common financial query patterns
   - Include optimal Tavily parameters for each

5. **Implement keyword-based intent classification**
   - Fast, zero-token intent detection
   - Fall back to LLM only for ambiguous queries

6. **Use Tavily's `include_answer` feature**
   - Get pre-generated summaries from Tavily
   - Reduce post-processing in your agent

### Metrics to Track

| Metric | Current (Est.) | Target | Improvement |
|--------|----------------|--------|-------------|
| Tokens per search | ~200 | ~20 | 90% ↓ |
| LLM calls per request | 5 | 1 | 80% ↓ |
| Response time | ~2000ms | ~800ms | 60% ↓ |
| Monthly cost | $200+ | $120 | 40% ↓ |
| Query accuracy | Good | Excellent | ↑ |

---

## Conclusion

The **Template-Based Hybrid Approach** offers the best balance for your Financial Advisor project:

- ✅ **90% token reduction** in query generation
- ✅ **60% faster** response times
- ✅ **40% cost reduction** in LLM API usage
- ✅ **Improved consistency** in search results
- ✅ **Maintained flexibility** for complex queries

The key insight is that financial queries are highly predictable and domain-specific. Pre-defined templates with proper Tavily parameters will outperform LLM-generated queries in most cases while being significantly more efficient.

---

## References

1. [Tavily API Documentation](https://docs.tavily.com)
2. [Tavily Search Best Practices](https://docs.tavily.com/documentation/best-practices/best-practices-search)
3. [Tavily Search API Reference](https://docs.tavily.com/documentation/api-reference/endpoint/search)
4. [LangChain Tavily Integration](https://python.langchain.com/docs/integrations/tools/tavily_search)

---

*Document generated for Financial_Advisor project optimization*
