import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

batch3_prices = {
    'PK 150': 70,
    'PK 151': 35,
    'PK 152': 48,
    'PK 153': 90,
    'PK 154': 170,
    'PK 155': 60,
    'PK 156': 60,
    'D 201': 75,
    'D 202': 120,
    'D 203': 120,
    'D 204': 135,
    'D 205': 130,
    'D 206': 155,
    'D 207': 130,
    'D 208': 155,
    'D 209': 130,
    'D 210': 165,
    'D 211': 120,
    'D 212': 110,
    'D 213': 120,
    'D 214': 140,
    'D 215': 130,
    'D 216': 130,
    'D 217': 165,
    'D 220': 120,
    'D 221': 170,
    'D 222': 175,
    'D 224': 165,
    'D 225': 180,
    'DP 301': 140,
    'DP 302': 200,
    'DP 303': 225,
    'DP 304': 240,
    'DP 305': 220,
    'DP 306': 220,
    'DP 307': 220,
    'DP 308': 240,
    'DP 309': 220,
    'DP 310': 240,
    'DP 311': 170,
    'DP 312': 180,
    'DP 313': 190,
    'DP 314': 220,
    'DP 315': 220,
    'DP 316': 220,
    'DP 317': 250,
    'DP 319': 355,
    'O 320': 650,
    'O 321': 525,
    'O 322': 550,
    'O 323': 280,
    'PD 324': 1550,
    'PD 325': 1600,
    'PD 326': 1850,
    'PD 327': 1600,
    'PD 328': 1900,
    'PD 329': 1850,
    'PD 330': 2200,
    'PD 331': 1450,
    'PD 332': 2100,
    'PD 333': 700,
    'BTP 401': 380,
    'DBP 402': 290,
    'DBP 403': 350
}

def update_batch3():
    print("## Batch 3 Price Update (+60%)\n")
    print("| Product Name | Old Base Price | New Price (+60%) |")
    print("|---|---|---|")
    
    missing = []
    
    for key, base_price in batch3_prices.items():
        # Search for key as-is
        products = Product.objects.filter(name__icontains=key)
        
        # If not found, try replacing space with hyphen (e.g. PK-150)
        if not products.exists():
            alt_key = key.replace(' ', '-')
            products = Product.objects.filter(name__icontains=alt_key)
            
        if not products.exists():
            # Try removing space completely (e.g. PK150)
            alt_key = key.replace(' ', '')
            products = Product.objects.filter(name__icontains=alt_key)
            
        if products.exists():
            for p in products:
                new_price = round(base_price * 1.60)
                p.price = Decimal(str(new_price))
                p.save(update_fields=['price'])
                
                print(f"| {p.name} | Rs. {base_price} | **Rs. {new_price}** |")
        else:
            missing.append(key)
            
    if missing:
        print("\n**Warning: The following products were not found in the database:**")
        for m in missing:
            print(f"- {m}")

if __name__ == '__main__':
    update_batch3()
