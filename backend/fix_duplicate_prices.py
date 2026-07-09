import os
import django
import re
from collections import defaultdict
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_duplicate_prices():
    print("## Fixing Duplicate Product Prices")
    
    products = Product.objects.all()
    code_groups = defaultdict(list)
    
    for p in products:
        name = p.name
        code = None
        parts = name.replace("-", " ").replace("(", " ").replace(")", " ").split()
        if parts:
            last = parts[-1].lower()
            if any(char.isdigit() for char in last):
                code = last
            else:
                n_match = re.search(r'([0-9]{3,4}[A-Za-z]?)', name)
                if n_match:
                    code = n_match.group(1).lower()
        if code:
            code_groups[code].append(p)
            
    duplicates = {code: prods for code, prods in code_groups.items() if len(prods) > 1}
    
    fixed_count = 0
    for code, prods in duplicates.items():
        # Check if there's a mix of 999.00 and other prices
        prices = [float(p.price) for p in prods]
        if 999.0 in prices and len(set(prices)) > 1:
            # Find the "correct" price which is not 999.0
            non_999_prods = [p for p in prods if float(p.price) != 999.0 and float(p.price) != 0.0]
            
            for p_999 in [p for p in prods if float(p.price) == 999.0]:
                best_match = None
                best_overlap = -1
                
                words_999 = set(p_999.name.replace("-", " ").lower().split())
                
                for p_valid in non_999_prods:
                    words_valid = set(p_valid.name.replace("-", " ").lower().split())
                    overlap = len(words_999.intersection(words_valid))
                    if overlap > best_overlap:
                        best_overlap = overlap
                        best_match = p_valid
                
                if best_match and best_overlap >= 1:
                    print(f"Fixing ID {p_999.id} ({p_999.name}): Rs. 999.00 -> Rs. {best_match.price} (Matched with ID {best_match.id})")
                    p_999.price = best_match.price
                    p_999.save(update_fields=['price'])
                    fixed_count += 1
                    
    print(f"\nFixed {fixed_count} duplicate items that had placeholder prices.")

if __name__ == '__main__':
    fix_duplicate_prices()
