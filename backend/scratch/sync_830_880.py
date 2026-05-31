import os
import sys
import json
import subprocess

# ── Django Setup ──────────────────────────────────────────────────────────────
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from products.models import Product

# ── Paths (OneDrive - CORRECT project) ────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(BACKEND_DIR), 'frontend')
JSON_PATH    = os.path.join(FRONTEND_DIR, 'src', 'data', 'customization.json')
SYNC_SCRIPT  = os.path.join(BACKEND_DIR, 'sync_customization.py')

print(f"JSON PATH: {JSON_PATH}")
print(f"SYNC SCRIPT: {SYNC_SCRIPT}")

# ── Parsed Log Data (830-880, skipping 837, 839, 856) ─────────────────────────
LOG_DATA = {
    830: {"name-1": {"x": 312, "y": 142, "angle": 0},   "extra-1": {"x": 304, "y": 296, "angle": 0}},
    831: {"name-1": {"x": 468, "y": 666, "angle": 11},  "extra-1": {"x": 540, "y": 478, "angle": 0}},
    832: {"name-1": {"x": 536, "y": 716, "angle": 0},   "extra-1": {"x": 796, "y": 604, "angle": 0}},
    833: {"name-1": {"x": 630, "y": 606, "angle": 346}, "extra-1": {"x": 568, "y": 510, "angle": 0}},
    834: {"name-1": {"x": 586, "y": 684, "angle": 269}, "extra-1": {"x": 496, "y": 478, "angle": 0}},
    835: {"name-1": {"x": 586, "y": 712, "angle": 270}, "extra-1": {"x": 508, "y": 478, "angle": 0}},
    836: {"name-1": {"x": 560, "y": 722, "angle": 271}, "extra-1": {"x": 502, "y": 478, "angle": 0}},
    # 837: MISSING - skipped
    838: {"name-1": {"x": 470, "y": 642, "angle": 270}, "extra-1": {"x": 408, "y": 396, "angle": 0}},
    # 839: MISSING - skipped
    840: {"name-1": {"x": 584, "y": 694, "angle": 269}, "extra-1": {"x": 494, "y": 454, "angle": 0}},
    841: {"name-1": {"x": 560, "y": 606, "angle": 271}, "extra-1": {"x": 504, "y": 396, "angle": 0}},
    842: {"name-1": {"x": 588, "y": 672, "angle": 269}, "extra-1": {"x": 504, "y": 382, "angle": 0}},
    843: {"name-1": {"x": 846, "y": 526, "angle": 266}, "extra-1": {"x": 620, "y": 364, "angle": 0}},
    844: {"name-1": {"x": 726, "y": 766, "angle": 269}, "extra-1": {"x": 320, "y": 710, "angle": 0}},
    845: {"name-1": {"x": 580, "y": 584, "angle": 268}, "extra-1": {"x": 504, "y": 392, "angle": 0}},
    846: {"name-1": {"x": 470, "y": 682, "angle": 268}, "extra-1": {"x": 354, "y": 420, "angle": 0}},
    847: {"name-1": {"x": 880, "y": 558, "angle": 268}, "extra-1": {"x": 648, "y": 608, "angle": 0}},
    848: {"name-1": {"x": 736, "y": 680, "angle": 268}, "extra-1": {"x": 672, "y": 404, "angle": 0}},
    849: {"name-1": {"x": 578, "y": 714, "angle": 269}, "extra-1": {"x": 520, "y": 454, "angle": 0}},
    850: {"name-1": {"x": 586, "y": 732, "angle": 269}, "extra-1": {"x": 522, "y": 478, "angle": 0}},
    851: {"name-1": {"x": 576, "y": 656, "angle": 271}, "extra-1": {"x": 508, "y": 436, "angle": 0}},
    852: {"name-1": {"x": 536, "y": 636, "angle": 271}, "extra-1": {"x": 474, "y": 390, "angle": 0}},
    853: {"name-1": {"x": 632, "y": 638, "angle": 270}, "extra-1": {"x": 392, "y": 454, "angle": 0}},
    854: {"name-1": {"x": 666, "y": 556, "angle": 246}, "extra-1": {"x": 404, "y": 472, "angle": 0}},
    855: {"name-1": {"x": 640, "y": 592, "angle": 269}, "extra-1": {"x": 468, "y": 424, "angle": 0}},
    # 856: MISSING - skipped
    857: {"name-1": {"x": 570, "y": 640, "angle": 269}, "extra-1": {"x": 508, "y": 396, "angle": 0}},
    858: {"name-1": {"x": 542, "y": 574, "angle": 271}, "extra-1": {"x": 470, "y": 394, "angle": 0}},
    859: {"name-1": {"x": 558, "y": 574, "angle": 271}, "extra-1": {"x": 476, "y": 382, "angle": 0}},
    860: {"name-1": {"x": 356, "y": 730, "angle": 0},   "extra-1": {"x": 380, "y": 304, "angle": 0}},
    861: {"name-1": {"x": 634, "y": 770, "angle": 0},   "extra-1": {"x": 644, "y": 298, "angle": 0}},
    862: {"name-1": {"x": 516, "y": 698, "angle": 0},   "extra-1": {"x": 530, "y": 428, "angle": 0}},
    863: {"name-1": {"x": 636, "y": 862, "angle": 0},   "extra-1": {"x": 602, "y": 238, "angle": 0}},
    864: {"name-1": {"x": 566, "y": 636, "angle": 271}, "extra-1": {"x": 492, "y": 424, "angle": 0}},
    865: {"name-1": {"x": 566, "y": 682, "angle": 272}, "extra-1": {"x": 482, "y": 382, "angle": 0}},
    866: {"name-1": {"x": 584, "y": 672, "angle": 270}, "extra-1": {"x": 488, "y": 404, "angle": 0}},
    867: {"name-1": {"x": 642, "y": 684, "angle": 270}, "extra-1": {"x": 520, "y": 444, "angle": 0}},
    868: {"name-1": {"x": 616, "y": 698, "angle": 267}, "extra-1": {"x": 528, "y": 298, "angle": 0}},
    869: {"name-1": {"x": 562, "y": 696, "angle": 270}, "extra-1": {"x": 482, "y": 406, "angle": 0}},
    870: {"name-1": {"x": 594, "y": 718, "angle": 268}, "extra-1": {"x": 498, "y": 378, "angle": 0}},
    871: {"name-1": {"x": 546, "y": 654, "angle": 270}, "extra-1": {"x": 476, "y": 414, "angle": 0}},
    872: {"name-1": {"x": 286, "y": 118, "angle": 0},   "extra-1": {"x": 306, "y": 340, "angle": 0}},
    873: {"name-1": {"x": 300, "y": 146, "angle": 0},   "extra-1": {"x": 320, "y": 366, "angle": 0}},
    874: {"name-1": {"x": 304, "y": 158, "angle": 0},   "extra-1": {"x": 334, "y": 348, "angle": 0}},
    875: {"name-1": {"x": 308, "y": 122, "angle": 0},   "extra-1": {"x": 326, "y": 366, "angle": 0}},
    876: {"name-1": {"x": 866, "y": 490, "angle": 0},   "extra-1": {"x": 866, "y": 544, "angle": 0}},
    877: {"name-1": {"x": 852, "y": 490, "angle": 0},   "extra-1": {"x": 840, "y": 546, "angle": 0}},
    878: {"name-1": {"x": 436, "y": 622, "angle": 271}, "extra-1": {"x": 506, "y": 254, "angle": 0}},
    879: {"name-1": {"x": 466, "y": 608, "angle": 271}, "extra-1": {"x": 498, "y": 310, "angle": 0}},
    880: {"name-1": {"x": 466, "y": 626, "angle": 272}, "extra-1": {"x": 500, "y": 298, "angle": 0}},
}

