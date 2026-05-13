import os
import json
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def export_to_json():
    json_path = os.path.join('../frontend/src/data/customization.json')
    
    # Load existing data
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []
        
    existing_slugs = {item.get('slug') for item in existing_data}
    
    # Get all products from DB
    all_products = Product.objects.all()
    
    new_entries = 0
    for product in all_products:
        if product.slug not in existing_slugs:
            # Create entry for JSON
            entry = {
                "productId": product.id,
                "productName": product.name,
                "slug": product.slug,
                "baseImage": product.image,
                "zones": json.loads(product.customization_config) if product.customization_config else []
            }
            existing_data.append(entry)
            new_entries += 1
            
    # Save back to JSON
    with open(json_path, 'w') as f:
        json.dump(existing_data, f, indent=2)
        
    print(f"Successfully added {new_entries} products to customization.json")
    print(f"Total products in JSON now: {len(existing_data)}")

if __name__ == '__main__':
    export_to_json()
