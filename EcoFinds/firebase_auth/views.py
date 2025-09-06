from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .firebase_auth import FirebaseAuthentication
import json
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_login(request):
    """
    API endpoint for Firebase authentication
    """
    try:
        data = request.data
        id_token = data.get('idToken')
        
        if not id_token:
            return Response(
                {'error': 'ID token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        firebase_auth = FirebaseAuthentication()
        decoded_token = firebase_auth.verify_token(id_token)
        
        if not decoded_token:
            return Response(
                {'error': 'Invalid Firebase token'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Get user info from token
        firebase_uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')
        
        # Get or create Django user
        from django.contrib.auth.models import User
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Create new user
            username = email.split('@')[0]
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
        
        # Login the user
        login(request, user)
        
        return Response({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
        
    except Exception as e:
        logger.error(f"Firebase login error: {str(e)}")
        return Response(
            {'error': 'Authentication failed'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def firebase_logout(request):
    """
    API endpoint for logout
    """
    try:
        logout(request)
        return Response({'success': True})
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return Response(
            {'error': 'Logout failed'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_user_info(request):
    """
    Get current user information
    """
    if request.user.is_authenticated:
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_authenticated': True,
            }
        })
    else:
        return Response({
            'user': {
                'is_authenticated': False,
            }
        })


def login_page(request):
    """
    Render login page
    """
    return render(request, 'auth/login.html')


def register_page(request):
    """
    Render registration page
    """
    return render(request, 'auth/register.html')


@login_required
def profile_page(request):
    """
    Render user profile page
    """
    return render(request, 'auth/profile.html')