print("=" * 60)
print("SYNC: Products 830-880 (OneDrive - CORRECT project)")
print(f"Total: {len(LOG_DATA)} products | Skipped: 837, 839, 856")
print("=" * 60)

# ── Step 1: Map DB IDs to Slugs ───────────────────────────────────────────────
print("\n[STEP 1] Mapping DB IDs to slugs...")
id_to_slug = {}
for db_id in LOG_DATA:
    try:
        product = Product.objects.get(id=db_id)
        id_to_slug[db_id] = product.slug
    except Product.DoesNotExist:
        print(f"  [SKIP] ID {db_id} not found in DB")
print(f"Mapped: {len(id_to_slug)} products")

# ── Step 2: Load customization.json ──────────────────────────────────────────
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    cust_data = json.load(f)
print(f"\n[STEP 2] Loaded {len(cust_data)} entries from customization.json")

slug_index = {item['slug']: i for i, item in enumerate(cust_data) if 'slug' in item}

# ── Step 3: Update Zones ──────────────────────────────────────────────────────
print("\n[STEP 3] Updating zones...")
updated_count = 0
zone_miss = []

for db_id, zone_updates in LOG_DATA.items():
    slug = id_to_slug.get(db_id)
    if not slug:
        continue
    if slug not in slug_index:
        print(f"  [NOT IN JSON] '{slug}' (ID {db_id})")
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
    print(f"  [OK] ID {db_id} '{slug}' -> zones: {updated_zones}")

# ── Step 4: Save ──────────────────────────────────────────────────────────────
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(cust_data, f, indent=2, ensure_ascii=False)
print(f"\n[STEP 4] SAVED: {updated_count} products to {JSON_PATH}")

# ── Step 5: DB Sync ───────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("[STEP 5] Running sync_customization.py...")
print("=" * 60)
try:
    result = subprocess.run(
        [sys.executable, SYNC_SCRIPT],
        capture_output=True, text=True, check=True,
        cwd=BACKEND_DIR
    )
    lines = result.stdout.strip().split('\n')
    for line in lines[-10:]:
        print(line)
    print("\n[SUCCESS] SQLite DB sync complete!")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Sync failed:\n{e.stderr}")
    sys.exit(1)

print("\n" + "=" * 60)
print(f"DONE: {updated_count} products updated | Zone mismatches: {len(zone_miss)}")
print("=" * 60)
