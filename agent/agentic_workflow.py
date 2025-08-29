from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from utils.model_loader import ModelLoader
from tools.web_search_tool import WebSearchTool
from langchain_core.messages import HumanMessage, SystemMessage
# from prompt_library.prompt import SYSTEM_PROMPT

class GraphBuilder:
    def __init__(self, model_provider: str = "groq"):
        # Defining llm loading
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()

        # Defining tools
        self.web_search_tool = WebSearchTool()
        self.tools = [self.web_search_tool.get_tool()]
        
        # Bind tools to the LLM
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def agent_function(self, state: MessagesState):
        """
        Main agent function that processes messages and decides on actions
        """
        messages = state["messages"]
        
        # Add system prompt if needed
        system_prompt = """You are a helpful financial advisor assistant. 
        You have access to web search tools to find current financial information, market data, 
        news, and other relevant information to help answer user questions.
        
        When you need current information or specific data that you don't have, use the web search tool.
        Always provide accurate, helpful, and well-sourced information."""
        
        # Prepare messages with system prompt
        full_messages = [SystemMessage(content=system_prompt)] + messages
        
        # Get response from LLM
        response = self.llm_with_tools.invoke(full_messages)
        
        return {"messages": [response]}

    def build_graph(self):
        """
        Build the agent workflow graph
        """
        graph_builder = StateGraph(MessagesState)
        
        # Add nodes
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        
        # Add edges
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges(
            "agent",
            tools_condition,
        )
        graph_builder.add_edge("tools", "agent")
        
        # Compile the graph
        self.graph = graph_builder.compile()
        return self.graph

    def __call__(self):
        return self.build_graph()
    
    def run(self, user_message: str):
        """
        Run the agent with a user message
        """
        if not hasattr(self, 'graph'):
            self.build_graph()
        
        # Create initial state
        initial_state = {
            "messages": [HumanMessage(content=user_message)]
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return result["messages"][-1].content