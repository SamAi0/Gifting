import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def export_prices():
    products = Product.objects.all().order_by('id')
    print(f"Exporting {products.count()} products to prices.csv...")
    
    with open('prices.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Product Name', 'Price'])
        
        for p in products:
            writer.writerow([p.id, p.name, p.price])
            
    print("Done! File 'prices.csv' created.")

if __name__ == '__main__':
    export_prices()
