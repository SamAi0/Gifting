import os
import sys
import json
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# All products customized in our session
product_ids = list(range(51, 88)) + list(range(88, 201)) + list(range(201, 264)) + list(range(731, 830))

json_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'frontend',
    'src',
    'data',
    'customization.json'
)

with open(json_path, 'r', encoding='utf-8') as f:
    customization_data = json.load(f)

slug_to_index = {item.get('slug'): i for i, item in enumerate(customization_data) if item.get('slug')}

updated_count = 0

for db_id in product_ids:
    try:
        product = Product.all_objects.get(id=db_id)
        slug = product.slug
        if slug in slug_to_index:
            idx = slug_to_index[slug]
            item = customization_data[idx]
            zones = item.get('zones', [])
            
            modified = False
            for z in zones:
                # Set fontSize to 12 for all zones in these products
                if z.get('fontSize') != 12 or z.get('minFontSize') != 10:
                    z['fontSize'] = 12
                    z['minFontSize'] = 10
                    modified = True
            
            if modified:
                updated_count += 1
                print(f"Set fontSize to 12 for product ID {db_id} (slug: {slug})")
    except Product.DoesNotExist:
        pass

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(customization_data, f, indent=2)

print(f"Finished setting fontSize to 12. Updated {updated_count} products.")
