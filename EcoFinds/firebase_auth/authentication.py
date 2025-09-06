from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from .firebase_auth import FirebaseAuthentication
import logging

logger = logging.getLogger(__name__)


class FirebaseAuthentication(BaseAuthentication):
    """
    Custom authentication class for Django REST Framework using Firebase
    """
    
    def authenticate(self, request):
        """
        Authenticate the request using Firebase token
        """
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
        
        try:
            # Extract token from "Bearer <token>" format
            scheme, token = auth_header.split(' ', 1)
            if scheme.lower() != 'bearer':
                return None
        except ValueError:
            return None
        
        try:
            firebase_auth = FirebaseAuthentication()
            decoded_token = firebase_auth.verify_token(token)
            
            if not decoded_token:
                raise AuthenticationFailed('Invalid Firebase token')
            
            # Get or create user
            firebase_uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            name = decoded_token.get('name', '')
            
            if not firebase_uid or not email:
                raise AuthenticationFailed('Invalid token data')
            
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
            
            return (user, token)
            
        except Exception as e:
            logger.error(f"Firebase authentication error: {str(e)}")
            raise AuthenticationFailed('Authentication failed')
    
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response.
        """
        return 'Bearer'
