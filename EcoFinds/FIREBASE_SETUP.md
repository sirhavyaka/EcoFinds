# 🔥 Firebase Authentication Setup for EcoFinds

## Quick Setup (5 minutes)

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Project name: `EcoFinds`
4. Enable Google Analytics (optional)
5. Click "Create project"

### 2. Enable Authentication
1. In Firebase Console, click "Authentication" → "Get started"
2. Go to "Sign-in method" tab
3. Enable **Email/Password**:
   - Click "Email/Password" → Enable → Save
4. Enable **Google**:
   - Click "Google" → Enable → Add support email → Save

### 3. Get Configuration
1. Go to Project Settings (⚙️) → General tab
2. Scroll to "Your apps" section
3. Click "Add app" → Web (</>)
4. App nickname: `EcoFinds Web`
5. Click "Register app"
6. Copy the configuration object

### 4. Update Django Project

#### Option A: Use the Setup Script (Recommended)
```bash
python setup_firebase.py
```

#### Option B: Manual Update
1. Open `templates/base.html`
2. Find the Firebase configuration section
3. Replace the placeholder values with your actual config:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "your-app-id"
};
```

### 5. Test Authentication
1. Run the server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/`
3. Click "Login" or "Register"
4. Try logging in with Google or email

## Advanced Setup (Optional)

### Firebase Admin SDK (Server-side Verification)
1. Go to Project Settings → Service Accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Rename to `firebase_credentials.json`
5. Place in project root directory

### Environment Variables
Create a `.env` file:
```env
FIREBASE_CREDENTIALS_JSON={"type":"service_account",...}
```

## Troubleshooting

### Common Issues

1. **"Firebase not defined" error**
   - Check if Firebase scripts are loaded in `base.html`
   - Verify Firebase configuration is correct

2. **Authentication not working**
   - Check browser console for errors
   - Verify Firebase project has authentication enabled
   - Check if domain is authorized in Firebase Console

3. **Google sign-in not working**
   - Verify Google provider is enabled
   - Check if OAuth consent screen is configured
   - Add your domain to authorized domains

4. **CORS errors**
   - Add your domain to Firebase authorized domains
   - Check CORS settings in Django

### Testing Checklist

- [ ] Firebase project created
- [ ] Authentication providers enabled
- [ ] Configuration updated in `base.html`
- [ ] Server running without errors
- [ ] Login page loads correctly
- [ ] Google sign-in works
- [ ] Email/password sign-in works
- [ ] User can access protected pages

## Security Notes

1. **Never commit Firebase credentials to version control**
2. **Use environment variables for production**
3. **Configure authorized domains in Firebase Console**
4. **Enable App Check for production (optional)**

## Support

If you encounter issues:
1. Check the browser console for errors
2. Verify Firebase Console settings
3. Check Django logs for server errors
4. Review the Firebase documentation

## Next Steps

After Firebase is set up:
1. Test the complete authentication flow
2. Add sample products to test the full functionality
3. Customize the UI and branding
4. Set up production deployment
