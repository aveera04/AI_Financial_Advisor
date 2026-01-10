import os
import json
from langchain_tavily import TavilySearch
from utils.model_loader import ModelLoader

class TavilyStockInfoSearch:
    def __init__(self, api_key: str = None):
        """
        Initialize the Tavily Stock Info search tool
        
        Args:
            api_key (str): Tavily API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        if not self.api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables or passed as parameter")
        
        # Initialize the search tool with stock-specific configuration
        self.search_tool = TavilySearch(api_key=self.api_key)
        
        # Initialize LLM for intelligent query generation (uses separate API key)
        try:
            self.query_generator = ModelLoader.from_env_key("groq_oss_20b", "GROQ_API_KEY_2").load_llm()
        except Exception as e:
            print(f"Warning: Could not initialize query generator: {e}")
            self.query_generator = None

    def _generate_stock_query(self, user_query: str, stock_context: str = "general") -> str:
        """
        Generate stock-optimized search queries using AI
        
        Args:
            user_query (str): Original user query
            stock_context (str): Stock context type ('performance', 'news', 'analysis', 'recommendation')
            
        Returns:
            str: AI-optimized stock search query
        """
        if not self.query_generator:
            # Fallback to manual query enhancement
            if stock_context == "performance":
                return f"{user_query} stock performance price history"
            elif stock_context == "news":
                return f"{user_query} latest stock news updates"
            elif stock_context == "analysis":
                return f"{user_query} stock analysis expert opinion"
            elif stock_context == "recommendation":
                return f"{user_query} stock buy sell recommendation"
            else:
                return f"{user_query} stock information India market"
        
        try:
            stock_prompt = f"""
            Generate an optimized search query for stock-related information based on the user's query.
            Focus on stock-specific terms and Indian market context.
            
            User Query: {user_query}
            Stock Context: {stock_context}
            
            Include relevant terms like: stock, share, price, performance, news, analysis, recommendation, India market
            
            Provide a concise and focused search query.
            """
            response = self.query_generator.invoke(stock_prompt)
            optimized_query = response.content.strip() if hasattr(response, 'content') else str(response).strip()

            # Clean and validate the response
            optimized_query = optimized_query.replace('"', '').replace("'", "").strip()
            if len(optimized_query) > 150:  # Fallback if too long
                return f"{user_query} stock information India"
            return optimized_query
        
        except Exception as e:
            print(f"Warning: Query generation failed: {e}")
            return f"{user_query} stock information India"

    def search_stock_overview(self, user_query: str) -> dict:
        """
        Search for comprehensive stock overview information
        
        Covers: Company Name, Sector, Market Cap, Current Price, 52-Week High/Low, 
        Trading Volume, Beta, Dividend Yield
        
        Args:
            user_query (str): User's stock overview query
            
        Returns:
            dict: Structured search results for stock overview
        """
        try:
            # Generate optimized query for stock overview
            overview_query = self._generate_stock_query(
                user_query + " company overview sector market cap current price NSE BSE 52-week high low trading volume beta dividend yield", 
                "overview"
            )
            
            print(f"[STOCK OVERVIEW] Optimized query: {overview_query}")
            
            # Perform the search
            results = self.search_tool.invoke(overview_query)
            
            return {
                "status": "success",
                "search_type": "stock_overview",
                "original_query": user_query,
                "optimized_query": overview_query,
                "results": results,
                "metadata": {
                    "categories": ["company_info", "price_data", "basic_metrics"],
                    "data_points": ["market_cap", "current_price", "52_week_range", "volume", "beta", "dividend_yield"]
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "search_type": "stock_overview",
                "original_query": user_query,
                "error": str(e),
                "fallback_suggestions": [
                    "Check NSE/BSE official websites",
                    "Use financial portals like MoneyControl",
                    "Refer to company investor relations page"
                ]
            }

    def search_fundamental_analysis(self, user_query: str) -> dict:
        """
        Search for fundamental analysis data
        
        Covers: Revenue Growth, Profit Margins, ROE, ROA, Debt-to-Equity, P/E Ratio,
        P/B Ratio, Current Ratio, Financial Health metrics
        
        Args:
            user_query (str): User's fundamental analysis query
            
        Returns:
            dict: Structured search results for fundamental analysis
        """
        try:
            # Generate optimized query for fundamental analysis
            fundamental_query = self._generate_stock_query(
                user_query + " financial analysis revenue growth profit margins ROE ROA debt equity ratio PE PB ratio current ratio financial health annual report", 
                "fundamental"
            )
            
            print(f"[FUNDAMENTAL ANALYSIS] Optimized query: {fundamental_query}")
            
            # Perform the search
            results = self.search_tool.invoke(fundamental_query)
            
            return {
                "status": "success",
                "search_type": "fundamental_analysis",
                "original_query": user_query,
                "optimized_query": fundamental_query,
                "results": results,
                "metadata": {
                    "categories": ["financial_ratios", "profitability", "valuation", "debt_analysis"],
                    "data_points": ["revenue_growth", "profit_margins", "roe", "roa", "debt_equity", "pe_ratio", "pb_ratio", "current_ratio"]
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "search_type": "fundamental_analysis",
                "original_query": user_query,
                "error": str(e),
                "fallback_suggestions": [
                    "Check annual reports on company website",
                    "Use Screener.in for financial ratios",
                    "Refer to BSE/NSE corporate announcements"
                ]
            }

    def search_technical_analysis(self, user_query: str) -> dict:
        """
        Search for technical analysis information
        
        Covers: Price Trends, Support/Resistance, Moving Averages, RSI, MACD,
        Volume Analysis, Chart Patterns, Price Targets
        
        Args:
            user_query (str): User's technical analysis query
            
        Returns:
            dict: Structured search results for technical analysis
        """
        try:
            # Generate optimized query for technical analysis
            technical_query = self._generate_stock_query(
                user_query + " technical analysis price chart support resistance moving averages RSI MACD volume analysis price targets bullish bearish", 
                "technical"
            )
            
            print(f"[TECHNICAL ANALYSIS] Optimized query: {technical_query}")
            
            # Perform the search
            results = self.search_tool.invoke(technical_query)
            
            return {
                "status": "success",
                "search_type": "technical_analysis",
                "original_query": user_query,
                "optimized_query": technical_query,
                "results": results,
                "metadata": {
                    "categories": ["price_action", "technical_indicators", "chart_patterns", "price_targets"],
                    "data_points": ["trend", "support_resistance", "moving_averages", "rsi", "macd", "volume", "price_targets"]
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "search_type": "technical_analysis",
                "original_query": user_query,
                "error": str(e),
                "fallback_suggestions": [
                    "Use TradingView for charts and indicators",
                    "Check technical analysis on investing.com",
                    "Refer to brokerage research reports"
                ]
            }

    def search_stock_news_events(self, user_query: str) -> dict:
        """
        Search for stock news and corporate events
        
        Covers: Latest News, Corporate Actions, Quarterly Results, Management Commentary,
        Sector Developments, Regulatory Changes, Dividends, Stock Splits
        
        Args:
            user_query (str): User's stock news/events query
            
        Returns:
            dict: Structured search results for stock news and events
        """
        try:
            # Generate optimized query for news and events
            news_query = self._generate_stock_query(
                user_query + " latest news corporate actions quarterly results earnings management commentary dividend bonus split regulatory SEBI", 
                "news"
            )
            
            print(f"[STOCK NEWS & EVENTS] Optimized query: {news_query}")
            
            # Perform the search
            results = self.search_tool.invoke(news_query)
            
            return {
                "status": "success",
                "search_type": "stock_news_events",
                "original_query": user_query,
                "optimized_query": news_query,
                "results": results,
                "metadata": {
                    "categories": ["corporate_news", "earnings", "corporate_actions", "regulatory_updates"],
                    "data_points": ["latest_news", "quarterly_results", "dividends", "bonus_splits", "management_commentary", "sector_trends"]
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "search_type": "stock_news_events",
                "original_query": user_query,
                "error": str(e),
                "fallback_suggestions": [
                    "Check Economic Times Markets section",
                    "Visit company investor relations page",
                    "Use BSE/NSE corporate announcements",
                    "Check financial news on MoneyControl"
                ]
            }

    def search_comprehensive_stock_data(self, user_query: str) -> dict:
        """
        Perform comprehensive stock search using all 4 specialized search methods
        
        Args:
            user_query (str): User's comprehensive stock query
            
        Returns:
            dict: Combined results from all search methods
        """
        try:
            print(f"[COMPREHENSIVE SEARCH] Starting multi-faceted search for: {user_query}")
            
            # Perform all 4 specialized searches
            overview_results = self.search_stock_overview(user_query)
            fundamental_results = self.search_fundamental_analysis(user_query)
            technical_results = self.search_technical_analysis(user_query)
            news_results = self.search_stock_news_events(user_query)
            
            return {
                "status": "success",
                "search_type": "comprehensive_stock_analysis",
                "original_query": user_query,
                "results": {
                    "overview": overview_results,
                    "fundamental": fundamental_results,
                    "technical": technical_results,
                    "news_events": news_results
                },
                "metadata": {
                    "search_methods_used": 4,
                    "comprehensive_coverage": True,
                    "data_categories": ["overview", "fundamental", "technical", "news_events"]
                }
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "search_type": "comprehensive_stock_analysis",
                "original_query": user_query,
                "error": str(e),
                "partial_results": "Some searches may have succeeded - check individual method results"
            }

    # Legacy compatibility method (if needed)
    def tavily_search_with_custom_query(self, query: str) -> dict:
        """
        Legacy method for backward compatibility
        Performs basic stock search using the general search
        """
        try:
            optimized_query = self._generate_stock_query(query, "general")
            results = self.search_tool.invoke(optimized_query)
            
            return {
                "status": "success",
                "original_query": query,
                "optimized_query": optimized_query,
                "results": results
            }
        except Exception as e:
            return {
                "status": "failed",
                "original_query": query,
                "error": str(e)
            }