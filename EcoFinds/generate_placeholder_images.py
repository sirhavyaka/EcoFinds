"""
Script to generate placeholder images for products
Run this script to create placeholder images in the media/products folder
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(text, filename, width=400, height=300):
    """Create a placeholder image with text"""
    # Create image with light gray background
    img = Image.new('RGB', (width, height), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Wrap text to fit image
    wrapped_text = textwrap.fill(text, width=20)
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text
    draw.text((x, y), wrapped_text, fill='#333333', font=font)
    
    # Add filename at bottom
    filename_text = f"Image: {filename}"
    bbox_small = draw.textbbox((0, 0), filename_text, font=small_font)
    small_width = bbox_small[2] - bbox_small[0]
    small_x = (width - small_width) // 2
    small_y = height - 30
    
    draw.text((small_x, small_y), filename_text, fill='#666666', font=small_font)
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

def main():
    """Generate all placeholder images"""
    # Ensure media/products directory exists
    os.makedirs('media/products', exist_ok=True)
    
    # List of all product images needed
    images = [
        'laptop1.jpg', 'laptop2.jpg',
        'handbag1.jpg', 'handbag2.jpg',
        'iphone1.jpg', 'iphone2.jpg',
        'headset1.jpg', 'headset2.jpg',
        'jacket1.jpg', 'jacket2.jpg',
        'sunglasses1.jpg', 'sunglasses2.jpg',
        'harrypotter1.jpg', 'harrypotter2.jpg',
        'programming1.jpg', 'programming2.jpg',
        'table1.jpg', 'table2.jpg',
        'lamp1.jpg', 'lamp2.jpg',
        'bike1.jpg', 'bike2.jpg',
        'weights1.jpg', 'weights2.jpg',
        'lego1.jpg', 'lego2.jpg',
        'boardgames1.jpg', 'boardgames2.jpg',
        'diningtable1.jpg', 'diningtable2.jpg',
        'bookshelf1.jpg', 'bookshelf2.jpg',
        'caraudio1.jpg', 'caraudio2.jpg',
        'tires1.jpg', 'tires2.jpg',
        'gardentools1.jpg', 'gardentools2.jpg',
        'kitchen1.jpg', 'kitchen2.jpg'
    ]
    
    # Product descriptions for each image
    descriptions = {
        'laptop1.jpg': 'MacBook Pro 13" - Front View',
        'laptop2.jpg': 'MacBook Pro 13" - Side View',
        'handbag1.jpg': 'Coach Handbag - Front',
        'handbag2.jpg': 'Coach Handbag - Interior',
        'iphone1.jpg': 'iPhone 12 Pro - Front',
        'iphone2.jpg': 'iPhone 12 Pro - Back',
        'headset1.jpg': 'SteelSeries Headset - Front',
        'headset2.jpg': 'SteelSeries Headset - Side',
        'jacket1.jpg': 'Levi\'s Jacket - Front',
        'jacket2.jpg': 'Levi\'s Jacket - Back',
        'sunglasses1.jpg': 'Ray-Ban Aviators - Front',
        'sunglasses2.jpg': 'Ray-Ban Aviators - Case',
        'harrypotter1.jpg': 'Harry Potter Set - Stack',
        'harrypotter2.jpg': 'Harry Potter Set - Spread',
        'programming1.jpg': 'Programming Books - Stack',
        'programming2.jpg': 'Programming Books - Open',
        'table1.jpg': 'Coffee Table - Top View',
        'table2.jpg': 'Coffee Table - Side View',
        'lamp1.jpg': 'Floor Lamp - Full View',
        'lamp2.jpg': 'Floor Lamp - Detail',
        'bike1.jpg': 'Mountain Bike - Side View',
        'bike2.jpg': 'Mountain Bike - Front View',
        'weights1.jpg': 'Weight Set - Full View',
        'weights2.jpg': 'Weight Set - Close Up',
        'lego1.jpg': 'LEGO Set - Box',
        'lego2.jpg': 'LEGO Set - Built',
        'boardgames1.jpg': 'Board Games - Stack',
        'boardgames2.jpg': 'Board Games - Spread',
        'diningtable1.jpg': 'Dining Table - Top View',
        'diningtable2.jpg': 'Dining Table - Side View',
        'bookshelf1.jpg': 'Bookshelf - Full View',
        'bookshelf2.jpg': 'Bookshelf - Detail',
        'caraudio1.jpg': 'Car Audio - System',
        'caraudio2.jpg': 'Car Audio - Components',
        'tires1.jpg': 'Car Tires - Set',
        'tires2.jpg': 'Car Tires - Detail',
        'gardentools1.jpg': 'Garden Tools - Set',
        'gardentools2.jpg': 'Garden Tools - Individual',
        'kitchen1.jpg': 'Kitchen Appliances - Set',
        'kitchen2.jpg': 'Kitchen Appliances - Individual'
    }
    
    print("Generating placeholder images...")
    
    for image in images:
        description = descriptions.get(image, f"Product Image - {image}")
        filepath = os.path.join('media/products', image)
        create_placeholder_image(description, filepath)
    
    print(f"\nGenerated {len(images)} placeholder images in media/products/")
    print("You can now replace these with actual product photos!")

if __name__ == '__main__':
    main()
