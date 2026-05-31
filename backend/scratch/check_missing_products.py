import os
import sys
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

for name in ['Discount Test Product', 'Speed Pen Golden Clip 2015 Black', 'Speed Pen Golden Clip 2015 Golden', 'Tik tik Curve Pen 2041 White']:
    try:
        p = Product.objects.get(name=name)
        print(f"FOUND: ID={p.id} | Name='{p.name}' | Image='{p.image}'")
    except Product.DoesNotExist:
        print(f"NOT FOUND: Name='{name}'")
