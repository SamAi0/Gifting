import os
import sys
import json
import re
import django

# Setup Django environment so we can use models
if '__file__' in globals():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BACKEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
else:
    # If run via manage.py shell < scripts/process_products.py, CWD is backend/
    BACKEND_DIR = os.getcwd()

FRONTEND_DIR = os.path.abspath(os.path.join(BACKEND_DIR, '..', 'frontend'))

if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category
from django.contrib.auth import get_user_model

# Path to the customization JSON
JSON_PATH = os.path.join(FRONTEND_DIR, 'src', 'data', 'customization.json')
# Path to the products images
STATIC_PRODUCTS_PATH = os.path.join(BACKEND_DIR, 'static', 'products')

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
    
    if os.path.exists(STATIC_PRODUCTS_PATH):
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
    else:
        print(f"Warning: {STATIC_PRODUCTS_PATH} does not exist.")

    # Save back to JSON
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    print(f"Successfully added {new_items_count} new products to customization.json")
    
    print("Syncing data to Database...")
    # Clean the database to prevent duplicates on redeploy
    Product.all_objects.all().delete()
    print("Cleared existing products from DB.")
    
    # Pre-create all categories
    categories_map = {
        "Gift Sets": Category.objects.get_or_create(name="Gift Sets")[0],
        "Drinkware": Category.objects.get_or_create(name="Drinkware")[0],
        "Diaries & Notebooks": Category.objects.get_or_create(name="Diaries & Notebooks")[0],
        "Pens": Category.objects.get_or_create(name="Pens")[0],
        "Office Accessories": Category.objects.get_or_create(name="Office Accessories")[0],
        "Tech & Gadgets": Category.objects.get_or_create(name="Tech & Gadgets")[0],
        "Keychains": Category.objects.get_or_create(name="Keychains")[0],
        "Bags & Wallets": Category.objects.get_or_create(name="Bags & Wallets")[0]
    }
    
    db_items_count = 0
    products_to_create = []
    
    for item in data:
        name = item['productName'].lower()
        
        # Determine category based on keywords
        if any(k in name for k in ['set', 'combo', 'in 1', '4 in 1', '2 in 1', '3 in 1']):
            cat = categories_map["Gift Sets"]
        elif any(k in name for k in ['bottle', 'cup', 'mug', 'flask', 'glass', 'copper']):
            cat = categories_map["Drinkware"]
        elif any(k in name for k in ['diary', 'notebook', 'file', 'dairy']):
            cat = categories_map["Diaries & Notebooks"]
        elif 'pen' in name and 'stand' not in name:
            cat = categories_map["Pens"]
        elif any(k in name for k in ['stand', 'cardholder', 'organizer', 'holder']):
            cat = categories_map["Office Accessories"]
        elif any(k in name for k in ['pendrive', 'powerbank', 'speaker', 'clock']):
            cat = categories_map["Tech & Gadgets"]
        elif any(k in name for k in ['keychain', 'ring']):
            cat = categories_map["Keychains"]
        elif any(k in name for k in ['purse', 'wallet', 'bag', 'pouch']):
            cat = categories_map["Bags & Wallets"]
        else:
            cat = categories_map["Gift Sets"] # default fallback
            
        products_to_create.append(
            Product(
                name=item['productName'],
                slug=item['slug'],
                description=f"Premium {item['productName']} for corporate gifting.",
                price=999.00,
                category=cat,
                image=item['baseImage'],
                customization_config=json.dumps(item.get('zones', [])),
                is_active=True
            )
        )
    Product.objects.bulk_create(products_to_create, batch_size=200, ignore_conflicts=True)
    db_items_count = len(products_to_create)
        
    print(f"Successfully inserted {db_items_count} products into Database.")
    
    print("\nSetting up Admin User...")
    User = get_user_model()
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", admin_password)
        print("Superuser 'admin' created successfully.")
    else:
        print("Superuser 'admin' already exists.")

# When piped via manage.py shell < ..., __name__ may not be '__main__'.
# Only run main if executed directly.
if __name__ == '__main__' or 'manage' in getattr(sys.modules['__main__'], '__file__', ''):
    main()
