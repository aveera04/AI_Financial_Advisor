import os
from langchain_tavily import TavilySearch

class TavilyStockInfoSearch:
    def __init__(self, api_key: str = None):
        """Initialize the Tavily Stock Info search tool"""
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

    def search_stock_overview(self, user_query: str) -> dict:
        """Search for stock overview"""
        return self.search(f"{user_query} stock price NSE BSE India")

    def search_fundamental_analysis(self, user_query: str) -> dict:
        """Search for fundamental analysis"""
        return self.search(f"{user_query} fundamental analysis PE ratio India")

    def search_technical_analysis(self, user_query: str) -> dict:
        """Search for technical analysis"""
        return self.search(f"{user_query} technical analysis chart India")

    def search_stock_news_events(self, user_query: str) -> dict:
        """Search for stock news"""
        return self.search(f"{user_query} stock news India")

    def search_comprehensive_stock_data(self, user_query: str) -> dict:
        """Simple comprehensive search - just run the user query"""
        return self.search(user_query)