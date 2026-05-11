import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Category

def fix_categories():
    # Define categories and their keywords
    cat_mapping = {
        "Advocate Sets": ["Advocate"],
        "CA Sets": ["CA_Set"],
        "Doctor Sets": ["Doctor"],
        "Diary & Notebook Sets": ["Dairy", "Diary", "Notebook"],
        "Pen & Keychain Sets": ["Pen_Keychain", "PK", "KP"],
        "Corporate Gift Sets": ["Bottle", "Cup", "Set"],
    }
    
    # Create categories if they don't exist
    category_objs = {}
    for cat_name in cat_mapping:
        cat, created = Category.objects.get_or_create(name=cat_name)
        category_objs[cat_name] = cat
        
    products = Product.objects.all()
    updated = 0
    
    for product in products:
        # Skip original products that are already categorized well
        if not product.name.startswith("RC_"):
            # Optional: Check if they are in "Collections" and re-categorize
            pass
            
        found = False
        for cat_name, keywords in cat_mapping.items():
            for kw in keywords:
                if kw.lower() in product.name.lower():
                    product.category = category_objs[cat_name]
                    product.save()
                    updated += 1
                    found = True
                    break
            if found: break
            
    print(f"Successfully re-categorized {updated} products.")

if __name__ == '__main__':
    fix_categories()
