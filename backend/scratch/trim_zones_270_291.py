import json, os, sys, subprocess

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

print("=" * 60)
print("UPDATING ZONES FOR 270-291")
print("=" * 60)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

slug_index = {item['slug']: i for i, item in enumerate(data) if 'slug' in item}
updated_count = 0

for db_id in range(270, 292): # 270 to 291
    try:
        p = Product.objects.get(id=db_id)
        slug = p.slug
    except Product.DoesNotExist:
        print(f"  [SKIP] ID {db_id} not in DB")
        continue

    if slug not in slug_index:
        print(f"  [NOT IN JSON] ID {db_id} '{slug}'")
        continue

    idx = slug_index[slug]
    zones = data[idx].get('zones', [])
    before = len(zones)
    
    # Sort zones to ensure we keep the right ones based on ID suffix
    zones = sorted(zones, key=lambda z: z.get('id', ''))

    if db_id == 270:
        # Keep 3 zones
        new_zones = [z for z in zones if z.get('id') in ['zone-270-1', 'zone-270-2', 'zone-270-3']]
    else:
        # Keep 2 zones for 271-291
        keep_ids = [f'zone-{db_id}-1', f'zone-{db_id}-2']
        new_zones = [z for z in zones if z.get('id') in keep_ids]

    after = len(new_zones)
    
    if before != after:
        data[idx]['zones'] = new_zones
        updated_count += 1
        print(f"  [OK] ID {db_id} '{slug}' - zones: {before} -> {after} { [z['id'] for z in new_zones] }")
    else:
        print(f"  [NO CHANGE] ID {db_id} '{slug}' - already has {after} zones")

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n[SAVED] {updated_count} products updated in customization.json")

# DB Sync
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
