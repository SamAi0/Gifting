import os
import django
import sys
from django.db import connection

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from products.models import Product

def reset_sequence():
    print("Products are already deleted. Resetting sequence...")
    with connection.cursor() as cursor:
        if connection.vendor == 'postgresql':
            print("Detected PostgreSQL. Resetting sequence with ALTER SEQUENCE...")
            cursor.execute("ALTER SEQUENCE products_product_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE products_productimage_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE products_productvariant_id_seq RESTART WITH 1;")
        elif connection.vendor == 'sqlite':
            print("Detected SQLite. Resetting sequence with sqlite_sequence...")
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products_product';")
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products_productimage';")
            cursor.execute("UPDATE sqlite_sequence SET seq = 0 WHERE name = 'products_productvariant';")
        else:
            print(f"Unknown database vendor: {connection.vendor}")
            
    print("Database sequence reset complete.")

if __name__ == "__main__":
    reset_sequence()
