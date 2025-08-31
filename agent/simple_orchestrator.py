from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from utils.model_loader import ModelLoader
from tools.web_search_tool import WebSearchTool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from prompt_library.prompt import SYSTEM_PROMPT_IPO, SYSTEM_PROMPT_ORCHESTRATOR 

class SimpleOrchestratorAgent:
    """Simplified orchestrator agent without sub-graphs"""
    def __init__(self, model_provider: str = "groq"):
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        # Initialize web search tool
        self.web_search_tool = WebSearchTool()
        
        # Create specialized agent tools
        self.agent_tools = self._create_agent_tools()
        
        # General search tool
        self.general_tools = [self.web_search_tool.search_web]
        
        # All tools
        self.all_tools = self.agent_tools + self.general_tools
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.all_tools)
        
        print(f"🎯 Simple Orchestrator loaded {len(self.all_tools)} tools: {[tool.name for tool in self.all_tools]}")
        
        self.system_prompt = SYSTEM_PROMPT_ORCHESTRATOR

    def _create_agent_tools(self):
        """Create tools that represent specialized agents"""
        
        @tool
        def ipo_advisor_agent(query: str) -> str:
            """
            Route IPO-related queries to the specialized IPO advisor agent.
            Use this for questions about:
            - IPO recommendations
            - IPO analysis
            - Grey Market Premium (GMP)
            - IPO listing dates
            - IPO investment strategies
            
            Args:
                query (str): The IPO-related query to process
                
            Returns:
                str: Response from the IPO advisor agent
            """
            try:
                # Create a simple IPO response using web search tools
                ipo_search_tool = self.web_search_tool.search_ipo_info
                search_result = ipo_search_tool.invoke(query)
                
                # Process with IPO prompt
                ipo_llm = ModelLoader().load_llm()
                messages = [SYSTEM_PROMPT_IPO, HumanMessage(content=f"Based on this search data: {search_result}\n\nUser query: {query}")]
                response = ipo_llm.invoke(messages)
                
                return f"IPO Advisor Response:\n{response.content}"
                
            except Exception as e:
                return f"IPO Advisor Error: {str(e)}"
        
        return [ipo_advisor_agent]

    def orchestrator_function(self, state: MessagesState):
        """Main orchestrator function"""
        messages = state["messages"]
        full_messages = [self.system_prompt] + messages
        response = self.llm_with_tools.invoke(full_messages)
        return {"messages": [response]}

    def build_graph(self):
        """Build orchestrator graph"""
        graph_builder = StateGraph(MessagesState)
        
        graph_builder.add_node("orchestrator", self.orchestrator_function)
        graph_builder.add_node("tools", ToolNode(tools=self.all_tools))
        
        graph_builder.add_edge(START, "orchestrator")
        graph_builder.add_conditional_edges("orchestrator", tools_condition)
        graph_builder.add_edge("tools", "orchestrator")
        
        self.graph = graph_builder.compile()
        return self.graph

    def run(self, user_message: str):
        """Run orchestrator"""
        if not hasattr(self, 'graph'):
            self.build_graph()
        
        initial_state = {"messages": [HumanMessage(content=user_message)]}
        result = self.graph.invoke(initial_state)
        return result["messages"][-1].content

# Legacy support
class GraphBuilder(SimpleOrchestratorAgent):
    """Legacy alias"""
    pass
