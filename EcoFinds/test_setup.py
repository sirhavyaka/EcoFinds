#!/usr/bin/env python
"""
Test script to verify EcoFinds Django setup
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def test_setup():
    """Test if Django setup is working correctly"""
    print("Testing EcoFinds Django Setup...")
    print("=" * 50)
    
    # Test 1: Django settings
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoFinds.settings')
        django.setup()
        print("✅ Django settings loaded successfully")
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False
    
    # Test 2: Database connection
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False
    
    # Test 3: Check if all apps are loaded
    try:
        from django.apps import apps
        app_names = [app.label for app in apps.get_app_configs()]
        expected_apps = ['firebase_auth', 'main', 'products', 'cart', 'orders', 'user_profile', 'chatbot']
        
        for app in expected_apps:
            if app in app_names:
                print(f"✅ App '{app}' loaded successfully")
            else:
                print(f"❌ App '{app}' not found")
                return False
    except Exception as e:
        print(f"❌ App loading error: {e}")
        return False
    
    # Test 4: Check if models can be imported
    try:
        from products.models import Product, Category
        from cart.models import Cart, CartItem
        from orders.models import Order, OrderItem
        from user_profile.models import UserProfile, Address
        print("✅ All models imported successfully")
    except Exception as e:
        print(f"❌ Model import error: {e}")
        return False
    
    # Test 5: Check if URLs are configured
    try:
        from django.urls import reverse
        from django.test import Client
        client = Client()
        
        # Test home page
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home page accessible")
        else:
            print(f"❌ Home page error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ URL configuration error: {e}")
        return False
    
    print("=" * 50)
    print("🎉 All tests passed! EcoFinds is ready to use.")
    print("\nNext steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Configure Firebase authentication")
    print("3. Run the server: python manage.py runserver")
    print("4. Visit http://127.0.0.1:8000/")
    
    return True

if __name__ == "__main__":
    success = test_setup()
    sys.exit(0 if success else 1)
