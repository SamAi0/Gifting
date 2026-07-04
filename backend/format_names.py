import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_product_names_and_slugs():
    products = Product.objects.all()
    updated_count = 0
    
    for p in products:
        # Check if the product has an image path
        image_path = p.image or (p.image_file.name if p.image_file else None)
        
        if image_path:
            # Extract exactly the filename (e.g. 'RC_Premium_Mug_Black.png')
            filename = os.path.basename(image_path)
            
            # Remove extension
            exact_name = os.path.splitext(filename)[0]
            
            # 1. Slug should be the exact filename without extension
            new_slug = exact_name
            
            # 2. Name should be the exact filename, but with underscores replaced by spaces
            new_name = exact_name.replace('_', ' ')
            
            # Prevent duplicate slugs
            base_slug = new_slug
            counter = 1
            while Product.objects.filter(slug=new_slug).exclude(id=p.id).exists():
                new_slug = f"{base_slug}_{counter}"
                counter += 1
            
            p.name = new_name
            p.slug = new_slug
            p.save(update_fields=['name', 'slug'])
            updated_count += 1
            print(f"Updated ID {p.id} -> Name: '{p.name}' | URL Slug: '{p.slug}'")
            
    print(f"\n[SUCCESS] Successfully formatted names and URLs for {updated_count} products!")

if __name__ == '__main__':
    update_product_names_and_slugs()
