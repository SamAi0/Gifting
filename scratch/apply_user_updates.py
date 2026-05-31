import json
import os
import sys
import django

# Set up Django environment
backend_dir = r"c:\Users\Asus\Downloads\New folder\Gifting\backend"
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

json_path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Original items in customization.json: {len(data)}")

# 1. Remove ID 350 (Discount Test Product)
cleaned_data = [item for item in data if item.get('productId') != 350]
print(f"Items after removing ID 350: {len(cleaned_data)}")

# 2. Modify zones for ID 433 (Crock Diary DBCCPK 710)
for item in cleaned_data:
    if item.get('productId') == 433:
        zones = item.get('zones', [])
        # Keep only name-1 and logo-1
        clean_zones = [z for z in zones if z.get('id') in ['name-1', 'logo-1']]
        item['zones'] = clean_zones
        print(f"Successfully cleaned zones for ID 433 ({item.get('productName')}) -> kept {len(clean_zones)} zones.")

# Save updated customization.json
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=2)
print("Saved updated customization.json successfully.")

# 3. Delete ID 350 from SQLite database (using both objects and all_objects to be completely thorough)
deleted_active, _ = Product.objects.filter(id=350).delete()
deleted_all, _ = Product.all_objects.filter(id=350).delete()
print(f"Deleted product ID 350 from DB (active: {deleted_active}, all: {deleted_all})")
