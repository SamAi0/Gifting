import os, sys, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

# ── Parsed Log Data (501-549) ─────────────────────────────────────────────────
# Note: action="delete" used for zones that need removal (e.g., 521, 522).
LOG_DATA = {
    501: {"name-1": {"x": 440, "y": 688, "angle": 334}},
    502: {"name-1": {"x": 284, "y": 664, "angle": 330}},
    503: {"name-1": {"x": 272, "y": 660, "angle": 332}},
    504: {"name-1": {"x": 244, "y": 502, "angle": 21}},
    505: {"name-1": {"x": 188, "y": 734, "angle": 47}},
    506: {"name-1": {"x": 302, "y": 684, "angle": 348}},
    507: {"name-1": {"x": 352, "y": 704, "angle": 342}},
    508: {"name-1": {"x": 496, "y": 750, "angle": 10}},
    510: {"name-1": {"x": 476, "y": 446, "angle": 316}},
    511: {"name-1": {"x": 500, "y": 632, "angle": 274}},
    512: {"name-1": {"x": 478, "y": 620, "angle": 3}, "logo-1": {"x": 784, "y": 634, "angle": 0}},
    513: {"name-1": {"x": 376, "y": 624, "angle": 0}, "logo-1": {"x": 700, "y": 610, "angle": 0}},
    514: {"name-1": {"x": 364, "y": 640, "angle": 0}, "logo-1": {"x": 730, "y": 636, "angle": 0}},
    515: {"logo-1": {"x": 526, "y": 394, "angle": 0}, "name-1": {"x": 760, "y": 394, "angle": 1}},
    516: {"name-1": {"x": 504, "y": 616, "angle": 0}, "logo-1": {"x": 158, "y": 556, "angle": 0}},
    517: {"name-1": {"x": 388, "y": 538, "angle": 0}},
    518: {"name-1": {"x": 440, "y": 584, "angle": 316}},
    519: {"name-1": {"x": 382, "y": 592, "angle": 320}},
    520: {"name-1": {"x": 374, "y": 622, "angle": 317}},
    521: {"name-1": {"x": 520, "y": 726, "angle": 276}, "extra-1": {"action": "delete"}},
    522: {"name-1": {"x": 548, "y": 722, "angle": 270}, "extra-1": {"action": "delete"}},
    523: {"name-1": {"x": 452, "y": 728, "angle": 270}},
    524: {"name-1": {"x": 548, "y": 726, "angle": 272}},
    525: {"name-1": {"x": 464, "y": 748, "angle": 271}},
    526: {"name-1": {"x": 434, "y": 776, "angle": 272}},
    527: {"name-1": {"x": 424, "y": 684, "angle": 271}},
    528: {"name-1": {"x": 444, "y": 756, "angle": 272}},
    529: {"name-1": {"x": 422, "y": 704, "angle": 270}},
    530: {"name-1": {"x": 432, "y": 692, "angle": 0}, "extra-1": {"x": 432, "y": 554, "angle": 0}},
    531: {"name-1": {"x": 446, "y": 554, "angle": 0}, "extra-1": {"x": 450, "y": 688, "angle": 0}},
    532: {"name-1": {"x": 510, "y": 448, "angle": 0}, "extra-1": {"x": 516, "y": 360, "angle": 0}},
    533: {"name-1": {"x": 410, "y": 528, "angle": 0}, "extra-1": {"x": 420, "y": 616, "angle": 0}},
    534: {"extra-1": {"x": 152, "y": 566, "angle": 269}, "name-1": {"x": 344, "y": 348, "angle": 0}},
    535: {"name-1": {"x": 380, "y": 302, "angle": 0}, "extra-1": {"x": 368, "y": 798, "angle": 0}},
    536: {"name-1": {"x": 364, "y": 244, "angle": 0}, "extra-1": {"x": 322, "y": 822, "angle": 0}},
    537: {"name-1": {"x": 346, "y": 176, "angle": 0}, "extra-1": {"x": 300, "y": 832, "angle": 0}},
    538: {"name-1": {"x": 398, "y": 338, "angle": 0}, "extra-1": {"x": 402, "y": 456, "angle": 0}},
    539: {"name-1": {"x": 508, "y": 398, "angle": 0}, "extra-1": {"x": 504, "y": 530, "angle": 0}},
    540: {"name-1": {"x": 546, "y": 352, "angle": 0}, "extra-1": {"x": 562, "y": 482, "angle": 0}},
    541: {"name-1": {"x": 620, "y": 446, "angle": 0}, "extra-1": {"x": 606, "y": 650, "angle": 0}},
    542: {"name-1": {"x": 368, "y": 432, "angle": 0}, "extra-1": {"x": 370, "y": 676, "angle": 0}},
    543: {"name-1": {"x": 370, "y": 452, "angle": 0}, "extra-1": {"x": 372, "y": 562, "angle": 0}},
    544: {"name-1": {"x": 492, "y": 416, "angle": 0}, "extra-1": {"x": 502, "y": 580, "angle": 0}},
    545: {"name-1": {"x": 450, "y": 324, "angle": 0}, "extra-1": {"x": 442, "y": 494, "angle": 0}},
    546: {"name-1": {"x": 407, "y": 442, "angle": 0}, "extra-1": {"x": 426, "y": 631, "angle": 0}},
    547: {"name-1": {"x": 500, "y": 400, "angle": 0}, "extra-1": {"x": 504, "y": 496, "angle": 0}},
    548: {"name-1": {"x": 496, "y": 404, "angle": 0}, "extra-1": {"x": 500, "y": 700, "angle": 0}},
    549: {"name-1": {"x": 636, "y": 304, "angle": 0}, "extra-1": {"x": 644, "y": 514, "angle": 0}},
}

print("=" * 60)
print(f"SYNC: Products 501-549 Coordinate Logs")
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
    
    updated_actions = []

    for zone_id, coords in zone_updates.items():
        if coords.get("action") == "delete":
            if zone_id in zone_id_map:
                del zone_id_map[zone_id]
                updated_actions.append(f"DELETED {zone_id}")
        else:
            if zone_id in zone_id_map:
                zone_id_map[zone_id]['x'] = coords['x']
                zone_id_map[zone_id]['y'] = coords['y']
                zone_id_map[zone_id]['angle'] = coords['angle']
                updated_actions.append(f"UPDATED {zone_id}")
            else:
                zone_miss.append((db_id, slug, zone_id))
                print(f"  [ZONE MISSING] ID {db_id} '{slug}' - zone '{zone_id}'")

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

print("\n" + "=" * 60)
print(f"DONE: {updated_count} products | Zone mismatches: {len(zone_miss)}")
if zone_miss:
    for db_id, slug, zid in zone_miss:
        print(f"  -> ID {db_id} '{slug}' zone '{zid}'")
print("=" * 60)
