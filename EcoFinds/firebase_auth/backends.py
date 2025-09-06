from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .firebase_auth import FirebaseAuthentication
import logging

logger = logging.getLogger(__name__)


class FirebaseAuthenticationBackend(BaseBackend):
    """
    Custom authentication backend for Firebase authentication
    """
    
    def authenticate(self, request, token=None, **kwargs):
        if not token:
            return None
            
        try:
            firebase_auth = FirebaseAuthentication()
            decoded_token = firebase_auth.verify_token(token)
            
            if decoded_token:
                # Get or create user
                firebase_uid = decoded_token.get('uid')
                email = decoded_token.get('email')
                name = decoded_token.get('name', '')
                
                if not firebase_uid or not email:
                    return None
                
                # Try to get existing user by email
                try:
                    user = User.objects.get(email=email)
                    # Update Firebase UID if not set
                    if not hasattr(user, 'firebase_uid'):
                        user.firebase_uid = firebase_uid
                        user.save()
                except User.DoesNotExist:
                    # Create new user
                    username = email.split('@')[0]
                    # Ensure username is unique
                    counter = 1
                    original_username = username
                    while User.objects.filter(username=username).exists():
                        username = f"{original_username}{counter}"
                        counter += 1
                    
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=name.split(' ')[0] if name else '',
                        last_name=' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else '',
                    )
                    user.firebase_uid = firebase_uid
                    user.save()
                
                return user
                
        except Exception as e:
            logger.error(f"Firebase authentication error: {str(e)}")
            return None
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
