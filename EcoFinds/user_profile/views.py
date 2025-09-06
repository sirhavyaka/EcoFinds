from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from .models import UserProfile, Address, SellerProfile, Milestone, UserMilestone, Chat, Message
from products.models import Wishlist, Product
from orders.models import Order
import json


@login_required
def profile_view(request):
    """
    User profile view with product management and progress tracking
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    
    # Get user's products
    user_products = Product.objects.filter(seller=request.user).order_by('-created_at')
    
    # Get user's milestones
    user_milestones = UserMilestone.objects.filter(user=request.user)
    available_milestones = Milestone.objects.filter(
        is_active=True,
        points_required__lte=profile.points
    ).exclude(
        id__in=user_milestones.values_list('milestone_id', flat=True)
    )
    
    # Get user's chats
    user_chats = Chat.objects.filter(participants=request.user).order_by('-updated_at')
    
    context = {
        'profile': profile,
        'addresses': addresses,
        'user_products': user_products,
        'user_milestones': user_milestones,
        'available_milestones': available_milestones,
        'user_chats': user_chats,
    }
    
    return render(request, 'user_profile/profile.html', context)


@login_required
def edit_profile(request):
    """
    Edit user profile
    """
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Update profile fields
            profile.phone = data.get('phone', profile.phone)
            profile.bio = data.get('bio', profile.bio)
            profile.website = data.get('website', profile.website)
            profile.instagram = data.get('instagram', profile.instagram)
            profile.twitter = data.get('twitter', profile.twitter)
            profile.email_notifications = data.get('email_notifications', profile.email_notifications)
            profile.sms_notifications = data.get('sms_notifications', profile.sms_notifications)
            profile.newsletter_subscription = data.get('newsletter_subscription', profile.newsletter_subscription)
            
            profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error updating profile'
            }, status=500)
    
    context = {
        'profile': profile,
    }
    
    return render(request, 'user_profile/edit_profile.html', context)


@login_required
def address_list(request):
    """
    List user addresses
    """
    addresses = Address.objects.filter(user=request.user)
    
    context = {
        'addresses': addresses,
    }
    
    return render(request, 'user_profile/address_list.html', context)


@login_required
def add_address(request):
    """
    Add new address
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            address = Address.objects.create(
                user=request.user,
                address_type=data.get('address_type', 'home'),
                name=data.get('name', ''),
                phone=data.get('phone', ''),
                address_line_1=data.get('address_line_1', ''),
                address_line_2=data.get('address_line_2', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                pincode=data.get('pincode', ''),
                country=data.get('country', 'India'),
                is_default=data.get('is_default', False)
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Address added successfully',
                'address_id': address.id
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error adding address'
            }, status=500)
    
    return render(request, 'user_profile/add_address.html')


@login_required
def edit_address(request, address_id):
    """
    Edit address
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            address.address_type = data.get('address_type', address.address_type)
            address.name = data.get('name', address.name)
            address.phone = data.get('phone', address.phone)
            address.address_line_1 = data.get('address_line_1', address.address_line_1)
            address.address_line_2 = data.get('address_line_2', address.address_line_2)
            address.city = data.get('city', address.city)
            address.state = data.get('state', address.state)
            address.pincode = data.get('pincode', address.pincode)
            address.country = data.get('country', address.country)
            address.is_default = data.get('is_default', address.is_default)
            
            address.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Address updated successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error updating address'
            }, status=500)
    
    context = {
        'address': address,
    }
    
    return render(request, 'user_profile/edit_address.html', context)


@login_required
def delete_address(request, address_id):
    """
    Delete address
    """
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully')
        return redirect('user_profile:address_list')
    
    context = {
        'address': address,
    }
    
    return render(request, 'user_profile/delete_address.html', context)


@login_required
def seller_profile(request):
    """
    Seller profile view
    """
    seller_profile, created = SellerProfile.objects.get_or_create(user=request.user)
    
    context = {
        'seller_profile': seller_profile,
    }
    
    return render(request, 'user_profile/seller_profile.html', context)


@login_required
def register_seller(request):
    """
    Register as seller
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            seller_profile, created = SellerProfile.objects.get_or_create(user=request.user)
            
            seller_profile.business_name = data.get('business_name', '')
            seller_profile.business_type = data.get('business_type', 'individual')
            seller_profile.gst_number = data.get('gst_number', '')
            seller_profile.pan_number = data.get('pan_number', '')
            seller_profile.business_address = data.get('business_address', '')
            
            seller_profile.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Seller registration submitted successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error registering as seller'
            }, status=500)
    
    return render(request, 'user_profile/register_seller.html')


@login_required
def user_orders(request):
    """
    User orders list
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'user_profile/user_orders.html', context)


@login_required
def wishlist_view(request):
    """
    User wishlist
    """
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'user_profile/wishlist.html', context)


@login_required
def delete_product(request, product_id):
    """
    Delete user's product
    """
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('user_profile:profile_view')
    
    context = {
        'product': product,
    }
    
    return render(request, 'user_profile/delete_product.html', context)


@login_required
def claim_milestone(request, milestone_id):
    """
    Claim a milestone reward
    """
    milestone = get_object_or_404(Milestone, id=milestone_id, is_active=True)
    profile = request.user.profile
    
    if profile.points >= milestone.points_required:
        user_milestone, created = UserMilestone.objects.get_or_create(
            user=request.user,
            milestone=milestone
        )
        
        if created:
            messages.success(request, f'Milestone "{milestone.name}" claimed successfully!')
        else:
            messages.info(request, 'Milestone already claimed')
    else:
        messages.error(request, 'Insufficient points to claim this milestone')
    
    return redirect('user_profile:profile_view')


# Chat Views
@login_required
def start_chat(request, user_id, product_id=None):
    """
    Start a chat with another user
    """
    other_user = get_object_or_404(User, id=user_id)
    
    if other_user == request.user:
        messages.error(request, 'Cannot start chat with yourself')
        return redirect('user_profile:profile_view')
    
    # Check if chat already exists
    existing_chat = Chat.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_chat:
        return redirect('user_profile:chat_detail', chat_id=existing_chat.id)
    
    # Create new chat
    chat = Chat.objects.create()
    chat.participants.add(request.user, other_user)
    
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            chat.product = product
            chat.save()
        except Product.DoesNotExist:
            pass
    
    return redirect('user_profile:chat_detail', chat_id=chat.id)


@login_required
def chat_list(request):
    """
    List all user's chats
    """
    chats = Chat.objects.filter(participants=request.user).order_by('-updated_at')
    
    context = {
        'chats': chats,
    }
    
    return render(request, 'user_profile/chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    """
    Chat detail view
    """
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages_list = Message.objects.filter(chat=chat).order_by('created_at')
    
    # Mark messages as read
    Message.objects.filter(chat=chat, sender__in=chat.participants.exclude(id=request.user.id)).update(is_read=True)
    
    context = {
        'chat': chat,
        'messages': messages_list,
        'other_user': chat.participants.exclude(id=request.user.id).first(),
    }
    
    return render(request, 'user_profile/chat_detail.html', context)


@login_required
def send_message(request, chat_id):
    """
    Send a message in chat
    """
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
            
            if content:
                message = Message.objects.create(
                    chat=chat,
                    sender=request.user,
                    content=content
                )
                
                # Update chat timestamp
                chat.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Message sent successfully',
                    'message_id': message.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Message content cannot be empty'
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error sending message'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)