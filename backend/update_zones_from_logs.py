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

INPUT_LOGS = """
products/31
set cardholder name zones 1-Cardholder text ,2-Text,3-Pen text
  Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 677, "y": 302, "angle": 229
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 389, "y": 534, "angle": 327
CanvasCustomizer.jsx:117 ----------------------------------

products/32
set cardholder name zones 1-Cardholder text,2-Pen text
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 582, "y": 556, "angle": 279
CanvasCustomizer.jsx:117 ------------------

....

products/36
set cardholder name zones 1-Cardholder text,2-Pen text
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 519, "y": 502, "angle": 277
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 701, "y": 528, "angle": 280
CanvasCustomizer.jsx:117 --------------------------


products/37
set placeholder name zones 1-Your name,2-Pen text
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 497, "y": 515, "angle": 277
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 713, "y": 549, "angle": 278
CanvasCustomizer.jsx:117 --------------------------






products/38
set placeholder name zones 1-Your name,2-Pen text
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 392, "y": 443, "angle": 342
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 468, "y": 772, "angle": 338
CanvasCustomizer.jsx:117 --------------------------







products/39
set placeholder name zones 1 -Pen text, and 2 zone-extra text and remove, 3rd zone
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 542, "y": 621, "angle": 271







products/40
set placeholder name zones 1 -Pen text, and 2 zone-extra text and remove, 3rd zone
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 612, "y": 634, "angle": 282
CanvasCustomizer.jsx:117 --------------------------
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
            
        # Match product id line (e.g. products/31)
        prod_match = re.search(r'products/(\d+)', line)
        if prod_match:
            current_db_id = int(prod_match.group(1))
            data[current_db_id] = {
                'zone_names': {},  # maps "zone-1" -> "Cardholder text"
                'zone_coords': {}  # maps "zone-1" -> {'x': 695, 'y': 311, 'angle': 229}
            }
            current_zone = None
            continue
            
        # Match zone names configuration line
        if current_db_id and 'zones' in line:
            if "remove" in line and "3rd" in line:
                data[current_db_id]['zone_names'] = {
                    'zone-1': 'Pen text',
                    'zone-2': 'extra text'
                }
            else:
                zones_part_match = re.search(r'zones\s+(.*)', line)
                if zones_part_match:
                    zones_str = zones_part_match.group(1)
                    # Split by comma
                    parts = [p.strip() for p in zones_str.split(',') if p.strip()]
                    for part in parts:
                        subparts = part.split('-', 1)
                        if len(subparts) == 2:
                            num = subparts[0].strip()
                            name = subparts[1].strip()
                            zone_id = f"zone-{num}"
                            data[current_db_id]['zone_names'][zone_id] = name
            continue
            
        # Match Zone Update line
        zone_match = re.search(r'Zone Update\s+\[(.*?)\]', line)
        if zone_match:
            current_zone = zone_match.group(1)
            continue
            
        # Match x, y, angle coordinates line
        coord_match = re.search(r'"x":\s*(-?\d+),\s*"y":\s*(-?\d+),\s*"angle":\s*(-?\d+)', line)
        if coord_match and current_db_id and current_zone:
            x = int(coord_match.group(1))
            y = int(coord_match.group(2))
            angle = int(coord_match.group(3))
            data[current_db_id]['zone_coords'][current_zone] = {
                'x': x,
                'y': y,
                'angle': angle
            }
            
    return data

def main():
    parsed = parse_logs(INPUT_LOGS)
    print("[INFO] Parsed Logs data:")
    for db_id, info in parsed.items():
        print(f"  Product ID: {db_id}")
        print(f"    Zone Names: {info['zone_names']}")
        print(f"    Zone Coords: {info['zone_coords']}")
            
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
    
    # Map db_id to slug, then build the target update mapping
    slug_updates = {}
    for db_id, info in parsed.items():
        try:
            product = Product.objects.get(id=db_id)
            slug = product.slug
            slug_updates[slug] = info
            print(f"[INFO] Mapped DB ID {db_id} to slug: '{slug}' ({product.name})")
        except Product.DoesNotExist:
            print(f"[ERROR] Product with ID {db_id} not found in DB!")
            sys.exit(1)
            
    # Perform update on customization_data
    updated_products_count = 0
    for item in customization_data:
        slug = item.get('slug')
        if slug in slug_updates:
            print(f"\n[INFO] Updating zones for slug '{slug}':")
            info = slug_updates[slug]
            zone_names = info['zone_names']
            zone_coords = info['zone_coords']
            
            # Reconstruct the zones list, keeping only the zones specified in the logs
            existing_zones_by_id = {z.get('id'): z for z in item.get('zones', [])}
            
            new_zones = []
            for zone_id in sorted(zone_names.keys()):
                # Default zone structure if not found
                default_zone = {
                    "id": zone_id,
                    "name": zone_names[zone_id],
                    "type": "text",
                    "originX": "center",
                    "originY": "center",
                    "maxWidth": 300,
                    "maxChars": 15,
                    "fontFamily": "Outfit, sans-serif",
                    "fontSize": 12,
                    "fill": "#ffffff",
                    "opacity": 0.9,
                }
                
                # Retrieve existing zone structure to preserve other fields
                zone_data = existing_zones_by_id.get(zone_id, default_zone).copy()
                
                # Update properties
                name = zone_names[zone_id]
                # Fallback to existing coordinates if not in log
                coords = zone_coords.get(zone_id, {
                    'x': zone_data.get('x', 400),
                    'y': zone_data.get('y', 200),
                    'angle': zone_data.get('angle', 0)
                })
                
                print(f"  Zone {zone_id}:")
                print(f"    Name: '{zone_data.get('name')}' -> '{name}'")
                print(f"    Placeholder: '{zone_data.get('placeholder')}' -> '{name.upper()}'")
                print(f"    Coords: x: {zone_data.get('x')}->{coords['x']}, y: {zone_data.get('y')}->{coords['y']}, angle: {zone_data.get('angle')}->{coords['angle']}")
                
                zone_data['name'] = name
                zone_data['placeholder'] = name.upper()
                zone_data['x'] = coords['x']
                zone_data['y'] = coords['y']
                zone_data['angle'] = coords['angle']
                
                new_zones.append(zone_data)
                
            item['zones'] = new_zones
            updated_products_count += 1
            
    # Save back customization.json with pretty print formatting
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(customization_data, f, indent=2)
    print(f"\n[SUCCESS] Wrote updates to customization.json for {updated_products_count} products.")
    
if __name__ == '__main__':
    main()
