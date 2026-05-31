import json
import os
import re

def safe_filename(filename):
    name, ext = os.path.splitext(filename)
    # Remove special characters like &
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[-\s]+', '_', name)
    return f"{name}{ext}"

def fix_json_images():
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    if not os.path.exists(json_path):
        print(f"[ERROR] customization.json not found at {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
        
    print(f"[INFO] Loaded {len(customization_data)} products from customization.json")
    
    updated_count = 0
    for item in customization_data:
        base_img = item.get('baseImage')
        if base_img:
            dir_name = os.path.dirname(base_img)
            old_filename = os.path.basename(base_img)
            new_filename = safe_filename(old_filename)
            
            if old_filename != new_filename:
                new_path = os.path.join(dir_name, new_filename).replace('\\', '/')
                # Ensure starts with a single leading slash if it was there originally
                if base_img.startswith('/') and not new_path.startswith('/'):
                    new_path = '/' + new_path
                
                item['baseImage'] = new_path
                updated_count += 1
                
    if updated_count > 0:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(customization_data, f, indent=2)
        print(f"[SUCCESS] Updated {updated_count} image paths in customization.json!")
    else:
        print("[INFO] All image paths in customization.json are already clean and correct!")

if __name__ == '__main__':
    fix_json_images()
