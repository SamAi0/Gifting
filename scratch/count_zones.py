import json
import os

def count_zones():
    json_path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    counts = {}
    for item in data:
        name = item.get('productName', 'Unknown')
        zones = item.get('zones', [])
        counts[name] = len(zones)
    
    # Sort by number of zones descending
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Total Products: {len(data)}")
    print("\nTop Products by Zone Count:")
    for name, count in sorted_counts[:20]:
        print(f"- {name}: {count} zones")

    # Grouping by count
    stats = {}
    for count in counts.values():
        stats[count] = stats.get(count, 0) + 1
    
    print("\nZone Distribution:")
    for count in sorted(stats.keys()):
        print(f"- {count} zones: {stats[count]} products")

if __name__ == "__main__":
    count_zones()
