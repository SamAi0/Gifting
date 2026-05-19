import os
import json
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_product_ids():
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
        
    with open(json_path, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
        
    print(f"[INFO] Loaded {len(customization_data)} products from customization.json")
    
    updated_count = 0
    not_found_count = 0
    already_correct_count = 0
    
    for item in customization_data:
        slug = item.get('slug')
        current_json_id = item.get('productId')
        
        if not slug:
            continue
            
        try:
            # Query the database for this slug
            product = Product.objects.get(slug=slug)
            db_id = product.id
            
            if current_json_id != db_id:
                print(f"[UPDATE] Slug '{slug}': JSON ID {current_json_id} -> DB ID {db_id}")
                item['productId'] = db_id
                updated_count += 1
            else:
                already_correct_count += 1
                
        except Product.DoesNotExist:
            print(f"[WARNING] Product with slug '{slug}' not found in database")
            not_found_count += 1
            
    # Save the updated JSON back with pretty-printing
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(customization_data, f, indent=2)
        
    print(f"\n{'='*50}")
    print(f"[SUCCESS] Finished updating customization.json!")
    print(f"[INFO] Already Correct IDs: {already_correct_count}")
    print(f"[SUCCESS] Updated mismatch IDs: {updated_count}")
    if not_found_count > 0:
        print(f"[WARNING] Slugs not found in DB: {not_found_count}")
    print(f"{'='*50}")

if __name__ == '__main__':
    fix_product_ids()
