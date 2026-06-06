import os
import django
import sys

sys.path.append(os.path.abspath('backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
import urllib.parse

def verify_images():
    static_dir = os.path.abspath(r'backend/static/products')
    actual_files = set(os.listdir(static_dir))
    
    missing_count = 0
    for p in Product.objects.all():
        if p.image:
            # Extract filename from path
            filename = urllib.parse.unquote(p.image.split('/')[-1])
            if filename not in actual_files:
                print(f"Broken DB image link: Product ID {p.id} ({p.name}) -> {p.image} -> expects {filename}")
                missing_count += 1
                
    print(f"Total broken links: {missing_count}")

if __name__ == '__main__':
    verify_images()
