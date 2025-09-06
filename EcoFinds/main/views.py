from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product, Category
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json


def home(request):
    """
    Home page view
    """
    # Get featured products
    featured_products = Product.objects.filter(
        is_featured=True, 
        status='available'
    )[:8]
    
    # Get latest products
    latest_products = Product.objects.filter(
        status='available'
    ).order_by('-created_at')[:8]
    
    # Get categories
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    }
    
    return render(request, 'main/home.html', context)


def product_list(request):
    """
    Product listing page
    """
    products = Product.objects.filter(status='available')
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            pass
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Filter by condition
    condition = request.GET.get('condition')
    if condition:
        products = products.filter(condition=condition)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sort products
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'oldest':
        products = products.order_by('created_at')
    else:  # newest
        products = products.order_by('-created_at')
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'condition': condition,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    
    return render(request, 'main/product_list.html', context)


def product_detail(request, slug):
    """
    Product detail page
    """
    try:
        product = Product.objects.get(slug=slug, status='available')
        related_products = Product.objects.filter(
            category=product.category,
            status='available'
        ).exclude(id=product.id)[:4]
        
        context = {
            'product': product,
            'related_products': related_products,
        }
        
        return render(request, 'main/product_detail.html', context)
    except Product.DoesNotExist:
        return render(request, 'main/404.html', status=404)


@login_required
def cart_view(request):
    """
    Shopping cart view
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    
    return render(request, 'main/cart.html', context)


@login_required
def add_to_cart(request):
    """
    Add product to cart
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = Product.objects.get(id=product_id, status='available')
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart',
                'cart_total': cart.total_items
            })
            
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error adding product to cart'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request):
    """
    Remove product from cart
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Product removed from cart',
                'cart_total': cart.total_items
            })
            
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return JsonResponse({
                'success': False,
                'message': 'Item not found in cart'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error removing product from cart'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def about(request):
    """
    About page
    """
    return render(request, 'main/about.html')


def contact(request):
    """
    Contact page
    """
    return render(request, 'main/contact.html')