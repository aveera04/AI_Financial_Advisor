# Financial Advisor Orchestrator Agent

## 🎯 Overview
You now have a sophisticated **Orchestrator Agent** that can control multiple specialized financial advisor agents and route queries to the appropriate agent based on the query type.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           ORCHESTRATOR AGENT            │
│  (Routes queries to specialized agents) │
└─────────────────────┬───────────────────┘
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ IPO ADVISOR │ │GENERAL      │ │FUTURE: STOCK│
│    AGENT    │ │SEARCH  TOOL │ │ADVISOR AGENT│
└─────────────┘ └─────────────┘ └─────────────┘
```

## 📁 Files Created/Modified

### 1. **Main Orchestrator** (`agent/agentic_workflow.py`)
- `OrchestratorAgent`: Main orchestrator that routes queries
- `IPOAdvisorAgent`: Specialized IPO advisor with full LangGraph workflow
- `GraphBuilder`: Legacy alias for backward compatibility

### 2. **Simplified Version** (`agent/simple_orchestrator.py`)
- `SimpleOrchestratorAgent`: Simpler version without sub-graphs
- Better for testing and debugging

### 3. **Test Scripts**
- `test_orchestrator.py`: Comprehensive testing
- `simple_test.py`: Basic orchestrator test
- `test_simple_orchestrator.py`: Simple version test

## 🛠️ How It Works

### 1. **Query Analysis**
The orchestrator analyzes incoming queries using `SYSTEM_PROMPT_ORCHESTRATOR`:
- Determines if query is IPO-related → routes to IPO Advisor Agent
- Determines if query is general → uses web search tool
- Future: Will route stock questions to Stock Advisor Agent

### 2. **Tool Routing**
```python
# Available tools for orchestrator:
tools = [
    "ipo_advisor_agent",    # Routes to specialized IPO agent
    "search_web",          # General web search
    # Future: "stock_advisor_agent"
]
```

### 3. **IPO Agent Processing**
When IPO queries are detected:
1. Routes to `ipo_advisor_agent` tool
2. IPO agent uses `SYSTEM_PROMPT_IPO` 
3. IPO agent has access to `search_web` and `search_ipo_info` tools
4. Returns structured IPO analysis with GMP, dates, recommendations

## 🚀 Usage Examples

### Basic Usage
```python
from agent.agentic_workflow import OrchestratorAgent

# Initialize orchestrator
orchestrator = OrchestratorAgent(model_provider="groq")

# IPO Query - Routes to IPO Advisor Agent
response = orchestrator.run("Tell me about upcoming IPOs in India with good GMP")

# General Query - Uses web search tool  
response = orchestrator.run("What are the current market trends?")
```

### Legacy Support
```python
# Still works for backward compatibility
from agent.agentic_workflow import GraphBuilder

agent = GraphBuilder()  # Actually creates OrchestratorAgent
response = agent.run("IPO query here")
```

## 🔧 Features Implemented

### ✅ Current Features
1. **Smart Query Routing** - Automatically detects IPO vs general queries
2. **IPO Specialist Agent** - Dedicated agent with IPO-specific prompts and tools
3. **Web Search Integration** - Both general and IPO-specific search capabilities
4. **LangGraph Workflow** - Full graph-based agent workflow with tool conditions
5. **Legacy Compatibility** - Existing code still works with new orchestrator

### 🚧 Future Enhancements (Ready to Add)
1. **Stock Advisor Agent** - Add dedicated stock analysis agent
2. **Portfolio Management Agent** - Personal portfolio advice
3. **Market Research Agent** - Broader market analysis
4. **Risk Assessment Agent** - Risk analysis and compliance

## 📊 Tool Routing Logic

### IPO Queries → IPO Advisor Agent
- "IPO recommendations"
- "Grey Market Premium" 
- "IPO listing dates"
- "Should I invest in [Company] IPO?"
- "Upcoming IPOs"

### General Queries → Web Search Tool
- "Market trends"
- "Economic news"
- "Stock market analysis"
- "Company financial reports"

## 🎯 Benefits

1. **Specialized Expertise** - Each agent has domain-specific knowledge and tools
2. **Scalable Architecture** - Easy to add new specialized agents
3. **Efficient Routing** - Queries go directly to the most qualified agent
4. **Maintained Performance** - Each agent optimized for specific use cases
5. **Tool Isolation** - Agents only have tools relevant to their domain

## 🧪 Testing

Run the tests to verify everything works:

```bash
# Test simplified orchestrator (recommended for debugging)
python test_simple_orchestrator.py

# Test full orchestrator
python test_orchestrator.py

# Test backward compatibility
python test_agent.py  # Should still work with new orchestrator
```

## 🚀 Next Steps

### Adding Stock Advisor Agent:
1. Create `StockAdvisorAgent` class
2. Add stock-specific system prompt to `prompt_library/prompt.py`  
3. Create `stock_advisor_agent` tool in orchestrator
4. Update routing logic to detect stock queries

### Example Implementation:
```python
@tool
def stock_advisor_agent(query: str) -> str:
    """Route stock analysis queries to stock advisor agent"""
    return self.stock_agent.process_query(query)
```

The orchestrator is now ready and working! 🎉
