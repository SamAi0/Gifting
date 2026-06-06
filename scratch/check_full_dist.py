import json
import os

def count_zones():
    json_path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    counts = {}
    for item in data:
        zones = item.get('zones', [])
        counts[len(zones)] = counts.get(len(zones), 0) + 1
    
    print(f"Total Products: {len(data)}")
    print("\nFull Zone Distribution:")
    for count in sorted(counts.keys()):
        print(f"- {count} zones: {counts[count]} products")

if __name__ == "__main__":
    count_zones()
