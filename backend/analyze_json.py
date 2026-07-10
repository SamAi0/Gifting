import os
import json
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def analyze_json():
    json_path = r'C:\Users\Asus\OneDrive\Desktop\A HRTECHINFO\sohamgift\Soham_Gift\frontend\src\data\customization.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    missing_ids = []
    needs_update = []
    valid = 0
    
    for item in data:
        pid = item.get('productId')
        try:
            prod = Product.objects.get(id=pid)
            # Check if name or slug needs update
            if prod.name != item.get('productName') or prod.slug != item.get('slug'):
                needs_update.append({
                    'id': pid,
                    'old_name': item.get('productName'),
                    'new_name': prod.name,
                    'old_slug': item.get('slug'),
                    'new_slug': prod.slug
                })
            else:
                valid += 1
        except Product.DoesNotExist:
            missing_ids.append((pid, item.get('productName')))
            
    print(f"Total items in JSON: {len(data)}")
    print(f"Valid and perfect: {valid}")
    print(f"Needs name/slug update: {len(needs_update)}")
    print(f"Missing from DB (deleted): {len(missing_ids)}")
    
    if missing_ids:
        print("\nMissing items:")
        for m in missing_ids[:10]:
            print(f"  ID: {m[0]}, Name: {m[1]}")
            
if __name__ == '__main__':
    analyze_json()
