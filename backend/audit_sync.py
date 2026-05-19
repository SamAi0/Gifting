import os
import json
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def run_comprehensive_audit():
    print("=" * 60)
    print("COMPREHENSIVE SYNC & ASSET AUDIT")
    print("=" * 60)
    
    # 1. Load customization.json
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
        
    # 2. Get DB Products
    db_products = Product.objects.all()
    
    json_slugs = {item.get('slug') for item in customization_data if item.get('slug')}
    db_slugs = {p.slug for p in db_products}
    
    # 3. Check Slug Harmony
    missing_in_db = json_slugs - db_slugs
    missing_in_json = db_slugs - json_slugs
    
    print(f"\n--- Slug & Synchronization ---")
    print(f"Total Products in customization.json: {len(customization_data)}")
    print(f"Total Products in SQLite Database: {len(db_products)}")
    
    if not missing_in_db and not missing_in_json:
        print("[SUCCESS] All product slugs are 100% in sync between JSON and DB!")
    else:
        if missing_in_db:
            print(f"[WARNING] Slugs in JSON but missing in DB ({len(missing_in_db)}): {list(missing_in_db)[:5]}...")
        if missing_in_json:
            print(f"[WARNING] Slugs in DB but missing in JSON ({len(missing_in_json)}): {list(missing_in_json)[:5]}...")
            
    # 4. Check Product ID Match
    id_mismatches = []
    for item in customization_data:
        slug = item.get('slug')
        json_id = item.get('productId')
        try:
            product = db_products.get(slug=slug)
            if json_id != product.id:
                id_mismatches.append((slug, json_id, product.id))
        except Product.DoesNotExist:
            pass
            
    print(f"\n--- Product ID Alignment ---")
    if not id_mismatches:
        print("[SUCCESS] All productIds in customization.json perfectly match SQLite IDs!")
    else:
        print(f"[WARNING] Found {len(id_mismatches)} productId mismatches:")
        for slug, j_id, d_id in id_mismatches[:5]:
            print(f"  * Slug '{slug}': JSON ID {j_id} vs DB ID {d_id}")
            
    # 5. Check Image Files in static/products
    missing_images = []
    for item in customization_data:
        image_path = item.get('baseImage')
        slug = item.get('slug')
        if not image_path:
            missing_images.append((slug, "NO_IMAGE_PATH"))
            continue
            
        # Clean static prefix
        relative_path = image_path.replace('/static/', '').replace('static/', '')
        full_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'backend',
            'static',
            relative_path
        )
        
        # Also check relative path directly in backend/static
        if not os.path.exists(full_path):
            missing_images.append((slug, image_path))
            
    print(f"\n--- Image Assets Integrity ---")
    if not missing_images:
        print("[SUCCESS] All product images are present in static/products!")
    else:
        print(f"[WARNING] Found {len(missing_images)} missing or broken product images:")
        for slug, img in missing_images:
            print(f"  * Product '{slug}': File not found -> '{img}'")
            
    # 6. Check Zones Config Structure
    empty_zones = []
    for item in customization_data:
        zones = item.get('zones', [])
        slug = item.get('slug')
        if not zones:
            empty_zones.append(slug)
            
    print(f"\n--- Customization Zones Config ---")
    if not empty_zones:
        print("[SUCCESS] All products in customization.json have active customization zones!")
    else:
        print(f"[INFO] {len(empty_zones)} products have empty/no customization zones.")
        
    print("=" * 60)

if __name__ == '__main__':
    run_comprehensive_audit()
