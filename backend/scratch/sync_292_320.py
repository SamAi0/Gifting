import os, sys, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

# ── Parsed Log Data (292-320) ─────────────────────────────────────────────────
LOG_DATA = {
    292: {"zone-292-1": {"x": 501, "y": 193, "angle": 0}, "zone-292-2": {"x": 506, "y": 642, "angle": 0}, "zone-292-3": {"x": 498, "y": 706, "angle": 0}},
    293: {"zone-293-1": {"x": 496, "y": 200, "angle": 0}, "zone-293-2": {"x": 492, "y": 732, "angle": 0}, "zone-293-3": {"x": 488, "y": 800, "angle": 0}},
    294: {"zone-294-2": {"x": 502, "y": 738, "angle": 0}, "zone-294-3": {"x": 498, "y": 804, "angle": 0}, "zone-294-1": {"x": 498, "y": 204, "angle": 0}},
    295: {"zone-295-1": {"x": 484, "y": 230, "angle": 359}, "zone-295-2": {"x": 490, "y": 766, "angle": 0}, "zone-295-3": {"x": 488, "y": 824, "angle": 0}},
    296: {"zone-296-1": {"x": 500, "y": 232, "angle": 0}, "zone-296-3": {"x": 494, "y": 828, "angle": 0}, "zone-296-2": {"x": 498, "y": 774, "angle": 0}},
    297: {"zone-297-1": {"x": 512, "y": 210, "angle": 0}, "zone-297-2": {"x": 524, "y": 714, "angle": 0}, "zone-297-3": {"x": 522, "y": 776, "angle": 0}},
    298: {"zone-298-1": {"x": 507, "y": 199, "angle": 0}, "zone-298-2": {"x": 659, "y": 506, "angle": 360}, "zone-298-3": {"x": 499, "y": 768, "angle": 0}},
    299: {"zone-299-1": {"x": 504, "y": 194, "angle": 0}, "zone-299-2": {"x": 516, "y": 698, "angle": 0}, "zone-299-3": {"x": 510, "y": 464, "angle": 0}},
    300: {"zone-300-1": {"x": 504, "y": 246, "angle": 0}, "zone-300-2": {"x": 502, "y": 526, "angle": 0}, "zone-300-3": {"x": 500, "y": 748, "angle": 0}},
    301: {"zone-301-1": {"x": 491, "y": 241, "angle": 1}, "zone-301-2": {"x": 493, "y": 622, "angle": 0}, "zone-301-3": {"x": 756, "y": 804, "angle": 270}},
    302: {"zone-302-1": {"x": 504, "y": 236, "angle": 0}, "zone-302-2": {"x": 472, "y": 460, "angle": 0}, "zone-302-3": {"x": 502, "y": 770, "angle": 0}},
    303: {"zone-303-1": {"x": 500, "y": 176, "angle": 0}, "zone-303-2": {"x": 500, "y": 460, "angle": 0}, "zone-303-3": {"x": 482, "y": 862, "angle": 0}},
    304: {"zone-304-1": {"x": 503, "y": 444, "angle": 359}, "zone-304-2": {"x": 495, "y": 552, "angle": 360}, "zone-304-3": {"x": 500, "y": 499, "angle": 360}},
    305: {"zone-305-1": {"x": 520, "y": 204, "angle": 0}, "zone-305-3": {"x": 506, "y": 848, "angle": 0}, "zone-305-2": {"x": 530, "y": 522, "angle": 0}},
    306: {"zone-306-1": {"x": 504, "y": 178, "angle": 0}, "zone-306-2": {"x": 516, "y": 506, "angle": 0}, "zone-306-3": {"x": 530, "y": 860, "angle": 0}},
    307: {"zone-307-1": {"x": 485, "y": 188, "angle": 360}, "zone-307-3": {"x": 461, "y": 769, "angle": 1}, "zone-307-2": {"x": 464, "y": 533, "angle": 360}},
    308: {"zone-308-1": {"x": 514, "y": 128, "angle": 0}, "zone-308-3": {"x": 504, "y": 724, "angle": 0}, "zone-308-2": {"x": 506, "y": 658, "angle": 0}},
    309: {"zone-309-1": {"x": 518, "y": 142, "angle": 0}, "zone-309-2": {"x": 512, "y": 665, "angle": 0}, "zone-309-3": {"x": 506, "y": 724, "angle": 0}},
    310: {"zone-310-1": {"x": 541, "y": 143, "angle": 0}, "zone-310-2": {"x": 540, "y": 440, "angle": 0}, "zone-310-3": {"x": 536, "y": 728, "angle": 0}},
    311: {"zone-311-1": {"x": 282, "y": 168, "angle": 0}, "zone-311-2": {"x": 508, "y": 280, "angle": 271}, "zone-311-3": {"x": 278, "y": 372, "angle": 0}},
    312: {"zone-312-2": {"x": 376, "y": 206, "angle": 270}, "zone-312-1": {"x": 576, "y": 236, "angle": 270}},
    313: {"zone-313-1": {"x": 623, "y": 239, "angle": 271}, "zone-313-2": {"x": 426, "y": 210, "angle": 271}},
    314: {"zone-314-1": {"x": 412, "y": 77, "angle": 0}, "zone-314-2": {"x": 412, "y": 318, "angle": 0}, "zone-314-3": {"x": 406, "y": 379, "angle": 0}},
    315: {"zone-315-1": {"x": 184, "y": 232, "angle": 0}, "zone-315-2": {"x": 190, "y": 442, "angle": 0}, "zone-315-3": {"x": 190, "y": 494, "angle": 0}},
    316: {"zone-316-2": {"x": 396, "y": 376, "angle": 270}},  # Taking the second logged value for zone-2
    317: {"zone-317-1": {"x": 530, "y": 544, "angle": 271}, "zone-317-2": {"x": 384, "y": 338, "angle": 269}, "zone-317-3": {"x": 532, "y": 904, "angle": 0}},
    318: {"zone-318-1": {"x": 379, "y": 573, "angle": 270}, "zone-318-2": {"x": 558, "y": 520, "angle": 1}, "zone-318-3": {"x": 538, "y": 850, "angle": 0}},
    319: {"zone-319-1": {"x": 387, "y": 563, "angle": 270}, "zone-319-2": {"x": 562, "y": 530, "angle": 0}, "zone-319-3": {"x": 541, "y": 844, "angle": 0}},
    320: {"zone-320-1": {"x": 394, "y": 574, "angle": 270}, "zone-320-2": {"x": 580, "y": 518, "angle": 0}, "zone-320-3": {"x": 568, "y": 854, "angle": 0}},
}

print("=" * 60)
print(f"SYNC: Products 292-320 Coordinate Logs")
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
