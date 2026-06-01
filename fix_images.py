import os
import json
import urllib.parse
import django
import sys

sys.path.append(os.path.abspath('backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_images():
    static_dir = os.path.abspath(r'backend/static/products')
    json_path = os.path.abspath(r'frontend/src/data/customization.json')
    
    if not os.path.exists(static_dir):
        print(f"Static dir not found: {static_dir}")
        return
        
    actual_files = os.listdir(static_dir)
    # create a case-insensitive map
    lower_to_actual = {f.lower(): f for f in actual_files}
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    fixed_count = 0
    
    for item in data:
        base_img = item.get('baseImage')
        if base_img:
            filename = urllib.parse.unquote(base_img.split('/')[-1])
            # If filename doesn't match case-sensitively
            if filename not in actual_files:
                # Try case-insensitive
                if filename.lower() in lower_to_actual:
                    correct_filename = lower_to_actual[filename.lower()]
                    item['baseImage'] = f"/static/products/{urllib.parse.quote(correct_filename)}"
                    fixed_count += 1
                else:
                    # Try removing _ or replacing spaces
                    alt_lower = filename.lower().replace(' ', '_')
                    alt_lower2 = filename.lower().replace('_', ' ')
                    found = False
                    for lf, af in lower_to_actual.items():
                        if lf == alt_lower or lf == alt_lower2:
                            correct_filename = af
                            item['baseImage'] = f"/static/products/{urllib.parse.quote(correct_filename)}"
                            fixed_count += 1
                            found = True
                            break
                    if not found:
                        print(f"Could not find match for: {filename}")
    
    print(f"Fixed {fixed_count} image paths in JSON.")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    # Also fix DB
    db_fixed = 0
    for p in Product.objects.all():
        if p.image:
            filename = urllib.parse.unquote(p.image.split('/')[-1])
            if filename not in actual_files:
                if filename.lower() in lower_to_actual:
                    correct_filename = lower_to_actual[filename.lower()]
                    p.image = f"/static/products/{correct_filename}"
                    p.save(update_fields=['image'])
                    db_fixed += 1
                else:
                    alt_lower = filename.lower().replace(' ', '_')
                    alt_lower2 = filename.lower().replace('_', ' ')
                    for lf, af in lower_to_actual.items():
                        if lf == alt_lower or lf == alt_lower2:
                            p.image = f"/static/products/{af}"
                            p.save(update_fields=['image'])
                            db_fixed += 1
                            break
                            
    print(f"Fixed {db_fixed} image paths in DB.")

if __name__ == '__main__':
    fix_images()
