import os
import json
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def apply_corrections():
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'frontend',
        'src',
        'data',
        'customization.json'
    )
    
    if not os.path.exists(json_path):
        print(f"[ERROR] customization.json not found at {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        customization_data = json.load(f)
        
    # 1. Correct discount-test image path to a valid fallback placeholder
    updated_json = False
    for item in customization_data:
        slug = item.get('slug')
        if slug == 'discount-test' and (not item.get('baseImage') or item.get('baseImage') == 'NO_IMAGE_PATH'):
            item['baseImage'] = '/static/placeholders/logo.png'
            print("[CORRECTION] Updated 'discount-test' image path to '/static/placeholders/logo.png' in JSON.")
            updated_json = True
            
        # 2. Correct calender-pen-2038-pink image path to an existing 2038 pen image fallback (e.g., Red or Tan)
        # since Pink is physically missing on disk.
        if slug == 'calender-pen-2038-pink' and 'Pink' in item.get('baseImage', ''):
            # We fallback to Red version since it is physically present
            item['baseImage'] = '/static/products/RC_Calender_Pen_2038_Red.jpg'
            print("[CORRECTION] Updated 'calender-pen-2038-pink' image path to existing '/static/products/RC_Calender_Pen_2038_Red.jpg' in JSON.")
            updated_json = True
            
    if updated_json:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(customization_data, f, indent=2)
            
    # Apply identical corrections in SQLite Database
    try:
        discount_product = Product.objects.get(slug='discount-test')
        if not discount_product.image:
            discount_product.image = '/static/placeholders/logo.png'
            discount_product.save()
            print("[CORRECTION] Updated 'discount-test' image path to '/static/placeholders/logo.png' in SQLite.")
    except Product.DoesNotExist:
        pass
        
    try:
        pink_pen = Product.objects.get(slug='calender-pen-2038-pink')
        if 'Pink' in pink_pen.image:
            pink_pen.image = '/static/products/RC_Calender_Pen_2038_Red.jpg'
            pink_pen.save()
            print("[CORRECTION] Updated 'calender-pen-2038-pink' image path to '/static/products/RC_Calender_Pen_2038_Red.jpg' in SQLite.")
    except Product.DoesNotExist:
        pass

if __name__ == '__main__':
    apply_corrections()
