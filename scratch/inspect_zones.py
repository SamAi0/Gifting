import json

def inspect_zones():
    json_path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    by_count = {5: [], 6: [], 7: []}
    for item in data:
        count = len(item.get('zones', []))
        if count in by_count:
            by_count[count].append(item)
    
    for count in [5, 6, 7]:
        if by_count[count]:
            print(f"\n--- Example of product with {count} zones ---")
            item = by_count[count][0]
            print(f"Product: {item['productName']}")
            for i, zone in enumerate(item['zones']):
                print(f"  {i+1}. ID: {zone['id']}, Type: {zone['type']}, Placeholder: {zone.get('placeholder', 'N/A')}")

if __name__ == "__main__":
    inspect_zones()
