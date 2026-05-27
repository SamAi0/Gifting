import os
import sys
import json
import subprocess

json_path = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"

if not os.path.exists(json_path):
    print("[ERROR] customization.json not found!")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Revert bolttle-cup-set-bc (ID 25)
target_slug = 'bolttle-cup-set-bc'
original_zones = {
    "zone-1": {"x": 400, "y": 160, "angle": 0},
    "zone-2": {"x": 400, "y": 220, "angle": 0},
    "zone-3": {"x": 400, "y": 280, "angle": 0},
    "zone-4": {"x": 400, "y": 340, "angle": 0}
}

found = False
for item in data:
    if item.get('slug') == target_slug:
        print(f"Reverting '{target_slug}' (ID 25) coordinates...")
        for zone in item.get('zones', []):
            zone_id = zone.get('id')
            if zone_id in original_zones:
                orig_val = original_zones[zone_id]
                zone['x'] = orig_val['x']
                zone['y'] = orig_val['y']
                zone['angle'] = orig_val['angle']
                print(f"  Reverted '{zone_id}' -> x: {zone['x']}, y: {zone['y']}, angle: {zone['angle']}")
        found = True
        break

if not found:
    print(f"[ERROR] Product slug '{target_slug}' not found in customization.json!")
    sys.exit(1)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nSuccessfully updated customization.json. Running database synchronization...")
