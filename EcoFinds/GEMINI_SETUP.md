# Gemini API Setup Guide

This guide will help you set up the Gemini API integration for the EcoFinds chatbot.

## Prerequisites

1. A Google Cloud Platform account
2. Access to the Gemini API (formerly Bard API)

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## Step 2: Set Environment Variable

### Option A: Using Environment Variables (Recommended)

Set the environment variable in your system:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_actual_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_actual_api_key_here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### Option B: Using .env file

1. Create a `.env` file in the project root (`EcoFinds/EcoFinds/.env`)
2. Add the following line:
```
GEMINI_API_KEY=your_actual_api_key_here
```

## Step 3: Install Dependencies

Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Test the Integration

1. Start your Django development server:
```bash
python manage.py runserver
```

2. Navigate to `http://localhost:8000/chatbot/` in your browser
3. Log in to your account
4. Try sending a message to the chatbot

## Troubleshooting

### API Key Not Working
- Ensure your API key is correctly set in the environment variable
- Check that the API key has the necessary permissions
- Verify the key is active in Google AI Studio

### Fallback Mode
If the Gemini API is not available or misconfigured, the chatbot will automatically fall back to a simple rule-based system that can still provide helpful responses about EcoFinds.

### Common Issues
- **403 Forbidden**: Check your API key permissions
- **429 Too Many Requests**: You've exceeded the API rate limit
- **Network Error**: Check your internet connection

## Security Notes

- Never commit your API key to version control
- Use environment variables for production deployments
- Consider using a secrets management service for production

## Support

If you encounter any issues, please check the Django logs for error messages or contact the development team.
