"""
Specialized Stock Web Search Tools
Uses the TavilyStockInfoSearch utility to provide LangChain tools for stock analysis
"""
import os
from typing import Any
from langchain.tools import tool
from utils.stock_info_search import TavilyStockInfoSearch
from dotenv import load_dotenv
import json

load_dotenv()

class StockWebSearchTool:
    """
    Stock-specific web search tools wrapper for LangChain integration
    Provides 4 specialized tools + 1 comprehensive tool for stock analysis
    """
    
    def __init__(self):
        """Initialize the Stock Web Search Tool with Tavily API"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        # Initialize the stock search utility
        self.stock_search_utility = TavilyStockInfoSearch(self.api_key)
    
    def _format_search_results(self, results: dict, search_type: str) -> str:
        """
        Format search results for better readability in agent responses
        
        Args:
            results (dict): Raw search results from utility
            search_type (str): Type of search performed
            
        Returns:
            str: Formatted results string
        """
        if results["status"] == "failed":
            return f"❌ {search_type.title()} search failed: {results.get('error', 'Unknown error')}"
        
        # Format successful results
        formatted_results = f"📊 **{search_type.upper()} SEARCH RESULTS**\n"
        formatted_results += f"🔍 Query: '{results['original_query']}'\n"
        formatted_results += f"🎯 Optimized: '{results['optimized_query']}'\n"
        formatted_results += "="*60 + "\n\n"
        
        # Process results based on type
        search_results = results.get('results', {})
        
        if isinstance(search_results, dict):
            # Handle Tavily response format
            if 'answer' in search_results:
                formatted_results += f"📋 **Summary**: {search_results['answer']}\n\n"
            
            if 'results' in search_results:
                sources = search_results['results'][:5]  # Limit to top 5 sources
                for i, source in enumerate(sources, 1):
                    title = source.get('title', 'No title')
                    url = source.get('url', 'No URL')
                    content = source.get('content', 'No content available')
                    
                    formatted_results += f"🔗 **Source {i}**: {title}\n"
                    formatted_results += f"🌐 URL: {url}\n"
                    formatted_results += f"📄 Content: {content[:300]}...\n"
                    formatted_results += "-" * 40 + "\n\n"
        else:
            formatted_results += f"📄 Raw Results: {str(search_results)[:500]}...\n"
        
        # Add metadata if available
        if 'metadata' in results:
            metadata = results['metadata']
            formatted_results += f"📊 **Data Categories**: {', '.join(metadata.get('categories', []))}\n"
            formatted_results += f"📈 **Key Metrics**: {', '.join(metadata.get('data_points', []))}\n"
        
        return formatted_results

    @tool
    def search_stock_overview(query: str) -> str:
        """
        Search for comprehensive stock overview information including company details, market cap, current price, and basic metrics.
        
        Perfect for: Company overview, sector information, market capitalization, current stock price, 52-week range, trading volume, beta, dividend yield.
        
        Args:
            query (str): Stock overview query (e.g., "RELIANCE stock overview", "TCS company information")
            
        Returns:
            str: Formatted stock overview information with company fundamentals
        """
        try:
            tool_instance = StockWebSearchTool()
            results = tool_instance.stock_search_utility.search_stock_overview(query)
            return tool_instance._format_search_results(results, "Stock Overview")
        except Exception as e:
            return f"❌ Stock Overview search error: {str(e)}"

    @tool  
    def search_fundamental_analysis(query: str) -> str:
        """
        Search for fundamental analysis data including financial ratios, revenue growth, profitability metrics, and valuation.
        
        Perfect for: Revenue growth, profit margins, ROE, ROA, debt-to-equity ratios, P/E ratio, P/B ratio, financial health analysis.
        
        Args:
            query (str): Fundamental analysis query (e.g., "HDFC Bank financial ratios", "TCS revenue growth analysis")
            
        Returns:
            str: Formatted fundamental analysis with financial metrics and ratios
        """
        try:
            tool_instance = StockWebSearchTool()
            results = tool_instance.stock_search_utility.search_fundamental_analysis(query)
            return tool_instance._format_search_results(results, "Fundamental Analysis")
        except Exception as e:
            return f"❌ Fundamental Analysis search error: {str(e)}"

    @tool
    def search_technical_analysis(query: str) -> str:
        """
        Search for technical analysis information including price trends, technical indicators, and chart patterns.
        
        Perfect for: Price trends, support/resistance levels, moving averages, RSI, MACD, volume analysis, price targets, chart patterns.
        
        Args:
            query (str): Technical analysis query (e.g., "RELIANCE technical analysis", "HDFC Bank price targets")
            
        Returns:
            str: Formatted technical analysis with indicators and price targets
        """
        try:
            tool_instance = StockWebSearchTool()
            results = tool_instance.stock_search_utility.search_technical_analysis(query)
            return tool_instance._format_search_results(results, "Technical Analysis")
        except Exception as e:
            return f"❌ Technical Analysis search error: {str(e)}"

    @tool
    def search_stock_news_events(query: str) -> str:
        """
        Search for latest stock news, corporate events, earnings results, and market developments.
        
        Perfect for: Latest news, corporate actions, quarterly results, management commentary, sector developments, regulatory changes, dividends.
        
        Args:
            query (str): Stock news query (e.g., "TCS latest news", "RELIANCE quarterly results", "banking sector updates")
            
        Returns:
            str: Formatted stock news and corporate events information
        """
        try:
            tool_instance = StockWebSearchTool()
            results = tool_instance.stock_search_utility.search_stock_news_events(query)
            return tool_instance._format_search_results(results, "Stock News & Events")
        except Exception as e:
            return f"❌ Stock News & Events search error: {str(e)}"

    @tool
    def search_comprehensive_stock_analysis(query: str) -> str:
        """
        Perform comprehensive stock analysis using all specialized search methods (overview, fundamental, technical, news).
        
        Perfect for: Complete stock analysis, investment decision making, comprehensive research covering all aspects of a stock.
        
        Args:
            query (str): Comprehensive stock query (e.g., "Complete analysis of RELIANCE", "Full research on TCS stock")
            
        Returns:
            str: Complete stock analysis with all four aspects covered
        """
        try:
            tool_instance = StockWebSearchTool()
            results = tool_instance.stock_search_utility.search_comprehensive_stock_data(query)
            
            if results["status"] == "failed":
                return f"❌ Comprehensive stock analysis failed: {results.get('error', 'Unknown error')}"
            
            # Format comprehensive results
            formatted_results = f"🎯 **COMPREHENSIVE STOCK ANALYSIS**\n"
            formatted_results += f"🔍 Query: '{results['original_query']}'\n"
            formatted_results += "="*80 + "\n\n"
            
            # Process each section
            sections = results.get('results', {})
            section_icons = {
                'overview': '📈',
                'fundamental': '📊', 
                'technical': '📉',
                'news_events': '📰'
            }
            
            for section_name, section_data in sections.items():
                icon = section_icons.get(section_name, '📋')
                formatted_results += f"{icon} **{section_name.upper().replace('_', ' ')}**\n"
                formatted_results += "-" * 40 + "\n"
                
                if section_data.get('status') == 'success':
                    formatted_results += f"✅ Status: Success\n"
                    formatted_results += f"🎯 Query: {section_data.get('optimized_query', 'N/A')}\n"
                    
                    # Add summary of results
                    section_results = section_data.get('results', {})
                    if isinstance(section_results, dict) and 'answer' in section_results:
                        formatted_results += f"📋 Summary: {section_results['answer'][:200]}...\n"
                else:
                    formatted_results += f"❌ Status: {section_data.get('status', 'Failed')}\n"
                    formatted_results += f"⚠️  Error: {section_data.get('error', 'Unknown error')}\n"
                
                formatted_results += "\n"
            
            # Add metadata
            metadata = results.get('metadata', {})
            formatted_results += f"📊 **Analysis Coverage**: {metadata.get('search_methods_used', 0)} methods used\n"
            formatted_results += f"📋 **Categories Covered**: {', '.join(metadata.get('data_categories', []))}\n"
            
            return formatted_results
            
        except Exception as e:
            return f"❌ Comprehensive Stock Analysis error: {str(e)}"

    def get_all_stock_tools(self):
        """Return all stock-specific search tools for LangChain integration"""
        return [
            self.search_stock_overview,
            self.search_fundamental_analysis,
            self.search_technical_analysis,
            self.search_stock_news_events,
            self.search_comprehensive_stock_analysis
        ]
    
    def get_essential_stock_tools(self):
        """Return essential stock tools (overview + news) for lightweight integration"""
        return [
            self.search_stock_overview,
            self.search_stock_news_events
        ]
    
    def get_analysis_tools(self):
        """Return analysis-focused tools (fundamental + technical)"""
        return [
            self.search_fundamental_analysis, 
            self.search_technical_analysis
        ]
    
    def get_tools(self):
        """Return all available stock search tools for compatibility"""
        return self.get_all_stock_tools()

# Standalone tool functions for LangChain integration
@tool
def search_stock_performance(query: str) -> str:
    """
    Search for stock performance information.
    
    Args:
        query (str): Stock performance query
        
    Returns:
        str: Stock performance results
    """
    tool = StockWebSearchTool()
    return tool.search_stock_overview(query)

@tool  
def search_stock_news(query: str) -> str:
    """
    Search for stock news and events.
    
    Args:
        query (str): Stock news query
        
    Returns:
        str: Stock news results
    """
    tool = StockWebSearchTool()
    return tool.search_stock_news_events(query)

@tool
def search_stock_analysis(query: str) -> str:
    """
    Search for stock analysis information.
    
    Args:
        query (str): Stock analysis query
        
    Returns:
        str: Stock analysis results
    """
    tool = StockWebSearchTool()
    return tool.search_fundamental_analysis(query)

@tool
def search_stock_recommendations(query: str) -> str:
    """
    Search for stock recommendations.
    
    Args:
        query (str): Stock recommendations query
        
    Returns:
        str: Stock recommendations results
    """
    tool = StockWebSearchTool()
    return tool.search_comprehensive_stock_analysis(query)
