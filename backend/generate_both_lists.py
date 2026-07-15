import json
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from products.models import Product

with open('../frontend/src/data/customization.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

db_products = list(Product.objects.filter(is_active=True))

json_slugs = set()
json_items = []
for item in data:
    if isinstance(item, dict) and item.get('slug'):
        raw = item['slug'].strip()
        norm = raw.lower().replace('-', '_')
        json_slugs.add(raw)
        json_slugs.add(norm)
        # Store for the first list
        name = item.get('productName') or item.get('name') or 'Unknown'
        json_items.append({"name": name, "slug": raw})

unmatched_db = []
for p in db_products:
    raw_slug = p.slug.strip()
    norm_slug = raw_slug.lower().replace('-', '_')
    if raw_slug not in json_slugs and norm_slug not in json_slugs:
        unmatched_db.append(p)

json_items.sort(key=lambda x: x["name"])
unmatched_db.sort(key=lambda x: x.name)

# Artifact Paths
artifact_dir = r"C:\Users\Asus\.gemini\antigravity-ide\brain\1ee6a60e-9bfe-493d-8973-5401a5e1a6d7"
matched_path = os.path.join(artifact_dir, "json_223_products_list.md")
missing_path = os.path.join(artifact_dir, "missing_522_products_list.md")

with open(matched_path, 'w', encoding='utf-8') as f:
    f.write(f"# JSON Products List ({len(json_items)} Items)\n\n")
    f.write("Yeh wo products hain jo aapki `customization.json` file ke andar successfully add hain.\n\n")
    f.write("| Product Name | JSON Slug |\n")
    f.write("|---|---|\n")
    for item in json_items:
        f.write(f"| {item['name']} | `{item['slug']}` |\n")

with open(missing_path, 'w', encoding='utf-8') as f:
    f.write(f"# Missing Products List ({len(unmatched_db)} Items)\n\n")
    f.write("Yeh wo products hain jo Database mein hain lekin `customization.json` mein poori tarah MISSING hain.\n\n")
    f.write("| Product Name | Database Slug |\n")
    f.write("|---|---|\n")
    for p in unmatched_db:
        f.write(f"| {p.name} | `{p.slug}` |\n")

print(f"Artifacts created successfully.")
