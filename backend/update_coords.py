import os
import sys
import json
import django
import subprocess

# 1. Input logs data structure
LOG_UPDATES = {
    270: {
        "zone-270-1": {"x": 625, "y": 520, "angle": 93},
        "zone-270-2": {"x": 131, "y": 297, "angle": 271},
        "zone-270-3": {"x": 203, "y": 283, "angle": 360}
    },
    271: {
        "zone-271-1": {"x": 235, "y": 372, "angle": 13},
        "zone-271-2": {"x": 382, "y": 350, "angle": 282}
    },
    272: {
        "zone-272-1": {"x": 264, "y": 253, "angle": 341},
        "zone-272-2": {"x": 241, "y": 419, "angle": 340}
    },
    273: {
        "zone-273-1": {"x": 423, "y": 772, "angle": 339},
        "zone-273-2": {"x": 503, "y": 432, "angle": 0}
    },
    274: {
        "zone-274-1": {"x": 276, "y": 207, "angle": 11},
        "zone-274-2": {"x": 378, "y": 371, "angle": 279}
    },
    275: {
        "zone-275-1": {"x": 377, "y": 358, "angle": 283},
        "zone-275-2": {"x": 294, "y": 189, "angle": 18}
    },
    276: {
        "zone-276-1": {"x": 381, "y": 355, "angle": 281},
        "zone-276-2": {"x": 284, "y": 188, "angle": 6}
    },
    277: {
        "zone-277-1": {"x": 517, "y": 546, "angle": 284},
        "zone-277-2": {"x": 382, "y": 338, "angle": 284}
    }
}

# 2. Bootstrap Django Environment
print("[INFO] Bootstrapping Django environment...")
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(backend_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# 3. Map Database IDs to Slugs
print("[INFO] Mapping DB IDs to slugs...")
id_to_slug = {}
for db_id in LOG_UPDATES.keys():
    try:
        product = Product.objects.get(id=db_id)
        id_to_slug[db_id] = product.slug
        print(f"  ID {db_id} -> Slug: '{product.slug}' (Name: '{product.name}')")
    except Product.DoesNotExist:
        print(f"[ERROR] Product with ID {db_id} not found in database!")
        sys.exit(1)

# 4. Load customization.json
json_path = os.path.join(
    os.path.dirname(backend_dir),
    'frontend',
    'src',
    'data',
    'customization.json'
)
print(f"[INFO] Loading customization.json from {json_path}...")
with open(json_path, 'r', encoding='utf-8') as f:
    customization_data = json.load(f)

# 5. Update customization.json matching by slug
print("[INFO] Updating customization zones by product slug...")
slug_to_item = {item['slug']: item for item in customization_data if 'slug' in item}

updated_zones_count = 0
for db_id, zones_updates in LOG_UPDATES.items():
    slug = id_to_slug[db_id]
    if slug not in slug_to_item:
        print(f"[WARNING] Slug '{slug}' (ID {db_id}) not found in customization.json!")
        continue
    
    product_item = slug_to_item[slug]
    for zone_id, new_coords in zones_updates.items():
        # Find zone in product_item['zones']
        zone_found = False
        for zone in product_item.get('zones', []):
            if zone.get('id') == zone_id:
                old_coords = {k: zone.get(k) for k in new_coords}
                zone.update(new_coords)
                print(f"  Updated '{slug}' Zone '{zone_id}': {old_coords} -> {new_coords}")
                updated_zones_count += 1
                zone_found = True
                break
        if not zone_found:
            print(f"[WARNING] Zone '{zone_id}' not found in customization.json for slug '{slug}'!")

# 6. Save customization.json with pretty-print formatting
print("[INFO] Saving customization.json...")
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(customization_data, f, indent=2, ensure_ascii=False)
print(f"[SUCCESS] Updated customization.json successfully! (Updated {updated_zones_count} zones)")

# 7. Execute 'python sync_customization.py' in the 'backend' folder
print("[INFO] Executing sync_customization.py to update SQLite DB...")
sync_script_path = os.path.join(backend_dir, 'sync_customization.py')
result = subprocess.run([sys.executable, sync_script_path], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print("[ERROR stderr in sync]:", result.stderr)

if result.returncode == 0:
    print("[SUCCESS] DB Sync completed successfully!")
else:
    print(f"[ERROR] DB Sync failed with return code {result.returncode}")
    sys.exit(result.returncode)
