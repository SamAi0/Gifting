import os
import sys
import json
import django

# 1. Bootstrapping Django
sys.path.append(r'd:\Gifting\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Input logs mapped to python dictionary
log_updates = {
    51: [
        {"zoneId": "zone-1", "x": 560, "y": 564, "angle": 274},
        {"zoneId": "zone-2", "x": 370, "y": 521, "angle": 269},
    ],
    52: [
        {"zoneId": "zone-1", "x": 574, "y": 584, "angle": 272},
        {"zoneId": "zone-2", "x": 375, "y": 630, "angle": 273},
    ],
    53: [
        {"zoneId": "zone-1", "x": 278, "y": 588, "angle": 0},
        {"zoneId": "zone-2", "x": 644, "y": 514, "angle": 267},
        {"zoneId": "zone-3", "x": 832, "y": 502, "angle": 263},
    ],
    54: [
        {"zoneId": "zone-1", "x": 524, "y": 588, "angle": 269},
        {"zoneId": "zone-2", "x": 392, "y": 510, "angle": 270},
    ],
    55: [
        {"zoneId": "zone-1", "x": 622, "y": 653, "angle": 271},
        {"zoneId": "zone-2", "x": 461, "y": 596, "angle": 269},
    ],
    56: [
        {"zoneId": "zone-1", "x": 622, "y": 653, "angle": 271},
        {"zoneId": "zone-2", "x": 461, "y": 596, "angle": 269},
    ],
    57: [
        {"zoneId": "zone-1", "x": 460, "y": 636, "angle": 269},
        {"zoneId": "zone-2", "x": 654, "y": 620, "angle": 0},
    ],
    58: [
        {"zoneId": "zone-1", "x": 420, "y": 610, "angle": 245},
        {"zoneId": "zone-2", "x": 552, "y": 513, "angle": 336},
    ],
    59: [
        {"zoneId": "zone-1", "x": 666, "y": 694, "angle": 269},
        {"zoneId": "zone-2", "x": 459, "y": 619, "angle": 269},
    ],
    60: [
        {"zoneId": "zone-1", "x": 569, "y": 581, "angle": 270},
        {"zoneId": "zone-2", "x": 393, "y": 597, "angle": 269},
    ]
}

# 2. Get slugs
id_to_slug = {}
for db_id in log_updates.keys():
    try:
        product = Product.objects.get(id=db_id)
        id_to_slug[db_id] = product.slug
    except Product.DoesNotExist:
        print(f"Product with id {db_id} not found.")

print(f"Mapped slugs: {id_to_slug}")

# 3. Load customization.json
json_path = r'd:\Gifting\frontend\src\data\customization.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0

# 4. Update JSON data
for db_id, updates in log_updates.items():
    if db_id not in id_to_slug:
        continue
    slug = id_to_slug[db_id]
    
    # Find item in JSON
    for item in data:
        if item.get("slug") == slug:
            zones = item.get("zones", [])
            for update in updates:
                zone_id = update["zoneId"]
                for zone in zones:
                    if zone.get("id") == zone_id:
                        zone["x"] = update["x"]
                        zone["y"] = update["y"]
                        zone["angle"] = update["angle"]
                        updated_count += 1
                        print(f"Updated {slug} zone {zone_id} to x={update['x']}, y={update['y']}, angle={update['angle']}")

print(f"Total zones updated in JSON: {updated_count}")

# 5. Save JSON data
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Saved customization.json successfully.")
