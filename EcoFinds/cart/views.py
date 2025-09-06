from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product
import json


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
    
    return render(request, 'cart/cart.html', context)


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


@login_required
def update_cart_item(request):
    """
    Update cart item quantity
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            
            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Cart updated',
                'cart_total': cart.total_items,
                'item_total': cart_item.total_price if quantity > 0 else 0
            })
            
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return JsonResponse({
                'success': False,
                'message': 'Item not found in cart'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error updating cart'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def clear_cart(request):
    """
    Clear all items from cart
    """
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart.clear()
            
            return JsonResponse({
                'success': True,
                'message': 'Cart cleared'
            })
            
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cart not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error clearing cart'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)