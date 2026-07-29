import os
from typing import List, Dict, Any
from langchain.tools import tool
from langchain_tavily import TavilySearch
from utils.ipo_info_search import TavilyIPOInfoSearch
from utils.stock_info_search import TavilyStockInfoSearch
from dotenv import load_dotenv
import json

load_dotenv()

class WebSearchTool:
    def __init__(self):
        """Initialize the Web Search Tool with Tavily API"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        # Initialize Tavily search tools
        self.tavily_ipo_search = TavilyIPOInfoSearch(self.api_key)
        self.tavily_search = TavilySearch(api_key=self.api_key)

    @tool
    def search_web(query: str) -> str:
        """
        Search the web for general information.
        
        Args:
            query (str): The search query
            
        Returns:
            str: Search results
        """
        try:
            from tools.web_search_tool import get_web_search_tool
            web_tool = get_web_search_tool()
            results = web_tool.tavily_search.invoke(query)
            
            if not results:
                return "No results found."
            
            formatted = f"Search Results for: '{query}'\n\n"
            if isinstance(results, list):
                for i, r in enumerate(results[:5], 1):
                    if isinstance(r, dict):
                        formatted += f"{i}. {r.get('title', 'No title')}\n"
                        formatted += f"   {r.get('url', '')}\n"
                        formatted += f"   {r.get('content', '')[:200]}...\n\n"
            else:
                formatted += str(results)
            return formatted
        except Exception as e:
            return f"Error: {str(e)}"
        
    @tool
    def search_ipo_info(query: str) -> str:
        """
        Search for IPO information.
        
        Args:
            query (str): The IPO-related search query
            
        Returns:
            str: IPO search results
        """
        try:
            from tools.web_search_tool import get_web_search_tool
            web_tool = get_web_search_tool()
            results = web_tool.tavily_ipo_search.search(query)
            
            if not results:
                return f"No IPO info found for: '{query}'"
            
            formatted = f"IPO Results for: '{query}'\n\n"
            if isinstance(results, list):
                for i, r in enumerate(results[:5], 1):
                    if isinstance(r, dict):
                        formatted += f"{i}. {r.get('title', 'No title')}\n"
                        formatted += f"   {r.get('url', '')}\n"
                        formatted += f"   {r.get('content', '')[:200]}...\n\n"
            elif isinstance(results, dict) and 'results' in results:
                for i, r in enumerate(results['results'][:5], 1):
                    formatted += f"{i}. {r.get('title', 'No title')}\n"
                    formatted += f"   {r.get('content', '')[:200]}...\n\n"
            else:
                formatted += str(results)
            return formatted
        except Exception as e:
            return f"Error: {str(e)}"
    
    @tool
    def tavily_smart_search(query: str, search_context: str = "general") -> str:
        """
        Search with context hint.
        
        Args:
            query (str): The search query
            search_context (str): Context hint (ignored - kept for compatibility)
            
        Returns:
            str: Search results
        """
        try:
            from tools.web_search_tool import get_web_search_tool
            web_tool = get_web_search_tool()
            results = web_tool.tavily_search.invoke(query)
            
            if not results:
                return f"No results for: '{query}'"
            
            formatted = f"Results for: '{query}'\n\n"
            if isinstance(results, list):
                for i, r in enumerate(results[:5], 1):
                    if isinstance(r, dict):
                        formatted += f"{i}. {r.get('title', 'No title')}\n"
                        formatted += f"   {r.get('content', '')[:200]}...\n\n"
            else:
                formatted += str(results)
            return formatted
        except Exception as e:
            return f"Error: {str(e)}"
    
    @tool
    def tavily_financial_search(query: str) -> str:
        """
        Search for financial market information.
        
        Args:
            query (str): Financial query
            
        Returns:
            str: Financial search results
        """
        try:
            from tools.web_search_tool import get_web_search_tool
            web_tool = get_web_search_tool()
            results = web_tool.tavily_search.invoke(query)
            
            if not results:
                return f"No financial info for: '{query}'"
            
            formatted = f"Financial Results for: '{query}'\n\n"
            if isinstance(results, list):
                for i, r in enumerate(results[:5], 1):
                    if isinstance(r, dict):
                        formatted += f"{i}. {r.get('title', 'No title')}\n"
                        formatted += f"   {r.get('content', '')[:200]}...\n\n"
            else:
                formatted += str(results)
            return formatted
        except Exception as e:
            return f"Error: {str(e)}"

    def get_ipo_search_tools(self):
        """Return all search tools for LangChain integration"""
        return [
            self.search_web, 
            self.search_ipo_info, 
            self.tavily_smart_search, 
            self.tavily_financial_search,
        ]
    
    def get_search_tool(self):
        """Return the general search tool for backward compatibility"""
        return self.search_web
    
    def get_advanced_tools(self):
        """Return advanced AI-powered search tools"""
        return [self.tavily_smart_search, self.tavily_financial_search]
    
    def get_stock_tools(self):
        """Return stock-specific search tools"""
        return [
            self.tavily_smart_search,
            self.tavily_financial_search,
            search_stock_performance,  # Use the function directly
            search_stock_news,
            search_stock_analysis,
            search_stock_recommendations
        ]
    
    def get_tools(self):
        """Return all available tools"""
        return [
            self.search_web,
            self.search_ipo_info,
            self.tavily_smart_search,
            self.tavily_financial_search,
            search_stock_performance,  # Use the function directly
            search_stock_news,
            search_stock_analysis,
            search_stock_recommendations
        ]
    
    # Late binding of stock search functions
    def __post_init__(self):
        """Bind stock search functions after they are defined"""
        self.search_stock_performance = search_stock_performance
        self.search_stock_news = search_stock_news
        self.search_stock_analysis = search_stock_analysis  
        self.search_stock_recommendations = search_stock_recommendations

# Stock Performance Search Tool
@tool
def search_stock_performance(query: str) -> str:
    """
    Search for detailed stock performance information including price history, charts, and market data.
    
    Args:
        query (str): Stock performance query (e.g., "RELIANCE stock performance", "TCS share price analysis")
        
    Returns:
        str: Formatted stock performance information with price data and trends
    """
    try:
        # Initialize the stock search utility
        search_tool = TavilyStockInfoSearch()
        results = search_tool.search_stock_performance(query)
        
        if results["status"] == "failed":
            return f"❌ Stock performance search failed: {results.get('error', 'Unknown error')}"
        
        # Format the results for better readability
        formatted_results = f"📈 STOCK PERFORMANCE ANALYSIS\n"
        formatted_results += f"Query: '{query}'\n"
        formatted_results += f"Optimized Search: '{results['optimized_query']}'\n"
        formatted_results += "="*60 + "\n\n"
        
        if isinstance(results['results'], dict) and 'results' in results['results']:
            for i, result in enumerate(results['results']['results'][:6], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content available')
                
                formatted_results += f"📊 Performance Data #{i}\n"
                formatted_results += f"Title: {title}\n"
                formatted_results += f"Source: {url}\n"
                formatted_results += f"Analysis: {content[:300]}...\n"
                formatted_results += "─"*50 + "\n\n"
        elif isinstance(results['results'], list):
            for i, result in enumerate(results['results'][:6], 1):
                formatted_results += f"📊 Performance #{i}: {str(result)}\n\n"
        else:
            formatted_results += f"Performance Data: {str(results['results'])}\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error searching stock performance: {str(e)}"

# Stock News Search Tool
@tool  
def search_stock_news(query: str) -> str:
    """
    Search for latest stock news, announcements, and market updates.
    
    Args:
        query (str): Stock news query (e.g., "TATA Motors latest news", "banking sector updates")
        
    Returns:
        str: Formatted stock news with latest updates and market sentiment
    """
    try:
        # Initialize the stock search utility
        search_tool = TavilyStockInfoSearch()
        results = search_tool.search_stock_news(query)
        
        if results["status"] == "failed":
            return f"❌ Stock news search failed: {results.get('error', 'Unknown error')}"
        
        # Format the results for better readability
        formatted_results = f"📰 STOCK NEWS & UPDATES\n"
        formatted_results += f"Query: '{query}'\n"
        formatted_results += f"News Search: '{results['optimized_query']}'\n"
        formatted_results += "="*60 + "\n\n"
        
        if isinstance(results['results'], dict) and 'results' in results['results']:
            for i, result in enumerate(results['results']['results'][:8], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content available')
                
                formatted_results += f"🗞️ News #{i}\n"
                formatted_results += f"Headline: {title}\n"
                formatted_results += f"Source: {url}\n"
                formatted_results += f"Summary: {content[:250]}...\n"
                formatted_results += "─"*50 + "\n\n"
        elif isinstance(results['results'], list):
            for i, result in enumerate(results['results'][:8], 1):
                formatted_results += f"🗞️ News #{i}: {str(result)}\n\n"
        else:
            formatted_results += f"News Data: {str(results['results'])}\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error searching stock news: {str(e)}"

# Stock Analysis Search Tool
@tool
def search_stock_analysis(query: str) -> str:
    """
    Search for detailed stock analysis, technical charts, and expert opinions.
    
    Args:
        query (str): Stock analysis query (e.g., "HDFC Bank technical analysis", "IT sector fundamental analysis")
        
    Returns:
        str: Formatted stock analysis with expert insights and technical data
    """
    try:
        # Initialize the stock search utility
        search_tool = TavilyStockInfoSearch()
        results = search_tool.search_stock_analysis(query)
        
        if results["status"] == "failed":
            return f"❌ Stock analysis search failed: {results.get('error', 'Unknown error')}"
        
        # Format the results for better readability
        formatted_results = f"📊 STOCK ANALYSIS & INSIGHTS\n"
        formatted_results += f"Query: '{query}'\n"
        formatted_results += f"Analysis Search: '{results['optimized_query']}'\n"
        formatted_results += "="*60 + "\n\n"
        
        if isinstance(results['results'], dict) and 'results' in results['results']:
            for i, result in enumerate(results['results']['results'][:5], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content available')
                
                formatted_results += f"🔍 Analysis #{i}\n"
                formatted_results += f"Title: {title}\n"
                formatted_results += f"Source: {url}\n"
                formatted_results += f"Expert View: {content[:350]}...\n"
                formatted_results += "─"*50 + "\n\n"
        elif isinstance(results['results'], list):
            for i, result in enumerate(results['results'][:5], 1):
                formatted_results += f"🔍 Analysis #{i}: {str(result)}\n\n"
        else:
            formatted_results += f"Analysis Data: {str(results['results'])}\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error searching stock analysis: {str(e)}"

# Stock Recommendations Search Tool
@tool
def search_stock_recommendations(query: str) -> str:
    """
    Search for stock recommendations, analyst ratings, and buy/sell suggestions.
    
    Args:
        query (str): Stock recommendation query (e.g., "Infosys buy recommendation", "pharma stocks to buy")
        
    Returns:
        str: Formatted stock recommendations with analyst ratings and target prices
    """
    try:
        # Initialize the stock search utility
        search_tool = TavilyStockInfoSearch()
        results = search_tool.search_stock_recommendations(query)
        
        if results["status"] == "failed":
            return f"❌ Stock recommendations search failed: {results.get('error', 'Unknown error')}"
        
        # Format the results for better readability
        formatted_results = f"💡 STOCK RECOMMENDATIONS & RATINGS\n"
        formatted_results += f"Query: '{query}'\n"
        formatted_results += f"Recommendations Search: '{results['optimized_query']}'\n"
        formatted_results += "="*60 + "\n\n"
        
        if isinstance(results['results'], dict) and 'results' in results['results']:
            for i, result in enumerate(results['results']['results'][:6], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content available')
                
                formatted_results += f"🎯 Recommendation #{i}\n"
                formatted_results += f"Title: {title}\n"
                formatted_results += f"Source: {url}\n"
                formatted_results += f"Expert Advice: {content[:300]}...\n"
                formatted_results += "─"*50 + "\n\n"
        elif isinstance(results['results'], list):
            for i, result in enumerate(results['results'][:6], 1):
                formatted_results += f"🎯 Recommendation #{i}: {str(result)}\n\n"
        else:
            formatted_results += f"Recommendations Data: {str(results['results'])}\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error searching stock recommendations: {str(e)}"

# General Web Search Tool
@tool  
def search_general_web(query: str) -> str:
    """
    Perform general web search using Tavily for any topic.
    
    Args:
        query (str): Search query for general web search
        
    Returns:
        str: Formatted search results from the web
    """
    try:
        from langchain_tavily import TavilySearch
        import os
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "❌ TAVILY_API_KEY not found in environment variables"
            
        tavily_search = TavilySearch(api_key=api_key)
        results = tavily_search.invoke(query)
        
        formatted_results = f"🌐 GENERAL WEB SEARCH RESULTS\n"
        formatted_results += f"Query: '{query}'\n"
        formatted_results += "="*60 + "\n\n"
        
        if isinstance(results, list):
            for i, result in enumerate(results[:5], 1):
                if isinstance(result, dict):
                    title = result.get('title', 'No title')
                    url = result.get('url', 'No URL')
                    content = result.get('content', 'No content available')
                    
                    formatted_results += f"🔍 Result #{i}\n"
                    formatted_results += f"Title: {title}\n"
                    formatted_results += f"URL: {url}\n"
                    formatted_results += f"Content: {content[:400]}...\n"
                    formatted_results += "─"*50 + "\n\n"
                else:
                    formatted_results += f"🔍 Result #{i}: {str(result)}\n\n"
        else:
            formatted_results += f"Search Data: {str(results)}\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error in general web search: {str(e)}"

# IPO-specific search tools
@tool
def search_ipo_news(query: str) -> str:
    """
    Search for IPO news and announcements.
    
    Args:
        query (str): IPO news query
        
    Returns:
        str: Formatted IPO news results
    """
    try:
        from utils.ipo_info_search import TavilyIPOInfoSearch
        import os
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "❌ TAVILY_API_KEY not found in environment variables"
            
        ipo_search = TavilyIPOInfoSearch(api_key)
        results = ipo_search.search_ipo_news(query)
        
        return f"📰 IPO NEWS RESULTS\nQuery: '{query}'\n{'='*60}\n{results}"
        
    except Exception as e:
        return f"Error searching IPO news: {str(e)}"

@tool
def search_ipo_analysis(query: str) -> str:
    """
    Search for IPO analysis and expert opinions.
    
    Args:
        query (str): IPO analysis query
        
    Returns:
        str: Formatted IPO analysis results
    """
    try:
        from utils.ipo_info_search import TavilyIPOInfoSearch
        import os
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "❌ TAVILY_API_KEY not found in environment variables"
            
        ipo_search = TavilyIPOInfoSearch(api_key)
        results = ipo_search.search_ipo_analysis(query)
        
        return f"📊 IPO ANALYSIS RESULTS\nQuery: '{query}'\n{'='*60}\n{results}"
        
    except Exception as e:
        return f"Error searching IPO analysis: {str(e)}"

@tool
def search_ipo_recommendations(query: str) -> str:
    """
    Search for IPO recommendations and ratings.
    
    Args:
        query (str): IPO recommendations query
        
    Returns:
        str: Formatted IPO recommendations results
    """
    try:
        from utils.ipo_info_search import TavilyIPOInfoSearch
        import os
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "❌ TAVILY_API_KEY not found in environment variables"
            
        ipo_search = TavilyIPOInfoSearch(api_key)
        results = ipo_search.search_ipo_recommendations(query)
        
        return f"💡 IPO RECOMMENDATIONS RESULTS\nQuery: '{query}'\n{'='*60}\n{results}"
        
    except Exception as e:
        return f"Error searching IPO recommendations: {str(e)}"

@tool
def search_ipo_performance(query: str) -> str:
    """
    Search for IPO performance and market data.
    
    Args:
        query (str): IPO performance query
        
    Returns:
        str: Formatted IPO performance results
    """
    try:
        from utils.ipo_info_search import TavilyIPOInfoSearch
        import os
        
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "❌ TAVILY_API_KEY not found in environment variables"
            
        ipo_search = TavilyIPOInfoSearch(api_key)
        results = ipo_search.search_ipo_performance(query)
        
        return f"📈 IPO PERFORMANCE RESULTS\nQuery: '{query}'\n{'='*60}\n{results}"
        
    except Exception as e:
        return f"Error searching IPO performance: {str(e)}"


# ============================================================================
# SINGLETON PATTERN FOR PERFORMANCE OPTIMIZATION
# ============================================================================
# Avoid recreating WebSearchTool on every tool call (saves ~300ms per call)

_web_search_tool_instance: WebSearchTool = None

def get_web_search_tool() -> WebSearchTool:
    """
    Get or create singleton WebSearchTool instance.
    This avoids expensive re-initialization on every tool call.
    
    Returns:
        WebSearchTool: Cached singleton instance
    """
    global _web_search_tool_instance
    if _web_search_tool_instance is None:
        _web_search_tool_instance = WebSearchTool(use_optimized=True)
    return _web_search_tool_instance

def reset_web_search_tool():
    """Reset the singleton instance (useful for testing)"""
    global _web_search_tool_instance
    _web_search_tool_instance = None