#!/usr/bin/env python
"""
Test script for Gemini API integration
Run this script to test if the Gemini API is properly configured
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoFinds.settings')
django.setup()

from chatbot.gemini_service import GeminiService
from django.conf import settings

def test_gemini_integration():
    """Test the Gemini API integration"""
    print("🤖 Testing Gemini API Integration for EcoFinds Chatbot")
    print("=" * 60)
    
    # Check if API key is configured
    if not settings.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY environment variable is not set")
        print("Please set your Gemini API key as an environment variable:")
        print("Windows: $env:GEMINI_API_KEY=\"your_api_key_here\"")
        print("Linux/Mac: export GEMINI_API_KEY=\"your_api_key_here\"")
        return False
    
    print(f"✅ GEMINI_API_KEY is configured")
    
    try:
        # Test Gemini service initialization
        print("🔄 Initializing Gemini service...")
        gemini_service = GeminiService()
        print("✅ Gemini service initialized successfully")
        
        # Test a simple query
        print("🔄 Testing API call...")
        test_message = "Hello! Can you tell me about EcoFinds?"
        response = gemini_service.get_chat_response(test_message)
        
        print("✅ API call successful!")
        print(f"📝 Test message: {test_message}")
        print(f"🤖 AI Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        print("This might be due to:")
        print("- Invalid API key")
        print("- Network connectivity issues")
        print("- API quota exceeded")
        print("- API service unavailable")
        return False

def test_fallback_mode():
    """Test the fallback response system"""
    print("\n🔄 Testing fallback mode...")
    
    try:
        from chatbot.views import get_chatbot_response
        
        test_messages = [
            "Hello",
            "What products do you have?",
            "How does EcoFinds promote sustainability?",
            "What are your shipping options?"
        ]
        
        for message in test_messages:
            response = get_chatbot_response(message)
            print(f"✅ Fallback response for '{message}': {response[:50]}...")
        
        print("✅ Fallback mode working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Error testing fallback mode: {str(e)}")
        return False

if __name__ == "__main__":
    print("EcoFinds Chatbot Integration Test")
    print("=" * 40)
    
    # Test Gemini integration
    gemini_success = test_gemini_integration()
    
    # Test fallback mode
    fallback_success = test_fallback_mode()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"Gemini API Integration: {'✅ PASS' if gemini_success else '❌ FAIL'}")
    print(f"Fallback Mode: {'✅ PASS' if fallback_success else '❌ FAIL'}")
    
    if gemini_success:
        print("\n🎉 All tests passed! Your chatbot is ready to use.")
        print("Visit http://localhost:8000/chatbot/ to start chatting!")
    elif fallback_success:
        print("\n⚠️  Gemini API is not working, but fallback mode is available.")
        print("The chatbot will still work with basic responses.")
        print("Check your API key configuration and try again.")
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
    
    print("\nFor setup help, see GEMINI_SETUP.md")
