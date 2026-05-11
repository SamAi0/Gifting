import os
import json
import re

# Path to the customization JSON
JSON_PATH = r"c:\Users\Asus\Downloads\New folder\Gifting\frontend\src\data\customization.json"
# Path to the products images
STATIC_PRODUCTS_PATH = r"c:\Users\Asus\Downloads\New folder\Gifting\backend\static\products"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def clean_name(filename):
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Replace underscores with spaces
    name = name.replace('_', ' ')
    # Capitalize each word
    return name.title()

def generate_zones(product_id_prefix):
    zones = []
    for i in range(1, 8):
        zones.append({
            "id": f"zone-{product_id_prefix}-{i}",
            "type": "text",
            "x": 500,
            "y": 100 + (i * 100),
            "originX": "center",
            "originY": "center",
            "angle": 0,
            "maxWidth": 400,
            "maxChars": 15,
            "fontFamily": "Outfit, sans-serif",
            "fontSize": 24,
            "minFontSize": 12,
            "fill": "#000000",
            "opacity": 0.9,
            "placeholder": f"ZONE {i} TEXT"
        })
    return zones

def main():
    # Load existing data
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    existing_slugs = {item['slug'] for item in data}
    existing_images = {item['baseImage'] for item in data}
    
    if data:
        max_id = max(item['productId'] for item in data)
    else:
        max_id = 0

    new_items_count = 0
    files = sorted(os.listdir(STATIC_PRODUCTS_PATH))
    
    for filename in files:
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue
            
        base_image = f"/static/products/{filename}"
        if base_image in existing_images:
            continue
            
        name = clean_name(filename)
        slug = slugify(name)
        
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        max_id += 1
        new_item = {
            "productId": max_id,
            "productName": name,
            "slug": slug,
            "baseImage": base_image,
            "zones": generate_zones(max_id)
        }
        
        data.append(new_item)
        existing_slugs.add(slug)
        new_items_count += 1

    # Save back to JSON
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully added {new_items_count} new products to customization.json")

if __name__ == "__main__":
    main()
