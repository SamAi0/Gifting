import os, sys, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

# ── Parsed Log Data (270-291) ─────────────────────────────────────────────────
LOG_DATA = {
    270: {
        "zone-270-1": {"x": 625, "y": 520, "angle": 93},
        "zone-270-2": {"x": 131, "y": 297, "angle": 271},
        "zone-270-3": {"x": 203, "y": 283, "angle": 360},
    },
    271: {
        "zone-271-1": {"x": 235, "y": 372, "angle": 13},
        "zone-271-2": {"x": 382, "y": 350, "angle": 282},
    },
    272: {
        "zone-272-1": {"x": 264, "y": 253, "angle": 341},
        "zone-272-2": {"x": 241, "y": 419, "angle": 340},
    },
    273: {
        "zone-273-1": {"x": 423, "y": 772, "angle": 339},
        "zone-273-2": {"x": 503, "y": 432, "angle": 0},
    },
    274: {
        "zone-274-1": {"x": 276, "y": 207, "angle": 11},
        "zone-274-2": {"x": 378, "y": 371, "angle": 279},
    },
    275: {
        "zone-275-1": {"x": 377, "y": 358, "angle": 283},
        "zone-275-2": {"x": 294, "y": 189, "angle": 18},
    },
    276: {
        "zone-276-1": {"x": 381, "y": 355, "angle": 281},
        "zone-276-2": {"x": 284, "y": 188, "angle": 6},
    },
    277: {
        "zone-277-1": {"x": 517, "y": 546, "angle": 284},
        "zone-277-2": {"x": 382, "y": 338, "angle": 284},
    },
    278: {
        "zone-278-1": {"x": 478, "y": 188, "angle": 0},
        "zone-278-2": {"x": 464, "y": 802, "angle": 0},
    },
    279: {
        "zone-279-1": {"x": 390, "y": 244, "angle": 341},
        "zone-279-2": {"x": 546, "y": 794, "angle": 343},
        "zone-279-3": {"x": 480, "y": 532, "angle": 340},
    },
    280: {
        "zone-280-1": {"x": 392, "y": 240, "angle": 339},
        "zone-280-2": {"x": 695, "y": 394, "angle": 70},
        "zone-280-3": {"x": 555, "y": 673, "angle": 338},
    },
    281: {
        "zone-281-1": {"x": 390, "y": 278, "angle": 339},
        "zone-281-2": {"x": 556, "y": 722, "angle": 340},
        "zone-281-3": {"x": 482, "y": 528, "angle": 0},
    },
    282: {
        "zone-282-1": {"x": 374, "y": 204, "angle": 340},
        "zone-282-2": {"x": 594, "y": 710, "angle": 342},
        "zone-282-3": {"x": 494, "y": 500, "angle": 341},
    },
    283: {
        "zone-283-1": {"x": 476, "y": 165, "angle": 0},
        "zone-283-2": {"x": 480, "y": 755, "angle": 360},
        "zone-283-3": {"x": 478, "y": 809, "angle": 359},
    },
    284: {
        "zone-284-1": {"x": 492, "y": 176, "angle": 0},
        "zone-284-2": {"x": 496, "y": 798, "angle": 0},
        "zone-284-3": {"x": 496, "y": 870, "angle": 0},
    },
    285: {
        "zone-285-1": {"x": 495, "y": 196, "angle": 0},
        "zone-285-2": {"x": 494, "y": 754, "angle": 0},
        "zone-285-3": {"x": 488, "y": 824, "angle": 0},
    },
    286: {
        "zone-286-1": {"x": 462, "y": 173, "angle": 0},
        "zone-286-2": {"x": 460, "y": 756, "angle": 0},
        "zone-286-3": {"x": 458, "y": 814, "angle": 0},
    },
    287: {
        "zone-287-1": {"x": 495, "y": 194, "angle": 0},
        "zone-287-2": {"x": 487, "y": 734, "angle": 0},
        "zone-287-3": {"x": 485, "y": 788, "angle": 0},
    },
    288: {
        "zone-288-1": {"x": 502, "y": 202, "angle": 0},
        "zone-288-2": {"x": 510, "y": 796, "angle": 0},
        "zone-288-3": {"x": 516, "y": 852, "angle": 0},
    },
    289: {
        "zone-289-1": {"x": 472, "y": 172, "angle": 0},
        "zone-289-2": {"x": 484, "y": 756, "angle": 0},
        "zone-289-3": {"x": 484, "y": 834, "angle": 0},
    },
    290: {
        "zone-290-1": {"x": 500, "y": 200, "angle": 0},
        "zone-290-2": {"x": 490, "y": 648, "angle": 0},
        "zone-290-3": {"x": 484, "y": 700, "angle": 0},
    },
    291: {
        "zone-291-1": {"x": 492, "y": 198, "angle": 0},
        "zone-291-2": {"x": 492, "y": 714, "angle": 0},
        "zone-291-3": {"x": 480, "y": 772, "angle": 0},
    },
}

print("=" * 60)
print(f"SYNC: Products 270-291 Coordinate Logs")
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
print(f"Mapped: {len(id_to_slug)} products")

# Step 2: Load JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    cust_data = json.load(f)
slug_index = {item['slug']: i for i, item in enumerate(cust_data) if 'slug' in item}
print(f"\n[STEP 2] Loaded {len(cust_data)} entries from customization.json")

# Step 3: Update zones
print("\n[STEP 3] Updating zones...")
updated_count = 0
zone_miss = []

for db_id, zone_updates in LOG_DATA.items():
    slug = id_to_slug.get(db_id)
    if not slug:
        continue
    if slug not in slug_index:
        print(f"  [NOT IN JSON] ID {db_id} '{slug}'")
        continue

    idx = slug_index[slug]
    zones = cust_data[idx].get('zones', [])
    zone_id_map = {z['id']: z for z in zones}
    updated_zones = []

    for zone_id, coords in zone_updates.items():
        if zone_id in zone_id_map:
            zone_id_map[zone_id]['x'] = coords['x']
            zone_id_map[zone_id]['y'] = coords['y']
            zone_id_map[zone_id]['angle'] = coords['angle']
            updated_zones.append(zone_id)
        else:
            zone_miss.append((db_id, slug, zone_id))
            print(f"  [ZONE MISSING] ID {db_id} '{slug}' - zone '{zone_id}'")

    cust_data[idx]['zones'] = list(zone_id_map.values())
    updated_count += 1
    print(f"  [OK] ID {db_id} '{slug}' -> {updated_zones}")

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

print("\n" + "=" * 60)
print(f"DONE: {updated_count} products | Zone mismatches: {len(zone_miss)}")
if zone_miss:
    for db_id, slug, zid in zone_miss:
        print(f"  -> ID {db_id} '{slug}' zone '{zid}'")
print("=" * 60)
