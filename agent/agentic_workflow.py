from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from utils.model_loader import ModelLoader
from tools.web_search_tool import WebSearchTool
from tools.stock_web_search_tool import StockWebSearchTool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from prompt_library.prompt import SYSTEM_PROMPT_IPO, SYSTEM_PROMPT_ORCHESTRATOR, SYSTEM_PROMPT_STOCK 


class IPOAdvisorAgent:
    """Specialized IPO advisor agent"""
    def __init__(self, model_provider: str = "groq_deepseek", api_key_name: str = "GROQ_API_KEY"):
        self.model_loader = ModelLoader.from_env_key(model_provider, api_key_name)
        self.llm = self.model_loader.load_llm()
        
        # IPO-specific tools with enhanced Tavily search
        self.web_search_tool = WebSearchTool()
        self.tools = self.web_search_tool.get_ipo_search_tools()  # Gets all 4 tools including new ones
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.system_prompt = SYSTEM_PROMPT_IPO
        
        # Build the IPO agent graph
        self.graph = self._build_ipo_graph()

    def _build_ipo_graph(self):
        """Build the IPO agent workflow graph"""
        graph_builder = StateGraph(MessagesState)
        
        # Add nodes
        graph_builder.add_node("ipo_agent", self._ipo_agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))  # Must be named "tools" for tools_condition
        
        # Add edges
        graph_builder.add_edge(START, "ipo_agent")
        graph_builder.add_conditional_edges(
            "ipo_agent",
            tools_condition,
        )
        graph_builder.add_edge("tools", "ipo_agent")
        
        return graph_builder.compile()

    def _ipo_agent_function(self, state: MessagesState):
        """IPO agent function for LangGraph"""
        messages = state["messages"]
        full_messages = [self.system_prompt] + messages
        response = self.llm_with_tools.invoke(full_messages)
        return {"messages": [response]}

    def process_query(self, query: str) -> str:
        """Process IPO-related queries using the graph"""
        try:
            initial_state = {"messages": [HumanMessage(content=query)]}
            result = self.graph.invoke(initial_state)
            return result["messages"][-1].content
        except Exception as e:
            return f"IPO Agent Error: {str(e)}"

class StockAdvisorAgent:
    """Specialized Stock advisor agent with advanced stock analysis tools"""
    def __init__(self, model_provider: str = "groq_oss", api_key_name: str = "GROQ_API_KEY"):
        self.model_loader = ModelLoader.from_env_key(model_provider, api_key_name)
        self.llm = self.model_loader.load_llm()
        
        # Initialize specialized stock search tools
        self.stock_web_search_tool = StockWebSearchTool()
        self.tools = self.stock_web_search_tool.get_all_stock_tools()  # Gets all 5 specialized stock tools
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.system_prompt = SYSTEM_PROMPT_STOCK

        # Build the stock agent graph
        self.graph = self._build_stock_graph()

    def _build_stock_graph(self):
        """Build the stock agent workflow graph"""
        graph_builder = StateGraph(MessagesState)
        
        # Add nodes
        graph_builder.add_node("stock_agent", self._stock_agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))  # Must be named "tools" for tools_condition
        
        # Add edges
        graph_builder.add_edge(START, "stock_agent")
        graph_builder.add_conditional_edges(
            "stock_agent",
            tools_condition,
        )
        graph_builder.add_edge("tools", "stock_agent")
        
        return graph_builder.compile()

    def _stock_agent_function(self, state: MessagesState):
        """Stock agent function for LangGraph"""
        messages = state["messages"]
        full_messages = [self.system_prompt] + messages
        response = self.llm_with_tools.invoke(full_messages)
        return {"messages": [response]}

    def process_query(self, query: str) -> str:
        """Process stock-related queries using the graph"""
        try:
            initial_state = {"messages": [HumanMessage(content=query)]}
            result = self.graph.invoke(initial_state)
            return result["messages"][-1].content
        except Exception as e:
            return f"Stock Agent Error: {str(e)}"



