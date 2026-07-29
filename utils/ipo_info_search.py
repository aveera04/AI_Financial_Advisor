import os
import json
from langchain_tavily import TavilySearch

class TavilyIPOInfoSearch:
    def __init__(self, api_key: str = None):
        """Initialize the Tavily IPO search tool"""
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found")
        self.search_tool = TavilySearch(api_key=self.api_key)

    def search(self, query: str) -> dict:
        """Simple search - pass query directly to Tavily"""
        try:
            return self.search_tool.invoke(query)
        except Exception as e:
            return {"error": str(e), "results": []}
    
    def search_ipo_by_company(self, company_name: str) -> dict:
        """Search for company IPO info"""
        return self.search(f"{company_name} IPO India")
    
    def search_upcoming_ipos(self) -> dict:
        """Search for upcoming IPOs"""
        return self.search("upcoming IPO India 2025")
    
    def search_recent_ipos(self) -> dict:
        """Search for recent IPOs"""
        return self.search("recent IPO listings India 2025")
    
    def search_ipo_gmp(self, company_name: str = None) -> dict:
        """Search for GMP info"""
        if company_name:
            return self.search(f"{company_name} IPO GMP grey market premium")
        return self.search("IPO GMP grey market premium today India")
    
    def search_ipo_subscription_status(self, company_name: str) -> dict:
        """Search for subscription status"""
        return self.search(f"{company_name} IPO subscription status")

    def search_comprehensive_ipo_data(self, user_query: str, company_name: str = None) -> dict:
        """Simple comprehensive search - just run the user query"""
        return self.search(user_query)