import json, os, sys, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

ZONES_TO_REMOVE = {'extra-1', 'extra-2'}
ID_START, ID_END = 536, 639

print("=" * 60)
print(f"REMOVING {ZONES_TO_REMOVE} from products {ID_START}-{ID_END}")
print("=" * 60)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
slug_index = {item['slug']: i for i, item in enumerate(data) if 'slug' in item}

updated_count = 0
for db_id in range(ID_START, ID_END + 1):
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
    data[idx]['zones'] = [z for z in zones if z.get('id') not in ZONES_TO_REMOVE]
    after = len(data[idx]['zones'])

    if before != after:
        updated_count += 1
        print(f"  [OK] ID {db_id} '{slug}' - zones: {before} -> {after}")
    else:
        print(f"  [NO CHANGE] ID {db_id} '{slug}' - no extra zones found")

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

print(f"\nDONE: extra-1 & extra-2 removed from {updated_count} products ({ID_START}-{ID_END})")
