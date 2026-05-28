import os
import sys
import json
import django
import re

sys.path.append(r'd:\Gifting\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

text = open(r'd:\Gifting\logs_201_260.txt', 'r', encoding='utf-8').read()
products = re.split(r'products/(\d+)', text)
log_updates = {}
for i in range(1, len(products), 2):
    pid = int(products[i])
    ptext = products[i+1]
    
    # We use a broad regex to catch anything like "Zone Update [zone-106-1] \nCanvasCustomizer.jsx:116 "x": 600, "y": 306, "angle": 0"
    zones = re.findall(r'(?i)zone update\s*\[([^\]]+)\][\s\S]*?CanvasCustomizer\.jsx:116\s*"x"\s*:\s*(-?\d+),\s*"y"\s*:\s*(-?\d+),\s*"angle"\s*:\s*(-?\d+)', ptext)
    
    if zones:
        log_updates[pid] = [{'zoneId': z[0], 'x': int(z[1]), 'y': int(z[2]), 'angle': int(z[3])} for z in zones]

print(f"Extracted {len(log_updates)} products from log.")

id_to_slug = {}
for db_id in log_updates.keys():
    try:
        product = Product.objects.get(id=db_id)
        id_to_slug[db_id] = product.slug
    except Product.DoesNotExist:
        print(f"Product with id {db_id} not found.")

json_path = r'd:\Gifting\frontend\src\data\customization.json'
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated_count = 0
for db_id, updates in log_updates.items():
    if db_id not in id_to_slug:
        continue
    slug = id_to_slug[db_id]
    
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

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Saved customization.json successfully.")
