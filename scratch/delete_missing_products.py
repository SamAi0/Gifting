import os
import sys
import json
import django

def delete_missing():
    # 1. Update customization.json
    json_path = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"
    
    missing_images = [
        "/static/products/RC_Speed_Pen_Golden_Clip_2015_Black.png",
        "/static/products/RC_Speed_Pen_Golden_Clip_2015_Golden.png",
        "/static/products/RC_Tik_tik_Curve_Pen_2041_White.png"
    ]
    
    if not os.path.exists(json_path):
        print(f"[ERROR] customization.json not found at {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    original_count = len(data)
    # Filter out products referencing the missing images
    filtered_data = [item for item in data if item.get('baseImage') not in missing_images]
    new_count = len(filtered_data)
    
    removed_items = [item.get('productName') for item in data if item.get('baseImage') in missing_images]
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2)
        
    print(f"[SUCCESS] Removed {original_count - new_count} products from customization.json:")
    for name in removed_items:
        print(f"  - Removed: {name}")

    # 2. Setup Django environment and delete/deactivate from Database
    backend_dir = r"c:\Users\Asus\Downloads\New folder\Gifting\backend"
    sys.path.append(backend_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    from products.models import Product
    
    print("\n[INFO] Updating Django Database...")
    db_updated = 0
    for img_path in missing_images:
        # Find product in database by image path
        # Since default manager might filter out already deleted ones, use all_objects
        products = Product.all_objects.filter(image=img_path)
        for p in products:
            p.is_deleted = True
            p.is_active = False
            p.save()
            print(f"  - Deactivated & Soft-Deleted in DB: {p.name} (Slug: {p.slug})")
            db_updated += 1
            
    print(f"[SUCCESS] Updated {db_updated} products in Django database.")

if __name__ == '__main__':
    delete_missing()
