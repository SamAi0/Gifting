import json
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from products.models import Product

with open('../frontend/src/data/customization.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

db_products = list(Product.objects.filter(is_active=True))

json_slugs = set()
for item in data:
    if isinstance(item, dict) and item.get('slug'):
        raw = item['slug'].strip()
        norm = raw.lower().replace('-', '_')
        json_slugs.add(raw)
        json_slugs.add(norm)

unmatched_db = []
for p in db_products:
    raw_slug = p.slug.strip()
    norm_slug = raw_slug.lower().replace('-', '_')
    if raw_slug not in json_slugs and norm_slug not in json_slugs:
        unmatched_db.append(p)

unmatched_db.sort(key=lambda x: x.name)

# Create artifact file
artifact_path = r"C:\Users\Asus\.gemini\antigravity-ide\brain\1ee6a60e-9bfe-493d-8973-5401a5e1a6d7\missing_products_list.md"

with open(artifact_path, 'w', encoding='utf-8') as af:
    af.write(f"# Missing Products List ({len(unmatched_db)} Items)\n\n")
    af.write("Yeh wo products hain jo aapke Database mein toh hain, lekin `customization.json` file mein missing hain.\n\n")
    af.write("| Product Name | Product ID / Slug |\n")
    af.write("|---|---|\n")
    for p in unmatched_db:
        af.write(f"| {p.name} | `{p.slug}` |\n")

print(f"Artifact created at {artifact_path} with {len(unmatched_db)} items.")
