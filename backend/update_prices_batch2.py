import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

prices = {
    'cp 118': 85,
    'cp 119': 85,
    'cp 120': 65,
    'cp 121': 90,
    'cp 122': 100,
    'cp 123': 100,
    'ckp 124': 120,
    'ckp 125': 135,
    'ckp 126': 125,
    'pf 127': 150,
    'po 128': 260,
    'ph 129': 150,
    'pm 130': 180,
    'tc 131': 850,
    'bpk 132': 250,
    'bpk 133': 225,
    'c 144': 625,
    'c 145': 550,
    'bc 146': 340,
    'bc 147': 340,
    'magnet pen stand 148': 110,
    'magnet pen stand -148': 110,
    'pk 149': 120,
}

def update_prices():
    for key, price in prices.items():
        # Cleaned search term to handle spacing differences like "C - 144" vs "C 144"
        search_key = key.replace(' - ', ' ').replace('-', ' ').strip()
        
        products = Product.objects.filter(name__icontains=search_key)
        if not products.exists():
            # Try alternate formatting
            alt_key = search_key.replace(' ', ' - ')
            products = Product.objects.filter(name__icontains=alt_key)
            
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
