from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('search/', views.search_products, name='search_products'),
    path('create/', views.create_product, name='create_product'),
    path('<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('<int:product_id>/review/', views.add_review, name='add_review'),
    path('<int:product_id>/wishlist/', views.toggle_wishlist, name='toggle_wishlist'),
]
