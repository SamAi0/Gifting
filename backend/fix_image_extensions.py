import os
import django
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_images():
    static_dir = os.path.abspath('static/products')
    if not os.path.exists(static_dir):
        print(f"Directory not found: {static_dir}")
        return

    actual_files = os.listdir(static_dir)
    
    # Map lowercase base name (without extension) to the exact filename
    base_name_map = {}
    for f in actual_files:
        base, ext = os.path.splitext(f)
        base_name_map[base.lower()] = f

    # Map full filenames in lowercase to handle case issues
    full_name_map = {}
    for f in actual_files:
        full_name_map[f.lower()] = f

    fixed_count = 0
    missing_count = 0

    for p in Product.objects.all():
        if not p.image:
            continue
            
        db_filename = urllib.parse.unquote(p.image.split('/')[-1])
        
        # If it exactly matches, nothing to do
        if db_filename in actual_files:
            continue
            
        # Check if it's just a case issue (e.g. .PNG vs .png)
        if db_filename.lower() in full_name_map:
            new_filename = full_name_map[db_filename.lower()]
            print(f"[{p.name}] Fixing case: {db_filename} -> {new_filename}")
            p.image = new_filename
            p.save(update_fields=['image'])
            fixed_count += 1
            continue
            
        # Check if it's an extension mismatch (e.g. .jpeg vs .png)
        base_db, ext_db = os.path.splitext(db_filename)
        if base_db.lower() in base_name_map:
            new_filename = base_name_map[base_db.lower()]
            print(f"[{p.name}] Fixing extension: {db_filename} -> {new_filename}")
            p.image = new_filename
            p.save(update_fields=['image'])
            fixed_count += 1
            continue
            
        # Still not found
        missing_count += 1

    print(f"\nCompleted. Fixed {fixed_count} images.")
    print(f"Still missing {missing_count} images.")

if __name__ == '__main__':
    fix_images()
