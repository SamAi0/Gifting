import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def search_missing_batch7():
    with open(r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\batch7_prices.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing_section = content.split("> **The following products were not found:**")
    if len(missing_section) > 1:
        missing_lines = missing_section[1].strip().split("\n")
        missing_names = [line.replace("-", "", 1).strip() for line in missing_lines if line.strip().startswith("-")]
        
        for name in missing_names:
            code_match = re.search(r'([0-9]{3,4})', name)
            if code_match:
                code = code_match.group(1)
                products = Product.objects.filter(name__icontains=code)
                if products.exists():
                    print(f"Code: {code} (Original: {name})")
                    for p in products:
                        print(f"  -> Found: {p.name} (Current Price: {p.price})")
                else:
                    print(f"Code: {code} -> STILL NOT FOUND")
            else:
                print(f"No code found for: {name}")

if __name__ == '__main__':
    search_missing_batch7()
