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

# 1. Parsed data from new INPUT LOGS
new_parsed_logs = {
    21: {
        "zone-1": {"x": 622, "y": 623, "angle": 0},
        "zone-4": {"x": 367, "y": 624, "angle": 0},
        "zone-2": {"x": 641, "y": 393, "angle": 269},
        "zone-3": {"x": 385, "y": 374, "angle": 272}
    },
    22: {
        "zone-1": {"x": 627, "y": 623, "angle": 271},
        "zone-2": {"x": 641, "y": 380, "angle": 272},
        "zone-3": {"x": 380, "y": 374, "angle": 270},
        "zone-4": {"x": 377, "y": 628, "angle": 271}
    },
    23: {
        "zone-1": {"x": 500, "y": 646, "angle": 271},
        "zone-2": {"x": 316, "y": 724, "angle": 0}
    },
    24: {
        "zone-1": {"x": 616, "y": 610, "angle": 272},
        "zone-2": {"x": 420, "y": 688, "angle": 0}
    },
    25: {
        "zone-1": {"x": 870, "y": 645, "angle": 260},
        "zone-2": {"x": 577, "y": 554, "angle": 260},
        "zone-3": {"x": 823, "y": 796, "angle": 349},
        "zone-4": {"x": 546, "y": 876, "angle": 347}
    },
    27: {
        "zone-4": {"x": 594, "y": 851, "angle": 0},
        "zone-1": {"x": 654, "y": 626, "angle": 268},
        "zone-3": {"x": 363, "y": 273, "angle": 0},
        "zone-2": {"x": 379, "y": 756, "angle": 271}
    },
    28: {
        "zone-1": {"x": 634, "y": 648, "angle": 268},
        "zone-2": {"x": 386, "y": 744, "angle": 269},
        "zone-3": {"x": 382, "y": 316, "angle": 271},
        "zone-4": {"x": 586, "y": 824, "angle": 0}
    }
}

# 2. Map db_id to slug
slug_to_id = {}
id_to_slug = {}

print("Mapping product IDs to slugs from SQLite via Django ORM...")
for db_id in new_parsed_logs.keys():
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
backup_path = json_path + ".bak2"

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
        updates = new_parsed_logs[db_id]
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
