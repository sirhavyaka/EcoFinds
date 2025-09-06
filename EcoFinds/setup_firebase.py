#!/usr/bin/env python
"""
Firebase Setup Script for EcoFinds
This script helps you configure Firebase authentication
"""
import os
import json

def setup_firebase():
    print("🔥 Firebase Setup for EcoFinds")
    print("=" * 50)
    
    print("\n1. Firebase Project Setup:")
    print("   - Go to https://console.firebase.google.com/")
    print("   - Create a new project named 'EcoFinds'")
    print("   - Enable Authentication with Google and Email/Password")
    
    print("\n2. Get Firebase Configuration:")
    print("   - Go to Project Settings > General")
    print("   - Scroll to 'Your apps' section")
    print("   - Click 'Add app' > Web")
    print("   - Copy the configuration object")
    
    # Get Firebase config from user
    print("\n3. Enter your Firebase configuration:")
    print("   (You can find this in your Firebase project settings)")
    
    api_key = input("   API Key: ").strip()
    auth_domain = input("   Auth Domain (e.g., your-project.firebaseapp.com): ").strip()
    project_id = input("   Project ID: ").strip()
    storage_bucket = input("   Storage Bucket (e.g., your-project.appspot.com): ").strip()
    messaging_sender_id = input("   Messaging Sender ID: ").strip()
    app_id = input("   App ID: ").strip()
    
    if not all([api_key, auth_domain, project_id, storage_bucket, messaging_sender_id, app_id]):
        print("❌ Please provide all required configuration values")
        return False
    
    # Update base.html template
    config_js = f"""    <!-- Firebase Configuration -->
    <script>
        // Firebase configuration
        const firebaseConfig = {{
            apiKey: "{api_key}",
            authDomain: "{auth_domain}",
            projectId: "{project_id}",
            storageBucket: "{storage_bucket}",
            messagingSenderId: "{messaging_sender_id}",
            appId: "{app_id}"
        }};
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
    </script>"""
    
    # Read current base.html
    base_template_path = "templates/base.html"
    if os.path.exists(base_template_path):
        with open(base_template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the Firebase config section
        import re
        pattern = r'    <!-- Firebase Configuration -->.*?    </script>'
        new_content = re.sub(pattern, config_js, content, flags=re.DOTALL)
        
        # Write updated content
        with open(base_template_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Updated templates/base.html with your Firebase configuration")
    else:
        print("❌ templates/base.html not found")
        return False
    
    # Create firebase_credentials.json if user wants
    setup_admin = input("\n4. Set up Firebase Admin SDK? (y/n): ").strip().lower()
    if setup_admin == 'y':
        print("\n   To get Firebase Admin SDK credentials:")
        print("   - Go to Project Settings > Service Accounts")
        print("   - Click 'Generate new private key'")
        print("   - Download the JSON file")
        print("   - Rename it to 'firebase_credentials.json'")
        print("   - Place it in the project root directory")
        
        # Check if credentials file exists
        if os.path.exists("firebase_credentials.json"):
            print("✅ firebase_credentials.json found")
        else:
            print("⚠️  firebase_credentials.json not found - you can add it later")
    
    print("\n5. Test your setup:")
    print("   - Run: python manage.py runserver")
    print("   - Visit: http://127.0.0.1:8000/")
    print("   - Try logging in with Google or email")
    
    print("\n" + "=" * 50)
    print("🎉 Firebase setup complete!")
    print("\nNext steps:")
    print("1. Test the authentication flow")
    print("2. Add some sample products")
    print("3. Customize the UI as needed")
    
    return True

if __name__ == "__main__":
    setup_firebase()
