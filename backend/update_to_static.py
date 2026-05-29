import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_to_static():
    products = Product.objects.all()
    for p in products:
        if p.image:
            old_image = p.image
            
            # Target: /static/products/filename.png
            clean_path = p.image.replace('static/', '').replace('media/', '').lstrip('/')
            new_image = f"/static/{clean_path}"
            
            if old_image != new_image:
                p.image = new_image
                p.save()
                print(f"Updated: {p.name} | {old_image} -> {new_image}")
            else:
                print(f"Skipped (already correct): {p.name} | {p.image}")

if __name__ == "__main__":
    update_to_static()
