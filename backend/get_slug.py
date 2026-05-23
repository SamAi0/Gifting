import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

try:
    product = Product.objects.get(id=1162)
    print(f"SLUG:{product.slug}")
except Exception as e:
    print(f"ERROR:{e}")
