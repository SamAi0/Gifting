import os
import sys
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

target_ids = [21, 22, 23, 25, 26, 27]

print("Checking target product IDs in database:")
for tid in target_ids:
    try:
        p = Product.all_objects.get(id=tid)
        print(f"ID: {tid} | Slug: {p.slug} | Name: {p.name} | Is Deleted: {p.is_deleted}")
    except Product.DoesNotExist:
        print(f"ID: {tid} does not exist in DB!")
