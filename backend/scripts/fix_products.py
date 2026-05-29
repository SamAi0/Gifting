import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_existing_products():
    """Update existing products with default badge_color if missing"""
    products = Product.objects.all()
    count = 0
    
    for product in products:
        if not product.badge_color:
            product.badge_color = "#D91656"
            product.save()
            count += 1
            print(f"Updated: {product.name}")
    
    print(f"\nFixed {count} products with missing badge_color")

if __name__ == "__main__":
    fix_existing_products()
