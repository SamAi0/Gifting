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
products/41

set placeholder name zones 1 -Pen text, and 2 zone-extra text and remove, 3rd zone
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 574, "y": 663, "angle": 284
CanvasCustomizer.jsx:117 --------------------------


products/42
set placeholder name zones 1 -Pen text, and 2 zone-extra text and remove, 3rd zone
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 625, "y": 523, "angle": 255
CanvasCustomizer.jsx:117 --------------------------



products/43
set placeholder name zones1Your Name,zone2-Top Text (Optional),zone3-Bottom Text (Optional)
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 374, "y": 160, "angle": 340
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 502, "y": 468, "angle": 338
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-3] 
CanvasCustomizer.jsx:116 "x": 622, "y": 754, "angle": 338



products/44
set placeholder name zones 1-Your name,2-Extra text
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 495, "y": 918, "angle": 358



products/45
set placeholder name zones 1-Your name,zones2-pen text
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 803, "y": 702, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 520, "y": 526, "angle": 256
CanvasCustomizer.jsx:117 --------------------------


products/46
set placeholder name zones1Your Name,zone2-Top Text (Optional),zone3-Bottom Text (Optional)
--------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 714, "y": 486, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 477, "y": 130, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-3] 
CanvasCustomizer.jsx:116 "x": 474, "y": 863, "angle": 0
CanvasCustomizer.jsx:117 --------------------------



products/47

set placeholder name zones 1-Your name,2-Nickname
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 608, "y": 552, "angle": 262
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 454, "y": 721, "angle": 263
CanvasCustomizer.jsx:117 ----------------------


products/48

set placeholder name zones 1-Your name,2-Nickname
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 490, "y": 340, "angle": 305
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 606, "y": 424, "angle": 305
CanvasCustomizer.jsx:117 --------------------------

products/49

set placeholder name zones 1-Your name,2-Pen text
 Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 593, "y": 918, "angle": 11
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 727, "y": 430, "angle": 270
CanvasCustomizer.jsx:117 --------------------------

products/50
set placeholder name zones 1-Your name,2-Pen text
Zone Update [zone-1] 
CanvasCustomizer.jsx:116 "x": 541, "y": 812, "angle": 0
CanvasCustomizer.jsx:117 --------------------------
CanvasCustomizer.jsx:115  Zone Update [zone-2] 
CanvasCustomizer.jsx:116 "x": 204, "y": 581, "angle": 268
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
            
        # Match product id line (e.g. products/41)
        prod_match = re.search(r'products/(\d+)', line)
        if prod_match:
            current_db_id = int(prod_match.group(1))
            data[current_db_id] = {
                'zone_names': {},  # maps "zone-1" -> "Your name"
                'zone_coords': {}  # maps "zone-1" -> {'x': 574, 'y': 663, 'angle': 284}
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
                cleaned = re.sub(r'^set\s+.*?zones\s*', '', line).strip()
                parts = [p.strip() for p in cleaned.split(',') if p.strip()]
                for p in parts:
                    m = re.search(r'(?:zones?|zone)?\s*(\d+)\s*-\s*(.*)', p)
                    if not m:
                        m = re.search(r'(?:zones?|zone)?\s*(\d+)\s*(.*)', p)
                    if m:
                        num = m.group(1)
                        name = m.group(2).strip()
                        data[current_db_id]['zone_names'][f'zone-{num}'] = name
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
