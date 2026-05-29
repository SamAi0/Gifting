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

product_placeholders = {}

for file in log_files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        current_product = None
        for line in lines:
            line = line.strip()
            
            m_prod = re.match(r'^products/(\d+)', line, re.IGNORECASE)
            if m_prod:
                current_product = int(m_prod.group(1))
            
            if current_product and 'set placeholder name' in line.lower():
                matches = re.findall(r'(?:zone\s*)?(\d+)\s*-\s*([^,\n]*)', line, flags=re.IGNORECASE)
                if matches:
                    if current_product not in product_placeholders:
                        product_placeholders[current_product] = {}
                    for z_idx, p_text in matches:
                        p_text = p_text.strip()
                        if p_text and not p_text.lower().startswith('remove'):
                            product_placeholders[current_product][z_idx] = p_text
                current_product = None 

updated_zones = 0
for db_id, placeholders in product_placeholders.items():
    if not (61 <= db_id <= 270):
        continue
    
    try:
        slug = Product.objects.get(id=db_id).slug
    except Product.DoesNotExist:
        continue
    
    for item in data:
        if item.get('slug') == slug:
            zones = item.get('zones', [])
            for z_idx, p_text in placeholders.items():
                for z in zones:
                    if z.get('id', '').endswith(f"-{z_idx}"):
                        z['placeholder'] = p_text
                        updated_zones += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(f"Updated {updated_zones} placeholders!")
