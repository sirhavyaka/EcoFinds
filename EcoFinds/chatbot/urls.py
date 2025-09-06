from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('history/', views.chat_history, name='chat_history'),
]
