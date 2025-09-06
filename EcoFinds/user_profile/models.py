from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ], blank=True)
    
    # Address Information
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')
    
    # Profile Information
    bio = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    # Social Media Links
    website = models.URLField(blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    newsletter_subscription = models.BooleanField(default=True)
    
    # Points and Rewards System
    points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    total_products_sold = models.PositiveIntegerField(default=0)
    total_products_listed = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    @property
    def points_to_next_level(self):
        """Calculate points needed for next level"""
        level_thresholds = {
            1: 100, 2: 250, 3: 500, 4: 1000, 5: 2000, 
            6: 3500, 7: 5000, 8: 7500, 9: 10000, 10: 15000
        }
        next_level = self.level + 1
        if next_level in level_thresholds:
            return level_thresholds[next_level] - self.points
        return 0
    
    @property
    def current_level_progress(self):
        """Calculate progress percentage for current level"""
        level_thresholds = {
            1: 100, 2: 250, 3: 500, 4: 1000, 5: 2000, 
            6: 3500, 7: 5000, 8: 7500, 9: 10000, 10: 15000
        }
        current_threshold = level_thresholds.get(self.level, 0)
        previous_threshold = level_thresholds.get(self.level - 1, 0)
        
        if current_threshold > previous_threshold:
            progress = ((self.points - previous_threshold) / (current_threshold - previous_threshold)) * 100
            return min(100, max(0, progress))
        return 0
    
    def add_points(self, points):
        """Add points and check for level up"""
        self.points += points
        self.check_level_up()
        self.save()
    
    def check_level_up(self):
        """Check if user should level up"""
        level_thresholds = {
            1: 100, 2: 250, 3: 500, 4: 1000, 5: 2000, 
            6: 3500, 7: 5000, 8: 7500, 9: 10000, 10: 15000
        }
        
        for level, threshold in level_thresholds.items():
            if self.points >= threshold and level > self.level:
                self.level = level


class Milestone(models.Model):
    """Milestone rewards for users"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.PositiveIntegerField()
    reward_type = models.CharField(max_length=50, choices=[
        ('badge', 'Badge'),
        ('discount', 'Discount'),
        ('feature', 'Special Feature'),
        ('title', 'Title'),
    ])
    reward_value = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=50, default='fas fa-trophy')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['points_required']


class UserMilestone(models.Model):
    """User's achieved milestones"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milestones')
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'milestone']
        ordering = ['-achieved_at']

    def __str__(self):
        return f"{self.user.username} - {self.milestone.name}"


class Chat(models.Model):
    """Chat between two users"""
    participants = models.ManyToManyField(User, related_name='chats')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat between {', '.join([p.username for p in self.participants.all()])}"

    @property
    def other_participant(self, user):
        """Get the other participant in the chat"""
        return self.participants.exclude(id=user.id).first()

    @property
    def last_message(self):
        """Get the last message in the chat"""
        return self.messages.last()


class Message(models.Model):
    """Individual messages in a chat"""
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='home')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}, {self.state}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Ensure only one default address per user
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    
    # Business Information
    business_name = models.CharField(max_length=200, blank=True)
    business_type = models.CharField(max_length=50, choices=[
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('organization', 'Organization'),
    ], default='individual')
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_documents = models.JSONField(default=dict, blank=True)
    
    # Business Details
    gst_number = models.CharField(max_length=15, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    business_address = models.TextField(blank=True)
    
    # Performance Metrics
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_orders = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Seller Profile"

    @property
    def average_rating(self):
        if self.total_reviews > 0:
            return round(self.rating / self.total_reviews, 2)
        return 0


# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=UserProfile)
def check_milestones(sender, instance, **kwargs):
    """Automatically award milestones when user reaches point thresholds"""
    if kwargs.get('created', False):
        return  # Don't check on creation
    
    # Get all milestones the user hasn't achieved yet
    achieved_milestones = UserMilestone.objects.filter(user=instance.user).values_list('milestone_id', flat=True)
    available_milestones = Milestone.objects.filter(
        is_active=True,
        points_required__lte=instance.points
    ).exclude(id__in=achieved_milestones)
    
    # Award new milestones
    for milestone in available_milestones:
        UserMilestone.objects.create(
            user=instance.user,
            milestone=milestone
        )