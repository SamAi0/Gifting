import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_999_items():
    print("## Updating 999.00 Priced Items")
    
    # 1. Delete "logo"
    try:
        p_logo = Product.objects.get(name__iexact="logo")
        print(f"Deleting product: {p_logo.name}")
        p_logo.delete()
    except Product.DoesNotExist:
        print("Product 'logo' not found.")
        
    # 2. Merge 1636 Bamboo & Wood
    try:
        p_bamboo = Product.objects.get(name__icontains="1636 bamboo")
        p_wood = Product.objects.get(name__icontains="1636 wood")
        print(f"Merging {p_bamboo.name} into {p_wood.name}")
        p_wood.name = "RC - Pendrive - 1636 Bamboo / Wood"
        p_wood.save()
        p_bamboo.delete()
    except Product.DoesNotExist:
        print("1636 bamboo or wood not found.")

    # 3. Explicit Pricing Updates (Base * 1.6)
    updates = [
        ("RC 2 in 1 Capsule Magnet Diary Set", 220),
        ("RC 2 in 1 Golden Border Magnet Diary Set", 220),
        ("RC 2 in 1 Jari Diary Set", 220),
        ("RC Organizer N TRP 0-322", 550),
        ("RC Organizer N TRB 0-320", 650),
        ("RC Organizer P SRCA 0-323", 280),
        ("RC 5202 Pen Stand 1416", 130),
        ("RC - Mobile Stand with Card Holder", 55),
        ("multicolor Analog Desktop Organizer Set with calendar", 190),
        ("RC - Copper Printed Pot - 1931 (2)", 650),
        ("Corporate Table Top Pen & Mobile Stand", 250),
        ("RC - Steel Glass without Clip - 1922", 110),
        ("RC - Straight Vaccum Bottle - 1918pink", 180),
        ("Wooden Table Clock With Pen Stand", 325),
        ("clock with pen stand", 200),
        ("RC Bottle A1954", 250),
        ("RC Cup 896", 380),
        ("Cricket Gift pen stand", 350),
        ("Perpetual Calendar Pen Holder with LCD display digital clock pen holder", 150),
        ("RC Belt Purse Bottle Set BBP 817", 390),
        ("silver plane pen holder stand", 380),
        ("Silver Metal Table Clock Pen Stand", 250),
    ]
    
    for name, base_price in updates:
        try:
            p = Product.objects.get(name=name)
            final_price = round(base_price * 1.6)
            p.price = final_price
            p.save(update_fields=['price'])
            print(f"Updated {p.name}: Base {base_price} -> Final {final_price}")
        except Product.DoesNotExist:
            print(f"Item not found for update: {name}")

    # 4. Handle "Call" Items (Set to 0.00 so they don't show as 999)
    remaining_999 = Product.objects.filter(price=999.0)
    count = 0
    for p in remaining_999:
        p.price = 0.0
        p.save(update_fields=['price'])
        count += 1
        
    print(f"\nSet {count} 'Call' / Unpriced items to Rs. 0.00 to remove the 999 placeholder.")
    
if __name__ == '__main__':
    update_999_items()
