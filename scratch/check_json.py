import json
import os

path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'

try:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total products: {len(data)}")
    
    slugs = {}
    ids = {}
    
    for i, item in enumerate(data):
        slug = item.get('slug')
        pid = item.get('productId')
        
        if slug in slugs:
            print(f"Duplicate slug found: '{slug}' at index {i} and {slugs[slug]}")
        else:
            slugs[slug] = i
            
        if pid in ids:
            print(f"Duplicate productId found: {pid} at index {i} and {ids[pid]}")
        else:
            ids[pid] = i
            
        # Check if zones have unique IDs within a product
        zone_ids = set()
        for zone in item.get('zones', []):
            zid = zone.get('id')
            if zid in zone_ids:
                print(f"Duplicate zone ID '{zid}' in product '{slug}' (index {i})")
            zone_ids.add(zid)
            
except Exception as e:
    print(f"Error reading or parsing JSON: {e}")
