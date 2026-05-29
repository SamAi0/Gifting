import os
import sys
import json
import shutil
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# 1. Parsed data from INPUT LOGS
parsed_logs = {
    21: {
        "zone-1": {"x": 336, "y": 335, "angle": 0},
        "zone-2": {"x": 333, "y": 207, "angle": 269},
        "zone-3": {"x": 201, "y": 208, "angle": 272},
        "zone-4": {"x": 207, "y": 338, "angle": 0}
    },
    22: {
        "zone-1": {"x": 337, "y": 337, "angle": 271},
        "zone-2": {"x": 339, "y": 202, "angle": 272},
        "zone-3": {"x": 210, "y": 202, "angle": 270},
        "zone-4": {"x": 205, "y": 338, "angle": 271}
    },
    23: {
        "zone-1": {"x": 612, "y": 606, "angle": 271},
        "zone-2": {"x": 354, "y": 820, "angle": 0},
        "zone-3": {"x": 288, "y": 230, "angle": 0}
    },
    25: {
        "zone-1": {"x": 1034, "y": 752, "angle": 260},
        "zone-2": {"x": 646, "y": 742, "angle": 350},
        "zone-3": {"x": 637, "y": 1039, "angle": 350},
        "zone-4": {"x": 637, "y": 966, "angle": 352}
    },
    26: {
        "zone-1": {"x": 822, "y": 631, "angle": 261},
        "zone-2": {"x": 561, "y": 566, "angle": 262},
        "zone-3": {"x": 788, "y": 814, "angle": 349},
        "zone-4": {"x": 548, "y": 891, "angle": 352}
    },
    27: {
        "zone-1": {"x": 742, "y": 700, "angle": 268},
        "zone-2": {"x": 445, "y": 894, "angle": 271},
        "zone-3": {"x": 485, "y": 331, "angle": 0},
        "zone-4": {"x": 682, "y": 1005, "angle": 0}
    }
}

# 2. Map db_id to slug
slug_to_id = {}
id_to_slug = {}

print("Mapping product IDs to slugs from SQLite via Django ORM...")
for db_id in parsed_logs.keys():
    try:
        product = Product.all_objects.get(id=db_id)
        id_to_slug[db_id] = product.slug
        slug_to_id[product.slug] = db_id
        print(f"Mapped ID {db_id} -> Slug '{product.slug}' (Name: {product.name})")
    except Product.DoesNotExist:
        print(f"[ERROR] Product ID {db_id} not found in database!")
        sys.exit(1)

# 3. Path setup and backup
json_path = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"
backup_path = json_path + ".bak"

if not os.path.exists(json_path):
    print(f"[ERROR] customization.json not found at {json_path}")
    sys.exit(1)

print(f"Backing up customization.json to {backup_path}...")
shutil.copy2(json_path, backup_path)

# 4. Load, Update and Save
print("Loading customization.json...")
with open(json_path, 'r', encoding='utf-8') as f:
    customization_data = json.load(f)

updated_products_count = 0
updated_zones_count = 0

for item in customization_data:
    slug = item.get('slug')
    if slug in slug_to_id:
        db_id = slug_to_id[slug]
        updates = parsed_logs[db_id]
        print(f"\nUpdating zones for slug '{slug}' (ID: {db_id}):")
        
        zones = item.get('zones', [])
        for zone in zones:
            zone_id = zone.get('id')
            if zone_id in updates:
                orig_x, orig_y, orig_angle = zone.get('x'), zone.get('y'), zone.get('angle')
                new_vals = updates[zone_id]
                zone['x'] = new_vals['x']
                zone['y'] = new_vals['y']
                zone['angle'] = new_vals['angle']
                print(f"  Zone '{zone_id}': (x: {orig_x} -> {zone['x']}, y: {orig_y} -> {zone['y']}, angle: {orig_angle} -> {zone['angle']})")
                updated_zones_count += 1
        
        updated_products_count += 1

print(f"\nSaving updated customization.json with pretty-print formatting...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(customization_data, f, indent=2, ensure_ascii=False)

print(f"[SUCCESS] Updated {updated_products_count} products and {updated_zones_count} zones in customization.json.")
