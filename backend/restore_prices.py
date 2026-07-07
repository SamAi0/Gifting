import os
import django
import csv
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def restore_prices():
    try:
        with open('prices.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            for row in reader:
                pid = row['ID']
                original_price = row['Price']
                
                try:
                    p = Product.objects.get(id=pid)
                    if str(p.price) != str(original_price):
                        p.price = Decimal(str(original_price))
                        p.save(update_fields=['price'])
                        count += 1
                except Product.DoesNotExist:
                    pass
            print(f"Successfully restored prices for {count} products.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    restore_prices()
