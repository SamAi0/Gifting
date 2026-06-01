import os
import sys
import django
import urllib.parse

sys.path.append(os.path.abspath('backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def list_missing_images():
    static_dir = os.path.abspath(r'backend/static/products')
    actual_files = set(os.listdir(static_dir))
    
    missing_products = []
    
    for p in Product.objects.all():
        if p.image:
            filename = urllib.parse.unquote(p.image.split('/')[-1])
            if filename not in actual_files:
                missing_products.append(f"- **{p.name}** (Expected file: `{filename}`)")
                
    with open('missing_images_list.md', 'w') as f:
        f.write("# 30 Products Missing Images\n\n")
        f.write("\n".join(missing_products))
        f.write("\n")

if __name__ == '__main__':
    list_missing_images()
