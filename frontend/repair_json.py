import sys
import json
from json_repair import repair_json

with open('src/data/customization.json', 'r', encoding='utf-8') as f:
    bad_json = f.read()

good_json_str = repair_json(bad_json)

try:
    parsed = json.loads(good_json_str)
except Exception as e:
    print("Could not repair:", e)
    sys.exit(1)
    
with open('src/data/customization.json', 'w', encoding='utf-8') as f:
    json.dump(parsed, f, indent=2)

print("Successfully repaired JSON!")