class OrchestratorAgent:
    """Main orchestrator agent that routes queries to specialized agents"""
    def __init__(self, model_provider: str = "groq_oss_120b", api_key_name: str = "GROQ_API_KEY"):
        # Initialize LLM for orchestrator
        self.model_loader = ModelLoader.from_env_key(model_provider, api_key_name)
        self.llm = self.model_loader.load_llm()
        
        # Initialize specialized agents
        self.ipo_agent = IPOAdvisorAgent(model_provider="groq_deepseek", api_key_name="GROQ_API_KEY")
        self.stock_agent = StockAdvisorAgent(model_provider="groq_oss", api_key_name="GROQ_API_KEY")

        # Initialize general web search tool with enhanced capabilities
        self.web_search_tool = WebSearchTool()
        self.general_search_tools = [
            self.web_search_tool.search_web,
            self.web_search_tool.tavily_smart_search,
            self.web_search_tool.tavily_financial_search
        ]  # Enhanced search tools for orchestrator
        
        # Create tools for the orchestrator to call specialized agents
        self.agent_tools = self._create_agent_tools()
        
        # All tools available to orchestrator
        self.all_tools = self.agent_tools + self.general_search_tools
        
        # Bind tools to orchestrator LLM
        self.llm_with_tools = self.llm.bind_tools(self.all_tools)
        
        print(f"🎯 Orchestrator ({model_provider}) loaded {len(self.all_tools)} tools: {[tool.name for tool in self.all_tools]}")
        print(f"📊 IPO Agent using: groq_deepseek (deepseek-r1-distill-llama-70b)")
        print(f"📈 Stock Agent using: groq_oss (openai/gpt-oss-120b)")

        self.system_prompt = SYSTEM_PROMPT_ORCHESTRATOR

    def _create_agent_tools(self):
        """Create tools that represent specialized agents"""
        
        @tool
        def ipo_advisor_agent(query: str) -> str:
            """
            Get IPO advice and information. Use for IPO-related queries.
            
            Args:
                query: The IPO question to answer
                
            Returns:
                str: IPO advisor response
            """
            try:
                result = self.ipo_agent.process_query(query)
                return f"IPO Advisor Response:\n{result}"
            except Exception as e:
                return f"Error from IPO Advisor: {str(e)}"
        
        @tool
        def stock_advisor_agent(query: str) -> str:
            """
            Get comprehensive stock analysis and investment advice. Use for stock-related queries including analysis, recommendations, price targets, and investment decisions.
            
            Args:
                query: The stock question to answer (e.g., "Analyze RELIANCE stock", "TCS buy recommendation", "HDFC Bank technical analysis")
                
            Returns:
                str: Stock advisor response with comprehensive analysis
            """
            try:
                result = self.stock_agent.process_query(query)
                return f"Stock Advisor Response:\n{result}"
            except Exception as e:
                error_msg = str(e)
                if "Connection error" in error_msg or "Invalid API Key" in error_msg:
                    return f"Notice: The specialized Stock Advisor tool required to generate an in‑depth analysis is currently unavailable due to an authentication error. Consequently, I am unable to provide the detailed analysis you requested at this time. Please try again later or let me know if you would like assistance with a different query."
                else:
                    return f"Error from Stock Advisor: {error_msg}"
        
        return [ipo_advisor_agent, stock_advisor_agent]

    def orchestrator_function(self, state: MessagesState):
        """Main orchestrator function that routes queries"""
        messages = state["messages"]
        
        # Add orchestrator system prompt
        full_messages = [self.system_prompt] + messages
        
        # Get response from orchestrator LLM with tools
        response = self.llm_with_tools.invoke(full_messages)
        
        return {"messages": [response]}

    def build_graph(self):
        """Build the orchestrator workflow graph"""
        graph_builder = StateGraph(MessagesState)
        
        # Add nodes
        graph_builder.add_node("orchestrator", self.orchestrator_function)
        graph_builder.add_node("tools", ToolNode(tools=self.all_tools))
        
        # Add edges
        graph_builder.add_edge(START, "orchestrator")
        graph_builder.add_conditional_edges(
            "orchestrator",
            tools_condition,
        )
        graph_builder.add_edge("tools", "orchestrator")
        
        # Compile the graph
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
    
    def run(self, user_message: str):
        """Run the orchestrator with a user message"""
        if not hasattr(self, 'graph'):
            self.build_graph()
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=user_message)]
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return result["messages"][-1].content

# Legacy support - keep the old GraphBuilder name for backward compatibility
class GraphBuilder(OrchestratorAgent):
    """Backward compatibility class for existing code"""
    pass
class GraphBuilder(OrchestratorAgent):
    """Legacy alias for OrchestratorAgent"""
    pass