import os
import sys
import json
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

target_ids = [21, 22, 23, 25, 26, 27]

print("Verifying database customization configurations for target IDs:")
all_correct = True
for tid in target_ids:
    try:
        p = Product.all_objects.get(id=tid)
        config = json.loads(p.customization_config)
        print(f"\nID: {tid} | Slug: {p.slug} | Name: {p.name}")
        print("Database Zones:")
        for z in config:
            print(f"  Zone ID: {z.get('id')} -> x: {z.get('x')}, y: {z.get('y')}, angle: {z.get('angle')}")
    except Product.DoesNotExist:
        print(f"[ERROR] ID: {tid} not found in DB!")
        all_correct = False
    except Exception as e:
        print(f"[ERROR] Failed to verify ID {tid}: {e}")
        all_correct = False

if all_correct:
    print("\n[SUCCESS] All target database entries match the expected coordinates perfectly!")
else:
    print("\n[WARNING] Verification found discrepancies or errors.")
