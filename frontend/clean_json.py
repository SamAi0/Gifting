import json

with open('src/data/customization.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if 'zones' in item and isinstance(item['zones'], list):
        # Keep only zones that are dicts and have an 'id'
        valid_zones = [z for z in item['zones'] if isinstance(z, dict) and 'id' in z]
        item['zones'] = valid_zones

with open('src/data/customization.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Successfully cleaned up corrupted zones!")
