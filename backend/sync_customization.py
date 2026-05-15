"""
Script to sync customization.json to the database
This updates all products with customization zones from the JSON file
"""
import os
import sys
import json
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def sync_customization_zones():
    """Sync customization.json to database"""
    
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    if not os.path.exists(json_path):
        print(f"[ERROR] customization.json not found at {json_path}")
        return
    
    with open(json_path, 'r') as f:
        customization_data = json.load(f)
    
    print(f"[INFO] Loaded {len(customization_data)} products from customization.json")
    
    updated_count = 0
    not_found_count = 0
    
    for item in customization_data:
        slug = item.get('slug')
        product_id = item.get('productId') # Keep for logging fallback
        
        try:
            if slug:
                product = Product.objects.get(slug=slug)
            else:
                product = Product.objects.get(id=product_id)
            
            # Extract zones only (without productId, productName, slug, baseImage)
            zones = item.get('zones', [])
            
            # Save as JSON string in customization_config
            product.customization_config = json.dumps(zones)
            product.save()
            
            print(f"[SUCCESS] Updated: {product.name} (ID: {product_id}) - {len(zones)} zones")
            updated_count += 1
            
        except Product.DoesNotExist:
            identifier = slug if slug else f"ID {product_id}"
            print(f"[WARNING] Product {identifier} not found in database")
            not_found_count += 1
    
    print(f"\n{'='*50}")
    print(f"[SUCCESS] Successfully updated: {updated_count} products")
    if not_found_count > 0:
        print(f"[WARNING] Not found in database: {not_found_count} products")
        print(f"[TIP] Run 'python import_all.py' to create missing products from the JSON file.")
    else:
        print(f"[SUCCESS] All products are perfectly in sync!")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Syncing customization.json to database...\n")
    sync_customization_zones()
    print("\nDone! Your changes should now be visible on localhost.")
