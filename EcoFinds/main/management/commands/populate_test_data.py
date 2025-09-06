from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify
from products.models import Product, Category, ProductImage
from user_profile.models import UserProfile
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate database with test data - 10 users with 2 products each'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')
        
        # Create categories first
        categories = self.create_categories()
        
        # Create 10 test users
        users = self.create_test_users()
        
        # Create 2 products for each user
        self.create_test_products(users, categories)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created test data!')
        )

    def create_categories(self):
        """Create product categories"""
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and garden items'},
            {'name': 'Sports & Fitness', 'description': 'Sports equipment and fitness gear'},
            {'name': 'Toys & Games', 'description': 'Toys, games, and entertainment'},
            {'name': 'Furniture', 'description': 'Furniture and home decor'},
            {'name': 'Automotive', 'description': 'Car parts and automotive accessories'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': slugify(cat_data['name'])
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        return categories

    def create_test_users(self):
        """Create 10 test users with profiles"""
        users_data = [
            {
                'username': 'alice_smith',
                'email': 'alice.smith@email.com',
                'first_name': 'Alice',
                'last_name': 'Smith',
                'phone': '+1-555-0101',
                'address': '123 Oak Street, Springfield, IL 62701',
                'bio': 'Love finding unique second-hand items and giving them new life!'
            },
            {
                'username': 'bob_johnson',
                'email': 'bob.johnson@email.com',
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'phone': '+1-555-0102',
                'address': '456 Pine Avenue, Chicago, IL 60601',
                'bio': 'Tech enthusiast selling quality electronics at great prices.'
            },
            {
                'username': 'carol_williams',
                'email': 'carol.williams@email.com',
                'first_name': 'Carol',
                'last_name': 'Williams',
                'phone': '+1-555-0103',
                'address': '789 Maple Drive, Rockford, IL 61101',
                'bio': 'Fashion lover with a passion for sustainable clothing.'
            },
            {
                'username': 'david_brown',
                'email': 'david.brown@email.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'phone': '+1-555-0104',
                'address': '321 Elm Street, Peoria, IL 61602',
                'bio': 'Book collector and avid reader sharing my collection.'
            },
            {
                'username': 'emma_davis',
                'email': 'emma.davis@email.com',
                'first_name': 'Emma',
                'last_name': 'Davis',
                'phone': '+1-555-0105',
                'address': '654 Cedar Lane, Aurora, IL 60502',
                'bio': 'Home decor enthusiast with unique vintage finds.'
            },
            {
                'username': 'frank_miller',
                'email': 'frank.miller@email.com',
                'first_name': 'Frank',
                'last_name': 'Miller',
                'phone': '+1-555-0106',
                'address': '987 Birch Road, Naperville, IL 60540',
                'bio': 'Sports equipment dealer with quality gear for all activities.'
            },
            {
                'username': 'grace_wilson',
                'email': 'grace.wilson@email.com',
                'first_name': 'Grace',
                'last_name': 'Wilson',
                'phone': '+1-555-0107',
                'address': '147 Spruce Court, Joliet, IL 60435',
                'bio': 'Toy collector and parent selling gently used children\'s items.'
            },
            {
                'username': 'henry_moore',
                'email': 'henry.moore@email.com',
                'first_name': 'Henry',
                'last_name': 'Moore',
                'phone': '+1-555-0108',
                'address': '258 Walnut Street, Elgin, IL 60120',
                'bio': 'Furniture restorer specializing in antique and vintage pieces.'
            },
            {
                'username': 'ivy_taylor',
                'email': 'ivy.taylor@email.com',
                'first_name': 'Ivy',
                'last_name': 'Taylor',
                'phone': '+1-555-0109',
                'address': '369 Cherry Avenue, Waukegan, IL 60085',
                'bio': 'Automotive enthusiast with quality car parts and accessories.'
            },
            {
                'username': 'jack_anderson',
                'email': 'jack.anderson@email.com',
                'first_name': 'Jack',
                'last_name': 'Anderson',
                'phone': '+1-555-0110',
                'address': '741 Ash Boulevard, Cicero, IL 60804',
                'bio': 'General collector with diverse items from electronics to books.'
            }
        ]
        
        users = []
        for user_data in users_data:
            # Create user
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            if created:
                user.set_password('testpass123')  # Set a default password
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            
            # Create user profile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': user_data['phone'],
                    'address': user_data['address'],
                    'city': user_data['address'].split(',')[1].strip(),
                    'state': user_data['address'].split(',')[2].strip(),
                    'bio': user_data['bio'],
                    'gender': random.choice(['male', 'female', 'other']),
                    'date_of_birth': f'19{random.randint(70, 90)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}',
                }
            )
            
            if profile_created:
                self.stdout.write(f'Created profile for: {user.username}')
            
            users.append(user)
        
        return users

    def create_test_products(self, users, categories):
        """Create 2 products for each user"""
        products_data = [
            # Alice Smith's products
            {
                'title': 'Vintage MacBook Pro 13" (2015)',
                'description': 'Excellent condition MacBook Pro with 8GB RAM, 256GB SSD. Perfect for students or professionals. Includes original charger and case.',
                'price': Decimal('450.00'),
                'condition': 'Good',
                'category': 'Electronics',
                'images': ['laptop1.jpg', 'laptop2.jpg']
            },
            {
                'title': 'Designer Handbag - Coach Leather',
                'description': 'Authentic Coach leather handbag in brown. Shows minimal wear, perfect for daily use. Comes with authenticity card.',
                'price': Decimal('120.00'),
                'condition': 'Good',
                'category': 'Clothing',
                'images': ['handbag1.jpg', 'handbag2.jpg']
            },
            # Bob Johnson's products
            {
                'title': 'iPhone 12 Pro - 128GB',
                'description': 'iPhone 12 Pro in excellent condition. Battery health 95%. Includes original box, charger, and screen protector.',
                'price': Decimal('650.00'),
                'condition': 'Excellent',
                'category': 'Electronics',
                'images': ['iphone1.jpg', 'iphone2.jpg']
            },
            {
                'title': 'Gaming Headset - SteelSeries Arctis 7',
                'description': 'Wireless gaming headset with excellent sound quality. Used for 6 months, in great condition. Includes all accessories.',
                'price': Decimal('80.00'),
                'condition': 'Good',
                'category': 'Electronics',
                'images': ['headset1.jpg', 'headset2.jpg']
            },
            # Carol Williams' products
            {
                'title': 'Vintage Denim Jacket - Levi\'s',
                'description': 'Classic Levi\'s denim jacket from the 90s. Size M, perfect fit. Shows authentic vintage wear. One of a kind piece.',
                'price': Decimal('75.00'),
                'condition': 'Fair',
                'category': 'Clothing',
                'images': ['jacket1.jpg', 'jacket2.jpg']
            },
            {
                'title': 'Designer Sunglasses - Ray-Ban Aviators',
                'description': 'Authentic Ray-Ban aviator sunglasses in gold frame. Includes original case and cleaning cloth. Perfect condition.',
                'price': Decimal('90.00'),
                'condition': 'Excellent',
                'category': 'Clothing',
                'images': ['sunglasses1.jpg', 'sunglasses2.jpg']
            },
            # David Brown's products
            {
                'title': 'Complete Harry Potter Book Set',
                'description': 'All 7 Harry Potter books in hardcover. First edition prints in excellent condition. Perfect for collectors or new readers.',
                'price': Decimal('150.00'),
                'condition': 'Excellent',
                'category': 'Books',
                'images': ['harrypotter1.jpg', 'harrypotter2.jpg']
            },
            {
                'title': 'Programming Books Collection',
                'description': 'Collection of programming books including Python, JavaScript, and React. All in good condition, perfect for developers.',
                'price': Decimal('60.00'),
                'condition': 'Good',
                'category': 'Books',
                'images': ['programming1.jpg', 'programming2.jpg']
            },
            # Emma Davis' products
            {
                'title': 'Vintage Wooden Coffee Table',
                'description': 'Beautiful vintage wooden coffee table with intricate carvings. Perfect for living room. Shows character and history.',
                'price': Decimal('200.00'),
                'condition': 'Good',
                'category': 'Furniture',
                'images': ['table1.jpg', 'table2.jpg']
            },
            {
                'title': 'Antique Brass Floor Lamp',
                'description': 'Stunning antique brass floor lamp with fabric shade. Adds elegance to any room. Fully functional with new wiring.',
                'price': Decimal('120.00'),
                'condition': 'Good',
                'category': 'Furniture',
                'images': ['lamp1.jpg', 'lamp2.jpg']
            },
            # Frank Miller's products
            {
                'title': 'Mountain Bike - Trek 820',
                'description': 'Trek 820 mountain bike in excellent condition. Recently serviced, new tires. Perfect for trails and commuting.',
                'price': Decimal('300.00'),
                'condition': 'Excellent',
                'category': 'Sports & Fitness',
                'images': ['bike1.jpg', 'bike2.jpg']
            },
            {
                'title': 'Weight Set - 100lbs Total',
                'description': 'Complete weight set with barbell and plates. Great for home gym. All weights in good condition, no rust.',
                'price': Decimal('150.00'),
                'condition': 'Good',
                'category': 'Sports & Fitness',
                'images': ['weights1.jpg', 'weights2.jpg']
            },
            # Grace Wilson's products
            {
                'title': 'LEGO Creator Set - Modular Building',
                'description': 'Complete LEGO Creator modular building set. All pieces included with instructions. Perfect for collectors or builders.',
                'price': Decimal('80.00'),
                'condition': 'Excellent',
                'category': 'Toys & Games',
                'images': ['lego1.jpg', 'lego2.jpg']
            },
            {
                'title': 'Board Game Collection - 5 Games',
                'description': 'Collection of 5 popular board games including Monopoly, Scrabble, and Risk. All complete with instructions.',
                'price': Decimal('45.00'),
                'condition': 'Good',
                'category': 'Toys & Games',
                'images': ['boardgames1.jpg', 'boardgames2.jpg']
            },
            # Henry Moore's products
            {
                'title': 'Antique Oak Dining Table',
                'description': 'Beautiful antique oak dining table seats 6. Shows beautiful patina and character. Perfect for family dinners.',
                'price': Decimal('400.00'),
                'condition': 'Good',
                'category': 'Furniture',
                'images': ['diningtable1.jpg', 'diningtable2.jpg']
            },
            {
                'title': 'Vintage Wooden Bookshelf',
                'description': 'Solid wood bookshelf with 5 shelves. Perfect for home office or living room. Shows minimal wear.',
                'price': Decimal('120.00'),
                'condition': 'Good',
                'category': 'Furniture',
                'images': ['bookshelf1.jpg', 'bookshelf2.jpg']
            },
            # Ivy Taylor's products
            {
                'title': 'Car Audio System - Pioneer',
                'description': 'Complete Pioneer car audio system with speakers, subwoofer, and amplifier. Perfect for car enthusiasts.',
                'price': Decimal('250.00'),
                'condition': 'Good',
                'category': 'Automotive',
                'images': ['caraudio1.jpg', 'caraudio2.jpg']
            },
            {
                'title': 'Car Tires - Michelin 4 New',
                'description': 'Set of 4 new Michelin tires, size 205/55R16. Never used, still have tags. Perfect for Honda Civic or similar.',
                'price': Decimal('300.00'),
                'condition': 'Excellent',
                'category': 'Automotive',
                'images': ['tires1.jpg', 'tires2.jpg']
            },
            # Jack Anderson's products
            {
                'title': 'Garden Tools Set - Complete',
                'description': 'Complete set of garden tools including shovel, rake, hoe, and pruners. All in good condition, perfect for gardening.',
                'price': Decimal('75.00'),
                'condition': 'Good',
                'category': 'Home & Garden',
                'images': ['gardentools1.jpg', 'gardentools2.jpg']
            },
            {
                'title': 'Kitchen Appliances Bundle',
                'description': 'Bundle of kitchen appliances including toaster, blender, and coffee maker. All working perfectly, great value.',
                'price': Decimal('100.00'),
                'condition': 'Good',
                'category': 'Home & Garden',
                'images': ['kitchen1.jpg', 'kitchen2.jpg']
            }
        ]
        
        for i, user in enumerate(users):
            for j in range(2):  # 2 products per user
                product_data = products_data[i * 2 + j]
                
                # Get category
                category = next(cat for cat in categories if cat.name == product_data['category'])
                
                # Create product
                product = Product.objects.create(
                    title=product_data['title'],
                    description=product_data['description'],
                    price=product_data['price'],
                    condition=product_data['condition'],
                    category=category,
                    seller=user,
                    status='available',
                    city=user.profile.city or "Springfield",
                    state=user.profile.state or "IL",
                    slug=slugify(product_data['title'])
                )
                
                # Create placeholder images
                for img_name in product_data['images']:
                    # Create a simple placeholder image content
                    image_content = ContentFile(
                        b'placeholder_image_data',
                        name=img_name
                    )
                    ProductImage.objects.create(
                        product=product,
                        image=image_content,
                        is_primary=(img_name == product_data['images'][0])
                    )
                
                self.stdout.write(f'Created product: {product.title} for {user.username}')
        
        self.stdout.write(f'Created {len(products_data)} products total!')
