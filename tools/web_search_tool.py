import os
from typing import List, Dict, Any
from langchain.tools import tool
from langchain_tavily import TavilySearch
from utils.ipo_info_search import TavilyIPOInfoSearch
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

    @tool
    def search_web(query: str) -> str:
        """
        Search the web for general information based on the given query.
        
        Args:
            query (str): The search query to find information on the web
            
        Returns:
            str: Formatted search results with sources
        """
        try:
            # Initialize the tool if not already done
            search_tool = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
            
            # Perform the search
            results = search_tool.invoke(query)
            
            if not results:
                return "No search results found for the given query."
            
            # Format the results
            formatted_results = f"Search Results for: '{query}'\n\n"
            
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
        Search for IPO information based on the query using specialized IPO sources.
        
        Args:
            query (str): The IPO-related search query
            
        Returns:
            str: Formatted IPO search results
        """
        try:
            # Initialize IPO search tool
            ipo_search = TavilyIPOInfoSearch(os.getenv("TAVILY_API_KEY"))
            
            # Perform the IPO search
            results = ipo_search.tavily_search_(query)
            
            if not results:
                return f"No IPO information found for: '{query}'"
            
            # Format the results
            formatted_results = f"IPO Information for: '{query}'\n\n"
            
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
    
    def get_tools(self):
        """Return both search tools for LangChain integration"""
        return [self.search_web, self.search_ipo_info]
    
    def get_tool(self):
        """Return the general search tool for backward compatibility"""
        return self.search_web

