import os
from typing import List, Dict, Any
from langchain.tools import tool
from langchain_tavily import TavilySearch
from utils.ipo_info_search import TavilyIPOInfoSearch
from utils.stock_info_search import TavilyStockInfoSearch
from utils.model_loader import ModelLoader
from dotenv import load_dotenv
import json

load_dotenv()

class WebSearchTool:
    def __init__(self):
        """Initialize the Web Search Tool with Tavily API"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        # Initialize Tavily IPO search tool
        self.tavily_ipo_search = TavilyIPOInfoSearch(self.api_key)
        
        # Initialize general Tavily search tool
        self.tavily_search = TavilySearch(api_key=self.api_key)
        
        # Initialize LLM for query generation (using lighter model for cost efficiency)
        try:
            self.query_generator = ModelLoader.from_env_key("groq_oss_20b", "GROQ_API_KEY_2").load_llm()
        except Exception as e:
            print(f"Warning: Could not initialize query generator: {e}")
            self.query_generator = None  # Fallback if model loading fails
        
        # Note: Stock search functions will be bound after they are defined
        # See __post_init__ method

    def _generate_search_query(self, user_query: str, search_type: str = "general") -> str:
        """
        Use LLM to generate optimized search queries based on user input
        
        Args:
            user_query (str): The original user query
            search_type (str): Type of search - 'general', 'ipo', 'market'
            
        Returns:
            str: Optimized search query
        """
        if not self.query_generator:
            return user_query  # Fallback to original query
        
        try:
            if search_type == "ipo":
                prompt = f"""
                Transform the following user query into an optimized search query for IPO information.
                Focus on IPO-specific terms, dates, prices, grey market premium (GMP), listing details.
                
                User Query: {user_query}
                
                Generate a concise, search-optimized query (max 20 words) that includes relevant IPO keywords:
                """
            elif search_type == "market":
                prompt = f"""
                Transform the following user query into an optimized search query for stock market information.
                Focus on market trends, stock prices, financial data, company analysis.
                
                User Query: {user_query}
                
                Generate a concise, search-optimized query (max 20 words) that includes relevant market keywords:
                """

        
            else:  # general
                prompt = f"""
                Transform the following user query into an optimized search query for web search.
                Make it more specific and search-friendly while preserving the user's intent.
                
                User Query: {user_query}
                
                Generate a concise, search-optimized query (max 20 words):
                """
            
            response = self.query_generator.invoke(prompt)
            optimized_query = response.content.strip() if hasattr(response, 'content') else str(response).strip()
            
            # Clean up the response (remove quotes, extra text)
            optimized_query = optimized_query.replace('"', '').replace("'", "")
            if len(optimized_query) > 100:  # Fallback if response is too long
                return user_query
            
            return optimized_query
            
        except Exception as e:
            print(f"Query generation error: {e}")
            return user_query  # Fallback to original query

    @tool
    def search_web(query: str) -> str:
        """
        Search the web for general information with AI-optimized query generation.
        
        Args:
            query (str): The search query to find information on the web
            
        Returns:
            str: Formatted search results with sources
        """
        try:
            # Create instance for accessing methods
            web_tool = WebSearchTool()
            
            # Generate optimized search query
            optimized_query = web_tool._generate_search_query(query, "general")
            print(f"🔍 Original: {query}")
            print(f"🎯 Optimized: {optimized_query}")
            
            # Initialize the tool if not already done
            search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
            
            # Perform the search with optimized query
            results = search_tool.invoke(optimized_query)
            
            if not results:
                return "No search results found for the given query."
            
            # Format the results
            formatted_results = f"Search Results for: '{query}'\n"
            formatted_results += f"(Optimized query: '{optimized_query}')\n\n"
            
            # Handle different result formats
            if isinstance(results, str):
                formatted_results += results
            elif isinstance(results, list):
                for i, result in enumerate(results, 1):
                    if isinstance(result, dict):
                        title = result.get('title', 'No title')
                        url = result.get('url', 'No URL')
                        content = result.get('content', 'No content available')
                        
                        formatted_results += f"{i}. **{title}**\n"
                        formatted_results += f"   URL: {url}\n"
                        formatted_results += f"   Content: {content}\n\n"
                    else:
                        formatted_results += f"{i}. {str(result)}\n\n"
            elif isinstance(results, dict):
                formatted_results += f"Results: {json.dumps(results, indent=2)}\n"
            else:
                formatted_results += f"Results: {str(results)}\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
        
    @tool
    def search_ipo_info(query: str) -> str:
        """
        Search for IPO information with AI-optimized query generation for specialized IPO sources.
        
        Args:
            query (str): The IPO-related search query
            
        Returns:
            str: Formatted IPO search results
        """
        try:
            # Create instance for accessing methods
            web_tool = WebSearchTool()
            
            # Generate optimized IPO search query
            optimized_query = web_tool._generate_search_query(query, "ipo")
            print(f"🔍 IPO Original: {query}")
            print(f"🎯 IPO Optimized: {optimized_query}")
            
            # Initialize IPO search tool
            ipo_search = TavilyIPOInfoSearch(os.getenv("TAVILY_API_KEY"))
            
            # Perform the IPO search with optimized query
            results = ipo_search.tavily_search_with_custom_query(optimized_query)
            
            if not results:
                return f"No IPO information found for: '{query}'"
            
            # Format the results
            formatted_results = f"IPO Information for: '{query}'\n"
            formatted_results += f"(Optimized query: '{optimized_query}')\n\n"
            
            if isinstance(results, dict):
                # Handle dictionary response
                if 'results' in results:
                    for i, result in enumerate(results['results'], 1):
                        title = result.get('title', 'No title')
                        url = result.get('url', 'No URL')
                        content = result.get('content', 'No content available')
                        
                        formatted_results += f"{i}. **{title}**\n"
                        formatted_results += f"   URL: {url}\n"
                        formatted_results += f"   Content: {content}\n\n"
                else:
                    formatted_results += f"Raw results: {json.dumps(results, indent=2)}\n"
            elif isinstance(results, list):
                # Handle list response
                for i, result in enumerate(results, 1):
                    if isinstance(result, dict):
                        title = result.get('title', 'No title')
                        url = result.get('url', 'No URL')
                        content = result.get('content', 'No content available')
                        
                        formatted_results += f"{i}. **{title}**\n"
                        formatted_results += f"   URL: {url}\n"
                        formatted_results += f"   Content: {content}\n\n"
                    else:
                        formatted_results += f"{i}. {str(result)}\n\n"
            else:
                formatted_results += f"Results: {str(results)}\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error performing IPO search: {str(e)}"
    
    @tool
    def tavily_smart_search(query: str, search_context: str = "general") -> str:
        """
        Advanced Tavily search with AI-powered query optimization and context awareness.
        
        Args:
            query (str): The user's search query
            search_context (str): Context for search optimization ('ipo', 'market', 'general', 'financial')
            
        Returns:
            str: Comprehensive search results with AI-enhanced queries
        """
        try:
            # Create instance for accessing methods
            web_tool = WebSearchTool()
            
            # Generate multiple optimized queries based on context
            optimized_query = web_tool._generate_search_query(query, search_context)
            
            print(f"🧠 Smart Search Context: {search_context}")
            print(f"🔍 Original Query: {query}")
            print(f"🎯 AI-Optimized Query: {optimized_query}")
            
            # Initialize Tavily search
            search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
            
            # Perform enhanced search
            results = search_tool.invoke(optimized_query)
            
            if not results:
                return f"No results found for: '{query}'"
            
            # Enhanced formatting with context awareness
            formatted_results = f"🧠 Smart Search Results\n"
            formatted_results += f"Context: {search_context.upper()}\n"
            formatted_results += f"Original Query: '{query}'\n"
            formatted_results += f"AI-Optimized Query: '{optimized_query}'\n"
            formatted_results += "="*60 + "\n\n"
            
            # Process results with enhanced formatting
            if isinstance(results, (list, dict)):
                result_list = results.get('results', results) if isinstance(results, dict) else results
                
                for i, result in enumerate(result_list[:5], 1):  # Limit to top 5 results
                    if isinstance(result, dict):
                        title = result.get('title', 'No title')
                        url = result.get('url', 'No URL')
                        content = result.get('content', 'No content available')
                        
                        formatted_results += f"🔍 Result #{i}: {title}\n"
                        formatted_results += f"🌐 Source: {url}\n"
                        formatted_results += f"📄 Summary: {content[:300]}...\n"
                        formatted_results += "-"*40 + "\n\n"
            else:
                formatted_results += f"Search Results: {str(results)}\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error in smart search: {str(e)}"
    
    @tool
    def tavily_financial_search(query: str) -> str:
        """
        Specialized financial search tool with AI query optimization for financial markets, IPOs, and investments.
        
        Args:
            query (str): Financial query about markets, stocks, IPOs, etc.
            
        Returns:
            str: Financial search results with market-specific optimization
        """
        try:
            # Create instance for accessing methods
            web_tool = WebSearchTool()
            
            # Generate financial-optimized query
            financial_query = web_tool._generate_search_query(query, "market")
            
            # Add financial context keywords
            enhanced_financial_query = f"{financial_query} financial market analysis stock price"
            
            print(f"💰 Financial Search Query: {query}")
            print(f"🎯 Market-Optimized: {enhanced_financial_query}")
            
            # Initialize search
            search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
            
            # Perform financial search
            results = search_tool.invoke(enhanced_financial_query)
            
            if not results:
                return f"No financial information found for: '{query}'"
            
            # Financial-specific formatting
            formatted_results = f"💰 FINANCIAL MARKET SEARCH\n"
            formatted_results += f"Query: '{query}'\n"
            formatted_results += f"Market-Optimized: '{enhanced_financial_query}'\n"
            formatted_results += "="*60 + "\n\n"
            
            # Process and format financial results
            if isinstance(results, dict) and 'results' in results:
                for i, result in enumerate(results['results'][:4], 1):
                    title = result.get('title', 'No title')
                    url = result.get('url', 'No URL')
                    content = result.get('content', 'No content available')
                    
                    formatted_results += f"📊 Financial Source #{i}\n"
                    formatted_results += f"Title: {title}\n"
                    formatted_results += f"URL: {url}\n"
                    formatted_results += f"Analysis: {content[:250]}...\n"
                    formatted_results += "─"*40 + "\n\n"
            elif isinstance(results, list):
                for i, result in enumerate(results[:4], 1):
                    formatted_results += f"📊 Result #{i}: {str(result)}\n\n"
            else:
                formatted_results += f"Financial Data: {str(results)}\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error in financial search: {str(e)}"

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