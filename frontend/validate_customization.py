import json

with open('src/data/customization.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

errors = []
for i, item in enumerate(data):
    if not isinstance(item, dict):
        errors.append(f"Item {i} is not a dictionary.")
        continue
        
    slug = item.get('slug', f'Index-{i}')
    
    if 'slug' not in item:
        errors.append(f"Item {i} missing 'slug'")
    if 'baseImage' not in item:
        errors.append(f"Item {slug} missing 'baseImage'")
    if 'zones' not in item or not isinstance(item['zones'], list):
        errors.append(f"Item {slug} missing or invalid 'zones'")
    else:
        for j, z in enumerate(item['zones']):
            if not isinstance(z, dict):
                errors.append(f"Item {slug} zone {j} is not a dictionary")
                continue
            if 'id' not in z:
                errors.append(f"Item {slug} zone {j} missing 'id'")

print(f"Schema validation found {len(errors)} errors.")
if errors:
    print(errors[:15])
