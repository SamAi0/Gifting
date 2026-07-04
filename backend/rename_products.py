import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils.text import slugify
from products.models import Product

def rename_products():
    products = Product.objects.all()
    updated_count = 0
    
    for p in products:
        # Check if the product has an image path
        image_path = p.image or (p.image_file.name if p.image_file else None)
        
        if image_path:
            # Extract just the filename (e.g. 'RC_Mug_Black.png' -> 'RC_Mug_Black.png')
            filename = os.path.basename(image_path)
            
            # Remove extension for the name
            name_without_ext = os.path.splitext(filename)[0]
            
            # Optionally replace underscores/hyphens with spaces for a nicer name
            # but user specifically asked for "same to same" exact name.
            new_name = name_without_ext
            new_slug = slugify(new_name)
            
            # Prevent duplicate slugs
            base_slug = new_slug
            counter = 1
            while Product.objects.filter(slug=new_slug).exclude(id=p.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            
            p.name = new_name
            p.slug = new_slug
            p.save(update_fields=['name', 'slug'])
            updated_count += 1
            print(f"Updated ID {p.id} -> Name: {p.name} | Slug: {p.slug}")
            
    print(f"Success! Renamed {updated_count} products based on their image names.")

if __name__ == '__main__':
    rename_products()
