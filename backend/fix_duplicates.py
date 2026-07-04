import os
import django
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_duplicates():
    print("Finding duplicates by name...")
    # Group by name and find counts > 1
    duplicate_names = Product.objects.values('name').annotate(count=Count('id')).filter(count__gt=1)
    
    deleted_count = 0
    for dup in duplicate_names:
        name = dup['name']
        # Fetch all products with this exact name, sorted by lowest ID first
        products = list(Product.objects.filter(name=name).order_by('id'))
        
        if len(products) > 1:
            original = products[0]
            duplicates_to_delete = products[1:]
            
            for p in duplicates_to_delete:
                # Delete the duplicate product
                print(f"Deleting duplicate ID {p.id} for product '{name}' (Keeping original ID {original.id})")
                p.delete()
                deleted_count += 1
                
    print(f"\n[SUCCESS] Safely deleted {deleted_count} duplicate products!")
    print(f"Total products remaining: {Product.objects.count()}")

def clean_slugs():
    print("\nCleaning up URLs (Slugs)...")
    products = Product.objects.all()
    updated_count = 0
    
    for p in products:
        original_slug = p.slug
        if ' ' in p.slug:
            # Replace spaces with underscores
            new_slug = p.slug.replace(' ', '_')
            
            # Handle potential collision just in case
            base_slug = new_slug
            counter = 1
            while Product.objects.filter(slug=new_slug).exclude(id=p.id).exists():
                new_slug = f"{base_slug}_{counter}"
                counter += 1
                
            p.slug = new_slug
            p.save(update_fields=['slug'])
            updated_count += 1
            print(f"Cleaned Slug ID {p.id}: '{original_slug}' -> '{p.slug}'")
            
    print(f"\n[SUCCESS] Cleaned spaces from {updated_count} URLs!")

if __name__ == '__main__':
    fix_duplicates()
    clean_slugs()
