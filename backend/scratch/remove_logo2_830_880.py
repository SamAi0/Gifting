import json, os, sys, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

ZONE_TO_REMOVE = 'logo-2'

print("=" * 60)
print(f"REMOVING '{ZONE_TO_REMOVE}' from products 830-880")
print("=" * 60)

# Load JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
slug_index = {item['slug']: i for i, item in enumerate(data) if 'slug' in item}

# Map DB IDs 830-880 to slugs
updated_count = 0
skipped = []

for db_id in range(830, 881):
    try:
        p = Product.objects.get(id=db_id)
        slug = p.slug
    except Product.DoesNotExist:
        skipped.append(db_id)
        continue

    if slug not in slug_index:
        print(f"  [NOT IN JSON] ID {db_id} '{slug}'")
        continue

    idx = slug_index[slug]
    zones = data[idx].get('zones', [])
    before = len(zones)
    zones_filtered = [z for z in zones if z.get('id') != ZONE_TO_REMOVE]
    after = len(zones_filtered)

    if before != after:
        data[idx]['zones'] = zones_filtered
        updated_count += 1
        print(f"  [REMOVED] ID {db_id} '{slug}' - zones: {before} -> {after}")
    else:
        print(f"  [NOT FOUND] ID {db_id} '{slug}' - '{ZONE_TO_REMOVE}' zone not present")

# Save JSON
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"\n[SAVED] {updated_count} products updated in customization.json")

# Sync to DB
print("\n" + "=" * 60)
print("Syncing to SQLite DB...")
print("=" * 60)
res = subprocess.run([sys.executable, SYNC_SCRIPT], capture_output=True, text=True, cwd=BACKEND_DIR)
lines = res.stdout.strip().split('\n')
for line in lines[-8:]:
    print(line)
if res.returncode == 0:
    print("\n[SUCCESS] DB sync complete!")
else:
    print(f"[ERROR] {res.stderr}")

print("\n" + "=" * 60)
print(f"DONE: '{ZONE_TO_REMOVE}' removed from {updated_count} products (830-880)")
print("=" * 60)
