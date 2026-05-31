import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         '..', 'frontend', 'src', 'data', 'customization.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

slug_index = {item['slug']: item for item in data if 'slug' in item}

print("%-6s %-52s %-8s %s" % ("ID", "Slug", "Zones", "Zone IDs"))
print("-" * 120)

zone_counts = {}
for db_id in range(830, 881):
    try:
        p = Product.objects.get(id=db_id)
        slug = p.slug
        if slug in slug_index:
            zones = slug_index[slug].get('zones', [])
            zone_ids = [z.get('id', '?') for z in zones]
            count = len(zones)
            zone_counts[count] = zone_counts.get(count, 0) + 1
            print("%-6d %-52s %-8d %s" % (db_id, slug[:52], count, zone_ids))
        else:
            print("%-6d %-52s NOT IN JSON" % (db_id, slug[:52]))
    except Product.DoesNotExist:
        print("%-6d NOT IN DB" % db_id)

print("\n--- SUMMARY ---")
for k, v in sorted(zone_counts.items()):
    print(f"  {k} zone(s): {v} products")
