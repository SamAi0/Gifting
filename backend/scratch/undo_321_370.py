import os
import sys
import json
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH     = os.path.join(WORKSPACE_DIR, 'frontend', 'src', 'data', 'customization.json')
BAK_PATH      = os.path.join(WORKSPACE_DIR, 'frontend', 'src', 'data', 'customization.json.clean_bak')

# Fallback to .bak if clean_bak missing
if not os.path.exists(BAK_PATH):
    BAK_PATH = os.path.join(WORKSPACE_DIR, 'frontend', 'src', 'data', 'customization.json.bak')

print("=" * 60)
print("UNDO: Restoring products 321-370 zones from backup")
print(f"Backup file: {os.path.basename(BAK_PATH)}")
print("=" * 60)

# --- Load both files ---
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    current_data = json.load(f)

with open(BAK_PATH, 'r', encoding='utf-8') as f:
    backup_data = json.load(f)

# --- Build slug list for products 321-370 via Django ---
slug_to_restore = {}
for db_id in range(321, 371):
    try:
        product = Product.objects.get(id=db_id)
        slug_to_restore[product.slug] = db_id
        print(f"  [MAP] ID {db_id} -> slug: '{product.slug}'")
    except Product.DoesNotExist:
        print(f"  [SKIP] Product ID {db_id} not found in DB")

print(f"\nTotal slugs to restore: {len(slug_to_restore)}")

# --- Build backup zones lookup by slug ---
backup_zones_by_slug = {}
for item in backup_data:
    slug = item.get('slug')
    if slug and slug in slug_to_restore:
        backup_zones_by_slug[slug] = item.get('zones', [])

print(f"Found in backup: {len(backup_zones_by_slug)} products")

# --- Apply backup zones back to current customization.json ---
restored_count = 0
not_in_backup = []

for item in current_data:
    slug = item.get('slug')
    if slug in slug_to_restore:
        if slug in backup_zones_by_slug:
            old_zones = item.get('zones', [])
            new_zones = backup_zones_by_slug[slug]
            item['zones'] = new_zones
            restored_count += 1
            print(f"  [RESTORED] '{slug}' (ID {slug_to_restore[slug]}) - zones: {len(old_zones)} -> {len(new_zones)}")
        else:
            not_in_backup.append(slug)
            print(f"  [NOT IN BACKUP] '{slug}' (ID {slug_to_restore[slug]}) - keeping current")

# --- Save updated customization.json ---
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(current_data, f, indent=2)

print(f"\n[SUCCESS] Restored {restored_count} products in customization.json")
if not_in_backup:
    print(f"[WARNING] {len(not_in_backup)} slugs not found in backup: {not_in_backup}")

# --- Run sync_customization.py to push to SQLite DB ---
print("\n" + "=" * 60)
print("SYNCING to SQLite Database...")
print("=" * 60)

import subprocess
sync_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sync_customization.py')
try:
    res = subprocess.run([sys.executable, sync_script], capture_output=True, text=True, check=True)
    # Print last 10 lines only to keep output clean
    lines = res.stdout.strip().split('\n')
    for line in lines[-10:]:
        print(line)
    print("\n[SUCCESS] Database sync complete!")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Sync failed: {e}")
    print(e.stderr)
    sys.exit(1)
