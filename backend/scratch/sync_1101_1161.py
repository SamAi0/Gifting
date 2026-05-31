import os, sys, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

# ── Parsed Log Data (1101-1161) ─────────────────────────────────────────────────
LOG_DATA = {
    1101: {"name-1": {"x": 420, "y": 596, "angle": 358}, "extra-1": {"x": 582, "y": 748, "angle": 0}},
    1103: {"name-1": {"x": 490, "y": 580, "angle": 279}},
    1104: {"name-1": {"x": 472, "y": 588, "angle": 280}},
    1105: {"name-1": {"x": 470, "y": 568, "angle": 279}},
    1106: {"name-1": {"x": 486, "y": 620, "angle": 276}},
    1107: {"name-1": {"x": 496, "y": 632, "angle": 278}},
    1108: {"name-1": {"x": 508, "y": 624, "angle": 279}},
    1109: {"name-1": {"x": 482, "y": 640, "angle": 276}},
    1110: {"name-1": {"x": 488, "y": 634, "angle": 279}},
    1111: {"name-1": {"x": 478, "y": 678, "angle": 276}},
    1112: {"name-1": {"x": 492, "y": 644, "angle": 276}},
    1113: {"name-1": {"x": 482, "y": 596, "angle": 278}},
    1114: {"name-1": {"x": 484, "y": 666, "angle": 280}},
    1115: {"name-1": {"x": 472, "y": 612, "angle": 279}},
    1116: {"name-1": {"x": 468, "y": 642, "angle": 279}},
    1117: {"name-1": {"x": 466, "y": 658, "angle": 280}},
    1118: {"name-1": {"x": 468, "y": 650, "angle": 280}},
    1119: {"extra-1": {"x": 462, "y": 312, "angle": 0}},
    1120: {"name-1": {"x": 494, "y": 624, "angle": 279}},
    1121: {"name-1": {"x": 482, "y": 662, "angle": 279}},
    1122: {"name-1": {"x": 478, "y": 654, "angle": 281}},
    1123: {"name-1": {"x": 466, "y": 650, "angle": 278}},
    1124: {"name-1": {"x": 468, "y": 678, "angle": 279}},
    1125: {"name-1": {"x": 466, "y": 678, "angle": 280}},
    1126: {"name-1": {"x": 484, "y": 654, "angle": 278}},
    1127: {"name-1": {"x": 494, "y": 650, "angle": 279}},
    1128: {"name-1": {"x": 466, "y": 654, "angle": 281}},
    1129: {"name-1": {"x": 502, "y": 628, "angle": 279}},
    1130: {"name-1": {"x": 490, "y": 644, "angle": 278}},
    1131: {"name-1": {"x": 472, "y": 590, "angle": 279}},
    1132: {"name-1": {"x": 500, "y": 602, "angle": 279}},
    1133: {"name-1": {"x": 476, "y": 614, "angle": 283}},
    1134: {"name-1": {"x": 486, "y": 662, "angle": 278}},
    1135: {"name-1": {"x": 480, "y": 634, "angle": 279}},
    1136: {"name-1": {"x": 464, "y": 678, "angle": 280}},
    1137: {"name-1": {"x": 468, "y": 658, "angle": 281}},
    1138: {"name-1": {"x": 468, "y": 658, "angle": 281}},
    1139: {"name-1": {"x": 458, "y": 668, "angle": 276}},
    1140: {"name-1": {"x": 478, "y": 670, "angle": 277}},
    1141: {"name-1": {"x": 478, "y": 652, "angle": 277}},
    1142: {"name-1": {"x": 498, "y": 648, "angle": 278}},
    1143: {"name-1": {"x": 486, "y": 652, "angle": 276}},
    1144: {"name-1": {"x": 486, "y": 672, "angle": 277}},
    1145: {"name-1": {"x": 476, "y": 680, "angle": 277}},
    1146: {"name-1": {"x": 450, "y": 588, "angle": 299}},
    1147: {"name-1": {"x": 428, "y": 612, "angle": 299}},
    1148: {"name-1": {"x": 492, "y": 634, "angle": 281}},
    1149: {"name-1": {"x": 474, "y": 618, "angle": 280}},
    1150: {"name-1": {"x": 480, "y": 672, "angle": 278}},
    1151: {"name-1": {"x": 478, "y": 650, "angle": 279}},
    1152: {"name-1": {"x": 308, "y": 532, "angle": 18}},
    1153: {"name-1": {"x": 334, "y": 524, "angle": 36}},
    1154: {"name-1": {"x": 292, "y": 482, "angle": 22}},
    1155: {"name-1": {"x": 490, "y": 646, "angle": 279}},
    1156: {"name-1": {"x": 464, "y": 656, "angle": 279}},
    1157: {"name-1": {"x": 462, "y": 664, "angle": 280}},
    1158: {"name-1": {"x": 484, "y": 672, "angle": 276}},
    1160: {"name-1": {"x": 596, "y": 786, "angle": 346}},
    1161: {"name-1": {"x": 524, "y": 510, "angle": 270}},
}

print("=" * 60)
print(f"SYNC: Products 1101-1161 Coordinate Logs")
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
