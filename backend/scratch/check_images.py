import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def check_product_images():
    products = Product.objects.all()[:20]
    print(f"{'ID':<5} {'Name':<40} {'Image Field':<60}")
    print("-" * 110)
    for p in products:
        print(f"{p.id:<5} {p.name[:38]:<40} {str(p.image):<60}")

if __name__ == '__main__':
    check_product_images()
