import os, sys, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

# ── Parsed Log Data (1097-1100 extras) ─────────────────────────────────────────────────
LOG_DATA = {
    1097: {"extra-3": {"x": 624, "y": 266, "angle": 325}, "extra-2": {"x": 544, "y": 466, "angle": 42}},
    1098: {"extra-3": {"x": 754, "y": 548, "angle": 332}, "extra-2": {"x": 722, "y": 330, "angle": 63}},
    1099: {"extra-2": {"x": 622, "y": 544, "angle": 81}, "extra-3": {"x": 246, "y": 630, "angle": 79}},
    1100: {"extra-3": {"x": 256, "y": 644, "angle": 75}, "extra-2": {"x": 577, "y": 496, "angle": 73}},
}

print("=" * 60)
print(f"SYNC: Products 1097-1100 Extra Coordinates")
print(f"Total: {len(LOG_DATA)} products")
print("=" * 60)

# Step 1: Map IDs to slugs
print("\n[STEP 1] Mapping DB IDs to slugs...")
id_to_slug = {}
for db_id in LOG_DATA:
    try:
        p = Product.objects.get(id=db_id)
        id_to_slug[db_id] = p.slug
        print(f"  [MAP] {db_id} -> '{p.slug}'")
    except Product.DoesNotExist:
        print(f"  [SKIP] ID {db_id} not in DB")

# Step 2: Load JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    cust_data = json.load(f)
slug_index = {item['slug']: i for i, item in enumerate(cust_data) if 'slug' in item}

# Step 3: Update zones
print("\n[STEP 3] Updating zones...")
updated_count = 0
for db_id, zone_updates in LOG_DATA.items():
    slug = id_to_slug.get(db_id)
    if not slug or slug not in slug_index:
        continue

    idx = slug_index[slug]
    zones = cust_data[idx].get('zones', [])
    zone_id_map = {z['id']: z for z in zones}
    
    updated_actions = []
    for zone_id, coords in zone_updates.items():
        if zone_id in zone_id_map:
            zone_id_map[zone_id]['x'] = coords['x']
            zone_id_map[zone_id]['y'] = coords['y']
            zone_id_map[zone_id]['angle'] = coords['angle']
            updated_actions.append(f"UPDATED {zone_id}")

    cust_data[idx]['zones'] = list(zone_id_map.values())
    updated_count += 1
    print(f"  [OK] ID {db_id} '{slug}' -> {', '.join(updated_actions)}")

# Step 4: Save
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(cust_data, f, indent=2, ensure_ascii=False)
print(f"\n[STEP 4] SAVED: {updated_count} products updated")

# Step 5: DB Sync
print("\n" + "=" * 60)
print("[STEP 5] Running sync_customization.py...")
print("=" * 60)
res = subprocess.run([sys.executable, SYNC_SCRIPT], capture_output=True, text=True, cwd=BACKEND_DIR)
for line in res.stdout.strip().split('\n')[-10:]:
    print(line)
if res.returncode == 0:
    print("\n[SUCCESS] SQLite DB sync complete!")
else:
    print(f"[ERROR] {res.stderr}")
