from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from utils.model_loader import ModelLoader
from tools.web_search_tool import WebSearchTool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from prompt_library.prompt import SYSTEM_PROMPT_IPO, SYSTEM_PROMPT_ORCHESTRATOR 

class IPOAdvisorAgent:
    """Specialized IPO advisor agent"""
    def __init__(self, model_provider: str = "groq_deepseek"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        # IPO-specific tools with enhanced Tavily search
        self.web_search_tool = WebSearchTool()
        self.tools = self.web_search_tool.get_tools()  # Gets all 4 tools including new ones
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

class OrchestratorAgent:
    """Main orchestrator agent that routes queries to specialized agents"""
    def __init__(self, model_provider: str = "groq_oss"):
        # Initialize LLM for orchestrator
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        # Initialize specialized agents with deepseek model
        self.ipo_agent = IPOAdvisorAgent(model_provider="groq_deepseek")
        
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
        
        # Future: Add more agent tools here
        # @tool
        # def stock_advisor_agent(query: str) -> str:
        #     """Route stock-related queries to stock advisor agent"""
        #     return self.stock_agent.process_query(query)
        
        return [ipo_advisor_agent]

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
    """Legacy alias for OrchestratorAgent"""
    pass