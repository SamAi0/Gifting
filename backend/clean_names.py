import os
import django
import re

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def clean_names():
    products = Product.objects.filter(name__startswith="RC_")
    updated = 0
    
    for p in products:
        # Example: RC_Bottle_Pen_Keychain_Set_BPK_132_Black
        # Remove RC_
        name = p.name.replace("RC_", "")
        # Remove underscores
        name = name.replace("_", " ")
        # Remove color at the end if present
        colors = ['Black', 'Blue', 'Red', 'White', 'Brown', 'Tan', 'Silver', 'Golden', 'Grey', 'Crock', 'Wooden']
        for color in colors:
            name = re.sub(rf'\s+{color}$', '', name, flags=re.IGNORECASE)
        
        # Proper case
        name = name.title()
        
        # Move SKU to parenthesis at the end
        sku_match = re.search(r'([A-Z]{1,3}\s+\d{3})', name)
        if sku_match:
            sku = sku_match.group(1).replace(" ", "-")
            name = name.replace(sku_match.group(1), "").strip()
            name = f"{name} ({sku})"
            
        p.name = name
        p.save()
        updated += 1
        
    print(f"Cleaned {updated} product names.")

if __name__ == '__main__':
    clean_names()
