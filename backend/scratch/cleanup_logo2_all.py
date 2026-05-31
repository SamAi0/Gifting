import json, os, sys, subprocess

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH   = os.path.join(BACKEND_DIR, '..', 'frontend', 'src', 'data', 'customization.json')
SYNC_SCRIPT = os.path.join(BACKEND_DIR, 'sync_customization.py')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

removed_count  = 0  # dono the, logo-2 remove kiya
renamed_count  = 0  # sirf logo-2 tha, rename kiya to logo-1
unchanged      = 0

print("=" * 60)
print("Cleaning logo-2 zones across ALL products")
print("=" * 60)

for item in data:
    slug  = item.get('slug', '?')
    zones = item.get('zones', [])
    zone_ids = [z.get('id', '') for z in zones]

    has_logo1 = 'logo-1' in zone_ids
    has_logo2 = 'logo-2' in zone_ids

    if has_logo1 and has_logo2:
        # Remove logo-2, keep logo-1
        item['zones'] = [z for z in zones if z.get('id') != 'logo-2']
        removed_count += 1
        print(f"  [REMOVED logo-2] '{slug}'")

    elif not has_logo1 and has_logo2:
        # Rename logo-2 -> logo-1
        for z in zones:
            if z.get('id') == 'logo-2':
                z['id'] = 'logo-1'
        renamed_count += 1
        print(f"  [RENAMED logo-2->logo-1] '{slug}'")

    else:
        unchanged += 1

print(f"\n[SAVED] Writing to customization.json...")
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"  logo-2 removed (had both)  : {removed_count} products")
print(f"  logo-2 renamed to logo-1   : {renamed_count} product")
print(f"  unchanged                  : {unchanged} products")

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

# Verify
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    verify = json.load(f)
logo2_remaining = sum(1 for item in verify for z in item.get('zones',[]) if z.get('id')=='logo-2')
print(f"\n[VERIFY] logo-2 zones remaining in JSON: {logo2_remaining}")
print("Done!")
