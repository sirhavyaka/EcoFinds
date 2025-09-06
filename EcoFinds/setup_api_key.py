#!/usr/bin/env python
"""
Setup script to configure Gemini API key
Run this script to set up your API key for the chatbot
"""

import os
import sys

def setup_api_key():
    """Setup the Gemini API key"""
    api_key = "AIzaSyBlbgtFoFsCeQ1sWIskG6dAZphNe8CQIvY"
    
    print("🔑 Setting up Gemini API Key...")
    print("=" * 40)
    
    # Set environment variable for current session
    os.environ['GEMINI_API_KEY'] = api_key
    
    print(f"✅ API Key set: {api_key[:20]}...")
    print("✅ Environment variable configured for current session")
    
    # Test the setup
    try:
        # Setup Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoFinds.settings')
        import django
        django.setup()
        
        from chatbot.gemini_service import GeminiService
        service = GeminiService()
        print("✅ Gemini service initialized successfully")
        
        # Test API call
        response = service.get_chat_response("Hello")
        print("✅ API test successful")
        print(f"📝 Sample response: {response[:50]}...")
        
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False
    
    print("\n🎉 Setup complete! Your chatbot is ready to use.")
    print("💡 Note: This sets the API key for the current session only.")
    print("   For permanent setup, use system environment variables.")
    
    return True

if __name__ == "__main__":
    setup_api_key()
