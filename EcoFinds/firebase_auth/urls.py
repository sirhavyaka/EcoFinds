from django.urls import path
from . import views

app_name = 'firebase_auth'

urlpatterns = [
    # API endpoints
    path('api/login/', views.firebase_login, name='firebase_login'),
    path('api/logout/', views.firebase_logout, name='firebase_logout'),
    path('api/user/', views.get_user_info, name='get_user_info'),
    
    # Page views
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
]
