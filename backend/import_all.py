import os
import sys
import json
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category

def import_all():
    json_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    if not os.path.exists(json_path):
        print(f"[ERROR] customization.json not found at {json_path}")
        return
    
    with open(json_path, 'r') as f:
        customization_data = json.load(f)
    
    print(f"[INFO] Loaded {len(customization_data)} products from customization.json")
    
    # Ensure default category exists
    default_category, _ = Category.objects.get_or_create(name="Gift Sets")
    
    # Category mapping helper
    def get_category_name(name):
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

    created_count = 0
    updated_count = 0
    
    for item in customization_data:
        slug = item.get('slug')
        name = item.get('productName')
        image = item.get('baseImage')
        zones = item.get('zones', [])
        
        if not slug or not name:
            continue
            
        category_name = get_category_name(name)
        category, _ = Category.objects.get_or_create(name=category_name)
            
        product, created = Product.all_objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'description': f"Premium {name} for corporate gifting.",
                'price': 999.00,
                'category': category,
                'image': image,
                'customization_config': json.dumps(zones),
                'is_active': True
            }
        )
        
        if created:
            created_count += 1
            # print(f"[NEW] Created product: {name}")
        else:
            product.customization_config = json.dumps(zones)
            # Update image if it was missing or different
            if not product.image:
                product.image = image
            product.save()
            updated_count += 1
    
    print(f"\n{'='*50}")
    print(f"[SUCCESS] Total products in JSON: {len(customization_data)}")
    print(f"[SUCCESS] Newly created: {created_count}")
    print(f"[SUCCESS] Updated existing: {updated_count}")
    print(f"[INFO] Total products in DB now: {Product.objects.count()}")
    print(f"{'='*50}")

if __name__ == '__main__':
    print("Importing products from customization.json...\n")
    import_all()
    print("\nDone!")
