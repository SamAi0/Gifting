import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text.strip('-')

def get_category(name):
    name = name.lower()
    if any(k in name for k in ['cup', 'mug', 'bottle', 'flask', 'thermos']):
        return "Drinkware"
    if any(k in name for k in ['pen', 'diary', 'notebook', 'stationary']):
        return "Stationery"
    if 'set' in name:
        return "Gift Sets"
    if any(k in name for k in ['keychain', 'cardholder', 'purse', 'belt', 'wallet', 'passport']):
        return "Accessories"
    if any(k in name for k in ['stand', 'clock', 'light', 'ashokstambh', 'hub']):
        return "Office Gifts"
    return "Gift Sets"

def main():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    static_products_dir = os.path.join(backend_dir, 'static', 'products')
    json_path = os.path.join(backend_dir, '..', 'frontend', 'src', 'data', 'customization.json')

    if not os.path.exists(json_path):
        print(f"Error: customization.json not found at {json_path}")
        return

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except:
            data = []

    existing_images = {os.path.basename(item['baseImage']) for item in data}
    files = [f for f in os.listdir(static_products_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    new_files = [f for f in files if f not in existing_images]
    print(f"Found {len(new_files)} new images to register.")

    if not new_files:
        print("No new images to add.")
        return

    max_id = max([item.get('productId', 0) for item in data]) if data else 0

    for filename in new_files:
        max_id += 1
        # Clean name: remove extension, replace underscores/dashes with spaces
        display_name = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ')
        # Remove 'RC ' prefix if exists
        display_name = re.sub(r'^RC\s+', '', display_name, flags=re.IGNORECASE)
        
        slug = slugify(display_name)
        
        # Default zones: 1 Text, 1 Logo
        new_entry = {
            "productId": max_id,
            "productName": display_name,
            "slug": slug,
            "baseImage": f"/static/products/{filename}",
            "zones": [
                {
                    "id": "name-1",
                    "type": "text",
                    "x": 500,
                    "y": 150,
                    "originX": "center",
                    "originY": "center",
                    "angle": 0,
                    "maxWidth": 400,
                    "maxChars": 15,
                    "fontFamily": "Inter, sans-serif",
                    "fontSize": 32,
                    "minFontSize": 20,
                    "fill": "#000000",
                    "opacity": 1.0,
                    "placeholder": "Your Name"
                },
                {
                    "id": "logo-1",
                    "type": "image",
                    "x": 500,
                    "y": 250,
                    "originX": "center",
                    "originY": "center",
                    "angle": 0,
                    "width": 120,
                    "height": 120,
                    "placeholderImage": "/static/placeholders/logo.png"
                }
            ]
        }
        data.append(new_entry)

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully added {len(new_files)} products to customization.json.")
    print("Next step: Run 'python import_all.py' and 'python scripts/populate_real_data.py'")

if __name__ == "__main__":
    main()
