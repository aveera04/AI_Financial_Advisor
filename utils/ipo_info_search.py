import os
import json
from langchain_tavily import TavilySearch
from utils.model_loader import ModelLoader

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
        
        # Initialize LLM for intelligent query generation
        try:
            self.query_generator = ModelLoader(model_provider="groq_oss").load_llm()
        except Exception as e:
            print(f"Warning: Could not initialize query generator: {e}")
            self.query_generator = None

    def _generate_ipo_query(self, user_query: str, ipo_context: str = "general") -> str:
        """
        Generate IPO-optimized search queries using AI
        
        Args:
            user_query (str): Original user query
            ipo_context (str): IPO context type ('listing', 'gmp', 'upcoming', 'performance')
            
        Returns:
            str: AI-optimized IPO search query
        """
        if not self.query_generator:
            # Fallback to manual query enhancement
            if ipo_context == "listing":
                return f"{user_query} IPO listing date price subscription"
            elif ipo_context == "gmp":
                return f"{user_query} grey market premium GMP kostak rate"
            elif ipo_context == "upcoming":
                return f"{user_query} upcoming IPO 2025 dates subscription"
            elif ipo_context == "performance":
                return f"{user_query} IPO performance stock price gains"
            else:
                return f"{user_query} IPO information India stock market"
        
        try:
            ipo_prompt = f"""
            Generate an optimized search query for IPO-related information based on the user's query.
            Focus on IPO-specific terms and Indian stock market context.
            
            User Query: {user_query}
            IPO Context: {ipo_context}
            
            Include relevant terms like: IPO, listing, grey market premium (GMP), subscription, 
            NSE, BSE, issue price, lot size, listing date, kostak rate, mainboard, SME
            
            Generate a concise search query (max 25 words) optimized for finding IPO information:
            """
            
            response = self.query_generator.invoke(ipo_prompt)
            optimized_query = response.content.strip() if hasattr(response, 'content') else str(response).strip()
            
            # Clean and validate the response
            optimized_query = optimized_query.replace('"', '').replace("'", "").strip()
            if len(optimized_query) > 150:  # Fallback if too long
                return f"{user_query} IPO information India"
            
            return optimized_query
            
        except Exception as e:
            print(f"IPO query generation error: {e}")
            return f"{user_query} IPO information grey market premium"

    def tavily_search_with_custom_query(self, custom_query: str) -> dict:
        """
        Search for IPO information using a custom generated query
        
        Args:
            custom_query (str): Pre-optimized search query
            
        Returns:
            dict: Search results from Tavily
        """
        try:
            # Use the custom query directly
            results = self.search_tool.invoke(custom_query)
            return results
            
        except Exception as e:
            return {
                "error": f"Error performing custom IPO search: {str(e)}",
                "query": custom_query,
                "results": []
            }

    def tavily_search_(self, query: str) -> dict:
        """
        Search for IPO information using Tavily API with AI-enhanced query
        
        Args:
            query (str): The search query for IPO information
            
        Returns:
            dict: Search results from Tavily
        """
        try:
            # Generate AI-optimized query
            enhanced_query = self._generate_ipo_query(query, "general")
            print(f"🎯 IPO Query Enhanced: {query} → {enhanced_query}")
            
            # Perform the search using enhanced query
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
        Search for specific company IPO information with AI query optimization
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: IPO information for the company
        """
        optimized_query = self._generate_ipo_query(f"{company_name} IPO", "listing")
        return self.tavily_search_with_custom_query(optimized_query)
    
    def search_upcoming_ipos(self) -> dict:
        """
        Search for upcoming IPO information with AI query optimization
        
        Returns:
            dict: Information about upcoming IPOs
        """
        optimized_query = self._generate_ipo_query("upcoming IPOs 2025", "upcoming")
        return self.tavily_search_with_custom_query(optimized_query)
    
    def search_recent_ipos(self) -> dict:
        """
        Search for recently listed IPO information with AI query optimization
        
        Returns:
            dict: Information about recent IPOs
        """
        optimized_query = self._generate_ipo_query("recent IPO listings 2025", "performance")
        return self.tavily_search_with_custom_query(optimized_query)
    
    def search_ipo_gmp(self, company_name: str = None) -> dict:
        """
        Search for Grey Market Premium (GMP) information with AI query optimization
        
        Args:
            company_name (str): Optional company name for specific GMP search
            
        Returns:
            dict: GMP information
        """
        query = f"{company_name} GMP" if company_name else "IPO grey market premium today"
        optimized_query = self._generate_ipo_query(query, "gmp")
        return self.tavily_search_with_custom_query(optimized_query)
    
    def search_ipo_subscription_status(self, company_name: str) -> dict:
        """
        Search for IPO subscription status with AI query optimization
        
        Args:
            company_name (str): Name of the company
            
        Returns:
            dict: Subscription status information
        """
        optimized_query = self._generate_ipo_query(f"{company_name} IPO subscription status", "listing")
        return self.tavily_search_with_custom_query(optimized_query)