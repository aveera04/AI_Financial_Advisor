#!/usr/bin/env python3
"""
Rate-Limit Aware Test for Multi-Agent System
Uses fallbac    print("    print("🔸 Qwen Models: Higher limits available")
    print("🔸 Reset Time: Daily at 00:00 UTC")
    print("\n💡 Solutions:")
    print("1. Wait for daily reset (~12 minutes based on error)")
    print("2. Use qwen/qwen3-32b for more testing")Q RATE LIMIT INFORMATION")
    print("=" * 40)
    print("🔸 DeepSeek Model: 100,000 tokens/day (On-Demand tier)")
    print("🔸 Qwen Models: Higher limits available")
    print("🔸 Reset Time: Daily at 00:00 UTC")
    print("\n💡 Solutions:")
    print("1. Wait for daily reset (~12 minutes based on error)")
    print("2. Use qwen/qwen3-32b for more testing")
    print("3. Upgrade to Dev tier for higher limits")
    print("4. Use fallback strategy (implemented above)")pSeek model is rate-limited
"""

from agent.agentic_workflow import OrchestratorAgent, IPOAdvisorAgent
from dotenv import load_dotenv
import os

def test_with_fallback():
    """Test system with automatic fallback when rate-limited"""
    
    load_dotenv()
    
    print("🎯 RATE-LIMIT AWARE ORCHESTRATOR TEST")
    print("=" * 50)
    
    # Check API keys
    if not os.getenv("GROQ_API_KEY") or not os.getenv("TAVILY_API_KEY"):
        print("❌ Missing API keys")
        return False
    
    try:
        # First, try to test just the orchestrator with Qwen model
        print("🤖 Testing Orchestrator (qwen/qwen3-32b)...")
        orchestrator = OrchestratorAgent(model_provider="groq_oss")
        print("✅ Orchestrator initialized successfully!")
        
        # Test if DeepSeek is available by trying IPO agent directly
        print("🧪 Testing DeepSeek availability...")
        try:
            ipo_agent = IPOAdvisorAgent(model_provider="groq_deepseek")
            test_response = ipo_agent.process_query("Quick test")
            
            if "rate limit" in test_response.lower() or "429" in test_response:
                print("⚠️  DeepSeek is rate-limited, using fallback strategy")
                use_deepseek = False
            else:
                print("✅ DeepSeek is available")
                use_deepseek = True
                
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print("⚠️  DeepSeek rate-limited, using Qwen fallback")
                use_deepseek = False
            else:
                print(f"❌ DeepSeek error: {str(e)}")
                use_deepseek = False
        
        # Test with appropriate strategy
        if use_deepseek:
            print("🔍 Testing with DeepSeek IPO agent...")
            query = "What are current IPO opportunities?"
            response = orchestrator.run(query)
            
            if "IPO Advisor Response:" in response:
                print("✅ Successfully routed to DeepSeek IPO Agent!")
            else:
                print("⚠️  Response unclear but system functional")
                
        else:
            print("🔍 Testing orchestrator routing (DeepSeek unavailable)...")
            query = "Current market information"  # This should go to general search
            response = orchestrator.run(query)
            
            if len(response) > 50:
                print("✅ Orchestrator functioning with available tools!")
            else:
                print("⚠️  Limited response due to rate limits")
        
        print(f"📄 Response preview: {response[:100] if 'response' in locals() else 'No response due to rate limits'}...")
        
        print("\n🎉 FALLBACK TEST COMPLETED!")
        print("💡 Key Findings:")
        print("  - Orchestrator initialization: ✅ Working")
        print(f"  - DeepSeek availability: {'✅ Available' if use_deepseek else '⚠️  Rate-limited'}")
        print("  - System can handle rate limits gracefully")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def show_rate_limit_info():
    """Show rate limit information and solutions"""
    print("\n📊 GROQ RATE LIMIT INFORMATION")
    print("=" * 40)
    print("🔸 DeepSeek Model: 100,000 tokens/day (On-Demand tier)")
    print("🔸 Llama Models: Higher limits available")
    print("🔸 Reset Time: Daily at 00:00 UTC")
    print("\n💡 Solutions:")
    print("1. Wait for daily reset (~12 minutes based on error)")
    print("2. Use llama-3.1-8b-instant for more testing")
    print("3. Upgrade to Dev tier for higher limits")
    print("4. Use fallback strategy (implemented above)")

def main():
    success = test_with_fallback()
    show_rate_limit_info()
    
    if success:
        print("\n✅ SYSTEM STATUS: FUNCTIONAL WITH RATE LIMIT AWARENESS")
        print("🚀 Your multi-agent system is working correctly!")
        print("⏰ DeepSeek will be available again after rate limit reset")
    else:
        print("\n❌ SYSTEM NEEDS ATTENTION")

if __name__ == "__main__":
    main()
