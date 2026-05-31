import os, sys, json, subprocess
import copy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

# ── Parsed Log Data (1001-1100) ─────────────────────────────────────────────────
LOG_DATA = {
    1001: {"name-1": {"x": 493, "y": 209, "angle": 0}, "extra-1": {"x": 501, "y": 425, "angle": 0}},
    1002: {"extra-1": {"x": 473, "y": 504, "angle": 0}, "name-1": {"x": 475, "y": 282, "angle": 0}},
    1003: {"extra-1": {"x": 500, "y": 585, "angle": 348}, "name-1": {"x": 463, "y": 318, "angle": 353}},
    1004: {"extra-1": {"x": 336, "y": 426, "angle": 0}, "name-1": {"x": 614, "y": 300, "angle": 4}},
    1005: {"extra-1": {"x": 506, "y": 415, "angle": 0}, "name-1": {"x": 504, "y": 190, "angle": 359}},
    1006: {"name-1": {"x": 556, "y": 201, "angle": 0}, "extra-1": {"x": 564, "y": 499, "angle": 0}},
    1007: {"name-1": {"x": 497, "y": 223, "angle": 0}, "extra-1": {"x": 496, "y": 567, "angle": 0}},
    1008: {"name-1": {"x": 488, "y": 234, "angle": 0}, "extra-1": {"x": 482, "y": 513, "angle": 0}},
    1009: {"name-1": {"x": 528, "y": 144, "angle": 0}, "extra-1": {"x": 525, "y": 601, "angle": 0}},
    1010: {"extra-1": {"x": 490, "y": 460, "angle": 0}, "name-1": {"x": 481, "y": 109, "angle": 0}},
    1011: {"name-1": {"x": 498, "y": 207, "angle": 0}, "extra-1": {"x": 502, "y": 683, "angle": 0}},
    1012: {"name-1": {"x": 508, "y": 241, "angle": 0}, "extra-1": {"x": 504, "y": 578, "angle": 0}},
    1013: {"name-1": {"x": 495, "y": 224, "angle": 0}, "extra-1": {"x": 503, "y": 622, "angle": 0}},
    1014: {"name-1": {"x": 489, "y": 234, "angle": 0}, "extra-1": {"x": 463, "y": 608, "angle": 0}},
    1015: {"name-1": {"x": 467, "y": 233, "angle": 0}, "extra-1": {"x": 475, "y": 605, "angle": 0}},
    1016: {"name-1": {"x": 521, "y": 285, "angle": 0}, "extra-1": {"x": 486, "y": 567, "angle": 0}},
    1017: {"name-1": {"x": 477, "y": 199, "angle": 0}, "extra-1": {"x": 486, "y": 692, "angle": 0}},
    1018: {"extra-1": {"x": 484, "y": 608, "angle": 0}, "name-1": {"x": 481, "y": 272, "angle": 0}},
    1019: {"name-1": {"x": 497, "y": 255, "angle": 0}, "extra-1": {"x": 389, "y": 622, "angle": 0}},
    1020: {"extra-1": {"x": 380, "y": 676, "angle": 0}, "name-1": {"x": 387, "y": 254, "angle": 0}},
    1021: {"extra-1": {"x": 366, "y": 606, "angle": 0}, "name-1": {"x": 590, "y": 455, "angle": 0}},
    1022: {"extra-1": {"x": 191, "y": 568, "angle": 0}, "name-1": {"x": 631, "y": 168, "angle": 0}},
    1023: {"name-1": {"x": 614, "y": 176, "angle": 0}, "extra-1": {"x": 210, "y": 533, "angle": 0}},
    1024: {"extra-1": {"x": 206, "y": 586, "angle": 0}, "name-1": {"x": 605, "y": 222, "angle": 0}},
    1025: {"extra-1": {"x": 134, "y": 553, "angle": 0}, "name-1": {"x": 651, "y": 141, "angle": 0}},
    1026: {"extra-1": {"x": 195, "y": 565, "angle": 0}, "name-1": {"x": 620, "y": 167, "angle": 0}},
    1027: {"extra-1": {"x": 763, "y": 488, "angle": 0}, "name-1": {"x": 589, "y": 475, "angle": 0}},
    1028: {"name-1": {"x": 454, "y": 734, "angle": 279}, "extra-1": {"x": 513, "y": 472, "angle": 97}},
    1029: {"name-1": {"x": 435, "y": 767, "angle": 0}, "extra-1": {"x": 488, "y": 442, "angle": 279}},
    1030: {"name-1": {"x": 548, "y": 199, "angle": 0}, "extra-1": {"x": 453, "y": 654, "angle": 285}},
    1031: {"name-1": {"x": 438, "y": 765, "angle": 0}, "extra-1": {"x": 491, "y": 479, "angle": 284}},
    1032: {"extra-1": {"x": 460, "y": 632, "angle": 284}, "name-1": {"x": 524, "y": 255, "angle": 0}},
    1033: {"name-1": {"x": 551, "y": 202, "angle": 0}, "extra-1": {"x": 484, "y": 543, "angle": 282}},
    1034: {"extra-1": {"x": 459, "y": 618, "angle": 285}},
    1035: {"name-1": {"x": 242, "y": 838, "angle": 0}, "extra-1": {"x": 541, "y": 830, "angle": 0}},
    1036: {"name-1": {"x": 536, "y": 259, "angle": 0}, "extra-1": {"x": 475, "y": 663, "angle": 278}},
    1037: {"name-1": {"x": 527, "y": 217, "angle": 0}, "extra-1": {"x": 473, "y": 603, "angle": 277}},
    1038: {"name-1": {"x": 559, "y": 214, "angle": 0}, "extra-1": {"x": 475, "y": 645, "angle": 284}},
    1039: {"name-1": {"x": 529, "y": 219, "angle": 0}, "extra-1": {"x": 465, "y": 653, "angle": 275}},
    1040: {"name-1": {"x": 546, "y": 192, "angle": 0}, "extra-1": {"x": 490, "y": 588, "angle": 281}},
    1041: {"name-1": {"x": 527, "y": 248, "angle": 0}, "extra-1": {"x": 481, "y": 559, "angle": 281}},
    1042: {"name-1": {"x": 569, "y": 209, "angle": 0}, "extra-1": {"x": 475, "y": 637, "angle": 279}},
    1043: {"name-1": {"x": 553, "y": 235, "angle": 0}, "extra-1": {"x": 505, "y": 611, "angle": 275}},
    1044: {"name-1": {"x": 552, "y": 210, "angle": 0}, "extra-1": {"x": 487, "y": 579, "angle": 283}},
    1045: {"name-1": {"x": 534, "y": 189, "angle": 0}, "extra-1": {"x": 472, "y": 597, "angle": 276}},
    1046: {"name-1": {"x": 540, "y": 192, "angle": 0}, "extra-1": {"x": 489, "y": 574, "angle": 278}},
    1047: {"name-1": {"x": 551, "y": 216, "angle": 0}, "extra-1": {"x": 495, "y": 615, "angle": 284}},
    1048: {"name-1": {"x": 537, "y": 212, "angle": 0}, "extra-1": {"x": 484, "y": 591, "angle": 280}},
    1049: {"name-1": {"x": 553, "y": 259, "angle": 0}, "extra-1": {"x": 490, "y": 643, "angle": 276}},
    1050: {"name-1": {"x": 553, "y": 234, "angle": 0}, "extra-1": {"x": 481, "y": 686, "angle": 275}},
    1051: {"name-1": {"x": 519, "y": 190, "angle": 0}, "extra-1": {"x": 459, "y": 630, "angle": 280}},
    1052: {"name-1": {"x": 534, "y": 230, "angle": 0}, "extra-1": {"x": 469, "y": 662, "angle": 277}},
    1053: {"name-1": {"x": 533, "y": 245, "angle": 0}, "extra-1": {"x": 467, "y": 674, "angle": 280}},
    1054: {"extra-1": {"x": 493, "y": 480, "angle": 0}, "name-1": {"x": 567, "y": 357, "angle": 0}},
    1055: {"name-1": {"x": 539, "y": 239, "angle": 0}, "extra-1": {"x": 469, "y": 627, "angle": 278}},
    1056: {"name-1": {"x": 539, "y": 225, "angle": 0}, "extra-1": {"x": 472, "y": 598, "angle": 281}},
    1057: {"name-1": {"x": 553, "y": 242, "angle": 0}, "extra-1": {"x": 462, "y": 686, "angle": 280}},
    1058: {"name-1": {"x": 540, "y": 256, "angle": 0}, "extra-1": {"x": 482, "y": 637, "angle": 277}},
    1059: {"name-1": {"x": 532, "y": 241, "angle": 0}, "extra-1": {"x": 480, "y": 542, "angle": 277}},
    1060: {"name-1": {"x": 529, "y": 230, "angle": 0}, "extra-1": {"x": 473, "y": 665, "angle": 279}},
    1061: {"name-1": {"x": 531, "y": 229, "angle": 0}, "extra-1": {"x": 461, "y": 682, "angle": 276}},
    1062: {"name-1": {"x": 511, "y": 207, "angle": 0}, "extra-1": {"x": 473, "y": 667, "angle": 273}},
    1063: {"name-1": {"x": 554, "y": 171, "angle": 0}, "extra-1": {"x": 461, "y": 673, "angle": 283}},
    1064: {"name-1": {"x": 542, "y": 230, "angle": 0}, "extra-1": {"x": 342, "y": 497, "angle": 280}},
    1065: {"name-1": {"x": 532, "y": 219, "angle": 0}, "extra-1": {"x": 467, "y": 618, "angle": 282}},
    1066: {"name-1": {"x": 515, "y": 247, "angle": 0}, "extra-1": {"x": 515, "y": 647, "angle": 0}},
    1067: {"name-1": {"x": 320, "y": 243, "angle": 0}, "extra-1": {"x": 693, "y": 585, "angle": 0}},
    1068: {"name-1": {"x": 492, "y": 273, "angle": 0}, "extra-1": {"x": 497, "y": 493, "angle": 0}},
    1069: {"name-1": {"x": 484, "y": 221, "angle": 0}, "extra-1": {"x": 484, "y": 519, "angle": 0}},
    1070: {"name-1": {"x": 500, "y": 791, "angle": 0}, "extra-1": {"x": 516, "y": 295, "angle": 0}},
    1071: {"name-1": {"x": 463, "y": 225, "angle": 0}, "extra-1": {"x": 452, "y": 466, "angle": 0}},
    1072: {"extra-1": {"x": 458, "y": 692, "angle": 278}, "name-1": {"x": 494, "y": 290, "angle": 0}},
    1073: {"extra-1": {"x": 464, "y": 669, "angle": 278}, "name-1": {"x": 498, "y": 233, "angle": 0}},
    1074: {"name-1": {"x": 506, "y": 238, "angle": 0}, "extra-1": {"x": 464, "y": 652, "angle": 275}},
    1075: {"name-1": {"x": 547, "y": 234, "angle": 0}, "extra-1": {"x": 459, "y": 675, "angle": 279}},
    1076: {"name-1": {"x": 525, "y": 253, "angle": 0}, "extra-1": {"x": 476, "y": 666, "angle": 283}},
    1077: {"name-1": {"x": 512, "y": 262, "angle": 0}, "extra-1": {"x": 476, "y": 701, "angle": 277}},
    1078: {"name-1": {"x": 516, "y": 247, "angle": 0}, "extra-1": {"x": 473, "y": 719, "angle": 276}},
    1079: {"name-1": {"x": 525, "y": 262, "angle": 0}, "extra-1": {"x": 459, "y": 722, "angle": 280}},
    1080: {"extra-1": {"x": 445, "y": 693, "angle": 277}, "name-1": {"x": 519, "y": 259, "angle": 0}},
    1081: {"name-1": {"x": 488, "y": 614, "angle": 281}},
    1082: {"name-1": {"x": 474, "y": 656, "angle": 280}},
    1083: {"name-1": {"x": 496, "y": 624, "angle": 275}},
    1084: {"name-1": {"x": 650, "y": 582, "angle": 0}},
    1085: {"name-1": {"x": 372, "y": 616, "angle": 269}},
    1086: {"name-1": {"x": 392, "y": 628, "angle": 270}},
    1087: {"name-1": {"x": 404, "y": 598, "angle": 270}},
    1088: {"name-1": {"x": 378, "y": 632, "angle": 271}},
    1089: {"name-1": {"x": 482, "y": 600, "angle": 280}},
    1090: {"name-1": {"x": 488, "y": 584, "angle": 279}},
    1091: {"name-1": {"x": 486, "y": 646, "angle": 276}},
    1092: {"name-1": {"x": 476, "y": 654, "angle": 275}},
    1093: {"name-1": {"x": 500, "y": 664, "angle": 275}},
    1094: {"name-1": {"x": 492, "y": 688, "angle": 275}},
    1095: {"name-1": {"x": 484, "y": 658, "angle": 278}},
    1096: {"name-1": {"x": 458, "y": 660, "angle": 278}},
    1097: {"extra-1": {"x": 732, "y": 364, "angle": 328}, "name-1": {"x": 346, "y": 518, "angle": 0}},
    1098: {"name-1": {"x": 295, "y": 491, "angle": 0}, "extra-1": {"x": 375, "y": 713, "angle": 337}},
    1099: {"name-1": {"x": 324, "y": 284, "angle": 0}, "extra-1": {"x": 464, "y": 670, "angle": 77}},
    1100: {"extra-1": {"x": 448, "y": 646, "angle": 75}, "name-1": {"x": 290, "y": 338, "angle": 340}},
}

