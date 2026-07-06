import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

prices = {
    'kp 102': 65,
    'kp 103': 75,
    'kp 104': 50,
    'kp 105': 45,
    'kp 106': 95,
    'kp 107': 70,
    'kp 108': 175,
    'kp 109': 200,
    'kp 110': 150,
    'kp 111': 125,
    'kp 112': 125,
    'kp 113': 150,
    'kp 114': 125,
    'kp 115': 150,
    'kp 116': 110,
    'cp 117': 90
}

def update_prices():
    for key, price in prices.items():
        # Using case-insensitive search
        products = Product.objects.filter(name__icontains=key)
        if products.exists():
            for p in products:
                old_price = p.price
                p.price = Decimal(str(price))
                p.save(update_fields=['price'])
                print(f"Updated '{p.name}' (ID: {p.id}): {old_price} -> {p.price}")
        else:
            print(f"WARNING: Product with '{key}' not found in database.")

if __name__ == '__main__':
    update_prices()
