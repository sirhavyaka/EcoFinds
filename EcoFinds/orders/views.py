from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Order, OrderItem, OrderTracking, Refund
from cart.models import Cart, CartItem
from products.models import Product
import json
import uuid


@login_required
def order_list(request):
    """
    List user orders
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_list.html', context)


@login_required
def create_order(request):
    """
    Create new order from cart
    """
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            
            if not cart_items.exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Cart is empty'
                }, status=400)
            
            # Get shipping address from request
            data = json.loads(request.body)
            shipping_data = data.get('shipping', {})
            payment_method = data.get('payment_method', 'cash_on_delivery')
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                payment_method=payment_method,
                subtotal=cart.total_price,
                total_amount=cart.total_price,  # Add shipping cost if needed
                shipping_name=shipping_data.get('name', ''),
                shipping_phone=shipping_data.get('phone', ''),
                shipping_address=shipping_data.get('address', ''),
                shipping_city=shipping_data.get('city', ''),
                shipping_state=shipping_data.get('state', ''),
                shipping_pincode=shipping_data.get('pincode', ''),
                shipping_country=shipping_data.get('country', 'India'),
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear cart
            cart.clear()
            
            return JsonResponse({
                'success': True,
                'message': 'Order created successfully',
                'order_id': order.id,
                'order_number': order.order_number
            })
            
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cart not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error creating order'
            }, status=500)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
def order_detail(request, order_id):
    """
    Order detail view
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    tracking = order.tracking.all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'tracking': tracking,
    }
    
    return render(request, 'orders/order_detail.html', context)


@login_required
def cancel_order(request, order_id):
    """
    Cancel order
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            
            # Add tracking entry
            OrderTracking.objects.create(
                order=order,
                status='cancelled',
                description='Order cancelled by customer'
            )
            
            messages.success(request, 'Order cancelled successfully')
        else:
            messages.error(request, 'Cannot cancel this order')
        
        return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/cancel_order.html', context)


@login_required
def track_order(request, order_id):
    """
    Track order
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    tracking = order.tracking.all()
    
    context = {
        'order': order,
        'tracking': tracking,
    }
    
    return render(request, 'orders/track_order.html', context)


@login_required
def request_refund(request, order_id):
    """
    Request refund for order
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reason = data.get('reason', '')
            
            # Check if refund already exists
            if hasattr(order, 'refund'):
                return JsonResponse({
                    'success': False,
                    'message': 'Refund request already exists'
                })
            
            # Create refund request
            refund = Refund.objects.create(
                order=order,
                reason=reason,
                amount=order.total_amount
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Refund request submitted successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error submitting refund request'
            }, status=500)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/request_refund.html', context)