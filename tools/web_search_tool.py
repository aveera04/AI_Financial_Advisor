import os
from typing import List, Dict, Any
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import json

load_dotenv()

class WebSearchTool:
    def __init__(self):
        """Initialize the Web Search Tool with Tavily API"""
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables")
        
        # Initialize Tavily search tool
        self.search_tool = TavilySearchResults(
            api_key=self.api_key,
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=False,
            include_images=False
        )
    
    @tool
    def search_web(query: str) -> str:
        """
        Search the web for information based on the given query.
        
        Args:
            query (str): The search query to find information on the web
            
        Returns:
            str: Formatted search results with sources
        """
        try:
            # Initialize the tool if not already done
            search_tool = TavilySearchResults(
                api_key=os.getenv("TAVILY_API_KEY"),
                search_depth="advanced",
                include_answer=True
            )
            
            # Perform the search
            results = search_tool.invoke({"query": query})
            
            if not results:
                return "No search results found for the given query."
            
            # Format the results
            formatted_results = f"Search Results for: '{query}'\n\n"
            
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                content = result.get('content', 'No content available')
                
                formatted_results += f"{i}. **{title}**\n"
                formatted_results += f"   URL: {url}\n"
                formatted_results += f"   Content: {content}\n\n"
            
            return formatted_results
            
        except Exception as e:
            return f"Error performing web search: {str(e)}"
    
    def get_tool(self):
        """Return the search tool for LangChain integration"""
        return self.search_web
    
    def search(self, query: str) -> Dict[str, Any]:
        """
        Direct search method that returns structured results
        
        Args:
            query (str): The search query
            
        Returns:
            Dict[str, Any]: Structured search results
        """
        try:
            results = self.search_tool.invoke({"query": query})
            return {
                "query": query,
                "results": results,
                "success": True
            }
        except Exception as e:
            return {
                "query": query,
                "error": str(e),
                "success": False
            }