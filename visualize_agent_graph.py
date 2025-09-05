#!/usr/bin/env python3
"""
Temporary file to visualize the agent workflow graph with tools
"""

import os
from dotenv import load_dotenv
from agent.agentic_workflow import OrchestratorAgent, IPOAdvisorAgent
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

# Load environment variables
load_dotenv()

def create_workflow_graph():
    """Create a visual representation of the agent workflow"""
    
    print("🎨 CREATING AGENT WORKFLOW VISUALIZATION")
    print("="*60)
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Define nodes with their types and colors - Agent-centric approach
    nodes = {
        # Input/Output
        "User Query": {"type": "input", "color": "#4CAF50", "pos": (0, 0)},
        "Final Response": {"type": "output", "color": "#FF9800", "pos": (8, 0)},
        
        # Main Agents (central nodes)
        "Orchestrator Agent\n(llama3-70b-8192)": {"type": "orchestrator", "color": "#2196F3", "pos": (2, 0)},
        "IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)": {"type": "agent", "color": "#9C27B0", "pos": (6, 0)},
        
        # Orchestrator Tools (connected to orchestrator)
        "search_web": {"type": "orch_tool", "color": "#FFC107", "pos": (1, 1.5)},
        "tavily_smart_search": {"type": "orch_tool", "color": "#FFC107", "pos": (2, 2)},
        "tavily_financial_search": {"type": "orch_tool", "color": "#FFC107", "pos": (3, 1.5)},
        
        # IPO Agent Tools (connected to IPO agent)
        "search_ipo_info": {"type": "ipo_tool", "color": "#00BCD4", "pos": (5, 1.5)},
        "ipo_search_web": {"type": "ipo_tool", "color": "#00BCD4", "pos": (6, 2)},
        "ipo_smart_search": {"type": "ipo_tool", "color": "#00BCD4", "pos": (7, 1.5)},
        "ipo_financial_search": {"type": "ipo_tool", "color": "#00BCD4", "pos": (6, -1.5)},
        
        # Decision Point
        "Route Decision": {"type": "decision", "color": "#F44336", "pos": (4, 0)},
    }
    
    # Add nodes to graph
    for node, attrs in nodes.items():
        G.add_node(node, **attrs)
    
    # Define edges (clean agent-tool connections)
    edges = [
        # Main flow
        ("User Query", "Orchestrator Agent\n(llama3-70b-8192)"),
        ("Orchestrator Agent\n(llama3-70b-8192)", "Route Decision"),
        
        # Route to IPO Agent or direct tool usage
        ("Route Decision", "IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)"),
        ("Route Decision", "Final Response"),  # Direct orchestrator response
        
        # Orchestrator Tools (connected to orchestrator)
        ("Orchestrator Agent\n(llama3-70b-8192)", "search_web"),
        ("Orchestrator Agent\n(llama3-70b-8192)", "tavily_smart_search"),
        ("Orchestrator Agent\n(llama3-70b-8192)", "tavily_financial_search"),
        
        # IPO Agent Tools (connected to IPO agent)
        ("IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)", "search_ipo_info"),
        ("IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)", "ipo_search_web"),
        ("IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)", "ipo_smart_search"),
        ("IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)", "ipo_financial_search"),
        
        # Final responses from agents
        ("IPO Advisor Agent\n(deepseek-r1-distill-llama-70b)", "Final Response"),
    ]
    
    # Add edges to graph
    G.add_edges_from(edges)
    
    return G, nodes

