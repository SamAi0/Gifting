import json
import re
import os
import sys
import django

# Setup Django settings
sys.path.append(r"C:\Users\Asus\Downloads\New folder\Gifting\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Absolute path to the customization JSON file
JSON_PATH = r"C:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"

# Raw logs pasted by the user
raw_logs = """
products/789
 Zone Update [name-1] 
VM219:58 "x": 582, "y": 1018, "angle": 0
VM219:58 --------------------------
VM219:58  Zone Update [extra-1] 
VM219:58 "x": 599, "y": 370, "angle": 0
VM219:58 --------------------------

products/788
 Zone Update [name-1] 
VM219:58 "x": 638, "y": 776, "angle": 357
VM219:58 --------------------------
VM219:58  Zone Update [extra-1] 
VM219:58 "x": 198, "y": 650, "angle": 21
VM219:58 --------------------------
VM219:58  Zone Update [extra-2] 
VM219:58 "x": 570, "y": 338, "angle": 351
VM219:58 --------------------------


products/787
 Zone Update [name-1] 
VM495:58 "x": 819, "y": 580, "angle": 351
VM495:58 --------------------------
VM495:58  Zone Update [extra-1] 
VM495:58 "x": 453, "y": 814, "angle": 350
VM495:58 --------------------------
VM495:58  Zone Update [extra-2] 
VM495:58 "x": 142, "y": 699, "angle": 26
VM495:58 --------------------------

products/785
Zone Update [name-1] 
VM495:58 "x": 486, "y": 874, "angle": 360

products/784
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 378, "y": 611, "angle": 315
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 833, "y": 686, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 820, "y": 786, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

products/783
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 267, "y": 580, "angle": 18
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 778, "y": 328, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 782, "y": 450, "angle": 0
CanvasCustomizer.jsx:117 --------------------------

products/781
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 602, "y": 512, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 782, "y": 702, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 791, "y": 812, "angle": 0

products/780
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 583, "y": 508, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 782, "y": 683, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 772, "y": 805, "angle": 0


products/779
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 618, "y": 435, "angle": 329
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 842, "y": 593, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 839, "y": 680, "angle": 0

/products/778
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 502, "y": 501, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 804, "y": 622, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 814, "y": 722, "angle": 0


products/777
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 496, "y": 507, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 791, "y": 641, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 798, "y": 744, "angle": 0
"""

def parse_logs(logs_text):
    updates = []
    current_product_db_id = None
    current_zone = None
    
    lines = logs_text.strip().split("\n")
    for line_num, line in enumerate(lines, 1):
        # 1. Look for product ID (from DB)
        product_match = re.search(r"products/(\d+)", line)
        if product_match:
            current_product_db_id = int(product_match.group(1))
            current_zone = None
            continue
            
        # 2. Look for zone name
        zone_match = re.search(r"Zone Update\s+\[([^\]]+)\]", line)
        if zone_match:
            current_zone = zone_match.group(1)
            continue
            
        # 3. Look for coordinates
        coords_match = re.search(r'"x":\s*(-?\d+),\s*"y":\s*(-?\d+),\s*"angle":\s*(-?\d+)', line)
        if coords_match:
            if current_product_db_id is None:
                print(f"[Warning] Found coordinates on line {line_num} but no product ID has been set yet!")
                continue
            if current_zone is None:
                print(f"[Warning] Found coordinates for product {current_product_db_id} on line {line_num} but no Zone name has been set yet!")
                continue
                
            x = int(coords_match.group(1))
            y = int(coords_match.group(2))
            angle = int(coords_match.group(3))
            
            updates.append({
                "db_id": current_product_db_id,
                "zoneId": current_zone,
                "x": x,
                "y": y,
                "angle": angle
            })
            current_zone = None
            
    return updates

def apply_updates():
    print("Parsing logs...")
    parsed_updates = parse_logs(raw_logs)
    print(f"Successfully parsed {len(parsed_updates)} zone updates.")

    # Get unique DB IDs from parsed updates
    db_ids = {u["db_id"] for u in parsed_updates}
    
    # Query database to get mapping from db_id -> slug
    print("Querying SQLite database to map product IDs to slugs...")
    db_products = Product.objects.filter(id__in=db_ids)
    db_map = {p.id: (p.slug, p.name) for p in db_products}
    
    # Map parsed updates to slugs
    valid_updates = []
    for u in parsed_updates:
        db_id = u["db_id"]
        if db_id not in db_map:
            print(f"[Error] Product with DB ID {db_id} not found in the SQLite database!")
            continue
        slug, name = db_map[db_id]
        u["slug"] = slug
        u["productName"] = name
        valid_updates.append(u)

    if not valid_updates:
        print("No valid updates found to apply!")
        return

    # Check if customization file exists
    if not os.path.exists(JSON_PATH):
        print(f"Error: JSON file not found at {JSON_PATH}")
        return

    print(f"Loading customization.json from {JSON_PATH}...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Index JSON products by slug for perfect mapping
    products_by_slug = {item.get("slug"): item for item in data if "slug" in item}

    updated_count = 0
    not_found_slugs = set()
    not_found_zones = []

    for update in valid_updates:
        slug = update["slug"]
        z_id = update["zoneId"]
        
        if slug not in products_by_slug:
            not_found_slugs.add(slug)
            continue
            
        product = products_by_slug[slug]
        zones = product.get("zones", [])
        
        # Find the zone by ID
        zone_found = False
        for zone in zones:
            if zone.get("id") == z_id:
                # Apply updates
                zone["x"] = update["x"]
                zone["y"] = update["y"]
                zone["angle"] = update["angle"]
                zone_found = True
                updated_count += 1
                break
                
        if not zone_found:
            not_found_zones.append((slug, z_id))

    # Save data back to JSON
    if updated_count > 0:
        print(f"Saving updated data back to {JSON_PATH}...")
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Successfully updated {updated_count} zones in customization.json!")
    else:
        print("No changes were made to customization.json.")

    # Show summary of errors/warnings
    if not_found_slugs:
        print(f"\n[Warning] The following slugs were not found in customization.json: {list(not_found_slugs)}")
    if not_found_zones:
        print("\n[Warning] The following zones were not found inside their products in customization.json:")
        for slug, z_id in not_found_zones:
            print(f"  - Product '{slug}' does not have a zone named '{z_id}'")

if __name__ == "__main__":
    apply_updates()
