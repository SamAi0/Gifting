import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_product_names():
    updates = [
        {"old": "RC 2 in 1 Magnet Diary Set DP 302", "new": " Pen Diary "},
        {"old": "RC 2 in 1 Capsule Magnet Diary Set", "new": "RC 2 in 1 Capsule Magnet Diary Set D - 215"},
        {"old": "RC 2 in 1 Golden Border Magnet Diary Set", "new": "RC 2 in 1 Golden Border Magnet Diary Set D - 207"}
    ]

    for update in updates:
        old_name = update["old"]
        new_name = update["new"]
        try:
            products = Product.objects.filter(name__iexact=old_name)
            if not products.exists():
                print(f"ERROR: Product not found '{old_name}'")
            else:
                for product in products:
                    product.name = new_name
                    product.save(update_fields=['name'])
                print(f"SUCCESS: Updated {products.count()} instance(s) of '{old_name}' -> '{new_name}'")
        except Exception as e:
            print(f"ERROR: Could not update '{old_name}': {e}")

if __name__ == '__main__':
    update_product_names()