print("=" * 60)
print(f"SYNC: Products 1001-1100 Coordinate Logs")
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

# Helper to create an extra zone
def create_extra_zone(zone_id, font_size):
    return {
        "id": zone_id,
        "type": "text",
        "x": 500,
        "y": 500,
        "originX": "center",
        "originY": "center",
        "angle": 0,
        "maxWidth": 200,
        "maxChars": 15,
        "fontFamily": "Inter, sans-serif",
        "fontSize": font_size,
        "minFontSize": font_size,
        "fill": "#000000",
        "opacity": 0.9,
        "placeholder": f"ZONE TEXT"
    }

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
        if zone_id in zone_id_map:
            zone_id_map[zone_id]['x'] = coords['x']
            zone_id_map[zone_id]['y'] = coords['y']
            zone_id_map[zone_id]['angle'] = coords['angle']
            updated_actions.append(f"UPDATED {zone_id}")
        else:
            zone_miss.append((db_id, slug, zone_id))
            print(f"  [ZONE MISSING] ID {db_id} '{slug}' - zone '{zone_id}'")

    # Add extra zones for 1097-1100
    if db_id in [1097, 1098, 1099, 1100]:
        font_size = 9 if db_id == 1098 else 10
        if "extra-2" not in zone_id_map:
            zone_id_map["extra-2"] = create_extra_zone("extra-2", font_size)
            updated_actions.append(f"ADDED extra-2 (font {font_size})")
        if "extra-3" not in zone_id_map:
            zone_id_map["extra-3"] = create_extra_zone("extra-3", font_size)
            updated_actions.append(f"ADDED extra-3 (font {font_size})")

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
