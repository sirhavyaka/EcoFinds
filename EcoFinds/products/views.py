from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Product, Category, ProductReview, Wishlist
import json


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
    
    return render(request, 'products/product_list.html', context)


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
        
        # Get reviews
        reviews = ProductReview.objects.filter(product=product)
        
        context = {
            'product': product,
            'related_products': related_products,
            'reviews': reviews,
        }
        
        return render(request, 'products/product_detail.html', context)
    except Product.DoesNotExist:
        return render(request, 'products/404.html', status=404)


def category_products(request, slug):
    """
    Products filtered by category
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status='available')
    
    context = {
        'category': category,
        'products': products,
    }
    
    return render(request, 'products/category_products.html', context)


def search_products(request):
    """
    Search products
    """
    query = request.GET.get('q', '')
    products = Product.objects.filter(status='available')
    
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query)
        )
    
    context = {
        'products': products,
        'query': query,
    }
    
    return render(request, 'products/search_results.html', context)


@login_required
def create_product(request):
    """
    Create new product
    """
    if request.method == 'POST':
        # Handle product creation
        pass
    
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    
    return render(request, 'products/create_product.html', context)


@login_required
def edit_product(request, product_id):
    """
    Edit product
    """
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        # Handle product update
        pass
    
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
    }
    
    return render(request, 'products/edit_product.html', context)


@login_required
def delete_product(request, product_id):
    """
    Delete product
    """
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/delete_product.html', context)


@login_required
def add_review(request, product_id):
    """
    Add product review
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = data.get('rating')
            title = data.get('title')
            comment = data.get('comment')
            
            # Create or update review
            review, created = ProductReview.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': rating,
                    'title': title,
                    'comment': comment
                }
            )
            
            if not created:
                review.rating = rating
                review.title = title
                review.comment = comment
                review.save()
            
            return JsonResponse({'success': True, 'message': 'Review added successfully'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error adding review'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def toggle_wishlist(request, product_id):
    """
    Add/remove product from wishlist
    """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        try:
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if not created:
                wishlist_item.delete()
                return JsonResponse({'success': True, 'message': 'Removed from wishlist', 'in_wishlist': False})
            else:
                return JsonResponse({'success': True, 'message': 'Added to wishlist', 'in_wishlist': True})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error updating wishlist'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})