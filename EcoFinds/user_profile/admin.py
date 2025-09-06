from django.contrib import admin
from .models import UserProfile, Address, SellerProfile, Milestone, UserMilestone, Chat, Message


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'level', 'total_products_sold', 'total_products_listed']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city', 'state', 'is_default']
    list_filter = ['address_type', 'is_default', 'state']
    search_fields = ['user__username', 'name', 'city']


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'business_type', 'is_verified', 'rating']
    list_filter = ['business_type', 'is_verified']
    search_fields = ['user__username', 'business_name']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_required', 'reward_type', 'is_active']
    list_filter = ['reward_type', 'is_active']
    search_fields = ['name', 'description']


@admin.register(UserMilestone)
class UserMilestoneAdmin(admin.ModelAdmin):
    list_display = ['user', 'milestone', 'achieved_at', 'is_claimed']
    list_filter = ['is_claimed', 'achieved_at']
    search_fields = ['user__username', 'milestone__name']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['participants__username', 'product__title']
    
    def get_participants(self, obj):
        return ', '.join([p.username for p in obj.participants.all()])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender', 'content', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['sender__username', 'content']
