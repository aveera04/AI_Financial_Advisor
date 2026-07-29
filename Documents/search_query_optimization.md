# Search Query Optimization - Execution Plan

## Financial Advisor Project Implementation Roadmap

**Document Version:** 1.0  
**Created:** January 29, 2026  
**Status:** Ready for Implementation  
**Estimated Duration:** 5-7 days  
**Priority:** High  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Assessment](#current-state-assessment)
3. [Target Architecture](#target-architecture)
4. [Implementation Phases](#implementation-phases)
5. [Phase 1: Foundation](#phase-1-foundation---day-1)
6. [Phase 2: Template System](#phase-2-template-system---day-2)
7. [Phase 3: Intent Classification](#phase-3-intent-classification---day-3)
8. [Phase 4: Integration](#phase-4-integration---day-3-4)
9. [Phase 5: Async Optimization](#phase-5-async-optimization---day-4-5)
10. [Phase 6: Testing](#phase-6-testing---day-5-6)
11. [Phase 7: Deployment](#phase-7-deployment---day-6-7)
12. [File Change Summary](#file-change-summary)
13. [Rollback Strategy](#rollback-strategy)
14. [Success Metrics](#success-metrics)

---

## Executive Summary

This execution plan details the step-by-step implementation of the **Template-Based Hybrid Query System** to optimize web search operations in the Financial Advisor project.

### Goals
- **Reduce token consumption** by 90% for query generation
- **Improve response time** by 60%
- **Lower API costs** by 40%
- **Maintain flexibility** for complex queries

### Key Changes
| Component | Current | Target |
|-----------|---------|--------|
| Query Generation | LLM-based (every query) | Template-based (90%) + LLM (10%) |
| Search Execution | Sequential | Parallel async |
| Token Usage | ~800/request | ~80/request |
| Latency | ~2000ms | ~800ms |

---

## Current State Assessment

### Files Requiring Changes

```
📁 Financial_Advisor/
├── 📁 utils/                          # Core changes here
│   ├── stock_info_search.py           # MODIFY - Remove LLM query gen
│   ├── ipo_info_search.py             # MODIFY - Remove LLM query gen
│   ├── query_templates.py             # CREATE - New template manager
│   ├── intent_classifier.py           # CREATE - New intent classifier
│   └── async_search.py                # CREATE - Async search utilities
├── 📁 tools/
│   ├── web_search_tool.py             # MODIFY - Use template system
│   └── stock_web_search_tool.py       # MODIFY - Use template system
├── 📁 config/
│   ├── config.yaml                    # MODIFY - Add search config
│   └── search_templates.yaml          # CREATE - Query templates
├── 📁 tests/
│   ├── unit/
│   │   ├── test_query_templates.py    # CREATE
│   │   └── test_intent_classifier.py  # CREATE
│   └── integration/
│       └── test_optimized_search.py   # CREATE
└── 📁 agent/
    └── agentic_workflow.py            # MINOR MODIFY - If needed
```

### Current LLM Usage for Query Generation

| File | Method | LLM Model | Tokens/Call |
|------|--------|-----------|-------------|
| `utils/stock_info_search.py` | `_generate_stock_query()` | groq_lamma_8b_instant | ~150 |
| `utils/ipo_info_search.py` | `_generate_ipo_query()` | groq_oss_20b | ~200 |
| `tools/web_search_tool.py` | `_generate_search_query()` | groq_oss_20b | ~200 |

**Total per comprehensive search:** ~800 tokens (4 calls)

---

## Target Architecture

### System Design

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         OPTIMIZED SEARCH SYSTEM                              │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────┐    ┌──────────────────────────────────────────────────────┐│
│  │ User Query  │───▶│              QUERY ROUTER                            ││
│  └─────────────┘    │  ┌─────────────────────────────────────────────────┐ ││
│                     │  │  Intent Classifier (Zero LLM)                   │ ││
│                     │  │  - Keyword matching                             │ ││
│                     │  │  - Pattern recognition                          │ ││
│                     │  │  - Entity extraction                            │ ││
│                     │  └─────────────────────────────────────────────────┘ ││
│                     └──────────────────────────────────────────────────────┘│
│                                        │                                     │
│                     ┌──────────────────┼──────────────────┐                 │
│                     ▼                  ▼                  ▼                 │
│  ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────────┐ │
│  │   TEMPLATE PATH      │ │   HYBRID PATH        │ │    LLM PATH          │ │
│  │   (Fast Track)       │ │   (Enhanced)         │ │    (Complex)         │ │
│  ├──────────────────────┤ ├──────────────────────┤ ├──────────────────────┤ │
│  │ • Stock price        │ │ • Template + entity  │ │ • Ambiguous queries  │ │
│  │ • IPO GMP            │ │ • Multi-topic split  │ │ • Comparative        │ │
│  │ • News search        │ │ • Conditional params │ │ • Open-ended         │ │
│  │ • Standard queries   │ │                      │ │                      │ │
│  ├──────────────────────┤ ├──────────────────────┤ ├──────────────────────┤ │
│  │ Tokens: 0            │ │ Tokens: ~50          │ │ Tokens: ~150         │ │
│  │ Latency: <10ms       │ │ Latency: ~100ms      │ │ Latency: ~500ms      │ │
│  │ Usage: 85%           │ │ Usage: 10%           │ │ Usage: 5%            │ │
│  └──────────────────────┘ └──────────────────────┘ └──────────────────────┘ │
│                     │                  │                  │                 │
│                     └──────────────────┼──────────────────┘                 │
│                                        ▼                                     │
│                     ┌──────────────────────────────────────────────────────┐│
│                     │            TAVILY SEARCH EXECUTOR                    ││
│                     │  ┌─────────────────────────────────────────────────┐ ││
│                     │  │  AsyncTavilyClient                              │ ││
│                     │  │  - Parallel execution                           │ ││
│                     │  │  - Optimized parameters                         │ ││
│                     │  │  - include_answer=True                          │ ││
│                     │  │  - Domain filtering                             │ ││
│                     │  └─────────────────────────────────────────────────┘ ││
│                     └──────────────────────────────────────────────────────┘│
│                                        │                                     │
│                                        ▼                                     │
│                     ┌──────────────────────────────────────────────────────┐│
│                     │            RESPONSE FORMATTER                        ││
│                     └──────────────────────────────────────────────────────┘│
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase Overview

| Phase | Description | Duration | Dependencies |
|-------|-------------|----------|--------------|
| **Phase 1** | Foundation - Config & Template Structure | Day 1 | None |
| **Phase 2** | Template System - Query Templates | Day 2 | Phase 1 |
| **Phase 3** | Intent Classification | Day 3 | Phase 1 |
| **Phase 4** | Integration - Connect Components | Day 3-4 | Phase 2, 3 |
| **Phase 5** | Async Optimization | Day 4-5 | Phase 4 |
| **Phase 6** | Testing | Day 5-6 | Phase 4, 5 |
| **Phase 7** | Deployment & Monitoring | Day 6-7 | Phase 6 |

---

## Phase 1: Foundation - Day 1

### Objective
Set up configuration structure and base classes for the template system.

### Step 1.1: Create Search Configuration

**File:** `config/search_templates.yaml`

```yaml
# Search Query Templates Configuration
# Version: 1.0

search_config:
  default_params:
    max_results: 5
    include_answer: true
    include_favicon: false
    country: "india"
  
  trusted_domains:
    financial:
      - "moneycontrol.com"
      - "economictimes.indiatimes.com"
      - "bseindia.com"
      - "nseindia.com"
      - "screener.in"
      - "tickertape.in"
    ipo:
      - "investorgain.com"
      - "chittorgarh.com"
      - "ipowatch.in"
      - "allipo.com"
  
  excluded_domains:
    - "reddit.com"
    - "quora.com"
    - "facebook.com"
    - "twitter.com"
    - "instagram.com"

templates:
  # Stock Templates
  stock_overview:
    pattern: "{entity} stock price NSE BSE today"
    search_depth: "basic"
    topic: "finance"
    max_results: 5
    description: "Current stock price and basic info"
    
  stock_fundamental:
    pattern: "{entity} stock P/E ratio ROE financial analysis"
    search_depth: "advanced"
    topic: "finance"
    max_results: 5
    description: "Fundamental analysis and financial ratios"
    
  stock_technical:
    pattern: "{entity} stock technical analysis chart support resistance"
    search_depth: "basic"
    topic: "finance"
    max_results: 3
    description: "Technical analysis and chart patterns"
    
  stock_news:
    pattern: "{entity} stock news latest"
    search_depth: "fast"
    topic: "news"
    time_range: "week"
    max_results: 5
    description: "Latest news and updates"
    
  stock_comprehensive:
    sub_queries:
      - "stock_overview"
      - "stock_fundamental"
      - "stock_news"
    parallel: true
    description: "Full stock analysis using multiple queries"

  # IPO Templates
  ipo_details:
    pattern: "{entity} IPO price band lot size subscription dates"
    search_depth: "advanced"
    topic: "finance"
    max_results: 5
    description: "IPO basic details and dates"
    
  ipo_gmp:
    pattern: "{entity} IPO grey market premium GMP today"
    search_depth: "basic"
    topic: "finance"
    time_range: "day"
    max_results: 3
    description: "Grey Market Premium information"
    
  ipo_subscription:
    pattern: "{entity} IPO subscription status QIB NII retail"
    search_depth: "basic"
    topic: "news"
    time_range: "day"
    max_results: 3
    description: "Subscription status by category"
    
  upcoming_ipo:
    pattern: "upcoming IPO India 2026"
    search_depth: "basic"
    topic: "news"
    time_range: "week"
    max_results: 10
    description: "List of upcoming IPOs"
    
  recent_ipo:
    pattern: "recent IPO listing India 2026 performance"
    search_depth: "basic"
    topic: "news"
    time_range: "month"
    max_results: 10
    description: "Recently listed IPOs"

  # General Templates
  market_news:
    pattern: "Indian stock market news today NSE BSE"
    search_depth: "fast"
    topic: "news"
    time_range: "day"
    max_results: 5
    description: "General market news"
    
  sector_analysis:
    pattern: "{entity} sector analysis India stocks"
    search_depth: "basic"
    topic: "finance"
    max_results: 5
    description: "Sector-specific analysis"

intent_patterns:
  stock_overview:
    keywords: ["stock", "share", "price", "current", "today", "trading"]
    entities: ["company_name", "stock_symbol"]
    priority: 1
    
  stock_fundamental:
    keywords: ["pe ratio", "p/e", "roe", "fundamental", "financial", "earnings", "revenue", "profit", "debt"]
    entities: ["company_name"]
    priority: 2
    
  stock_technical:
    keywords: ["technical", "chart", "support", "resistance", "rsi", "macd", "moving average", "trend"]
    entities: ["company_name"]
    priority: 2
    
  stock_news:
    keywords: ["news", "latest", "update", "announcement", "breaking"]
    entities: ["company_name"]
    priority: 1
    
  ipo_details:
    keywords: ["ipo", "issue", "price band", "lot size", "apply", "bid"]
    entities: ["company_name"]
    priority: 1
    
  ipo_gmp:
    keywords: ["gmp", "grey market", "gray market", "premium", "kostak"]
    entities: ["company_name"]
    priority: 1
    
  ipo_subscription:
    keywords: ["subscription", "subscribed", "times", "qib", "nii", "retail", "anchor"]
    entities: ["company_name"]
    priority: 2
    
  upcoming_ipo:
    keywords: ["upcoming", "next", "new ipo", "coming", "future"]
    entities: []
    priority: 1
    
  market_news:
    keywords: ["market", "sensex", "nifty", "index", "broader market"]
    entities: []
    priority: 2
```

### Step 1.2: Update Main Config

**File:** `config/config.yaml` - Add to existing file

```yaml
# Add to existing config.yaml

# Search optimization settings
search_optimization:
  enabled: true
  fallback_to_llm: true
  llm_threshold: 0.3  # Confidence threshold for template match
  cache_enabled: false  # Future: Redis caching
  logging_enabled: true
  
  # Performance tuning
  async_enabled: true
  max_parallel_searches: 4
  timeout_seconds: 30
  
  # LLM fallback configuration (for complex queries only)
  fallback_llm:
    model_provider: "groq_lamma_8b_instant"
    api_key_source: "GROQ_API_KEY_2"
    max_tokens: 50
```

### Step 1.3: Create Base Template Manager Structure

**File:** `utils/query_templates.py`

Create the skeleton structure (full implementation in Phase 2):

```python
#!/usr/bin/env python3
"""
Query Template Manager for Search Optimization
Provides template-based query generation with zero LLM overhead
"""

import yaml
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class QueryResult:
    """Result of query template resolution"""
    query: str
    search_depth: str
    topic: str
    max_results: int
    time_range: Optional[str] = None
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None
    use_llm_fallback: bool = False
    template_used: Optional[str] = None
    confidence: float = 1.0

class QueryTemplateManager:
    """
    Manages search query templates for optimal performance.
    Eliminates LLM calls for standard financial queries.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize with template configuration"""
        # Implementation in Phase 2
        pass
    
    def get_query(self, user_input: str, entity: str = None, 
                  intent: str = None) -> QueryResult:
        """
        Generate optimized query from template.
        
        Args:
            user_input: Original user query
            entity: Extracted entity (company name, etc.)
            intent: Pre-classified intent (optional)
            
        Returns:
            QueryResult with optimized query and parameters
        """
        # Implementation in Phase 2
        pass
    
    def get_composite_queries(self, user_input: str, 
                              entity: str = None) -> List[QueryResult]:
        """
        Generate multiple queries for comprehensive search.
        
        Returns:
            List of QueryResult objects for parallel execution
        """
        # Implementation in Phase 2
        pass

# Singleton instance
_template_manager = None

def get_template_manager() -> QueryTemplateManager:
    """Get or create singleton template manager"""
    global _template_manager
    if _template_manager is None:
        _template_manager = QueryTemplateManager()
    return _template_manager
```

### Step 1.4: Verification Checklist

- [ ] `config/search_templates.yaml` created
- [ ] `config/config.yaml` updated with search_optimization section
- [ ] `utils/query_templates.py` skeleton created
- [ ] All YAML files pass validation (no syntax errors)
- [ ] Existing tests still pass

---

## Phase 2: Template System - Day 2

### Objective
Implement the complete template resolution system.

### Step 2.1: Complete Query Template Manager

**File:** `utils/query_templates.py` - Full implementation

```python
#!/usr/bin/env python3
"""
Query Template Manager for Search Optimization
Provides template-based query generation with zero LLM overhead
"""

import yaml
import os
import re
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class QueryResult:
    """Result of query template resolution"""
    query: str
    search_depth: str = "basic"
    topic: str = "general"
    max_results: int = 5
    time_range: Optional[str] = None
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None
    include_answer: bool = True
    country: Optional[str] = "india"
    use_llm_fallback: bool = False
    template_used: Optional[str] = None
    confidence: float = 1.0
    original_query: str = ""
    entity: Optional[str] = None

@dataclass
class TemplateConfig:
    """Configuration for a single query template"""
    name: str
    pattern: str
    search_depth: str = "basic"
    topic: str = "general"
    max_results: int = 5
    time_range: Optional[str] = None
    description: str = ""
    sub_queries: List[str] = field(default_factory=list)
    parallel: bool = False

class QueryTemplateManager:
    """
    Manages search query templates for optimal performance.
    Eliminates LLM calls for standard financial queries.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize with template configuration"""
        if config_path is None:
            config_path = self._find_config_path()
        
        self.config_path = config_path
        self.templates: Dict[str, TemplateConfig] = {}
        self.intent_patterns: Dict[str, Dict] = {}
        self.default_params: Dict[str, Any] = {}
        self.trusted_domains: Dict[str, List[str]] = {}
        self.excluded_domains: List[str] = []
        
        self._load_config()
    
    def _find_config_path(self) -> str:
        """Find the search templates config file"""
        possible_paths = [
            Path(__file__).parent.parent / "config" / "search_templates.yaml",
            Path("config/search_templates.yaml"),
            Path("../config/search_templates.yaml"),
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        raise FileNotFoundError("search_templates.yaml not found")
    
    def _load_config(self):
        """Load and parse configuration from YAML"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Load search config defaults
        search_config = config.get('search_config', {})
        self.default_params = search_config.get('default_params', {})
        self.trusted_domains = search_config.get('trusted_domains', {})
        self.excluded_domains = search_config.get('excluded_domains', [])
        
        # Load templates
        templates_raw = config.get('templates', {})
        for name, template_data in templates_raw.items():
            self.templates[name] = TemplateConfig(
                name=name,
                pattern=template_data.get('pattern', ''),
                search_depth=template_data.get('search_depth', 'basic'),
                topic=template_data.get('topic', 'general'),
                max_results=template_data.get('max_results', 5),
                time_range=template_data.get('time_range'),
                description=template_data.get('description', ''),
                sub_queries=template_data.get('sub_queries', []),
                parallel=template_data.get('parallel', False)
            )
        
        # Load intent patterns
        self.intent_patterns = config.get('intent_patterns', {})
    
    def extract_entity(self, user_input: str) -> Optional[str]:
        """Extract company/stock name from user query"""
        patterns = [
            r"(?:about|for|of)\s+([A-Z][A-Za-z0-9&\s]+?)(?:\s+(?:stock|share|ipo|company|ltd|limited))",
            r"^([A-Z][A-Za-z0-9&\s]+?)(?:\s+(?:stock|share|ipo))",
            r"(?:how\s+is|what\s+about)\s+([A-Z][A-Za-z0-9&\s]+?)(?:\s+doing|\?|$)",
            r"^([A-Z][A-Za-z0-9&\s]+?)\s+(?:ipo|IPO)",
            r"\b([A-Z]{2,10})\b(?=\s+(?:stock|share|price|ipo))",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                entity = match.group(1).strip()
                entity = re.sub(r'\s+(ltd|limited|inc|corp)\.?$', '', entity, flags=re.IGNORECASE)
                return entity
        
        return None
    
    def classify_intent(self, user_input: str) -> Tuple[str, float]:
        """Classify user intent based on keyword matching"""
        query_lower = user_input.lower()
        scores = {}
        
        for intent_name, intent_config in self.intent_patterns.items():
            keywords = intent_config.get('keywords', [])
            score = 0
            
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', query_lower):
                        score += 1.0
                    else:
                        score += 0.5
            
            if keywords:
                scores[intent_name] = score / len(keywords)
            else:
                scores[intent_name] = 0
        
        if not scores or max(scores.values()) == 0:
            return ("unknown", 0.0)
        
        best_intent = max(scores, key=scores.get)
        confidence = scores[best_intent]
        
        return (best_intent, confidence)
    
    def get_query(self, user_input: str, entity: str = None,
                  intent: str = None, confidence: float = None) -> QueryResult:
        """Generate optimized query from template"""
        if entity is None:
            entity = self.extract_entity(user_input)
        
        if intent is None:
            intent, confidence = self.classify_intent(user_input)
        
        min_confidence = 0.3
        if confidence < min_confidence or intent == "unknown":
            return QueryResult(
                query=user_input,
                use_llm_fallback=True,
                original_query=user_input,
                entity=entity,
                confidence=confidence,
                template_used=None
            )
        
        template = self.templates.get(intent)
        if template is None:
            return QueryResult(
                query=user_input,
                use_llm_fallback=True,
                original_query=user_input,
                entity=entity,
                confidence=confidence,
                template_used=None
            )
        
        query = template.pattern
        if entity and "{entity}" in query:
            query = query.replace("{entity}", entity)
        elif "{entity}" in query:
            query = user_input
        
        include_domains = None
        if template.topic == "finance":
            include_domains = self.trusted_domains.get('financial', [])
        elif "ipo" in intent:
            include_domains = self.trusted_domains.get('ipo', [])
        
        return QueryResult(
            query=query,
            search_depth=template.search_depth,
            topic=template.topic,
            max_results=template.max_results,
            time_range=template.time_range,
            include_domains=include_domains,
            exclude_domains=self.excluded_domains,
            include_answer=self.default_params.get('include_answer', True),
            country=self.default_params.get('country', 'india'),
            use_llm_fallback=False,
            template_used=intent,
            confidence=confidence,
            original_query=user_input,
            entity=entity
        )
    
    def get_composite_queries(self, user_input: str,
                              entity: str = None,
                              template_name: str = None) -> List[QueryResult]:
        """Generate multiple queries for comprehensive search"""
        if entity is None:
            entity = self.extract_entity(user_input)
        
        if template_name is None:
            if entity:
                template_name = "stock_comprehensive"
            else:
                return [self.get_query(user_input, entity)]
        
        template = self.templates.get(template_name)
        if template is None or not template.sub_queries:
            return [self.get_query(user_input, entity)]
        
        queries = []
        for sub_template_name in template.sub_queries:
            result = self.get_query(
                user_input,
                entity=entity,
                intent=sub_template_name,
                confidence=1.0
            )
            result.template_used = sub_template_name
            queries.append(result)
        
        return queries
    
    def get_ipo_queries(self, company_name: str = None) -> List[QueryResult]:
        """Get queries for comprehensive IPO analysis"""
        queries = []
        
        if company_name:
            for template_name in ['ipo_details', 'ipo_gmp', 'ipo_subscription']:
                template = self.templates.get(template_name)
                if template:
                    query = template.pattern.replace("{entity}", company_name)
                    queries.append(QueryResult(
                        query=query,
                        search_depth=template.search_depth,
                        topic=template.topic,
                        max_results=template.max_results,
                        time_range=template.time_range,
                        include_domains=self.trusted_domains.get('ipo', []),
                        exclude_domains=self.excluded_domains,
                        include_answer=True,
                        country="india",
                        template_used=template_name,
                        confidence=1.0,
                        original_query=f"{company_name} IPO",
                        entity=company_name
                    ))
        else:
            template = self.templates.get('upcoming_ipo')
            if template:
                queries.append(QueryResult(
                    query=template.pattern,
                    search_depth=template.search_depth,
                    topic=template.topic,
                    max_results=template.max_results,
                    time_range=template.time_range,
                    include_domains=self.trusted_domains.get('ipo', []),
                    exclude_domains=self.excluded_domains,
                    include_answer=True,
                    country="india",
                    template_used='upcoming_ipo',
                    confidence=1.0,
                    original_query="upcoming IPO"
                ))
        
        return queries


# Singleton instance
_template_manager: Optional[QueryTemplateManager] = None

def get_template_manager() -> QueryTemplateManager:
    """Get or create singleton template manager"""
    global _template_manager
    if _template_manager is None:
        _template_manager = QueryTemplateManager()
    return _template_manager

def reset_template_manager():
    """Reset singleton (useful for testing)"""
    global _template_manager
    _template_manager = None
```

### Step 2.2: Verification Checklist

- [ ] `utils/query_templates.py` fully implemented
- [ ] Entity extraction working for common patterns
- [ ] Intent classification achieving 80%+ accuracy
- [ ] Query generation producing valid queries
- [ ] Composite queries generating multiple results

---

## Phase 3: Intent Classification - Day 3

### Objective
Create a standalone intent classifier module for reusability.

### Step 3.1: Create Intent Classifier Module

**File:** `utils/intent_classifier.py`

```python
#!/usr/bin/env python3
"""
Intent Classifier for Financial Queries
Zero-LLM keyword-based classification with entity extraction
"""

import re
from typing import Tuple, Optional, List, Dict
from dataclasses import dataclass
from enum import Enum

class QueryIntent(Enum):
    """Enumeration of supported query intents"""
    STOCK_OVERVIEW = "stock_overview"
    STOCK_FUNDAMENTAL = "stock_fundamental"
    STOCK_TECHNICAL = "stock_technical"
    STOCK_NEWS = "stock_news"
    IPO_DETAILS = "ipo_details"
    IPO_GMP = "ipo_gmp"
    IPO_SUBSCRIPTION = "ipo_subscription"
    UPCOMING_IPO = "upcoming_ipo"
    RECENT_IPO = "recent_ipo"
    MARKET_NEWS = "market_news"
    SECTOR_ANALYSIS = "sector_analysis"
    UNKNOWN = "unknown"

@dataclass
class ClassificationResult:
    """Result of intent classification"""
    intent: QueryIntent
    confidence: float
    entity: Optional[str]
    keywords_matched: List[str]
    requires_llm: bool = False

class IntentClassifier:
    """Fast, zero-LLM intent classifier for financial queries"""
    
    INTENT_KEYWORDS: Dict[QueryIntent, List[str]] = {
        QueryIntent.STOCK_OVERVIEW: [
            "stock", "share", "price", "current", "today", "trading",
            "quote", "live", "market price", "stock price"
        ],
        QueryIntent.STOCK_FUNDAMENTAL: [
            "pe ratio", "p/e", "roe", "roa", "fundamental", "financial",
            "earnings", "revenue", "profit", "debt", "balance sheet",
            "income statement", "eps", "book value", "dividend yield"
        ],
        QueryIntent.STOCK_TECHNICAL: [
            "technical", "chart", "support", "resistance", "rsi",
            "macd", "moving average", "trend", "breakout", "pattern"
        ],
        QueryIntent.STOCK_NEWS: [
            "news", "latest", "update", "announcement", "breaking",
            "headlines", "development", "report"
        ],
        QueryIntent.IPO_DETAILS: [
            "ipo", "issue", "price band", "lot size", "apply", "bid",
            "public offer", "initial public", "issue size", "ipo date"
        ],
        QueryIntent.IPO_GMP: [
            "gmp", "grey market", "gray market", "premium", "kostak",
            "expected listing", "listing gain"
        ],
        QueryIntent.IPO_SUBSCRIPTION: [
            "subscription", "subscribed", "times", "qib", "nii",
            "retail", "anchor", "oversubscribed", "allotment"
        ],
        QueryIntent.UPCOMING_IPO: [
            "upcoming", "next", "new ipo", "coming", "future",
            "this week", "this month", "scheduled"
        ],
        QueryIntent.MARKET_NEWS: [
            "market", "sensex", "nifty", "index", "broader market",
            "market today", "market update", "fii", "dii"
        ],
    }
    
    ENTITY_PATTERNS = [
        (r"(?:about|for|of)\s+([A-Z][A-Za-z0-9&\s]+?)(?:\s+(?:stock|share|ipo|company))", 1),
        (r"^([A-Z][A-Za-z0-9&\s]{1,30}?)(?:\s+(?:stock|share|ipo))", 1),
        (r"\b([A-Z]{2,15})\b(?=\s+(?:stock|share|price|ipo|pe|p/e))", 1),
        (r"(?:how\s+is|what\s+about|analyze|analysis\s+of)\s+([A-Z][A-Za-z0-9&\s]+?)(?:\s|$|\?)", 1),
    ]
    
    STOP_WORDS = {"stock", "share", "price", "ipo", "company", "analysis", "technical", "fundamental", "news", "today", "current"}
    
    def __init__(self, confidence_threshold: float = 0.3):
        self.confidence_threshold = confidence_threshold
    
    def extract_entity(self, query: str) -> Optional[str]:
        """Extract company/stock name from query"""
        for pattern, group_idx in self.ENTITY_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                entity = match.group(group_idx).strip()
                entity = re.sub(r'\s+(ltd|limited|inc|corp|stock|share|ipo)\.?$', '', entity, flags=re.IGNORECASE)
                entity = entity.strip()
                if entity.lower() in self.STOP_WORDS:
                    continue
                if len(entity) >= 2:
                    return entity
        return None
    
    def classify(self, query: str) -> ClassificationResult:
        """Classify query intent"""
        query_lower = query.lower()
        entity = self.extract_entity(query)
        
        scores: Dict[QueryIntent, Tuple[float, List[str]]] = {}
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            matched = []
            score = 0.0
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in query_lower:
                    if re.search(r'\b' + re.escape(keyword_lower) + r'\b', query_lower):
                        score += 1.0
                        matched.append(keyword)
                    else:
                        score += 0.3
                        matched.append(f"~{keyword}")
            
            if keywords:
                normalized_score = min(score / 3, 1.0)
                scores[intent] = (normalized_score, matched)
        
        if not scores:
            return ClassificationResult(
                intent=QueryIntent.UNKNOWN,
                confidence=0.0,
                entity=entity,
                keywords_matched=[],
                requires_llm=True
            )
        
        best_intent = max(scores.keys(), key=lambda k: scores[k][0])
        best_score, matched_keywords = scores[best_intent]
        
        requires_llm = best_score < self.confidence_threshold
        
        return ClassificationResult(
            intent=best_intent if not requires_llm else QueryIntent.UNKNOWN,
            confidence=best_score,
            entity=entity,
            keywords_matched=matched_keywords,
            requires_llm=requires_llm
        )

def classify_query(query: str) -> ClassificationResult:
    """Quick classification using default classifier"""
    classifier = IntentClassifier()
    return classifier.classify(query)
```

---

## Phase 4: Integration - Day 3-4

### Objective
Integrate the template system with existing search tools.

### Step 4.1: Create Optimized Search Wrapper

**File:** `utils/optimized_search.py`

```python
#!/usr/bin/env python3
"""
Optimized Search Module
Wraps Tavily search with template-based query optimization
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from langchain_tavily import TavilySearch

from utils.query_templates import QueryTemplateManager, QueryResult, get_template_manager
from utils.intent_classifier import IntentClassifier, QueryIntent
from utils.model_loader import ModelLoader

@dataclass
class SearchResult:
    """Standardized search result"""
    query_used: str
    original_query: str
    template_used: Optional[str]
    results: Any
    answer: Optional[str]
    search_depth: str
    tokens_used: int  # 0 for template, >0 for LLM
    status: str
    error: Optional[str] = None

class OptimizedSearchEngine:
    """Optimized search engine using template-based queries"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found")
        
        self.template_manager = get_template_manager()
        self.classifier = IntentClassifier()
        self.tavily = TavilySearch(api_key=self.api_key)
        self._llm = None
        self._llm_initialized = False
    
    @property
    def llm(self):
        """Lazy load LLM for fallback queries"""
        if not self._llm_initialized:
            try:
                loader = ModelLoader.from_env_key("groq_lamma_8b_instant", "GROQ_API_KEY_2")
                self._llm = loader.load_llm()
            except Exception as e:
                print(f"Warning: Could not load fallback LLM: {e}")
                self._llm = None
            self._llm_initialized = True
        return self._llm
    
    def _generate_llm_query(self, user_query: str, context: str = "general") -> str:
        """Generate optimized query using LLM (fallback)"""
        if not self.llm:
            return user_query
        
        prompt = f"""Convert this to a search query (max 50 words):
Query: {user_query}
Context: {context} financial data India

Search query:"""
        
        try:
            response = self.llm.invoke(prompt)
            result = response.content.strip() if hasattr(response, 'content') else str(response).strip()
            result = result.replace('"', '').replace("'", "")
            if len(result) > 200:
                return user_query
            return result
        except Exception:
            return user_query
    
    def search(self, user_query: str, force_template: str = None) -> SearchResult:
        """Execute optimized search"""
        tokens_used = 0
        
        classification = self.classifier.classify(user_query)
        
        if force_template:
            query_result = self.template_manager.get_query(
                user_query,
                entity=classification.entity,
                intent=force_template,
                confidence=1.0
            )
        else:
            query_result = self.template_manager.get_query(
                user_query,
                entity=classification.entity,
                intent=classification.intent.value if classification.intent != QueryIntent.UNKNOWN else None,
                confidence=classification.confidence
            )
        
        if query_result.use_llm_fallback:
            context = "stock" if "stock" in user_query.lower() else "general"
            if "ipo" in user_query.lower():
                context = "ipo"
            
            optimized_query = self._generate_llm_query(user_query, context)
            tokens_used = 100
            template_used = None
        else:
            optimized_query = query_result.query
            template_used = query_result.template_used
        
        try:
            search_params = {
                "query": optimized_query,
                "search_depth": query_result.search_depth,
                "topic": query_result.topic,
                "max_results": query_result.max_results,
                "include_answer": query_result.include_answer,
            }
            
            if query_result.time_range:
                search_params["time_range"] = query_result.time_range
            
            if query_result.include_domains:
                search_params["include_domains"] = query_result.include_domains[:10]
            
            if query_result.exclude_domains:
                search_params["exclude_domains"] = query_result.exclude_domains[:10]
            
            if query_result.country:
                search_params["country"] = query_result.country
            
            results = self.tavily.invoke(search_params)
            
            answer = None
            if isinstance(results, dict):
                answer = results.get('answer')
            
            return SearchResult(
                query_used=optimized_query,
                original_query=user_query,
                template_used=template_used,
                results=results,
                answer=answer,
                search_depth=query_result.search_depth,
                tokens_used=tokens_used,
                status="success"
            )
            
        except Exception as e:
            return SearchResult(
                query_used=optimized_query,
                original_query=user_query,
                template_used=template_used,
                results=None,
                answer=None,
                search_depth=query_result.search_depth,
                tokens_used=tokens_used,
                status="failed",
                error=str(e)
            )
    
    def search_stock(self, stock_name: str, search_type: str = "overview") -> SearchResult:
        """Search for stock information"""
        template_map = {
            "overview": "stock_overview",
            "fundamental": "stock_fundamental",
            "technical": "stock_technical",
            "news": "stock_news",
        }
        template = template_map.get(search_type, "stock_overview")
        query = f"{stock_name} stock {search_type}"
        return self.search(query, force_template=template)
    
    def search_ipo(self, company_name: str = None, search_type: str = "details") -> SearchResult:
        """Search for IPO information"""
        template_map = {
            "details": "ipo_details",
            "gmp": "ipo_gmp",
            "subscription": "ipo_subscription",
            "upcoming": "upcoming_ipo",
        }
        template = template_map.get(search_type, "ipo_details")
        
        if company_name:
            query = f"{company_name} IPO {search_type}"
        else:
            query = f"upcoming IPO India"
            template = "upcoming_ipo"
        
        return self.search(query, force_template=template)

_search_engine: Optional[OptimizedSearchEngine] = None

def get_search_engine() -> OptimizedSearchEngine:
    """Get or create singleton search engine"""
    global _search_engine
    if _search_engine is None:
        _search_engine = OptimizedSearchEngine()
    return _search_engine
```

### Step 4.2: Modify Existing Files

**File:** `utils/stock_info_search.py` - Add feature flag

```python
# ADD to __init__ method
def __init__(self, api_key: str = None, use_optimized: bool = True):
    """
    Initialize the Tavily Stock Info search tool
    
    Args:
        api_key: Tavily API key
        use_optimized: Use template-based optimization (default: True)
    """
    self.api_key = api_key or os.getenv("TAVILY_API_KEY")
    self.search_tool = TavilySearch(api_key=self.api_key)
    self.use_optimized = use_optimized
    
    if use_optimized:
        from utils.query_templates import get_template_manager
        from utils.intent_classifier import IntentClassifier
        self.template_manager = get_template_manager()
        self.classifier = IntentClassifier()
        self.query_generator = None  # Not needed with templates
    else:
        # Legacy LLM-based query generation
        # ... existing code ...
```

---

## Phase 5: Async Optimization - Day 4-5

### Objective
Implement parallel search execution for comprehensive queries.

### Step 5.1: Create Async Search Module

**File:** `utils/async_search.py`

```python
#!/usr/bin/env python3
"""Async Search Utilities - Parallel execution of multiple search queries"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from tavily import AsyncTavilyClient

from utils.query_templates import QueryResult, get_template_manager

@dataclass
class AsyncSearchResult:
    """Result from async search"""
    template: str
    query: str
    results: Any
    answer: Optional[str]
    status: str
    error: Optional[str] = None
    response_time_ms: float = 0.0

class AsyncSearchExecutor:
    """Executes multiple searches in parallel using async"""
    
    def __init__(self, api_key: str = None, max_concurrent: int = 4):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.max_concurrent = max_concurrent
        self.template_manager = get_template_manager()
        self._semaphore = asyncio.Semaphore(max_concurrent)
    
    async def _execute_single_search(self, client: AsyncTavilyClient, query_result: QueryResult) -> AsyncSearchResult:
        """Execute a single search with semaphore control"""
        import time
        start_time = time.time()
        
        async with self._semaphore:
            try:
                params = {
                    "query": query_result.query,
                    "search_depth": query_result.search_depth,
                    "topic": query_result.topic,
                    "max_results": query_result.max_results,
                    "include_answer": query_result.include_answer,
                }
                
                if query_result.time_range:
                    params["time_range"] = query_result.time_range
                if query_result.country:
                    params["country"] = query_result.country
                
                results = await client.search(**params)
                elapsed = (time.time() - start_time) * 1000
                
                return AsyncSearchResult(
                    template=query_result.template_used or "unknown",
                    query=query_result.query,
                    results=results,
                    answer=results.get('answer') if isinstance(results, dict) else None,
                    status="success",
                    response_time_ms=elapsed
                )
                
            except Exception as e:
                elapsed = (time.time() - start_time) * 1000
                return AsyncSearchResult(
                    template=query_result.template_used or "unknown",
                    query=query_result.query,
                    results=None,
                    answer=None,
                    status="failed",
                    error=str(e),
                    response_time_ms=elapsed
                )
    
    async def search_parallel(self, query_results: List[QueryResult]) -> List[AsyncSearchResult]:
        """Execute multiple searches in parallel"""
        async with AsyncTavilyClient(api_key=self.api_key) as client:
            tasks = [self._execute_single_search(client, qr) for qr in query_results]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(AsyncSearchResult(
                        template=query_results[i].template_used or "unknown",
                        query=query_results[i].query,
                        results=None,
                        answer=None,
                        status="error",
                        error=str(result)
                    ))
                else:
                    processed_results.append(result)
            
            return processed_results
    
    def search_parallel_sync(self, query_results: List[QueryResult]) -> List[AsyncSearchResult]:
        """Synchronous wrapper for parallel search"""
        return asyncio.run(self.search_parallel(query_results))
    
    async def comprehensive_stock_search(self, stock_name: str) -> Dict[str, AsyncSearchResult]:
        """Perform comprehensive stock analysis with parallel searches"""
        queries = self.template_manager.get_composite_queries(
            f"Analyze {stock_name} stock",
            entity=stock_name,
            template_name="stock_comprehensive"
        )
        
        results = await self.search_parallel(queries)
        return {result.template: result for result in results}
    
    async def comprehensive_ipo_search(self, company_name: str = None) -> Dict[str, AsyncSearchResult]:
        """Perform comprehensive IPO analysis with parallel searches"""
        queries = self.template_manager.get_ipo_queries(company_name)
        results = await self.search_parallel(queries)
        return {result.template: result for result in results}

def parallel_stock_search(stock_name: str) -> Dict[str, AsyncSearchResult]:
    """Quick comprehensive stock search (sync wrapper)"""
    executor = AsyncSearchExecutor()
    return asyncio.run(executor.comprehensive_stock_search(stock_name))

def parallel_ipo_search(company_name: str = None) -> Dict[str, AsyncSearchResult]:
    """Quick comprehensive IPO search (sync wrapper)"""
    executor = AsyncSearchExecutor()
    return asyncio.run(executor.comprehensive_ipo_search(company_name))
```

---

## Phase 6: Testing - Day 5-6

### Objective
Comprehensive testing of all new components.

### Step 6.1: Unit Tests

**File:** `tests/unit/test_query_templates.py`

```python
#!/usr/bin/env python3
"""Unit tests for Query Template Manager"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from utils.query_templates import QueryTemplateManager, get_template_manager, QueryResult

def test_entity_extraction():
    """Test entity extraction from queries"""
    manager = QueryTemplateManager()
    
    test_cases = [
        ("Tell me about RELIANCE stock", "RELIANCE"),
        ("RELIANCE stock price today", "RELIANCE"),
        ("What is TCS share price?", "TCS"),
        ("upcoming IPO", None),
    ]
    
    passed = 0
    for query, expected in test_cases:
        result = manager.extract_entity(query)
        if result == expected:
            passed += 1
            print(f"✅ '{query}' -> '{result}'")
        else:
            print(f"❌ '{query}' -> Expected '{expected}', got '{result}'")
    
    return passed == len(test_cases)

def test_intent_classification():
    """Test intent classification"""
    manager = QueryTemplateManager()
    
    test_cases = [
        ("RELIANCE stock price today", "stock_overview"),
        ("TCS P/E ratio analysis", "stock_fundamental"),
        ("upcoming IPOs this week", "upcoming_ipo"),
    ]
    
    passed = 0
    for query, expected_intent in test_cases:
        intent, confidence = manager.classify_intent(query)
        if intent == expected_intent:
            passed += 1
            print(f"✅ '{query}' -> {intent} (conf: {confidence:.2f})")
        else:
            print(f"❌ '{query}' -> Expected '{expected_intent}', got '{intent}'")
    
    return passed >= len(test_cases) * 0.8

def test_query_generation():
    """Test query generation from templates"""
    manager = QueryTemplateManager()
    
    result = manager.get_query("RELIANCE stock price")
    assert isinstance(result, QueryResult)
    assert "RELIANCE" in result.query
    assert result.use_llm_fallback == False
    print(f"✅ Stock query: '{result.query}'")
    
    result = manager.get_query("what should I invest in?")
    assert result.use_llm_fallback == True
    print(f"✅ Fallback triggered for ambiguous query")
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Query Template Manager\n")
    
    tests = [
        ("Entity Extraction", test_entity_extraction),
        ("Intent Classification", test_intent_classification),
        ("Query Generation", test_query_generation),
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"\n📋 {name}")
        print("-" * 40)
        try:
            if test_func():
                passed += 1
                print(f"✅ {name} PASSED")
            else:
                print(f"❌ {name} FAILED")
        except Exception as e:
            print(f"❌ {name} ERROR: {e}")
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

### Step 6.2: Integration Tests

**File:** `tests/integration/test_optimized_search.py`

```python
#!/usr/bin/env python3
"""Integration tests for optimized search system"""

import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv()

from utils.optimized_search import OptimizedSearchEngine, get_search_engine

def test_optimized_stock_search():
    """Test optimized stock search"""
    print("\n📊 Testing Optimized Stock Search")
    
    engine = get_search_engine()
    
    start = time.time()
    result = engine.search_stock("RELIANCE", "overview")
    elapsed = (time.time() - start) * 1000
    
    print(f"Query: '{result.query_used}'")
    print(f"Template: {result.template_used}")
    print(f"Tokens used: {result.tokens_used}")
    print(f"Time: {elapsed:.0f}ms")
    print(f"Status: {result.status}")
    
    assert result.status == "success"
    assert result.tokens_used == 0
    print("✅ Stock search passed")
    return True

def test_performance_comparison():
    """Compare performance: Template vs LLM"""
    print("\n📊 Performance Comparison")
    
    from utils.query_templates import get_template_manager
    
    manager = get_template_manager()
    start = time.time()
    manager.get_query("RELIANCE stock price")
    template_time = (time.time() - start) * 1000
    
    print(f"Template-based: {template_time:.2f}ms")
    print("✅ Performance comparison complete")
    return True

def main():
    """Run all integration tests"""
    print("🧪 Integration Tests: Optimized Search System")
    
    tests = [
        ("Optimized Stock Search", test_optimized_stock_search),
        ("Performance Comparison", test_performance_comparison),
    ]
    
    passed = 0
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} FAILED: {e}")
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

---

## Phase 7: Deployment - Day 6-7

### Step 7.1: Feature Flag Configuration

**File:** `config/config.yaml` - Add feature flags

```yaml
feature_flags:
  use_optimized_search: true
  use_parallel_search: true
  log_search_metrics: true
  fallback_to_legacy: true
```

### Step 7.2: Deployment Checklist

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Benchmark shows >50% improvement
- [ ] Feature flags configured
- [ ] Rollback procedure documented

### Step 7.3: Rollout Steps

1. **Stage 1: Shadow Mode (Day 6)** - Deploy with `use_optimized_search: false`, log template queries for comparison
2. **Stage 2: Partial Rollout (Day 6-7)** - Enable optimization with `fallback_to_legacy: true`
3. **Stage 3: Full Rollout (Day 7)** - Disable legacy fallback, remove deprecated code

---

## File Change Summary

### New Files to Create

| File | Description | Priority |
|------|-------------|----------|
| `config/search_templates.yaml` | Query templates configuration | P0 |
| `utils/query_templates.py` | Template manager | P0 |
| `utils/intent_classifier.py` | Intent classification | P0 |
| `utils/optimized_search.py` | Optimized search wrapper | P1 |
| `utils/async_search.py` | Async parallel search | P1 |
| `tests/unit/test_query_templates.py` | Unit tests | P1 |
| `tests/unit/test_intent_classifier.py` | Unit tests | P1 |
| `tests/integration/test_optimized_search.py` | Integration tests | P1 |

### Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| `config/config.yaml` | Add search optimization config | P0 |
| `utils/stock_info_search.py` | Add `use_optimized` flag | P1 |
| `utils/ipo_info_search.py` | Add `use_optimized` flag | P1 |
| `tools/web_search_tool.py` | Integrate optimized search | P1 |

---

## Rollback Strategy

### Immediate Rollback

```yaml
# config/config.yaml
feature_flags:
  use_optimized_search: false
  fallback_to_legacy: true
```

### Monitoring Triggers for Rollback

- Error rate > 5% for search operations
- Average latency increase > 50%
- User-reported accuracy issues

---

## Success Metrics

### Performance Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Tokens per query generation | ~200 | 0-50 | LLM API logs |
| Query generation latency | 500-1500ms | <50ms | Response time logs |
| Total search latency | ~2000ms | <1000ms | End-to-end timing |
| LLM API calls per request | 5 | 1 | API call count |

### Cost Metrics

| Metric | Current | Target | Savings |
|--------|---------|--------|---------|
| Monthly LLM token usage | ~84M | ~60M | ~$48-72 |

---

## Appendix: Quick Reference

### Intent to Template Mapping

| User Query Pattern | Intent | Template |
|-------------------|--------|----------|
| "{stock} stock price" | stock_overview | stock_overview |
| "{stock} P/E ratio" | stock_fundamental | stock_fundamental |
| "{stock} technical analysis" | stock_technical | stock_technical |
| "{stock} news" | stock_news | stock_news |
| "{company} IPO details" | ipo_details | ipo_details |
| "{company} IPO GMP" | ipo_gmp | ipo_gmp |
| "upcoming IPO" | upcoming_ipo | upcoming_ipo |

### Environment Variables Required

```env
TAVILY_API_KEY=tvly-xxxxx
GROQ_API_KEY=gsk-xxxxx
GROQ_API_KEY_2=gsk-xxxxx  # Optional, for LLM fallback
```

---

*Execution Plan v1.0 - Ready for Implementation*
