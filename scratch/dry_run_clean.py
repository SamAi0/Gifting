import json
from collections import Counter

path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_counts = []
for item in data:
    seen = set()
    clean_zones = []
    for z in item.get('zones', []):
        z_id = z.get('id')
        if z_id not in seen:
            seen.add(z_id)
            clean_zones.append(z)
    new_counts.append(len(clean_zones))

print("Deduplicated zone count distribution:")
print(sorted(Counter(new_counts).items()))
