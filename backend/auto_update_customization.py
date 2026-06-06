import os
import re
import json
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

LOGS = """
products/765
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 709, "y": 534, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 194, "y": 569, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 477, "y": 736, "angle": 0


products/764
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 709, "y": 534, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 194, "y": 569, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 477, "y": 736, "angle": 0

products/763
Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 709, "y": 534, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 194, "y": 569, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 477, "y": 736, "angle": 0

products/762
 Zone Update [name-1] 
CanvasCustomizer.jsx:116 "x": 574, "y": 539, "angle": 269
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-1] 
CanvasCustomizer.jsx:116 "x": 699, "y": 586, "angle": 270
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [extra-2] 
CanvasCustomizer.jsx:116 "x": 402, "y": 679, "angle": 0
"""

def parse_logs(log_text):
    data = {}
    current_db_id = None
    current_zone = None
    
    lines = log_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Match product id
        prod_match = re.search(r'products/(\d+)', line)
        if prod_match:
            current_db_id = int(prod_match.group(1))
            data[current_db_id] = {}
            current_zone = None
            continue
            
        # Match Zone Update
        zone_match = re.search(r'Zone Update\s+\[(.*?)\]', line)
        if zone_match:
            current_zone = zone_match.group(1)
            continue
            
        # Match x, y, angle coordinates
        coord_match = re.search(r'"x":\s*(-?\d+),\s*"y":\s*(-?\d+),\s*"angle":\s*(-?\d+)', line)
        if coord_match and current_db_id and current_zone:
            x = int(coord_match.group(1))
            y = int(coord_match.group(2))
            angle = int(coord_match.group(3))
            data[current_db_id][current_zone] = {
                'x': x,
                'y': y,
                'angle': angle
            }
            
    return data

def main():
    parsed = parse_logs(LOGS)
    print("[INFO] Parsed Logs data:")
    for db_id, zones in parsed.items():
        print(f"  Product ID: {db_id}")
        for zone, coords in zones.items():
            print(f"    Zone: {zone} -> {coords}")
            
    # Load customization.json
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    with open(json_path, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
        
    print(f"\n[INFO] Loaded customization.json with {len(customization_data)} items.")
    
    # Map db_id to slug, then update customization.json
    slug_updates = {}
    for db_id, zones in parsed.items():
        try:
            product = Product.objects.get(id=db_id)
            slug = product.slug
            slug_updates[slug] = zones
            print(f"[INFO] Mapped DB ID {db_id} to slug: '{slug}' ({product.name})")
        except Product.DoesNotExist:
            print(f"[ERROR] Product with ID {db_id} not found in DB!")
            sys.exit(1)
            
    # Perform update on customization_data
    updated_products_count = 0
    for item in customization_data:
        slug = item.get('slug')
        if slug in slug_updates:
            print(f"[INFO] Updating zones for slug '{slug}':")
            zones_to_update = slug_updates[slug]
            for zone_data in item.get('zones', []):
                zone_id = zone_data.get('id')
                if zone_id in zones_to_update:
                    coords = zones_to_update[zone_id]
                    print(f"  Updating {zone_id}: x: {zone_data.get('x')}->{coords['x']}, y: {zone_data.get('y')}->{coords['y']}, angle: {zone_data.get('angle')}->{coords['angle']}")
                    zone_data['x'] = coords['x']
                    zone_data['y'] = coords['y']
                    zone_data['angle'] = coords['angle']
            updated_products_count += 1
            
    # Save back customization.json with pretty print formatting
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(customization_data, f, indent=2)
    print(f"[SUCCESS] Wrote updates to customization.json for {updated_products_count} products.")
    
if __name__ == '__main__':
    main()
