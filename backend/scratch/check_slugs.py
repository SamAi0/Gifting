import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from products.models import Product

with open('../frontend/src/data/customization.json', 'r') as f:
    data = json.load(f)

print(f"Total items in JSON: {len(data)}")

matched = 0
for item in data:
    slug = item.get('slug')
    if slug:
        product = Product.objects.filter(slug=slug).first()
        if product:
            matched += 1

print(f"Total matched by slug: {matched}")
