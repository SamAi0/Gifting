import os
import json
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_json():
    json_path = r'C:\Users\Asus\OneDrive\Desktop\A HRTECHINFO\sohamgift\Soham_Gift\frontend\src\data\customization.json'
    backup_path = r'C:\Users\Asus\OneDrive\Desktop\A HRTECHINFO\sohamgift\Soham_Gift\frontend\src\data\customization.json.bak'
    
    # Backup
    shutil.copy2(json_path, backup_path)
    print("Created backup at customization.json.bak")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    updated_data = []
    updated_count = 0
    rescued_count = 0
    deleted_count = 0
    
    for item in data:
        pid = item.get('productId')
        old_name = item.get('productName')
        
        try:
            prod = Product.objects.get(id=pid)
            item['productName'] = prod.name
            item['slug'] = prod.slug
            updated_data.append(item)
            updated_count += 1
        except Product.DoesNotExist:
            # Try to rescue by exact name (case-insensitive)
            # or maybe the old name is the same
            matches = Product.objects.filter(name__iexact=old_name)
            if not matches.exists():
                # Try replacing spaces with hyphens or something
                matches = Product.objects.filter(slug__iexact=item.get('slug'))
                
            if matches.exists():
                prod = matches.first()
                item['productId'] = prod.id
                item['productName'] = prod.name
                item['slug'] = prod.slug
                updated_data.append(item)
                rescued_count += 1
            else:
                deleted_count += 1

    print(f"Original items: {len(data)}")
    print(f"Updated items: {updated_count}")
    print(f"Rescued items (found by name/slug): {rescued_count}")
    print(f"Deleted items (not in DB): {deleted_count}")
    print(f"New JSON length: {len(updated_data)}")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=2)
        
    print("Successfully updated customization.json")
    
if __name__ == '__main__':
    update_json()
