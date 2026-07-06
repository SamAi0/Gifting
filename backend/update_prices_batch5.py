import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

batch5_prices = {
    'DBKP 512': 425,
    'DBPP 513': 550,
    'DCPP 514': 625,
    'DCKP 515': 425,
    'DCKP 516': 475,
    'BCPK 517': 300,
    'DCPC 518': 450,
    'DCBP 519': 725,
    'DCPK 520': 280,
    'DCPK 521': 280
}

def update_batch5():
    print("## Batch 5 Price Update (+60%)\n")
    print("| Product Name | Old Base Price | New Price (+60%) |")
    print("|---|---|---|")
    
    missing = []
    
    for key, base_price in batch5_prices.items():
        products = Product.objects.filter(name__icontains=key)
        
        if not products.exists():
            alt_key = key.replace(' ', '-')
            products = Product.objects.filter(name__icontains=alt_key)
            
        if not products.exists():
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
    update_batch5()
