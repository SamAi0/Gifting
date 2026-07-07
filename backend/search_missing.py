import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

missing_items = {
    '1059': 180,
    '1212': 45,
    '1219': 48,
    '1406': 230,
    'A1428': 125,
    '1454': 260,
    '1455': 450,
    '1456': 170,
    '1457': 260,
    '1458': 350,
    '1459': 250,
    '1460': 300,
    '1463': 325,
    '1464': 275,
    '1466': 200,
    '1467': 380,
    '1468': 650,
    '1469': 150,
    '1470': 350,
    '1610': 'Call',
    '1616': 'Call',
    '1617': 'Call',
    '1619': 'Call',
    '1625': 'Call',
    '1627': 'Call',
    '1640': 400,
    '1641': 400,
    '1643': 250,
    '1642': 250,
    '1701': 55,
    '1711': 45,
    '1716': 60,
    '1816': 110,
    '1818': 110,
    '1819': 100,
    '1820': 125,
    '1821': 200,
    '1822': 220,
    '1823': 380,
    '1824': 340,
}

def search_missing():
    print("## Checking Missing Items in DB\n")
    for code, price in missing_items.items():
        products = Product.objects.filter(name__icontains=code)
        if products.exists():
            print(f"Code: {code} (Target Price: {price})")
            for p in products:
                print(f"  -> Found: {p.name} (Current Price: {p.price})")
        else:
            print(f"Code: {code} -> STILL NOT FOUND")
        print()

if __name__ == '__main__':
    search_missing()
