import json
import re
from collections import Counter

path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_counts = []
for item in data:
    p_id = item.get('productId')
    seen = set()
    clean = []
    for z in item.get('zones', []):
        z_id = z.get('id')
        if z_id in seen:
            continue
        
        # Check if it has a pattern like zone-194-1
        m = re.search(r'zone-(\d+)-', z_id)
        if m:
            linked_id = int(m.group(1))
            if linked_id != p_id:
                # Discard zone belonging to another product ID
                continue
                
        seen.add(z_id)
        clean.append(z)
        
    new_counts.append(len(clean))

print("Cleaned zone counts distribution:")
print(sorted(Counter(new_counts).items()))
