from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def chat_view(request):
    """
    Chat interface view
    """
    return render(request, 'chatbot/chat.html')


@csrf_exempt
@login_required
def chat_api(request):
    """
    Chat API endpoint
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # Simple chatbot logic - you can integrate with AI services here
            response = get_chatbot_response(message)
            
            return JsonResponse({
                'success': True,
                'response': response
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error processing message'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def chat_history(request):
    """
    Chat history view
    """
    # Implement chat history logic here
    return render(request, 'chatbot/chat_history.html')


def get_chatbot_response(message):
    """
    Simple chatbot response logic
    """
    message_lower = message.lower()
    
    # Greeting responses
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! Welcome to EcoFinds. How can I help you today?"
    
    # Product search
    elif any(word in message_lower for word in ['search', 'find', 'looking for', 'need']):
        return "I can help you find products! You can use our search bar or browse by categories. What type of product are you looking for?"
    
    # Pricing questions
    elif any(word in message_lower for word in ['price', 'cost', 'expensive', 'cheap']):
        return "Our products are competitively priced second-hand items. Prices vary based on condition and brand. You can filter products by price range on our product page."
    
    # Condition questions
    elif any(word in message_lower for word in ['condition', 'quality', 'used', 'damaged']):
        return "All our products are categorized by condition: Excellent, Good, Fair, and Poor. Each product listing includes detailed condition information and photos."
    
    # Shipping questions
    elif any(word in message_lower for word in ['shipping', 'delivery', 'ship', 'send']):
        return "We offer various shipping options. Shipping costs and delivery times depend on your location and the seller's location. Check the product page for specific shipping details."
    
    # Return/refund questions
    elif any(word in message_lower for word in ['return', 'refund', 'exchange', 'problem']):
        return "We have a return and refund policy. If you're not satisfied with your purchase, you can request a return within 7 days. Contact our support team for assistance."
    
    # Account questions
    elif any(word in message_lower for word in ['account', 'profile', 'login', 'register']):
        return "You can manage your account through your profile page. If you need help with login or registration, I can guide you through the process."
    
    # General help
    elif any(word in message_lower for word in ['help', 'support', 'assistance']):
        return "I'm here to help! You can ask me about products, pricing, shipping, returns, or any other questions about EcoFinds. What would you like to know?"
    
    # Default response
    else:
        return "I understand you're asking about: " + message + ". Could you please provide more details so I can help you better? You can also browse our FAQ section or contact our support team for specific assistance."