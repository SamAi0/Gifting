import os
import sys
import json
import django

sys.path.append(r'd:\Gifting\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

log_updates = {
    61: [{"zoneId": "zone-1", "x": 563, "y": 509, "angle": 350}, {"zoneId": "zone-2", "x": 383, "y": 487, "angle": 268}],
    62: [{"zoneId": "zone-1", "x": 476, "y": 678, "angle": 253}, {"zoneId": "zone-2", "x": 642, "y": 564, "angle": 252}],
    63: [{"zoneId": "zone-1", "x": 490, "y": 644, "angle": 271}, {"zoneId": "zone-2", "x": 722, "y": 596, "angle": 265}],
    64: [{"zoneId": "zone-1", "x": 474, "y": 664, "angle": 254}, {"zoneId": "zone-2", "x": 656, "y": 596, "angle": 254}],
    65: [{"zoneId": "zone-1", "x": 334, "y": 504, "angle": 0}, {"zoneId": "zone-2", "x": 618, "y": 724, "angle": 0}],
    66: [{"zoneId": "zone-1", "x": 376, "y": 584, "angle": 240}, {"zoneId": "zone-2", "x": 703, "y": 557, "angle": 235}],
    67: [{"zoneId": "zone-1", "x": 552, "y": 473, "angle": 258}, {"zoneId": "zone-2", "x": 372, "y": 592, "angle": 256}],
    68: [{"zoneId": "zone-1", "x": 620, "y": 512, "angle": 272}, {"zoneId": "zone-2", "x": 425, "y": 616, "angle": 273}, {"zoneId": "zone-3", "x": 306, "y": 604, "angle": 274}],
    69: [{"zoneId": "zone-1", "x": 696, "y": 552, "angle": 250}, {"zoneId": "zone-2", "x": 275, "y": 457, "angle": 337}, {"zoneId": "zone-3", "x": 347, "y": 680, "angle": 341}],
    70: [{"zoneId": "zone-70-1", "x": 358, "y": 774, "angle": 0}, {"zoneId": "zone-70-2", "x": 738, "y": 483, "angle": 270}, {"zoneId": "zone-70-3", "x": 461, "y": 158, "angle": 0}],
    71: [{"zoneId": "zone-71-1", "x": 488, "y": 206, "angle": 0}, {"zoneId": "zone-71-2", "x": 740, "y": 553, "angle": 267}, {"zoneId": "zone-71-3", "x": 496, "y": 778, "angle": 0}],
    72: [{"zoneId": "zone-72-1", "x": 524, "y": 204, "angle": 0}, {"zoneId": "zone-72-2", "x": 732, "y": 538, "angle": 268}, {"zoneId": "zone-72-3", "x": 524, "y": 770, "angle": 0}],
    73: [{"zoneId": "zone-73-1", "x": 537, "y": 179, "angle": 0}, {"zoneId": "zone-73-2", "x": 785, "y": 611, "angle": 269}, {"zoneId": "zone-73-3", "x": 549, "y": 875, "angle": 0}],
    74: [{"zoneId": "zone-74-1", "x": 534, "y": 186, "angle": 0}, {"zoneId": "zone-74-2", "x": 762, "y": 574, "angle": 267}, {"zoneId": "zone-74-3", "x": 513, "y": 810, "angle": 0}],
    75: [{"zoneId": "zone-75-1", "x": 495, "y": 766, "angle": 0}, {"zoneId": "zone-75-2", "x": 720, "y": 556, "angle": 269}],
    76: [{"zoneId": "zone-76-1", "x": 580, "y": 813, "angle": 0}, {"zoneId": "zone-76-2", "x": 812, "y": 562, "angle": 269}],
    77: [{"zoneId": "zone-77-1", "x": 519, "y": 766, "angle": 0}, {"zoneId": "zone-77-2", "x": 711, "y": 534, "angle": 271}],
    78: [{"zoneId": "zone-78-1", "x": 620, "y": 704, "angle": 0}, {"zoneId": "zone-78-2", "x": 817, "y": 511, "angle": 268}],
    79: [{"zoneId": "zone-79-1", "x": 636, "y": 709, "angle": 0}, {"zoneId": "zone-79-2", "x": 861, "y": 490, "angle": 269}],
    80: [{"zoneId": "zone-80-1", "x": 672, "y": 722, "angle": 0}, {"zoneId": "zone-80-2", "x": 879, "y": 495, "angle": 268}],
    81: [{"zoneId": "zone-81-1", "x": 682, "y": 720, "angle": 0}, {"zoneId": "zone-81-2", "x": 878, "y": 481, "angle": 267}],
    82: [{"zoneId": "zone-82-1", "x": 658, "y": 665, "angle": 329}, {"zoneId": "zone-82-2", "x": 665, "y": 432, "angle": 235}],
    83: [{"zoneId": "zone-83-1", "x": 605, "y": 851, "angle": 0}, {"zoneId": "zone-83-2", "x": 822, "y": 597, "angle": 268}],
    84: [{"zoneId": "zone-84-1", "x": 545, "y": 762, "angle": 0}, {"zoneId": "zone-84-2", "x": 710, "y": 537, "angle": 269}],
    85: [{"zoneId": "zone-85-1", "x": 333, "y": 707, "angle": 0}, {"zoneId": "zone-85-2", "x": 676, "y": 531, "angle": 269}],
    86: [{"zoneId": "zone-86-1", "x": 316, "y": 738, "angle": 0}, {"zoneId": "zone-86-2", "x": 694, "y": 555, "angle": 270}],
    87: [{"zoneId": "zone-87-1", "x": 464, "y": 773, "angle": 0}, {"zoneId": "zone-87-2", "x": 749, "y": 559, "angle": 267}],
    88: [{"zoneId": "zone-88-1", "x": 439, "y": 860, "angle": 0}, {"zoneId": "zone-88-2", "x": 792, "y": 568, "angle": 270}],
    89: [{"zoneId": "zone-89-1", "x": 576, "y": 502, "angle": 0}, {"zoneId": "zone-89-2", "x": 775, "y": 588, "angle": 270}],
    90: [{"zoneId": "zone-90-1", "x": 553, "y": 470, "angle": 0}, {"zoneId": "zone-90-2", "x": 751, "y": 552, "angle": 267}],
    91: [{"zoneId": "zone-91-1", "x": 536, "y": 521, "angle": 0}, {"zoneId": "zone-91-2", "x": 686, "y": 584, "angle": 270}],
    92: [{"zoneId": "zone-92-1", "x": 529, "y": 520, "angle": 359}, {"zoneId": "zone-92-2", "x": 763, "y": 591, "angle": 271}],
    93: [{"zoneId": "zone-93-1", "x": 653, "y": 504, "angle": 0}, {"zoneId": "zone-93-2", "x": 816, "y": 573, "angle": 270}],
    94: [{"zoneId": "zone-94-1", "x": 630, "y": 497, "angle": 0}, {"zoneId": "zone-94-2", "x": 805, "y": 561, "angle": 269}],
    95: [{"zoneId": "zone-95-1", "x": 569, "y": 765, "angle": 0}, {"zoneId": "zone-95-2", "x": 756, "y": 534, "angle": 268}],
    96: [{"zoneId": "zone-96-1", "x": 601, "y": 493, "angle": 0}, {"zoneId": "zone-96-2", "x": 811, "y": 583, "angle": 269}],
    97: [{"zoneId": "zone-97-1", "x": 567, "y": 507, "angle": 0}, {"zoneId": "zone-97-2", "x": 801, "y": 596, "angle": 269}],
    98: [{"zoneId": "zone-98-1", "x": 521, "y": 425, "angle": 0}, {"zoneId": "zone-98-2", "x": 723, "y": 494, "angle": 268}],
    99: [{"zoneId": "zone-99-1", "x": 567, "y": 507, "angle": 4}, {"zoneId": "zone-99-2", "x": 761, "y": 579, "angle": 273}],
    100: [{"zoneId": "zone-100-1", "x": 553, "y": 448, "angle": 341}, {"zoneId": "zone-100-2", "x": 753, "y": 471, "angle": 248}],
}

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
