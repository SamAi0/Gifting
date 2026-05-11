import os
import json
import django
import sys

# Set up Django environment
sys.path.append(r"c:\Users\Asus\Downloads\New folder\Gifting\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category

# Path to the customization JSON
JSON_PATH = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"

def get_category(name):
    name_lower = name.lower()
    if 'pen' in name_lower and 'keychain' in name_lower:
        return Category.objects.get(id=15) # Pen & Keychain Sets
    if 'diary' in name_lower or 'notebook' in name_lower:
        return Category.objects.get(id=14) # Diary & Notebook Sets
    if 'advocate' in name_lower:
        return Category.objects.get(id=11)
    if 'ca set' in name_lower:
        return Category.objects.get(id=12)
    if 'doctor' in name_lower:
        return Category.objects.get(id=13)
    if 'gift set' in name_lower:
        return Category.objects.get(id=9) # Corporate Gift Sets
    
    return Category.objects.get(id=7) # Gift Sets (Default)

def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)

    created_count = 0
    updated_count = 0

    for i, item in enumerate(customization_data):
        slug = item['slug']
        name = item['productName']
        image_path = item['baseImage']
        zones_json = json.dumps(item['zones'])
        
        # Explicitly set SKU to ensure uniqueness during bulk creation
        cat = get_category(name)
        cat_code = cat.name[:3].upper() if cat else "UNC"
        sku = f"SG-{cat_code}-{slug[:10].upper()}-{item['productId']}"

        product, created = Product.all_objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'sku': sku,
                'image': image_path,
                'category': cat,
                'price': 999.00,
                'description': f"Premium quality {name} perfect for corporate gifting. Fully customizable with your logo and text.",
                'customization_config': zones_json,
                'stock': 100,
                'is_active': True,
                'is_deleted': False
            }
        )

        if not created:
            # Update image and config if they changed
            product.image = image_path
            product.customization_config = zones_json
            product.save()
            updated_count += 1
        else:
            created_count += 1

    print(f"Sync complete: {created_count} products created, {updated_count} products updated.")

if __name__ == "__main__":
    main()
