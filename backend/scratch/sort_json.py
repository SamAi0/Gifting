import json
import os

JSON_PATH = r'c:\Users\Asus\OneDrive\Pictures\Camera Roll 1\Gifting\frontend\src\data\customization.json'

print("=" * 60)
print("SORTING customization.json by productId")
print("=" * 60)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sort the data by productId
# Use a high number for items without a productId (though we know all have one)
data.sort(key=lambda x: x.get('productId', 999999))

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n[SUCCESS] Successfully sorted {len(data)} products in sequence!")
