import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/src/data/customization.json'))

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

products_to_update = Product.objects.filter(id__gte=61, id__lte=270)
slugs = set(p.slug for p in products_to_update)

updated_count = 0
products_updated = 0

for item in data:
    if item.get('slug') in slugs:
        updated = False
        for zone in item.get('zones', []):
            zone['fontSize'] = 12
            updated_count += 1
            updated = True
        if updated:
            products_updated += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print(f"Updated {updated_count} zones across {products_updated} products to have fontSize = 12.")
