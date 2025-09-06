"""
Gemini API service for chatbot functionality
"""
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """Service class for interacting with Google's Gemini API"""
    
    def _init_(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_chat_response(self, user_message, context=""):
        """
        Get a response from Gemini API for user message
        
        Args:
            user_message (str): The user's message
            context (str): Additional context about EcoFinds
            
        Returns:
            str: The AI response
        """
        try:
            # Create a context-aware prompt for EcoFinds
            ecofinds_context = """
            
            You are an AI assistant for EcoFinds, an eco-friendly marketplace for second-hand products. 
            EcoFinds specializes in:
            - Second-hand clothing, electronics, furniture, books, and other items
            - Promoting sustainability and reducing waste
            - Connecting buyers and sellers in an eco-conscious community
            - Quality assurance with condition ratings (Excellent, Good, Fair, Poor)
            - Competitive pricing for pre-owned items
            
            Please provide helpful, friendly, and informative responses about:
            - Product recommendations and search assistance
            - Sustainability benefits of buying second-hand
            - Shopping tips and best practices
            - General questions about the platform
            - Eco-friendly lifestyle advice
            
            Keep responses concise, helpful, and focused on EcoFinds' mission of sustainable shopping.
            """
            
            # Combine context with user message
            full_prompt = f"{ecofinds_context}\n\nUser question: {user_message}"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            return self._get_fallback_response(user_message)
    
    def _get_fallback_response(self, user_message):
        """
        Fallback response when Gemini API is unavailable
        """
        message_lower = user_message.lower()
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! Welcome to EcoFinds. I'm here to help you find great second-hand products and answer questions about sustainable shopping. How can I assist you today?"
        
        # Product search
        elif any(word in message_lower for word in ['search', 'find', 'looking for', 'need', 'want']):
            return "I can help you find products on EcoFinds! We have a wide selection of second-hand items including clothing, electronics, furniture, and more. What type of product are you looking for?"
        
        # Sustainability questions
        elif any(word in message_lower for word in ['eco', 'sustainable', 'environment', 'green', 'recycle']):
            return "Great question! EcoFinds promotes sustainability by giving second-hand items a new life. Buying pre-owned products reduces waste, saves resources, and helps build a circular economy. Every purchase on our platform contributes to a more sustainable future!"
        
        # Pricing questions
        elif any(word in message_lower for word in ['price', 'cost', 'expensive', 'cheap', 'affordable']):
            return "Our products are competitively priced second-hand items, typically 30-70% less than retail prices. Prices vary based on condition, brand, and demand. You can filter products by price range on our product page to find items within your budget."
        
        # Condition questions
        elif any(word in message_lower for word in ['condition', 'quality', 'used', 'damaged', 'wear']):
            return "All our products are categorized by condition: Excellent (like new), Good (minor wear), Fair (moderate wear), and Poor (significant wear but functional). Each listing includes detailed condition descriptions and photos so you know exactly what you're getting."
        
        # General help
        elif any(word in message_lower for word in ['help', 'support', 'assistance', 'how']):
            return "I'm here to help! You can ask me about products, sustainability benefits, shopping tips, or any questions about EcoFinds. You can also browse our product categories, use the search function, or contact our support team for specific assistance."
        
        # Default response
        else:
            return f"I understand you're asking about: '{user_message}'. That's an interesting question! While I'd love to provide more detailed assistance, I'm currently experiencing some technical difficulties. Please try browsing our product categories or contact our support team for specific help. You can also search for products using keywords related to what you're looking for."