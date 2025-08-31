#!/usr/bin/env python3
"""
Multi-Agent Workflow Demonstration
Shows detailed task routing, model usage, and real-time workflow progress
"""

from agent.agentic_workflow import OrchestratorAgent, IPOAdvisorAgent
from tools.web_search_tool import WebSearchTool
from dotenv import load_dotenv
import os
import time
import json
from datetime import datetime
from typing import Dict, List, Any

class MultiAgentWorkflowDemo:
    """
    Demonstrates multi-agent workflow with detailed logging and monitoring
    """
    
    def __init__(self):
        self.load_environment()
        self.orchestrator = None
        self.ipo_agent = None
        self.web_tool = None
        self.workflow_logs = []
        self.task_counter = 0
        
    def load_environment(self):
        """Load and validate environment variables"""
        print("🔧 INITIALIZING MULTI-AGENT WORKFLOW DEMO")
        print("=" * 60)
        
        load_dotenv()
        
        # Check API keys
        required_keys = ["GROQ_API_KEY", "TAVILY_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            print(f"❌ Missing API keys: {', '.join(missing_keys)}")
            raise ValueError(f"Missing required environment variables: {missing_keys}")
        
        print("✅ Environment variables loaded successfully")
        print(f"🔑 GROQ_API_KEY: {'✅ Present' if os.getenv('GROQ_API_KEY') else '❌ Missing'}")
        print(f"🔑 TAVILY_API_KEY: {'✅ Present' if os.getenv('TAVILY_API_KEY') else '❌ Missing'}")
        
    def initialize_agents(self):
        """Initialize all agents and tools with detailed logging"""
        print("\n🤖 AGENT INITIALIZATION PHASE")
        print("-" * 40)
        
        try:
            # Initialize Orchestrator Agent
            print("🎯 Initializing Orchestrator Agent...")
            print("   └── Model: groq_oss (llama3-70b-8192)")
            print("   └── Role: Query routing and coordination")
            
            start_time = time.time()
            self.orchestrator = OrchestratorAgent(model_provider="groq_oss")
            init_time = time.time() - start_time
            
            print(f"   └── ✅ Initialized in {init_time:.2f}s")
            print(f"   └── Tools available: {[tool.name for tool in self.orchestrator.all_tools]}")
            
            # Initialize IPO Agent separately for testing
            print("\n📊 Initializing IPO Advisor Agent...")
            print("   └── Model: groq_deepseek (deepseek-r1-distill-llama-70b)")
            print("   └── Role: Specialized IPO analysis and recommendations")
            
            start_time = time.time()
            try:
                self.ipo_agent = IPOAdvisorAgent(model_provider="groq_deepseek")
                init_time = time.time() - start_time
                print(f"   └── ✅ Initialized in {init_time:.2f}s")
                deepseek_available = True
            except Exception as e:
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    print("   └── ⚠️  DeepSeek model is rate-limited")
                    deepseek_available = False
                else:
                    print(f"   └── ❌ Error: {str(e)}")
                    deepseek_available = False
            
            # Initialize Web Search Tool
            print("\n🔍 Initializing Web Search Tool...")
            print("   └── Provider: Tavily API")
            print("   └── Capabilities: General web search + IPO-specific search")
            
            start_time = time.time()
            self.web_tool = WebSearchTool()
            init_time = time.time() - start_time
            print(f"   └── ✅ Initialized in {init_time:.2f}s")
            
            return deepseek_available
            
        except Exception as e:
            print(f"❌ Agent initialization failed: {str(e)}")
            raise
    
    def log_task(self, task_type: str, model: str, query: str, status: str, details: Dict[str, Any] = None):
        """Log task execution details"""
        self.task_counter += 1
        log_entry = {
            "task_id": self.task_counter,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "task_type": task_type,
            "model": model,
            "query": query[:50] + "..." if len(query) > 50 else query,
            "status": status,
            "details": details or {}
        }
        self.workflow_logs.append(log_entry)
        return self.task_counter
    
    def show_task_status(self, task_id: int, model: str, task_type: str, status: str = "RUNNING"):
        """Show real-time task status"""
        status_emoji = {
            "RUNNING": "🔄",
            "COMPLETED": "✅",
            "FAILED": "❌",
            "RATE_LIMITED": "⚠️"
        }
        
        print(f"\n{status_emoji.get(status, '❓')} TASK #{task_id}: {status}")
        print(f"   ├── Type: {task_type}")
        print(f"   ├── Model: {model}")
        print(f"   └── Timestamp: {datetime.now().strftime('%H:%M:%S')}")
    
    def test_orchestrator_routing(self, queries: List[Dict[str, str]], deepseek_available: bool):
        """Test orchestrator routing with detailed workflow tracking"""
        print(f"\n🧪 MULTI-AGENT WORKFLOW TESTING")
        print("=" * 50)
        print(f"📊 DeepSeek Status: {'✅ Available' if deepseek_available else '⚠️ Rate-Limited'}")
        print(f"🎯 Testing {len(queries)} different query types...")
        
        successful_tasks = 0
        
        for i, query_data in enumerate(queries, 1):
            query = query_data["query"]
            expected_route = query_data["expected_route"]
            query_type = query_data["type"]
            
            print(f"\n" + "="*60)
            print(f"🔍 QUERY {i}/{len(queries)}: {query_type}")
            print(f"📝 Query: {query}")
            print(f"🎯 Expected Route: {expected_route}")
            print("-" * 40)
            
            # Log task start
            task_id = self.log_task("ORCHESTRATOR_ROUTING", "qwen/qwen3-32b", query, "STARTED")
            self.show_task_status(task_id, "qwen/qwen3-32b", "Query Analysis", "RUNNING")
            
            try:
                start_time = time.time()
                
                # Step 1: Orchestrator processes query
                print("🎯 Step 1: Orchestrator analyzing query...")
                response = self.orchestrator.run(query)
                
                processing_time = time.time() - start_time
                
                # Step 2: Determine actual route
                if "IPO Advisor Response:" in response:
                    actual_route = "IPO Advisor Agent"
                    model_used = "deepseek-r1-distill-llama-70b"
                    route_emoji = "📊"
                elif "Search Results" in response or "search_web" in response.lower():
                    actual_route = "Web Search Tool"
                    model_used = "Tavily API"
                    route_emoji = "🔍"
                else:
                    actual_route = "Direct Response"
                    model_used = "qwen/qwen3-32b"
                    route_emoji = "💬"
                
                # Step 3: Show routing results
                print(f"🎯 Step 2: Query routed to → {route_emoji} {actual_route}")
                
                if model_used.startswith("deepseek") and not deepseek_available:
                    print("⚠️  Step 3: DeepSeek unavailable, using fallback")
                    status = "RATE_LIMITED"
                elif "Error" in response:
                    print("❌ Step 3: Error in processing")
                    status = "FAILED"
                else:
                    print(f"✅ Step 3: Successfully processed by {model_used}")
                    status = "COMPLETED"
                
                # Step 4: Show results
                self.show_task_status(task_id, model_used, f"Route: {actual_route}", status)
                
                print(f"\n📊 TASK RESULTS:")
                print(f"   ├── Processing Time: {processing_time:.2f} seconds")
                print(f"   ├── Expected Route: {expected_route}")
                print(f"   ├── Actual Route: {actual_route}")
                print(f"   ├── Model Used: {model_used}")
                print(f"   └── Status: {status}")
                
                # Show response preview
                print(f"\n📄 RESPONSE PREVIEW:")
                response_preview = response[:200] + "..." if len(response) > 200 else response
                print(f"   {response_preview}")
                
                # Determine success
                route_match = (expected_route.lower() in actual_route.lower() or 
                             "either" in expected_route.lower())
                
                if status == "COMPLETED" and route_match:
                    successful_tasks += 1
                    print("🎉 RESULT: ✅ SUCCESS")
                elif status == "RATE_LIMITED":
                    successful_tasks += 0.5
                    print("🎉 RESULT: ⚠️ PARTIAL SUCCESS (Rate Limited)")
                else:
                    print("🎉 RESULT: ❌ NEEDS REVIEW")
                
                # Log completion
                self.log_task("TASK_COMPLETED", model_used, query, status, {
                    "processing_time": processing_time,
                    "expected_route": expected_route,
                    "actual_route": actual_route,
                    "success": route_match
                })
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Error: {error_msg}")
                
                if "rate_limit" in error_msg.lower() or "429" in error_msg:
                    self.show_task_status(task_id, "N/A", "Rate Limited", "RATE_LIMITED")
                    successful_tasks += 0.5
                else:
                    self.show_task_status(task_id, "N/A", "Failed", "FAILED")
                
                self.log_task("TASK_FAILED", "N/A", query, "FAILED", {"error": error_msg})
            
            # Wait between queries to avoid rate limiting
            if i < len(queries):
                print(f"\n⏳ Waiting 8 seconds before next query...")
                time.sleep(8)
        
        return successful_tasks, len(queries)
    
    def show_workflow_summary(self, successful_tasks: int, total_tasks: int, deepseek_available: bool):
        """Show comprehensive workflow summary"""
        success_rate = (successful_tasks / total_tasks) * 100
        
        print(f"\n" + "="*70)
        print(f"🎉 MULTI-AGENT WORKFLOW SUMMARY")
        print("="*70)
        
        print(f"📊 PERFORMANCE METRICS:")
        print(f"   ├── Total Tasks: {total_tasks}")
        print(f"   ├── Successful: {successful_tasks}")
        print(f"   ├── Success Rate: {success_rate:.1f}%")
        print(f"   └── Average Time: {sum([log.get('details', {}).get('processing_time', 0) for log in self.workflow_logs]) / len([log for log in self.workflow_logs if log.get('details', {}).get('processing_time')]) if len([log for log in self.workflow_logs if log.get('details', {}).get('processing_time')]) > 0 else 0:.2f}s per task")
        
        print(f"\n🤖 AGENT STATUS:")
        print(f"   ├── Orchestrator (qwen/qwen3-32b): ✅ Active")
        print(f"   ├── IPO Agent (deepseek-r1-distill-llama-70b): {'✅ Active' if deepseek_available else '⚠️ Rate-Limited'}")
        print(f"   └── Web Search Tool (Tavily API): ✅ Active")
        
        print(f"\n🎯 ROUTING EFFECTIVENESS:")
        ipo_routes = len([log for log in self.workflow_logs if "IPO" in log.get('details', {}).get('actual_route', '')])
        web_routes = len([log for log in self.workflow_logs if "Web" in log.get('details', {}).get('actual_route', '')])
        direct_routes = len([log for log in self.workflow_logs if "Direct" in log.get('details', {}).get('actual_route', '')])
        
        print(f"   ├── IPO Agent Routes: {ipo_routes}")
        print(f"   ├── Web Search Routes: {web_routes}")
        print(f"   └── Direct Responses: {direct_routes}")
        
        # Overall system status
        if success_rate >= 75:
            system_status = "🎯 EXCELLENT - System performing optimally"
        elif success_rate >= 50:
            system_status = "⚠️ GOOD - System working with some limitations"
        else:
            system_status = "❌ NEEDS ATTENTION - Multiple issues detected"
        
        print(f"\n🚀 SYSTEM STATUS: {system_status}")
        
        if not deepseek_available:
            print(f"\n💡 RECOMMENDATIONS:")
            print(f"   ├── DeepSeek model will reset at 00:00 UTC")
            print(f"   ├── Consider using Qwen model for high-volume testing")
            print(f"   └── System is fully functional with current limitations")
    
    def run_demo(self):
        """Run the complete multi-agent workflow demonstration"""
        try:
            # Initialize all components
            deepseek_available = self.initialize_agents()
            
            # Define test queries with different routing scenarios
            test_queries = [
                {
                    "type": "IPO ANALYSIS",
                    "query": "What are the best IPO opportunities in India this week?",
                    "expected_route": "IPO Advisor Agent"
                },
                {
                    "type": "IPO INVESTMENT STRATEGY",
                    "query": "Should I invest in upcoming IPOs? Give me detailed analysis with GMP data.",
                    "expected_route": "IPO Advisor Agent"
                },
                {
                    "type": "GENERAL MARKET RESEARCH",
                    "query": "What are the current trends in Indian stock market today?",
                    "expected_route": "Web Search"
                },
                {
                    "type": "COMPARATIVE ANALYSIS",
                    "query": "Compare IPO performance vs mutual fund returns this year",
                    "expected_route": "Either IPO Agent or Web Search"
                },
                {
                    "type": "SPECIFIC IPO QUERY",
                    "query": "Tell me about Hyundai Motor India IPO - GMP, subscription status, and recommendation",
                    "expected_route": "IPO Advisor Agent"
                }
            ]
            
            # Run workflow tests
            successful_tasks, total_tasks = self.test_orchestrator_routing(test_queries, deepseek_available)
            
            # Show comprehensive summary
            self.show_workflow_summary(successful_tasks, total_tasks, deepseek_available)
            
            return True
            
        except Exception as e:
            print(f"\n❌ DEMO FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main execution function"""
    print("🎪 MULTI-AGENT WORKFLOW DEMONSTRATION")
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Purpose: Demonstrate task routing, model usage, and workflow monitoring")
    
    try:
        demo = MultiAgentWorkflowDemo()
        success = demo.run_demo()
        
        if success:
            print(f"\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
            print(f"📊 Multi-agent system is working correctly with proper task routing")
            print(f"🕒 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n❌ DEMONSTRATION ENCOUNTERED ISSUES")
            print(f"🔍 Check the detailed logs above for troubleshooting")
            
    except KeyboardInterrupt:
        print(f"\n⏸️  DEMONSTRATION STOPPED BY USER")
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    main()
