from django.core.management.base import BaseCommand
from user_profile.models import Milestone


class Command(BaseCommand):
    help = 'Populate default milestones for the points system'

    def handle(self, *args, **options):
        milestones_data = [
            {
                'name': 'First Steps',
                'description': 'List your first product on EcoFinds',
                'points_required': 10,
                'reward_type': 'badge',
                'reward_value': 'New Seller Badge',
                'icon': 'fas fa-seedling'
            },
            {
                'name': 'Getting Started',
                'description': 'Reach 100 points by selling products',
                'points_required': 100,
                'reward_type': 'badge',
                'reward_value': 'Bronze Seller Badge',
                'icon': 'fas fa-medal'
            },
            {
                'name': 'Rising Star',
                'description': 'Reach 250 points and level up',
                'points_required': 250,
                'reward_type': 'discount',
                'reward_value': '5% listing fee discount',
                'icon': 'fas fa-star'
            },
            {
                'name': 'Active Seller',
                'description': 'Reach 500 points with consistent selling',
                'points_required': 500,
                'reward_type': 'badge',
                'reward_value': 'Silver Seller Badge',
                'icon': 'fas fa-award'
            },
            {
                'name': 'Eco Champion',
                'description': 'Reach 1000 points and become an eco champion',
                'points_required': 1000,
                'reward_type': 'feature',
                'reward_value': 'Featured listing priority',
                'icon': 'fas fa-leaf'
            },
            {
                'name': 'Top Seller',
                'description': 'Reach 2000 points and join the top sellers',
                'points_required': 2000,
                'reward_type': 'discount',
                'reward_value': '10% listing fee discount',
                'icon': 'fas fa-crown'
            },
            {
                'name': 'EcoFinds Expert',
                'description': 'Reach 3500 points and become an expert',
                'points_required': 3500,
                'reward_type': 'title',
                'reward_value': 'Expert Seller Title',
                'icon': 'fas fa-graduation-cap'
            },
            {
                'name': 'Marketplace Master',
                'description': 'Reach 5000 points and master the marketplace',
                'points_required': 5000,
                'reward_type': 'feature',
                'reward_value': 'Premium seller dashboard',
                'icon': 'fas fa-trophy'
            },
            {
                'name': 'EcoFinds Legend',
                'description': 'Reach 7500 points and become a legend',
                'points_required': 7500,
                'reward_type': 'title',
                'reward_value': 'Legendary Seller Title',
                'icon': 'fas fa-fire'
            },
            {
                'name': 'Ultimate EcoFinds',
                'description': 'Reach 10000 points and achieve ultimate status',
                'points_required': 10000,
                'reward_type': 'feature',
                'reward_value': 'Free premium features for life',
                'icon': 'fas fa-gem'
            },
            {
                'name': 'EcoFinds Hall of Fame',
                'description': 'Reach 15000 points and enter the hall of fame',
                'points_required': 15000,
                'reward_type': 'title',
                'reward_value': 'Hall of Fame Member',
                'icon': 'fas fa-star-of-life'
            }
        ]

        created_count = 0
        for milestone_data in milestones_data:
            milestone, created = Milestone.objects.get_or_create(
                name=milestone_data['name'],
                defaults=milestone_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created milestone: {milestone.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Milestone already exists: {milestone.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new milestones')
        )
