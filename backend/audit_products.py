import os
import sys
import json
import django
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category, ProductVariant

def audit():
    print("=" * 60)
    print("PRODUCT DATA AUDIT - DEEP SCAN")
    print("=" * 60)

    products = Product.objects.all()
    categories = Category.objects.all()
    total_products = products.count()
    
    errors = []
    warnings = []
    
    # Trackers
    names = []
    prices = []
    
    for p in products:
        names.append(p.name)
        prices.append(float(p.price))
        
        # 1. Price check (Placeholder check)
        if p.price == 999.0:
            warnings.append(f"[PLACEHOLDER] Product '{p.name}' has default price 999.0")
        elif p.price <= 0:
            errors.append(f"[ERROR] Product '{p.name}' has invalid price {p.price}")
        
        # 2. Description check
        if not p.description or len(p.description.strip()) < 20:
            warnings.append(f"[CONTENT] Product '{p.name}' has poor description: '{p.description}'")
            
        # 3. Image check
        if not p.image:
            errors.append(f"[ERROR] Product '{p.name}' has NO image path")
        else:
            img_path = os.path.join('static', 'products', os.path.basename(p.image))
            if not os.path.exists(img_path):
                errors.append(f"[IMAGE] Product '{p.name}' image file NOT FOUND: {img_path}")

        # 4. SEO Metadata check (Highly likely to be missing)
        if not p.meta_title or p.meta_title == p.name:
             warnings.append(f"[SEO] Product '{p.name}' missing unique meta_title")
        if not p.meta_description or len(p.meta_description) < 50:
             warnings.append(f"[SEO] Product '{p.name}' missing or short meta_description")

        # 5. Structured Data check
        try:
            features = json.loads(p.key_features)
            if not features or len(features) == 0:
                warnings.append(f"[DATA] Product '{p.name}' has NO key features")
        except:
            errors.append(f"[ERROR] Product '{p.name}' has invalid JSON in key_features")

        try:
            specs = json.loads(p.specifications)
            if not specs or len(specs) == 0:
                 warnings.append(f"[DATA] Product '{p.name}' has NO specifications")
        except:
            errors.append(f"[ERROR] Product '{p.name}' has invalid JSON in specifications")

    # 6. Global checks
    from collections import Counter
    name_counts = Counter(names)
    dup_names = {name: count for name, count in name_counts.items() if count > 1}
    if dup_names:
        for name, count in dup_names.items():
            errors.append(f"[DUPLICATE] Name '{name}' used {count} times")

    # 7. Check synchronization with customization.json
    json_path = os.path.join('..', 'frontend', 'src', 'data', 'customization.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            custom_data = json.load(f)
            json_slugs = {item.get('slug') for item in custom_data if item.get('slug')}
            db_slugs = {p.slug for p in products}
            
            missing_in_db = json_slugs - db_slugs
            if missing_in_db:
                errors.append(f"[SYNC] {len(missing_in_db)} products in JSON but MISSING from Database")
    
    # Summary
    print(f"Total Products: {total_products}")
    print(f"Total Categories: {categories.count()}")
    print("-" * 60)
    
    # Categorize warnings
    seo_warns = [w for w in warnings if "[SEO]" in w]
    placeholder_warns = [w for w in warnings if "[PLACEHOLDER]" in w]
    content_warns = [w for w in warnings if "[CONTENT]" in w]
    data_warns = [w for w in warnings if "[DATA]" in w]
    
    print(f"ERRORS: {len(errors)}")
    print(f"WARNINGS: {len(warnings)}")
    print(f"  - SEO Issues: {len(seo_warns)}")
    print(f"  - Placeholder Prices: {len(placeholder_warns)}")
    print(f"  - Content Issues: {len(content_warns)}")
    print(f"  - Structured Data Issues: {len(data_warns)}")
    print("-" * 60)
    
    if errors:
        print("\nTOP ERRORS:")
        for err in errors[:20]:
            print(err)
        if len(errors) > 20:
            print(f"... and {len(errors) - 20} more errors")
            
    if warnings:
        print("\nSAMPLE WARNINGS:")
        # Show a few of each type
        for warns in [seo_warns[:3], placeholder_warns[:3], content_warns[:3], data_warns[:3]]:
            for w in warns:
                print(w)


if __name__ == '__main__':
    audit()
