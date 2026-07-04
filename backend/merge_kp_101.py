import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, ProductVariant, Attribute, AttributeValue

def merge_kp_101():
    # Find all KP 101 products
    kp_products = list(Product.objects.filter(name__icontains='kp 101').order_by('id'))
    
    if not kp_products:
        print("No KP 101 products found.")
        return
        
    print(f"Found {len(kp_products)} KP 101 products.")
    
    # 1. Create Color attribute if it doesn't exist
    color_attr, _ = Attribute.objects.get_or_create(name='Color')
    
    # 2. Pick the main product (e.g., the Black one, or just the first one)
    main_product = kp_products[0]
    
    print(f"Main Product Selected: {main_product.name} (ID: {main_product.id})")
    
    # 3. Update main product details
    main_product.name = "RC Pen Keychain Set KP 101"
    main_product.price = Decimal('75.00')
    main_product.save()
    print("Main product name updated and price set to 75.00.")
    
    # 4. Extract color from the main product's original name and create a variant for it
    def get_color(name):
        name_lower = name.lower()
        if 'black' in name_lower: return 'Black'
        if 'red' in name_lower: return 'Red'
        if 'blue' in name_lower: return 'Blue'
        if 'tan' in name_lower: return 'Tan'
        return 'Default'
        
    main_color = get_color(main_product.name)
    color_val, _ = AttributeValue.objects.get_or_create(attribute=color_attr, value=main_color)
    
    # Create variant for the main product's original color if it doesn't exist
    main_variant, _ = ProductVariant.objects.get_or_create(
        product=main_product,
        color_name=main_color,
        defaults={'image': main_product.image, 'stock': 100}
    )
    main_variant.attribute_values.add(color_val)
    print(f"Created variant for main product color: {main_color}")
    
    # 5. Process the rest of the products
    for other_p in kp_products[1:]:
        color_name = get_color(other_p.name)
        color_val, _ = AttributeValue.objects.get_or_create(attribute=color_attr, value=color_name)
        
        variant, created = ProductVariant.objects.get_or_create(
            product=main_product,
            color_name=color_name,
            defaults={'image': other_p.image, 'stock': 100}
        )
        variant.attribute_values.add(color_val)
        
        # Soft delete or hard delete the old product?
        # Let's hard delete to keep DB clean, since they are essentially duplicates of the same model.
        other_id = other_p.id
        other_p.delete()
        
        print(f"Merged {color_name} variant from ID {other_id} and deleted the old product.")
        
    print("\n[SUCCESS] Merge Complete! 1 Main Product with variants remaining.")

if __name__ == '__main__':
    merge_kp_101()
