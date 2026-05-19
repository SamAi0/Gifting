import os
import json

backend_dir = r"c:\Users\Asus\Downloads\New folder\Gifting\backend"
static_products_dir = os.path.join(backend_dir, 'static', 'products')
json_path = os.path.join(backend_dir, '..', 'frontend', 'src', 'data', 'customization.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items in customization.json: {len(data)}")
if data:
    product_ids = [item.get('productId') for item in data if 'productId' in item]
    print(f"Max productId: {max(product_ids) if product_ids else 'None'}")
    print(f"Min productId: {min(product_ids) if product_ids else 'None'}")

# Look at file extensions in json
extensions = {}
for item in data:
    base_image = item.get('baseImage', '')
    ext = os.path.splitext(base_image)[1].lower()
    extensions[ext] = extensions.get(ext, 0) + 1

print("\nExtensions in customization.json:")
for ext, count in extensions.items():
    print(f"  {ext}: {count}")

# Check files in static/products
files_in_dir = os.listdir(static_products_dir)
print(f"\nTotal files in static/products: {len(files_in_dir)}")

dir_extensions = {}
for f in files_in_dir:
    ext = os.path.splitext(f)[1].lower()
    dir_extensions[ext] = dir_extensions.get(ext, 0) + 1

print("Extensions in static/products directory:")
for ext, count in dir_extensions.items():
    print(f"  {ext}: {count}")
