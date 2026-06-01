import os
import glob
import re
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/src/data/customization.json'))

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

log_files = glob.glob(r'd:\Gifting\*.txt')

product_data = {}

for file in log_files:
    lines = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(file, 'r', encoding='utf-16') as f:
                lines = f.readlines()
        except UnicodeError:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
    current_product = None
    current_zone_idx = None
    
    for line in lines:
        line = line.strip()
        
        m_prod = re.match(r'^products/(\d+)', line, re.IGNORECASE)
        if m_prod:
            current_product = int(m_prod.group(1))
            current_zone_idx = None
            if current_product not in product_data:
                product_data[current_product] = {}
        
        if current_product and 'set placeholder name' in line.lower():
            # Matches "1-Your name", "create zone 4-Text", "3-Bottle Text"
            matches = re.findall(r'(?:zone\s*)?(\d+)\s*-\s*([^,\n]*)', line, flags=re.IGNORECASE)
            for z_idx, p_text in matches:
                p_text = re.sub(r'\s+and\s+create\s+zone.*$', '', p_text, flags=re.IGNORECASE).strip()
                p_text = re.sub(r'\s+and\s+.*$', '', p_text, flags=re.IGNORECASE).strip()
                if p_text and not p_text.lower().startswith('remove'):
                    if z_idx not in product_data[current_product]:
                        product_data[current_product][z_idx] = {}
                    product_data[current_product][z_idx]['placeholder'] = p_text

        # Matches "Zone Update [zone-4]" or "Zone Update [zone-192-4]"
        m_zone = re.search(r'Zone Update\s*\[zone-(?:\d+-)?(\d+)\]', line, re.IGNORECASE)
        if m_zone and current_product:
            current_zone_idx = m_zone.group(1)
            if current_zone_idx not in product_data[current_product]:
                product_data[current_product][current_zone_idx] = {}
                
        # Matches '"x": 704, "y": 711, "angle": 89'
        m_coord = re.search(r'"x":\s*(-?\d+),\s*"y":\s*(-?\d+),\s*"angle":\s*(-?\d+)', line)
        if m_coord and current_product and current_zone_idx:
            product_data[current_product][current_zone_idx]['x'] = int(m_coord.group(1))
            product_data[current_product][current_zone_idx]['y'] = int(m_coord.group(2))
            product_data[current_product][current_zone_idx]['angle'] = int(m_coord.group(3))

updated_zones_count = 0
created_zones_count = 0

for db_id, zones_info in product_data.items():
    try:
        slug = Product.objects.get(id=db_id).slug
    except Product.DoesNotExist:
        continue
    
    for item in data:
        if item.get('slug') == slug:
            item_zones = item.setdefault('zones', [])
            existing_zones_by_idx = {}
            for z in item_zones:
                m_z = re.search(r'-(\d+)$', z.get('id', ''))
                if m_z:
                    existing_zones_by_idx[m_z.group(1)] = z

            for z_idx, info in zones_info.items():
                if z_idx in existing_zones_by_idx:
                    z = existing_zones_by_idx[z_idx]
                    if 'placeholder' in info: z['placeholder'] = info['placeholder']
                    if 'x' in info: z['x'] = info['x']
                    if 'y' in info: z['y'] = info['y']
                    if 'angle' in info: z['angle'] = info['angle']
                    updated_zones_count += 1
                else:
                    new_zone = {
                        "id": f"zone-{z_idx}",
                        "name": f"Zone {z_idx}",
                        "type": "text",
                        "x": info.get('x', 400),
                        "y": info.get('y', 200),
                        "originX": "center",
                        "originY": "center",
                        "angle": info.get('angle', 0),
                        "maxWidth": 300,
                        "maxChars": 15,
                        "fontFamily": "Outfit, sans-serif",
                        "fontSize": 12,
                        "fill": "#ffffff",
                        "opacity": 0.9,
                        "placeholder": info.get('placeholder', 'Text'),
                        "minFontSize": 10
                    }
                    item_zones.append(new_zone)
                    created_zones_count += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(f"Updated {updated_zones_count} existing zones.")
print(f"Created {created_zones_count} NEW missing zones.")
