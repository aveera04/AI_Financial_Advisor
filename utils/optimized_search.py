#!/usr/bin/env python3
"""
Optimized Search Module
Wraps Tavily search with template-based query optimization

This module provides an optimized search interface that uses templates
for 90% of queries (zero LLM tokens) and falls back to LLM only for
complex/ambiguous queries.
"""

import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from langchain_tavily import TavilySearch

from utils.query_templates import (
    QueryTemplateManager, QueryResult, get_template_manager
)
from utils.intent_classifier import IntentClassifier, QueryIntent


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
    """
    Optimized search engine using template-based queries
    
    This engine eliminates LLM calls for standard financial queries,
    reducing token consumption by 90% and improving response time.
    
    Usage:
        engine = OptimizedSearchEngine()
        result = engine.search("RELIANCE stock price")
        # result.tokens_used = 0 (template-based)
        
        result = engine.search_stock("TCS", "fundamental")
        # Uses stock_fundamental template
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the optimized search engine
        
        Args:
            api_key: Tavily API key (defaults to env var)
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment")
        
        self.template_manager = get_template_manager()
        self.classifier = IntentClassifier()
        self.tavily = TavilySearch(api_key=self.api_key)
        
        # Lazy-load LLM for fallback
        self._llm = None
        self._llm_initialized = False
    
    @property
    def llm(self):
        """Lazy load LLM for fallback queries only"""
        if not self._llm_initialized:
            try:
                from utils.model_loader import ModelLoader
                loader = ModelLoader.from_env_key(
                    "groq_lamma_8b_instant", "GROQ_API_KEY_2"
                )
                self._llm = loader.load_llm()
            except Exception as e:
                print(f"Warning: Could not load fallback LLM: {e}")
                self._llm = None
            self._llm_initialized = True
        return self._llm
    
    def _generate_llm_query(self, user_query: str, context: str = "general") -> str:
        """
        Generate optimized query using LLM (fallback only)
        
        Args:
            user_query: Original user query
            context: Context type (stock, ipo, general)
            
        Returns:
            Optimized search query
        """
        if not self.llm:
            return user_query
        
        prompt = f"""Convert this to a search query (max 50 words):
Query: {user_query}
Context: {context} financial data India

Search query:"""
        
        try:
            response = self.llm.invoke(prompt)
            result = response.content.strip() if hasattr(response, 'content') else str(response).strip()
            # Clean up
            result = result.replace('"', '').replace("'", "")
            if len(result) > 200:
                return user_query
            return result
        except Exception:
            return user_query
    
    def search(self, user_query: str, force_template: str = None) -> SearchResult:
        """
        Execute optimized search
        
        Args:
            user_query: User's search query
            force_template: Force a specific template (optional)
            
        Returns:
            SearchResult with query, results, and metrics
        """
        tokens_used = 0
        
        # Classify intent
        classification = self.classifier.classify(user_query)
        
        # Get query from template
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
        
        # Handle LLM fallback
        if query_result.use_llm_fallback:
            context = "stock" if "stock" in user_query.lower() else "general"
            if "ipo" in user_query.lower():
                context = "ipo"
            
            optimized_query = self._generate_llm_query(user_query, context)
            tokens_used = 100  # Approximate token usage
            template_used = None
        else:
            optimized_query = query_result.query
            template_used = query_result.template_used
        
        # Execute search
        try:
            search_params = {
                "query": optimized_query,
                "search_depth": query_result.search_depth,
                "topic": query_result.topic,
                "max_results": query_result.max_results,
                "include_answer": query_result.include_answer,
            }
            
            # Add optional parameters
            if query_result.time_range:
                search_params["time_range"] = query_result.time_range
            
            if query_result.include_domains:
                search_params["include_domains"] = query_result.include_domains[:10]
            
            if query_result.exclude_domains:
                search_params["exclude_domains"] = query_result.exclude_domains[:10]
            
            if query_result.country:
                search_params["country"] = query_result.country
            
            results = self.tavily.invoke(search_params)
            
            # Extract answer if available
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
        """
        Search for stock information
        
        Args:
            stock_name: Stock name or symbol
            search_type: Type of search (overview, fundamental, technical, news)
            
        Returns:
            SearchResult
        """
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
        """
        Search for IPO information
        
        Args:
            company_name: Company name (optional for upcoming IPOs)
            search_type: Type of search (details, gmp, subscription, upcoming)
            
        Returns:
            SearchResult
        """
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
    
    def search_market(self, topic: str = "news") -> SearchResult:
        """
        Search for market information
        
        Args:
            topic: Topic type (news, etc.)
            
        Returns:
            SearchResult
        """
        return self.search("market news today", force_template="market_news")


# Singleton instance
_search_engine: Optional[OptimizedSearchEngine] = None


def get_search_engine() -> OptimizedSearchEngine:
    """Get or create singleton search engine"""
    global _search_engine
    if _search_engine is None:
        _search_engine = OptimizedSearchEngine()
    return _search_engine


def reset_search_engine():
    """Reset singleton (useful for testing)"""
    global _search_engine
    _search_engine = None


# Convenience functions
def optimized_search(query: str) -> SearchResult:
    """Quick optimized search using default engine"""
    return get_search_engine().search(query)


def stock_search(stock_name: str, search_type: str = "overview") -> SearchResult:
    """Quick stock search"""
    return get_search_engine().search_stock(stock_name, search_type)


def ipo_search(company_name: str = None, search_type: str = "details") -> SearchResult:
    """Quick IPO search"""
    return get_search_engine().search_ipo(company_name, search_type)


if __name__ == "__main__":
    # Quick test (requires TAVILY_API_KEY)
    print("🧪 Testing OptimizedSearchEngine\n")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        engine = OptimizedSearchEngine()
        
        # Test template-based search
        result = engine.search("RELIANCE stock price today")
        print(f"Query: {result.original_query}")
        print(f"  Used: {result.query_used}")
        print(f"  Template: {result.template_used}")
        print(f"  Tokens: {result.tokens_used}")
        print(f"  Status: {result.status}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure TAVILY_API_KEY is set")
