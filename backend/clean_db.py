import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def delete_empty_products():
    print("Finding dummy products without an image...")
    
    # Find products where image is null or empty
    # Also handle the edge case where they might have an image_file but no image string?
    # Our previous check confirmed that ALL 826 products have BOTH image and image_file empty.
    empty_products = Product.objects.filter(image__isnull=True).exclude(image__exact='')
    # Actually, in Django CharFields, empty string is stored, not null. Let's cover both.
    from django.db.models import Q
    
    empty_products = Product.objects.filter(
        Q(image__isnull=True) | Q(image__exact='')
    ).filter(
        Q(image_file__isnull=True) | Q(image_file__exact='')
    )
    
    count_to_delete = empty_products.count()
    print(f"Found {count_to_delete} products to delete.")
    
    if count_to_delete > 0:
        deleted_count, _ = empty_products.delete()
        print(f"[SUCCESS] Deleted {deleted_count} dummy products.")
    
    total_remaining = Product.objects.count()
    print(f"[INFO] Total clean products remaining in database: {total_remaining}")

if __name__ == '__main__':
    delete_empty_products()
