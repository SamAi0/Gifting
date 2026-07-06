import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def clear_discount_prices():
    # Find all products that have a discount price set
    products = Product.objects.filter(discount_price__isnull=False)
    count = products.count()
    
    if count > 0:
        # Bulk update to set discount_price to None
        updated_count = products.update(discount_price=None)
        print(f"Successfully cleared discount prices for {updated_count} products.")
    else:
        print("No products had discount prices set. All clear!")

if __name__ == '__main__':
    clear_discount_prices()
