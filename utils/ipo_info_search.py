import os
import json
from langchain_tavily import TavilySearch

class TavilyIPOInfoSearch:
    def __init__(self, api_key: str = None):
        """
        Initialize the Tavily IPO search tool
        
        Args:
            api_key (str): Tavily API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables or passed as parameter")
        
        # Initialize the search tool with IPO-specific configuration
        self.search_tool = TavilySearch(api_key=self.api_key)

    def tavily_search_(self, query: str) -> dict:
        """
        Search for IPO information using Tavily API with domain filtering
        
        Args:
            query (str): The search query for IPO information
            
        Returns:
            dict: Search results from Tavily
        """
        try:
            # Add IPO-specific context to the query
            enhanced_query = f"IPO {query} grey market premium listing price"
            
            # Perform the search using TavilySearch tool
            results = self.search_tool.invoke(enhanced_query)
            
            return results
            
        except Exception as e:
            return {
                "error": f"Error performing IPO search: {str(e)}",
                "query": query,
                "results": []
            }
    
    def search_ipo_by_company(self, company_name: str) -> dict:
        """
        Search for specific company IPO information
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: IPO information for the company
        """
        query = f"{company_name} IPO listing date price GMP grey market premium"
        return self.tavily_search_(query)
    
    def search_upcoming_ipos(self) -> dict:
        """
        Search for upcoming IPO information
        
        Returns:
            dict: Information about upcoming IPOs
        """
        query = "upcoming IPO 2025 listing dates India stock market"
        return self.tavily_search_(query)
    
    def search_recent_ipos(self) -> dict:
        """
        Search for recently listed IPO information
        
        Returns:
            dict: Information about recent IPOs
        """
        query = "recent IPO listings 2025 performance stock price India"
        return self.tavily_search_(query)