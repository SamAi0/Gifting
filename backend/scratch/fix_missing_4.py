import os
import sys
import shutil
import django

# Setup Django settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

static_products_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'static',
    'products'
)

print("="*60)
print("FIXING THE REMAINING 4 IMAGE ERRORS")
print("="*60)

# 1. Fix 'Discount Test Product' by setting its image to None in DB
# This will make the frontend fall back to a beautiful default Unsplash image!
try:
    p1 = Product.objects.get(name='Discount Test Product')
    p1.image = None
    p1.save()
    print("[SUCCESS] Updated 'Discount Test Product' image to None in DB.")
except Product.DoesNotExist:
    print("[WARNING] 'Discount Test Product' not found in DB.")

# Helper to copy variant files as placeholders
def copy_placeholder(src_name, dest_name):
    src_path = os.path.join(static_products_dir, src_name)
    dest_path = os.path.join(static_products_dir, dest_name)
    
    if os.path.exists(src_path):
        try:
            shutil.copy2(src_path, dest_path)
            print(f"[SUCCESS] Copied: '{src_name}' -> '{dest_name}'")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to copy '{src_name}' to '{dest_name}': {e}")
    else:
        print(f"[ERROR] Source file '{src_name}' not found at '{src_path}'!")
    return False

# 2. Speed Pen Golden Clip 2015 Black placeholder (use Silver version as temporary placeholder)
copy_placeholder('RC_Speed_Pen_Golden_Clip_2015_silver.png', 'rc_speed_pen_golden_clip_2015_black.png')

# 3. Speed Pen Golden Clip 2015 Golden placeholder (use Silver version as temporary placeholder)
copy_placeholder('RC_Speed_Pen_Golden_Clip_2015_silver.png', 'rc_speed_pen_golden_clip_2015_golden.png')

# 4. Tik tik Curve Pen 2041 White placeholder (use Black version as temporary placeholder)
copy_placeholder('RC_Tik_tik_Curve_Pen_2041_Black.jpg', 'rc_tik_tik_curve_pen_2041_white.png')

print("="*60)
print("Done fixing remaining errors!")
