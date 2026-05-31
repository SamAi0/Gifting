import os, sys, json, subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from products.models import Product

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

print("=" * 60)
print("REMOVING 'extra-1' and 'extra-2' from products 501-549")
print("=" * 60)

# Step 1: Map IDs to slugs for the range
print("\n[STEP 1] Fetching products 501-549 from DB...")
target_slugs = set()
for p in Product.objects.filter(id__gte=501, id__lte=549):
    target_slugs.add(p.slug)

print(f"Found {len(target_slugs)} products in range.")

# Step 2: Load JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    cust_data = json.load(f)

# Step 3: Remove zones
print("\n[STEP 3] Updating zones...")
updated_count = 0
for item in cust_data:
    if item.get('slug') in target_slugs:
        original_zones = item.get('zones', [])
        new_zones = [z for z in original_zones if z.get('id') not in ['extra-1', 'extra-2']]
        
        if len(new_zones) != len(original_zones):
            removed = [z.get('id') for z in original_zones if z.get('id') in ['extra-1', 'extra-2']]
            item['zones'] = new_zones
            updated_count += 1
            print(f"  [OK] Removed {removed} from ID {item.get('productId')} ('{item.get('slug')}')")

if updated_count == 0:
    print("  No 'extra-1' or 'extra-2' zones were found in this range.")
else:
    # Step 4: Save
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(cust_data, f, indent=2, ensure_ascii=False)
    print(f"\n[STEP 4] SAVED: {updated_count} products updated in JSON")

    # Step 5: DB Sync
    print("\n" + "=" * 60)
    print("[STEP 5] Running sync_customization.py...")
    print("=" * 60)
    res = subprocess.run([sys.executable, SYNC_SCRIPT], capture_output=True, text=True, cwd=BACKEND_DIR)
    for line in res.stdout.strip().split('\n')[-10:]:
        print(line)
    if res.returncode == 0:
        print("\n[SUCCESS] SQLite DB sync complete!")
    else:
        print(f"[ERROR] {res.stderr}")

print("\n" + "=" * 60)
print(f"DONE: Removed extra zones from {updated_count} products.")
print("=" * 60)
