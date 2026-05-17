import os
import json

def fix_extensions():
    backend_dir = r"c:\Users\Asus\Downloads\New folder\Gifting\backend"
    static_products_dir = os.path.join(backend_dir, 'static', 'products')
    json_path = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"

    if not os.path.exists(json_path):
        print(f"Error: customization.json not found at {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} products from customization.json")
    
    # Get all files in static/products
    all_files = os.listdir(static_products_dir)
    # Map lowercase name without extension to actual filename
    file_map = {}
    for f in all_files:
        name_no_ext = os.path.splitext(f)[0].lower()
        file_map[name_no_ext] = f

    fixed_count = 0
    missing_count = 0

    for item in data:
        base_image = item.get('baseImage')
        if not base_image:
            continue
            
        filename = os.path.basename(base_image)
        full_path = os.path.join(backend_dir, base_image.lstrip('/'))
        
        # Check if the file exists
        if not os.path.exists(full_path):
            name_no_ext = os.path.splitext(filename)[0].lower()
            if name_no_ext in file_map:
                new_filename = file_map[name_no_ext]
                new_base_image = f"/static/products/{new_filename}"
                print(f"FIXING: {item['productName']}")
                print(f"  Old: {base_image}")
                print(f"  New: {new_base_image}")
                item['baseImage'] = new_base_image
                fixed_count += 1
            else:
                print(f"MISSING (No replacement found): {item['productName']} ({base_image})")
                missing_count += 1

    if fixed_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"\nSuccessfully fixed {fixed_count} image extensions in customization.json!")
    else:
        print("\nNo image extensions needed fixing in customization.json.")
        
    print(f"Total missing images left: {missing_count}")

if __name__ == '__main__':
    fix_extensions()
