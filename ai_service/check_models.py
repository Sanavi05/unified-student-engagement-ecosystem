#!/usr/bin/env python3
"""
Script to check available Gemini models for your API key
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found in .env file")
    print("Please add your API key to ai_service/.env")
    exit(1)

# Configure Gemini
genai.configure(api_key=api_key)

print("=" * 70)
print("🔍 Checking Available Gemini Models")
print("=" * 70)
print()

try:
    # List all available models
    models_list = list(genai.list_models())
    
    print(f"✅ Found {len(models_list)} models:\n")
    
    # Filter for available models
    available_models = []
    
    for idx, model in enumerate(models_list[:15], 1):  # Show first 15
        # Model comes as string like "models/gemini-pro"
        model_str = str(model)
        model_id = model_str.split('/')[-1] if '/' in model_str else model_str
        
        print(f"{idx}. {model_id}")
        available_models.append(model_id)
    
    print()
    print("=" * 70)
    print(f"\n🎯 Available models:")
    for model in available_models[:10]:
        print(f"  - {model}")
    
    # Try to pick the best one
    best_models_order = [
        'gemini-1.5-pro',
        'gemini-2.0-flash', 
        'gemini-1.5-flash',
        'gemini-1.0-pro',
        'gemini-pro'
    ]
    
    recommended = None
    for bm in best_models_order:
        if bm in available_models:
            recommended = bm
            break
    
    if recommended:
        print(f"\n💡 Recommended model to use:")
        print(f"   genai.GenerativeModel('{recommended}')")
    else:
        print(f"\n💡 Use this model:")
        print(f"   genai.GenerativeModel('{available_models[0]}')")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"\n📝 Error Details: {type(e).__name__}")
    import traceback
    traceback.print_exc()

