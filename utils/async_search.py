#!/usr/bin/env python3
"""
Async Search Utilities
Parallel execution of multiple search queries for comprehensive analysis

This module provides async/parallel search capabilities for executing
multiple Tavily queries simultaneously, reducing total response time.
"""

import asyncio
import os
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

try:
    from tavily import AsyncTavilyClient
    ASYNC_AVAILABLE = True
except ImportError:
    ASYNC_AVAILABLE = False
    print("Warning: AsyncTavilyClient not available. Install with: pip install tavily-python")

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
    """
    Executes multiple searches in parallel using async
    
    This executor significantly reduces total response time by running
    multiple Tavily searches concurrently instead of sequentially.
    
    Usage:
        executor = AsyncSearchExecutor()
        
        # Async usage
        results = await executor.comprehensive_stock_search("RELIANCE")
        
        # Sync wrapper
        results = executor.search_parallel_sync(queries)
    """
    
    def __init__(self, api_key: str = None, max_concurrent: int = 4):
        """
        Initialize the async executor
        
        Args:
            api_key: Tavily API key (defaults to env var)
            max_concurrent: Maximum concurrent searches
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment")
        
        self.max_concurrent = max_concurrent
        self.template_manager = get_template_manager()
        self._semaphore = None  # Created in async context
    
    async def _execute_single_search(
        self, client: "AsyncTavilyClient", query_result: QueryResult
    ) -> AsyncSearchResult:
        """
        Execute a single search with semaphore control
        
        Args:
            client: Async Tavily client
            query_result: Query configuration
            
        Returns:
            AsyncSearchResult
        """
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
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
    
    async def search_parallel(
        self, query_results: List[QueryResult]
    ) -> List[AsyncSearchResult]:
        """
        Execute multiple searches in parallel
        
        Args:
            query_results: List of query configurations
            
        Returns:
            List of AsyncSearchResult objects
        """
        if not ASYNC_AVAILABLE:
            raise RuntimeError("AsyncTavilyClient not available")
        
        async with AsyncTavilyClient(api_key=self.api_key) as client:
            tasks = [
                self._execute_single_search(client, qr)
                for qr in query_results
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
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
    
    def search_parallel_sync(
        self, query_results: List[QueryResult]
    ) -> List[AsyncSearchResult]:
        """
        Synchronous wrapper for parallel search
        
        Args:
            query_results: List of query configurations
            
        Returns:
            List of AsyncSearchResult objects
        """
        return asyncio.run(self.search_parallel(query_results))
    
    async def comprehensive_stock_search(
        self, stock_name: str
    ) -> Dict[str, AsyncSearchResult]:
        """
        Perform comprehensive stock analysis with parallel searches
        
        Args:
            stock_name: Stock name or symbol
            
        Returns:
            Dictionary mapping template names to results
        """
        queries = self.template_manager.get_composite_queries(
            f"Analyze {stock_name} stock",
            entity=stock_name,
            template_name="stock_comprehensive"
        )
        
        results = await self.search_parallel(queries)
        return {result.template: result for result in results}
    
    async def comprehensive_ipo_search(
        self, company_name: str = None
    ) -> Dict[str, AsyncSearchResult]:
        """
        Perform comprehensive IPO analysis with parallel searches
        
        Args:
            company_name: Company name (optional)
            
        Returns:
            Dictionary mapping template names to results
        """
        queries = self.template_manager.get_ipo_queries(company_name)
        results = await self.search_parallel(queries)
        return {result.template: result for result in results}
    
    def comprehensive_stock_search_sync(
        self, stock_name: str
    ) -> Dict[str, AsyncSearchResult]:
        """Sync wrapper for comprehensive stock search"""
        return asyncio.run(self.comprehensive_stock_search(stock_name))
    
    def comprehensive_ipo_search_sync(
        self, company_name: str = None
    ) -> Dict[str, AsyncSearchResult]:
        """Sync wrapper for comprehensive IPO search"""
        return asyncio.run(self.comprehensive_ipo_search(company_name))


# Convenience functions
def parallel_stock_search(stock_name: str) -> Dict[str, AsyncSearchResult]:
    """
    Quick comprehensive stock search (sync wrapper)
    
    Args:
        stock_name: Stock name or symbol
        
    Returns:
        Dictionary mapping template names to results
    """
    executor = AsyncSearchExecutor()
    return executor.comprehensive_stock_search_sync(stock_name)


def parallel_ipo_search(company_name: str = None) -> Dict[str, AsyncSearchResult]:
    """
    Quick comprehensive IPO search (sync wrapper)
    
    Args:
        company_name: Company name (optional)
        
    Returns:
        Dictionary mapping template names to results
    """
    executor = AsyncSearchExecutor()
    return executor.comprehensive_ipo_search_sync(company_name)


if __name__ == "__main__":
    # Quick test
    print("🧪 Testing AsyncSearchExecutor\n")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if not ASYNC_AVAILABLE:
        print("❌ AsyncTavilyClient not available")
        exit(1)
    
    try:
        executor = AsyncSearchExecutor()
        
        # Get queries
        queries = executor.template_manager.get_stock_queries("RELIANCE")
        print(f"Generated {len(queries)} queries:")
        for q in queries:
            print(f"  - {q.template_used}: {q.query}")
        print()
        
        # Execute parallel search
        print("Executing parallel searches...")
        start = time.time()
        results = executor.search_parallel_sync(queries)
        elapsed = (time.time() - start) * 1000
        
        print(f"Total time: {elapsed:.0f}ms\n")
        
        for result in results:
            print(f"  {result.template}:")
            print(f"    Status: {result.status}")
            print(f"    Time: {result.response_time_ms:.0f}ms")
            if result.error:
                print(f"    Error: {result.error}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure TAVILY_API_KEY is set")