def visualize_graph(G, nodes):
    """Create and save the workflow visualization"""
    
    # Set up the plot
    plt.figure(figsize=(16, 12))
    
    # Get positions
    pos = {node: attrs["pos"] for node, attrs in nodes.items()}
    
    # Draw nodes with different shapes and colors based on type
    for node, attrs in nodes.items():
        x, y = pos[node]
        color = attrs["color"]
        node_type = attrs["type"]
        
        if node_type == "input":
            plt.scatter(x, y, s=2000, c=color, marker='o', alpha=0.8, edgecolors='black', linewidth=2)
        elif node_type == "output":
            plt.scatter(x, y, s=2000, c=color, marker='s', alpha=0.8, edgecolors='black', linewidth=2)
        elif node_type == "orchestrator":
            plt.scatter(x, y, s=3000, c=color, marker='D', alpha=0.8, edgecolors='black', linewidth=3)
        elif node_type == "agent":
            plt.scatter(x, y, s=3000, c=color, marker='h', alpha=0.8, edgecolors='black', linewidth=2)
        elif node_type == "orch_tool":
            plt.scatter(x, y, s=1500, c=color, marker='^', alpha=0.8, edgecolors='black', linewidth=1)
        elif node_type == "ipo_tool":
            plt.scatter(x, y, s=1500, c=color, marker='v', alpha=0.8, edgecolors='black', linewidth=1)
        elif node_type == "decision":
            plt.scatter(x, y, s=1800, c=color, marker='D', alpha=0.8, edgecolors='black', linewidth=2)
    
    # Draw edges
    for edge in G.edges():
        start_pos = pos[edge[0]]
        end_pos = pos[edge[1]]
        
        # Determine arrow style based on connection type
        if "Agent" in edge[1] or "Agent" in edge[0]:
            plt.annotate("", xy=end_pos, xytext=start_pos,
                        arrowprops=dict(arrowstyle='->', lw=2.5, color='darkblue', alpha=0.8))
        elif "Decision" in edge[1] or "Decision" in edge[0]:
            plt.annotate("", xy=end_pos, xytext=start_pos,
                        arrowprops=dict(arrowstyle='->', lw=2, color='red', alpha=0.7))
        elif "search" in edge[1] or "ipo_" in edge[1] or "tavily" in edge[1]:
            plt.annotate("", xy=end_pos, xytext=start_pos,
                        arrowprops=dict(arrowstyle='-', lw=1.5, color='darkgreen', alpha=0.6))  # Tools connected, not directed flow
        else:
            plt.annotate("", xy=end_pos, xytext=start_pos,
                        arrowprops=dict(arrowstyle='->', lw=1.5, color='gray', alpha=0.7))
    
    # Add labels
    for node, (x, y) in pos.items():
        plt.text(x, y-0.3, node, ha='center', va='top', fontsize=8, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Create legend
    legend_elements = [
        mpatches.Patch(color='#4CAF50', label='Input'),
        mpatches.Patch(color='#FF9800', label='Output'),
        mpatches.Patch(color='#2196F3', label='Orchestrator Agent'),
        mpatches.Patch(color='#9C27B0', label='IPO Agent'), 
        mpatches.Patch(color='#FFC107', label='Orchestrator Tools'),
        mpatches.Patch(color='#00BCD4', label='IPO Agent Tools'),
        mpatches.Patch(color='#F44336', label='Route Decision'),
    ]
    
    plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0, 1))
    
    # Set title and labels
    plt.title('AI Financial Advisor - Agent-Tool Architecture\n(Clean View: Agents Connected to Their Tools)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Workflow Flow →', fontsize=12)
    plt.ylabel('Tool Distribution ↑', fontsize=12)
    
    # Remove axis ticks
    plt.xticks([])
    plt.yticks([])
    
    # Set axis limits
    plt.xlim(-1, 9)
    plt.ylim(-2.5, 2.5)
    
    # Add grid
    plt.grid(True, alpha=0.3)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('agent_workflow_graph.png', dpi=300, bbox_inches='tight')
    
    print("✅ Clean agent-tool architecture saved as 'agent_workflow_graph.png'")
    
    # Show the plot
    plt.show()

def print_workflow_details():
    """Print detailed workflow information"""
    
    print("\n📊 AGENT WORKFLOW ANALYSIS")
    print("="*60)
    
    try:
        # Initialize agents to get tool information
        print("🔧 Initializing agents...")
        orchestrator = OrchestratorAgent()
        ipo_agent = IPOAdvisorAgent()
        
        print("\n🎯 ORCHESTRATOR AGENT DETAILS:")
        print(f"Model: groq_oss (llama3-70b-8192)")
        print(f"Total Tools: {len(orchestrator.all_tools)}")
        for i, tool in enumerate(orchestrator.all_tools, 1):
            print(f"  {i}. {tool.name} - {tool.description.split('.')[0]}")
        
        print(f"\n📊 IPO AGENT DETAILS:")
        print(f"Model: groq_deepseek (deepseek-r1-distill-llama-70b)")
        print(f"Total Tools: {len(ipo_agent.tools)}")
        for i, tool in enumerate(ipo_agent.tools, 1):
            print(f"  {i}. {tool.name} - {tool.description.split('.')[0]}")
        
        print(f"\n🔍 ENHANCED SEARCH CAPABILITIES:")
        print("• AI-powered query optimization")
        print("• Context-aware search routing")
        print("• IPO-specific information retrieval")
        print("• Grey Market Premium (GMP) tracking")
        print("• Financial market analysis")
        print("• Smart search with multiple contexts")
        
        print(f"\n🎨 WORKFLOW FLOW:")
        print("1. User Query → Orchestrator Agent")
        print("2. Query Analysis & Tool Selection")
        print("3. Route to Appropriate Agent/Tool")
        print("4. Execute Search with AI-Optimized Queries")
        print("5. Process & Format Results")
        print("6. Return Comprehensive Response")
        
    except Exception as e:
        print(f"⚠️  Could not initialize agents: {e}")
        print("Using static workflow information...")

def main():
    """Main function to create and display the workflow graph"""
    
    print("🚀 AI FINANCIAL ADVISOR - WORKFLOW VISUALIZER")
    print("="*70)
    
    try:
        # Create the graph
        G, nodes = create_workflow_graph()
        print(f"✅ Created workflow graph with {len(G.nodes())} nodes and {len(G.edges())} edges")
        
        # Visualize the graph
        visualize_graph(G, nodes)
        
        # Print workflow details
        print_workflow_details()
        
        print("\n🎉 CLEAN AGENT-TOOL VISUALIZATION COMPLETE!")
        print("The diagram now shows:")
        print("• Agents as central nodes with their tools connected")
        print("• Clear agent-tool relationships")
        print("• Simple workflow: User → Orchestrator → (IPO Agent or Direct Response)")
        print("• Each agent clearly shows which tools it can use")
        
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        print("Make sure matplotlib and networkx are installed:")
        print("pip install matplotlib networkx")

if __name__ == "__main__":
    main()
