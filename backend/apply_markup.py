import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

base_prices = {
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
    'cp 117': 90,
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
    'pk-149': 120,
}

def apply_markup():
    print("## Price Update Report (+60%)\n")
    print("| Product | Old Price | New Price |")
    print("|---|---|---|")
    
    for key, base_price in base_prices.items():
        search_key = key.replace(' - ', ' ').replace('-', ' ').strip()
        
        products = Product.objects.filter(name__icontains=search_key)
        if not products.exists():
            alt_key = search_key.replace(' ', ' - ')
            products = Product.objects.filter(name__icontains=alt_key)
            
        if not products.exists() and key == 'pk-149':
             products = Product.objects.filter(name__icontains='pk-149')
             
        if products.exists():
            for p in products:
                old_price = base_price
                # Calculate 60% markup and round it
                new_price = round(base_price * 1.60)
                
                p.price = Decimal(str(new_price))
                p.save(update_fields=['price'])
                
                print(f"| {p.name} | Rs. {old_price} | **Rs. {new_price}** |")

if __name__ == '__main__':
    apply_markup()
