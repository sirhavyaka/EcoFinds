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
]
