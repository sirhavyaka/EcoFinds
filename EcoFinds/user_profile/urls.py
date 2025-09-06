from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile_view, name='profile_view'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/add/', views.add_address, name='add_address'),
    path('addresses/<int:address_id>/edit/', views.edit_address, name='edit_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address, name='delete_address'),
    path('seller/', views.seller_profile, name='seller_profile'),
    path('seller/register/', views.register_seller, name='register_seller'),
    path('orders/', views.user_orders, name='user_orders'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    
    # Product Management
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    
    # Milestones
    path('milestones/<int:milestone_id>/claim/', views.claim_milestone, name='claim_milestone'),
    
    # Chat
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
    path('chat/start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('chat/start/<int:user_id>/product/<int:product_id>/', views.start_chat, name='start_chat_with_product'),
]
