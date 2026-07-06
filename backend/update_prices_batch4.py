import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

batch4_prices = {
    'DBP 404': 375,
    'DBP 405': 375,
    'DBP 406': 375,
    'DBP 407': 480,
    'DBP 408': 350,
    'DCP 409': 480,
    'DCP 410': 425,
    'DCP 411': 410,
    'DCP 412': 450,
    'DKP 413': 180,
    'DKP 414': 230,
    'DKP 415': 250,
    'DKP 416': 230,
    'DKP 417': 275,
    'DLCP 419': 300,
    'DKP 420': 225,
    'DKP 421': 210,
    'PD 501': 2500,
    'DBKP 502': 380,
    'DBKP 503': 400,
    'DBKP 504': 425,
    'DBKP 505': 450,
    'DBKP 506': 425,
    'DBKP 507': 425,
    'DBKP 508': 425,
    'DBKP 509': 400,
    'DBKP 510': 390,
    'DBKP 511': 525
}

def update_batch4():
    print("## Batch 4 Price Update (+60%)\n")
    print("| Product Name | Old Base Price | New Price (+60%) |")
    print("|---|---|---|")
    
    missing = []
    
    for key, base_price in batch4_prices.items():
        # Search for key as-is
        products = Product.objects.filter(name__icontains=key)
        
        # If not found, try replacing space with hyphen
        if not products.exists():
            alt_key = key.replace(' ', '-')
            products = Product.objects.filter(name__icontains=alt_key)
            
        if not products.exists():
            # Try removing space completely
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
    update_batch4()
