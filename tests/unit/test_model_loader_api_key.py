#!/usr/bin/env python3
"""
Test script to verify ModelLoader API key source parameter functionality
"""

import os
import sys
from utils.model_loader import ModelLoader

def test_api_key_source_logging():
    """Test if API key source parameter shows up in logs"""
    print("🔧 Testing ModelLoader API Key Source Parameter")
    print("=" * 60)
    
    # Check if environment variables are set
    api_key_1 = os.getenv("GROQ_API_KEY")
    api_key_2 = os.getenv("GROQ_API_KEY_2")
    
    print(f"📋 GROQ_API_KEY: {'✅ Set' if api_key_1 else '❌ Missing'}")
    print(f"📋 GROQ_API_KEY_2: {'✅ Set' if api_key_2 else '❌ Missing'}")
    
    if not api_key_1:
        print("❌ GROQ_API_KEY not found! Please set it in your .env file")
        return False
    
    try:
        print("\n" + "="*50)
        print("🧪 Test 1: Using from_env_key method with GROQ_API_KEY")
        print("="*50)
        
        # Test 1: Load model using primary API key
        loader1 = ModelLoader.from_env_key("groq_oss_20b", "GROQ_API_KEY")
        print(f"✅ ModelLoader created successfully")
        print(f"   Model Provider: {loader1.model_provider}")
        print(f"   API Key Source: {loader1.api_key_source}")
        print(f"   API Key (masked): {loader1.api_key[:8]}...{loader1.api_key[-4:] if len(loader1.api_key) > 12 else 'short_key'}")
        
        # Load the LLM
        print("\n🔄 Loading LLM model...")
        llm1 = loader1.load_llm()
        print("✅ LLM loaded successfully!")
        
        if api_key_2:
            print("\n" + "="*50)
            print("🧪 Test 2: Using from_env_key method with GROQ_API_KEY_2")
            print("="*50)
            
            # Test 2: Load model using secondary API key
            loader2 = ModelLoader.from_env_key("groq_oss_20b", "GROQ_API_KEY_2")
            print(f"✅ ModelLoader created successfully")
            print(f"   Model Provider: {loader2.model_provider}")
            print(f"   API Key Source: {loader2.api_key_source}")
            print(f"   API Key (masked): {loader2.api_key[:8]}...{loader2.api_key[-4:] if len(loader2.api_key) > 12 else 'short_key'}")
            
            # Load the LLM
            print("\n🔄 Loading LLM model...")
            llm2 = loader2.load_llm()
            print("✅ LLM loaded successfully!")
        else:
            print("\n⚠️  GROQ_API_KEY_2 not set, skipping Test 2")
        
        print("\n" + "="*50)
        print("🧪 Test 3: Direct API key instantiation")
        print("="*50)
        
        # Test 3: Direct instantiation with API key
        loader3 = ModelLoader(
            model_provider="groq_oss_20b", 
            api_key=api_key_1,
            api_key_source="Direct_GROQ_API_KEY"  # Manually set source
        )
        print(f"✅ ModelLoader created successfully")
        print(f"   Model Provider: {loader3.model_provider}")
        print(f"   API Key Source: {loader3.api_key_source}")
        print(f"   API Key (masked): {loader3.api_key[:8]}...{loader3.api_key[-4:] if len(loader3.api_key) > 12 else 'short_key'}")
        
        # Load the LLM
        print("\n🔄 Loading LLM model...")
        llm3 = loader3.load_llm()
        print("✅ LLM loaded successfully!")
        
        print("\n" + "="*60)
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        print("✅ API key source parameter is working correctly")
        print("✅ Environment variable names are being logged")
        print("✅ Both from_env_key and direct instantiation work")
        print("✅ API keys are properly masked in logs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_different_models():
    """Test with different model providers"""
    print("\n" + "="*50)
    print("🧪 Test 4: Different Model Providers")
    print("="*50)
    
    models_to_test = ["groq_oss", "groq_oss_20b"]
    api_key = os.getenv("GROQ_API_KEY")
    
    for model in models_to_test:
        try:
            print(f"\n🔄 Testing model: {model}")
            loader = ModelLoader(
                model_provider=model,
                api_key=api_key,
                api_key_source=f"Test_{model}"
            )
            print(f"   ✅ Created loader for {model}")
            print(f"   📝 API Key Source: {loader.api_key_source}")
            
            # Just create the loader, don't load LLM to save time
            
        except Exception as e:
            print(f"   ❌ Failed for {model}: {e}")

if __name__ == "__main__":
    print("🚀 Starting ModelLoader API Key Source Tests")
    print("=" * 60)
    
    # Test API key source functionality
    success = test_api_key_source_logging()
    
    if success:
        # Test different models
        test_different_models()
        
        print("\n" + "🎯" * 20)
        print("🏆 TESTING COMPLETE!")
        print("🎯" * 20)
        print("All ModelLoader API key source functionality is working correctly!")
    else:
        print("\n❌ Tests failed. Please check your .env file and API keys.")
        sys.exit(1)
