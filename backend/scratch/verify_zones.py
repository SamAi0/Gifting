import os
import json

json_path = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"

with open(json_path, 'r') as f:
    data = json.load(f)

slugs = [
    '4-piece-cup-set-c',
    '4-piece-cup-set-c-1',
    'advocate-set-with-dome-keychain',
    'bolttle-cup-set-bc',
    'bolttle-cup-set-bc-1',
    'bottle-pen-keychain-set'
]

for slug in slugs:
    found = False
    for item in data:
        if item.get('slug') == slug:
            print(f"\nSlug: {slug} (Product ID: {item.get('productId')})")
            print("Zones:")
            for z in item.get('zones', []):
                print(f"  ID: {z.get('id')} | Type: {z.get('type')} | X: {z.get('x')} | Y: {z.get('y')} | Angle: {z.get('angle')}")
            found = True
            break
    if not found:
        print(f"Slug: {slug} not found in customization.json!")
