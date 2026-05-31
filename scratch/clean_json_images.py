import os
import json
import re

def safe_filename(filename):
    """
    Converts a filename to a safe version matching backend/fix_media_names.py:
    - Lowercase
    - Replaces spaces and special characters with underscores
    - Preserves the extension
    """
    name, ext = os.path.splitext(filename)
    # Remove special characters like &
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[-\s]+', '_', name)
    return f"{name}{ext}"

def main():
    json_path = os.path.join('frontend', 'src', 'data', 'customization.json')
    if not os.path.exists(json_path):
        print("[ERROR] customization.json not found!")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"[INFO] Loaded {len(data)} products from customization.json")
    
    static_products_dir = os.path.join('backend', 'static', 'products')
    
    updated_count = 0
    not_found_on_disk = 0

    for item in data:
        base_image = item.get('baseImage')
        if not base_image:
            continue
            
        old_filename = os.path.basename(base_image)
        new_filename = safe_filename(old_filename)
        
        if old_filename != new_filename:
            # Check if the clean file exists on disk
            clean_file_path = os.path.join(static_products_dir, new_filename)
            
            # Try matching case-insensitively if exact doesn't exist
            if not os.path.exists(clean_file_path):
                # Try locating it by lower-casing the list
                files_on_disk = os.listdir(static_products_dir)
                for f in files_on_disk:
                    if f.lower() == new_filename.lower():
                        new_filename = f
                        clean_file_path = os.path.join(static_products_dir, new_filename)
                        break
            
            if os.path.exists(clean_file_path):
                new_path = f"/static/products/{new_filename}"
                item['baseImage'] = new_path
                updated_count += 1
            else:
                not_found_on_disk += 1
                # Still update to safe name as fallback
                new_path = f"/static/products/{new_filename}"
                item['baseImage'] = new_path
                updated_count += 1

    # Save the updated customization.json back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"[SUCCESS] Updated {updated_count} image paths in customization.json")
    print(f"[INFO] {not_found_on_disk} clean images were not found on disk but updated to follow convention as fallback.")

if __name__ == '__main__':
    main()
