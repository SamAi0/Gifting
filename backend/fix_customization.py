import os
import sys
import re
import json
import subprocess

LOGS_DATA = """
products/830
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 312, "y": 142, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 304, "y": 296, "angle": 0

/products/831
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 468, "y": 666, "angle": 11
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 540, "y": 478, "angle": 0

/products/832
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 536, "y": 716, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 796, "y": 604, "angle": 0

/products/833
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 630, "y": 606, "angle": 346
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 568, "y": 510, "angle": 0

products/834
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 586, "y": 684, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 496, "y": 478, "angle": 0

products/835
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 586, "y": 712, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 508, "y": 478, "angle": 0

products/836
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 560, "y": 722, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 502, "y": 478, "angle": 0

/products/838
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 470, "y": 642, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 408, "y": 396, "angle": 0

/products/840
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 584, "y": 694, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 494, "y": 454, "angle": 0

products/841
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 560, "y": 606, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 504, "y": 396, "angle": 0

products/842
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 588, "y": 672, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 504, "y": 382, "angle": 0

/products/843
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 846, "y": 526, "angle": 266
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 620, "y": 364, "angle": 0

products/844
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 726, "y": 766, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 320, "y": 710, "angle": 0

products/845
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 580, "y": 584, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 504, "y": 392, "angle": 0

/products/846
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 470, "y": 682, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 354, "y": 420, "angle": 0

products/847
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 880, "y": 558, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 648, "y": 608, "angle": 0

products/848
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 736, "y": 680, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 672, "y": 404, "angle": 0

/products/849
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 578, "y": 714, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 520, "y": 454, "angle": 0

products/850
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 586, "y": 732, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 522, "y": 478, "angle": 0

products/851
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 576, "y": 656, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 508, "y": 436, "angle": 0

/products/852
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 536, "y": 636, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 474, "y": 390, "angle": 0

/products/853
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 632, "y": 638, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 392, "y": 454, "angle": 0

/products/854
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 666, "y": 556, "angle": 246
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 404, "y": 472, "angle": 0

products/855
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 640, "y": 592, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 468, "y": 424, "angle": 0

products/857 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 570, "y": 640, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 508, "y": 396, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

/products/858
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 542, "y": 574, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 470, "y": 394, "angle": 0

products/859
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 558, "y": 574, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 476, "y": 382, "angle": 0

products/860
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 356, "y": 730, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 380, "y": 304, "angle": 0

/products/861
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 634, "y": 770, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 644, "y": 298, "angle": 0

products/862
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 516, "y": 698, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 530, "y": 428, "angle": 0

/products/863
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 636, "y": 862, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 602, "y": 238, "angle": 0

products/864
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 566, "y": 636, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 492, "y": 424, "angle": 0

products/865
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 566, "y": 682, "angle": 272
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 482, "y": 382, "angle": 0

/products/866
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 584, "y": 672, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 488, "y": 404, "angle": 0

products/867
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 642, "y": 684, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 520, "y": 444, "angle": 0

products/868
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 616, "y": 698, "angle": 267
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 528, "y": 298, "angle": 0

/products/869
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 562, "y": 696, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 482, "y": 406, "angle": 0

products/870
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 594, "y": 718, "angle": 268
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 498, "y": 378, "angle": 0

/products/871
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 546, "y": 654, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 476, "y": 414, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

products/872
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 286, "y": 118, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 306, "y": 340, "angle": 01

products/872
CanvasCustomizer.jsx:115  Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 286, "y": 118, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 306, "y": 340, "angle": 0

products/873
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 300, "y": 146, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 320, "y": 366, "angle": 0

/products/874
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 304, "y": 158, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 334, "y": 348, "angle": 0

/products/875
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 308, "y": 122, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 326, "y": 366, "angle": 0

products/876
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 866, "y": 490, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 866, "y": 544, "angle": 0

products/877
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 852, "y": 490, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 840, "y": 546, "angle": 0

/products/878
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 436, "y": 622, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 506, "y": 254, "angle": 0

/products/879
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 466, "y": 608, "angle": 271
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 498, "y": 310, "angle": 0

/products/880
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 466, "y": 626, "angle": 272
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 500, "y": 298, "angle": 0
"""

def parse_logs():
    current_product_id = None
    current_zone_id = None
    updates = {}
    
    for line in LOGS_DATA.split('\n'):
        line = line.strip()
        prod_match = re.search(r"products/(\d+)", line)
        if prod_match:
            current_product_id = int(prod_match.group(1))
            continue
        
        zone_match = re.search(r"Zone Update \[([\w-]+)\]", line)
        if zone_match:
            current_zone_id = zone_match.group(1)
            continue
            
        coord_match = re.search(r'"x":\s*(-?\d+),\s*"y":\s*(-?\d+),\s*"angle":\s*(-?\d+)', line)
        if coord_match and current_product_id and current_zone_id:
            x = int(coord_match.group(1))
            y = int(coord_match.group(2))
            angle = int(coord_match.group(3))
            
            if current_product_id not in updates:
                updates[current_product_id] = {}
            updates[current_product_id][current_zone_id] = {
                'x': x,
                'y': y,
                'angle': angle
            }
    return updates

def main():
    updates = parse_logs()
    
    # Setup Django
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    import django
    django.setup()
    
    from products.models import Product
    
    db_id_to_slug = {}
    for db_id in updates.keys():
        try:
            p = Product.objects.get(id=db_id)
            db_id_to_slug[db_id] = p.slug
        except Product.DoesNotExist:
            print(f"[ERROR] Product {db_id} not found in DB")
            
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    with open(json_path, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
        
    json_slug_to_item = {item.get('slug'): item for item in customization_data if item.get('slug')}
    
    for db_id, zone_updates in updates.items():
        slug = db_id_to_slug.get(db_id)
        if not slug:
            continue
        json_item = json_slug_to_item.get(slug)
        if not json_item:
            continue
        
        zones = json_item.get('zones', [])
        json_zones_by_id = {z.get('id'): z for z in zones if z.get('id')}
        
        for zone_id, new_coords in zone_updates.items():
            z_item = json_zones_by_id.get(zone_id)
            if z_item:
                z_item['x'] = new_coords['x']
                z_item['y'] = new_coords['y']
                z_item['angle'] = new_coords['angle']
                
    # Save customization.json
    print("[INFO] Re-saving customization.json...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(customization_data, f, indent=2, ensure_ascii=False)
    print("[SUCCESS] customization.json saved!")
    
    # Run sync script
    sync_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sync_customization.py')
    subprocess.run([sys.executable, sync_script])
    print("[SUCCESS] SQLite database synced!")

if __name__ == '__main__':
    main()
