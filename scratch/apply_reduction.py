import json
import os

def reduce_zones():
    json_path = r'c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json'
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)
    
    modified_count = 0
    for item in data:
        zones = item.get('zones', [])
        current_count = len(zones)
        
        if current_count == 7:
            # Remove last 2
            item['zones'] = zones[:5]
            modified_count += 1
        elif current_count == 6:
            # Remove last 2
            item['zones'] = zones[:4]
            modified_count += 1
        elif current_count == 5:
            # Remove last 1
            item['zones'] = zones[:4]
            modified_count += 1
            
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully modified {modified_count} products.")

if __name__ == "__main__":
    reduce_zones()
