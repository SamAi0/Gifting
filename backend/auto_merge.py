import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, ProductVariant, Attribute, AttributeValue

# Comprehensive list of colors to look for at the end of product names
COLORS = [
    'black', 'white', 'red', 'blue', 'green', 'yellow', 'orange', 
    'purple', 'pink', 'silver', 'gold', 'brown', 'grey', 'gray', 
    'tan', 'teal', 'navy', 'maroon', 'magenta', 'cyan', 'multicolor'
]

def auto_merge_products(dry_run=True):
    print(f"Starting Auto-Merge... (Dry Run: {dry_run})")
    
    products = Product.objects.all().order_by('id')
    
    # Dictionary to group products by their base name
    # Format: { 'base_name': [product1, product2, ...] }
    grouped_products = {}
    
    color_regex = re.compile(r'\s+(' + '|'.join(COLORS) + r')\s*$', re.IGNORECASE)
    
    for p in products:
        match = color_regex.search(p.name)
        if match:
            # It has a color at the end
            color_found = match.group(1).title()
            base_name = p.name[:match.start()].strip()
            
            # If the base name ends with a hyphen, remove it too
            if base_name.endswith('-'):
                base_name = base_name[:-1].strip()
                
            if base_name not in grouped_products:
                grouped_products[base_name] = []
            
            grouped_products[base_name].append({
                'product': p,
                'color': color_found
            })
        else:
            # Also group products that don't explicitly have a color, 
            # maybe they are the base product itself?
            # E.g. "RC Cup 997" vs "RC Cup 997 Red"
            base_name = p.name.strip()
            if base_name not in grouped_products:
                grouped_products[base_name] = []
                
            grouped_products[base_name].append({
                'product': p,
                'color': 'Default'
            })
            
    # Now process the groups
    merge_count = 0
    
    color_attr, _ = Attribute.objects.get_or_create(name='Color') if not dry_run else (None, False)
    
    for base_name, items in grouped_products.items():
        if len(items) > 1:
            # We have multiple items for this base name, meaning we need to merge!
            print(f"\nGroup: {base_name}")
            
            if not dry_run:
                # The first item becomes the main product
                main_item = items[0]
                main_product = main_item['product']
                main_color = main_item['color']
                
                # Update main product name to base_name
                main_product.name = base_name
                main_product.save(update_fields=['name'])
                
                # Create variant for main product
                color_val, _ = AttributeValue.objects.get_or_create(attribute=color_attr, value=main_color)
                main_variant, _ = ProductVariant.objects.get_or_create(
                    product=main_product,
                    color_name=main_color,
                    defaults={'image': main_product.image, 'stock': 100}
                )
                main_variant.attribute_values.add(color_val)
                print(f"  -> Kept Main Product (ID: {main_product.id}), Created '{main_color}' variant.")
                
                # Merge the rest
                for item in items[1:]:
                    other_p = item['product']
                    other_color = item['color']
                    
                    if other_color == 'Default':
                        other_color = 'Standard' # Avoid duplicate default
                        
                    color_val, _ = AttributeValue.objects.get_or_create(attribute=color_attr, value=other_color)
                    variant, _ = ProductVariant.objects.get_or_create(
                        product=main_product,
                        color_name=other_color,
                        defaults={'image': other_p.image, 'stock': 100}
                    )
                    variant.attribute_values.add(color_val)
                    
                    # Delete old product
                    other_p.delete()
                    merge_count += 1
                    print(f"  -> Merged '{other_color}' variant from ID {other_p.id} and deleted original.")
            else:
                for item in items:
                    print(f"  - {item['product'].name} (Color: {item['color']})")
                merge_count += len(items) - 1
                
    if dry_run:
        print(f"\n[DRY RUN] If executed, {merge_count} products would be merged into variants.")
    else:
        print(f"\n[SUCCESS] Successfully merged {merge_count} products into variants!")

if __name__ == '__main__':
    # First do a dry run, if we run it with arg 'execute', do the real thing
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'execute':
        auto_merge_products(dry_run=False)
    else:
        auto_merge_products(dry_run=True)
