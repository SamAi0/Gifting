import json
import re
import shutil

path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'

# Backup current customization.json
shutil.copy2(path, path + '.clean_bak')
print("Created backup of customization.json to customization.json.clean_bak")

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_count = 0
total_zones_before = 0
total_zones_after = 0

for item in data:
    p_id = item.get('productId')
    zones = item.get('zones', [])
    total_zones_before += len(zones)
    
    seen = set()
    clean_zones = []
    
    for z in zones:
        z_id = z.get('id')
        if z_id in seen:
            continue
            
        # Match zone-XXX-X pattern where XXX is another product ID
        m = re.search(r'zone-(\d+)-', z_id)
        if m:
            linked_id = int(m.group(1))
            if linked_id != p_id:
                # Discard zone belonging to another product
                continue
                
        seen.add(z_id)
        clean_zones.append(z)
        
    if len(clean_zones) != len(zones):
        cleaned_count += 1
        
    item['zones'] = clean_zones
    total_zones_after += len(clean_zones)

# Save cleaned customization.json
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"\nSuccessfully cleaned zones for {cleaned_count} products!")
print(f"Total customization zones: reduced from {total_zones_before} to {total_zones_after} zones.")
print("Saved cleaned customization.json successfully.")
