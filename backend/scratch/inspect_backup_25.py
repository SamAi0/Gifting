import os
import json

backup_path = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json.bak"

if not os.path.exists(backup_path):
    print("Backup file not found!")
    exit(1)

with open(backup_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item.get('slug') == 'bolttle-cup-set-bc':
        print(f"Original configuration for bolttle-cup-set-bc (ID 25):")
        for z in item.get('zones', []):
            print(f"  Zone ID: {z.get('id')} -> x: {z.get('x')}, y: {z.get('y')}, angle: {z.get('angle')}")
        break
