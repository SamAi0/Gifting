import os
import django
import re
from collections import defaultdict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def delete_bad_duplicates():
    print("## Deleting Bad Duplicates (Rules 1, 2, 3)")
    
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
    
    deleted_count = 0
    deleted_names = []
    
    for code, prods in duplicates.items():
        # First, filter out items that have colors in their names
        # Common colors: red, blue, green, pink, black, white, yellow, orange, purple, teal, brown, golden, silver
        colors = ['red', 'blue', 'green', 'pink', 'black', 'white', 'yellow', 'orange', 'purple', 'teal', 'brown', 'golden', 'silver', '&']
        
        # If any product in the group has a color, we should be very careful.
        # But we can still delete a generic 'rc' if there's a generic 'RC'.
        
        # Identify "bad" names
        bad_prods = []
        good_prods = []
        
        for p in prods:
            name = p.name
            # Check for bad formatting: starts with lowercase 'rc ', has no hyphens when others do, or has typos like 'Fflip'
            is_bad = False
            if name.startswith('rc ') or name.startswith('sr ') or 'Fflip' in name:
                is_bad = True
                
            if is_bad:
                bad_prods.append(p)
            else:
                good_prods.append(p)
                
        # If we have both good and bad products in the SAME code group,
        # we can safely delete the bad ones, provided they aren't unique color variants 
        # not present in the good ones.
        if bad_prods and good_prods:
            for bad_p in bad_prods:
                # Make sure it's actually safe to delete.
                # If the bad one specifies a color that the good one doesn't, we might lose a variant.
                # But typically 'rc jute file 1507' vs 'RC - Jute File - 1507' is totally safe.
                bad_name_lower = bad_p.name.lower()
                has_unique_color = False
                for c in colors:
                    if c in bad_name_lower:
                        # Does any good prod have this color?
                        if not any(c in gp.name.lower() for gp in good_prods):
                            has_unique_color = True
                            
                if not has_unique_color or 'Fflip' in bad_p.name:
                    print(f"DELETING: {bad_p.name} (ID: {bad_p.id})")
                    deleted_names.append(bad_p.name)
                    bad_p.delete()
                    deleted_count += 1
                else:
                    print(f"SKIPPING (has unique color): {bad_p.name}")
                    
    print(f"\nDeleted {deleted_count} badly formatted duplicate items.")

if __name__ == '__main__':
    delete_bad_duplicates()
