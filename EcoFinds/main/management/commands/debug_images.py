from django.core.management.base import BaseCommand
from products.models import Product, ProductImage

class Command(BaseCommand):
    help = 'Debug product images'

    def handle(self, *args, **options):
        products = Product.objects.all()
        
        self.stdout.write(f"Total products: {products.count()}")
        
        for product in products:
            images = product.images.all()
            self.stdout.write(f"\nProduct: {product.title} (ID: {product.id})")
            self.stdout.write(f"  Images: {images.count()}")
            
            for i, image in enumerate(images):
                self.stdout.write(f"    Image {i+1}: {image.image.name} (Primary: {image.is_primary})")
                self.stdout.write(f"      URL: {image.image.url}")
                self.stdout.write(f"      Path: {image.image.path}")
                
                # Check if file exists
                import os
                if os.path.exists(image.image.path):
                    self.stdout.write(f"      File exists: YES")
                else:
                    self.stdout.write(f"      File exists: NO")
