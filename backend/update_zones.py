import os
import sys
import json
import django
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

log_data = """
products/791
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 186, "y": 658, "angle": 12
CanvasCustomizer.jsx:117 ---

products/792
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 486, "y": 893, "angle": 360
CanvasCustomizer.jsx:117 -----

products/793
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 381, "y": 448, "angle": 122
CanvasCustomizer.jsx:117 ---

products/794
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 611, "y": 502, "angle": 305
CanvasCustomizer.jsx:117 --

products/795
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 509, "y": 655, "angle": 0
CanvasCustomizer.jsx:117 ------

products/796
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 514, "y": 649, "angle": 0
CanvasCustomizer.jsx:117 -----

products/797
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 532, "y": 649, "angle": 0
CanvasCustomizer.jsx:117 ---

products/798
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 592, "y": 649, "angle": 353
CanvasCustomizer.jsx:117 -----

products/799
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 525, "y": 650, "angle": 0
CanvasCustomizer.jsx:117 ---

products/800
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 468, "y": 839, "angle": 7
CanvasCustomizer.jsx:117 --------------------------

products/801
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 178, "y": 439, "angle": 0
CanvasCustomizer.jsx:117 ---

products/802
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 221, "y": 404, "angle": 0
CanvasCustomizer.jsx:117 ----

products/803
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 179, "y": 459, "angle": 358
CanvasCustomizer.jsx:117 --

products/804
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 498, "y": 861, "angle": 0
CanvasCustomizer.jsx:117 -

products/805
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 515, "y": 776, "angle": 0
CanvasCustomizer.jsx:117 ---

products/806
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 527, "y": 813, "angle": 89
CanvasCustomizer.jsx:117 ---

products/807
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 169, "y": 450, "angle": 145
CanvasCustomizer.jsx:117 --

products/808
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 782, "y": 854, "angle": 352
CanvasCustomizer.jsx:117 --------------------------


products/809
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 419, "y": 584, "angle": 270
CanvasCustomizer.jsx:117 ----


products/810
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 383, "y": 876, "angle": 271
CanvasCustomizer.jsx:117 ---

products/811
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 383, "y": 759, "angle": 270
CanvasCustomizer.jsx:117 --

products/812
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 436, "y": 795, "angle": 270
CanvasCustomizer.jsx:117 -

products/813
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 444, "y": 719, "angle": 269
CanvasCustomizer.jsx:117 --

products/814
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 416, "y": 783, "angle": 269
CanvasCustomizer.jsx:117 ---

products/815
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 416, "y": 812, "angle": 270
CanvasCustomizer.jsx:117 --

products/816
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 422, "y": 804, "angle": 271
CanvasCustomizer.jsx:117 --

products/817
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 430, "y": 778, "angle": 270
CanvasCustomizer.jsx:117 ------

products/818
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 525, "y": 767, "angle": 357
CanvasCustomizer.jsx:117 --

products/819
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 447, "y": 653, "angle": 270
CanvasCustomizer.jsx:117 -

products/820
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 428, "y": 710, "angle": 271
CanvasCustomizer.jsx:117 --

products/821
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 449, "y": 793, "angle": 271
CanvasCustomizer.jsx:117 --------------------------


products/822
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 414, "y": 807, "angle": 270
CanvasCustomizer.jsx:117 -

products/823
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 386, "y": 805, "angle": 270
CanvasCustomizer.jsx:117 --

products/824
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 398, "y": 860, "angle": 270
CanvasCustomizer.jsx:117 ----

products/825
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 451, "y": 654, "angle": 269
CanvasCustomizer.jsx:117 --------------------------

products/826
create zone3 an set placeholder name cup2 Text,set zone 1 placeholder name-Bottle Text,zone2-Cup1 Text
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 386, "y": 747, "angle": 272
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 624, "y": 329, "angle": 270
CanvasCustomizer.jsx:117 --------------------------

products/827
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 435, "y": 740, "angle": 269
CanvasCustomizer.jsx:117 ---

products/828
remove extra text zone
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 441, "y": 747, "angle": 270
CanvasCustomizer.jsx:117 -

products/829
remove extra text zone
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 446, "y": 768, "angle": 270
CanvasCustomizer.jsx:117 ---
"""

updates = {}
current_product_id = None
current_zone = None

for line in log_data.split('\n'):
    line = line.strip()
    if line.startswith('products/'):
        current_product_id = int(line.split('/')[1])
        if current_product_id not in updates:
            updates[current_product_id] = {}
    elif "Zone Update" in line or "zone Update" in line:
        m = re.search(r'\[(.*?)\]', line)
        if m:
            current_zone = m.group(1)
            
    elif '"x":' in line and '"y":' in line and current_zone:
        m_x = re.search(r'"x":\s*([\d\.\-]+)', line)
        m_y = re.search(r'"y":\s*([\d\.\-]+)', line)
        m_a = re.search(r'"angle":\s*([\d\.\-]+)', line)
        if m_x and m_y and m_a:
            updates[current_product_id][current_zone] = {
                "x": float(m_x.group(1)),
                "y": float(m_y.group(1)),
                "angle": float(m_a.group(1))
            }
        current_zone = None

customization_path = os.path.join(BASE_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
customization_path = os.path.abspath(customization_path)

try:
    with open(customization_path, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
except FileNotFoundError:
    print(f"File not found: {customization_path}")
    sys.exit(1)

success_count = 0
for pid, zones in updates.items():
    try:
        product = Product.objects.get(id=pid)
        slug = product.slug
        
        prod_data = next((p for p in customization_data if p.get('slug') == slug), None)
        
        if prod_data:
            print(f"Updating {slug} (ID: {pid})")
            
            # Use index mapping to update zones sequentially
            updated_zone_ids = list(zones.keys())
            for idx, zone_id in enumerate(updated_zone_ids):
                coords = zones[zone_id]
                # Check if zone exists by id
                zone = next((z for z in prod_data.get('zones', []) if z.get('id') == zone_id), None)
                if not zone and idx < len(prod_data.get('zones', [])):
                    # Override by index
                    zone = prod_data['zones'][idx]
                    zone['id'] = zone_id
                    zone['type'] = 'text'
                    print(f"  Overrode zone at index {idx} to {zone_id}")
                
                if zone:
                    zone['x'] = coords['x']
                    zone['y'] = coords['y']
                    zone['angle'] = coords['angle']
                else:
                    print(f"  Zone {zone_id} not found and index {idx} out of bounds.")
            
            # Always truncate extra zones in this batch to match exactly what is provided in the logs
            if updated_zone_ids and len(prod_data.get('zones', [])) > len(updated_zone_ids):
                prod_data['zones'] = prod_data['zones'][:len(updated_zone_ids)]
                print(f"  Truncated zones to {len(updated_zone_ids)} elements.")

            success_count += 1
        else:
            print(f"Product slug {slug} not in customization.json")
    except Product.DoesNotExist:
        print(f"Product with ID {pid} not found in DB")

with open(customization_path, 'w', encoding='utf-8') as f:
    json.dump(customization_data, f, indent=4)

print(f"Done updating customization.json. Successfully processed {success_count} products.")
