#!/usr/bin/env python3
"""
Streamlit Web UI for Multi-Agent Financial Advisor
Simple chatbot interface to interact with the orchestrator system
"""

import streamlit as st
import time
from datetime import datetime
from agent.agentic_workflow import OrchestratorAgent
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Dark theme for main content */
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    /* Main header */
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #2d5aa0, #4caf50);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: #ffffff;
    }
    
    .user-message {
        background-color: #2d5aa0;
        border-left: 4px solid #4fc3f7;
        color: #ffffff;
    }
    
    .assistant-message {
        background-color: #424242;
        border-left: 4px solid #4caf50;
        color: #ffffff;
    }
    
    /* System info boxes */
    .system-info {
        background-color: #333333;
        border: 1px solid #4caf50;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #2d2d2d;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #333333;
        color: #ffffff;
        border: 1px solid #4caf50;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 5px;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
    }
    
    /* Chat input */
    .stChatInput > div > div > div > div > input {
        background-color: #333333 !important;
        color: #ffffff !important;
        border: 1px solid #4caf50 !important;
    }
    
    /* Success/Info/Warning messages */
    .stSuccess {
        background-color: #2e7d32;
        color: #ffffff;
    }
    
    .stInfo {
        background-color: #1976d2;
        color: #ffffff;
    }
    
    .stWarning {
        background-color: #f57c00;
        color: #ffffff;
    }
    
    .stError {
        background-color: #d32f2f;
        color: #ffffff;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #333333;
        padding: 0.5rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "system_initialized" not in st.session_state:
        st.session_state.system_initialized = False

def initialize_system():
    """Initialize the multi-agent system"""
    try:
        # Check API keys
        if not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
            st.error("❌ Missing API keys! Please set GROQ_API_KEY and TAVILY_API_KEY in your .env file")
            return False
        
        with st.spinner("🤖 Initializing AI Financial Advisor System..."):
            st.session_state.orchestrator = OrchestratorAgent(model_provider="groq_oss")
            st.session_state.system_initialized = True
            
        st.success("✅ AI Financial Advisor System initialized successfully!")
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {str(e)}")
        return False

def get_response(query):
    """Get response from the orchestrator"""
    try:
        with st.spinner("🔄 Processing your query..."):
            start_time = time.time()
            response = st.session_state.orchestrator.run(query)
            processing_time = time.time() - start_time
            
            # Determine which agent/tool was used
            if "IPO Advisor Response:" in response:
                agent_used = "📊 IPO Advisor Agent (DeepSeek)"
                route_info = "Specialized IPO Analysis"
            elif "Search Results" in response or "search_web" in response.lower():
                agent_used = "🔍 Web Search Tool (Tavily)"
                route_info = "General Market Research"
            else:
                agent_used = "🎯 Orchestrator (Qwen)"
                route_info = "Direct Response"
            
            return {
                "response": response,
                "agent_used": agent_used,
                "route_info": route_info,
                "processing_time": processing_time
            }
    except Exception as e:
        return {
            "response": f"❌ Error: {str(e)}",
            "agent_used": "❌ System Error",
            "route_info": "Error occurred",
            "processing_time": 0
        }

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Financial Advisor</h1>
        <p>Multi-Agent System with Qwen Orchestrator & DeepSeek IPO Specialist</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 System Information")
        
        if st.session_state.system_initialized:
            st.markdown("""
            <div class="system-info">
                <h4>✅ System Status: Active</h4>
                <ul style="color: #ffffff;">
                    <li><b>🎯 Orchestrator:</b> openai/gpt-oss-120b</li>
                    <li><b>📊 IPO Agent:</b> DeepSeek R1</li>
                    <li><b>🔍 Web Search:</b> Tavily API</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="system-info">
                <h4>⚠️ System Status: Not Initialized</h4>
                <p style="color: #ffffff;">Click 'Initialize System' to start</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Initialize button
        if st.button("🚀 Initialize System", type="primary"):
            initialize_system()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Sample queries
        st.header("💡 Sample Queries")
        sample_queries = [
            "What are the current IPO opportunities in India?",
            "Should I invest in upcoming IPOs this week?",
            "What are today's stock market trends?",
            "Compare IPO vs mutual fund returns",
            "Tell me about Hyundai Motor India IPO"
        ]
        
        for i, query in enumerate(sample_queries):
            if st.button(f"📝 {query[:30]}...", key=f"sample_{i}"):
                if st.session_state.system_initialized:
                    st.session_state.messages.append({"role": "user", "content": query})
                    st.rerun()
                else:
                    st.warning("Please initialize the system first!")
    
    # Main chat interface
    st.header("💬 Chat with AI Financial Advisor")
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <b style="color: #ffffff;">👤 You:</b><br>
                <span style="color: #ffffff;">{message["content"]}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <b style="color: #ffffff;">🤖 AI Advisor:</b><br>
                <span style="color: #ffffff;">{message["content"]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Show agent info if available
            if "agent_info" in message:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**Agent Used:** {message['agent_info']['agent_used']}")
                with col2:
                    st.info(f"**Route:** {message['agent_info']['route_info']}")
                with col3:
                    st.info(f"**Time:** {message['agent_info']['processing_time']:.2f}s")
    
    # Chat input
    if prompt := st.chat_input("Ask me about IPOs, stock market trends, investment advice..."):
        if not st.session_state.system_initialized:
            st.warning("⚠️ Please initialize the system first using the sidebar!")
            return
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get and add assistant response
        result = get_response(prompt)
        
        assistant_message = {
            "role": "assistant", 
            "content": result["response"],
            "agent_info": {
                "agent_used": result["agent_used"],
                "route_info": result["route_info"],
                "processing_time": result["processing_time"]
            }
        }
        
        st.session_state.messages.append(assistant_message)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #cccccc;">
        <p>⚠️ <b>Disclaimer:</b> This is not investment advice. Please consult a financial advisor before making investment decisions.</p>
        <p>🕒 Last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
