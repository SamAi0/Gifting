import os
import sys
import django
import difflib
import urllib.parse

sys.path.append(os.path.abspath('backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def fix_images_advanced():
    static_dir = os.path.abspath(r'backend/static/products')
    if not os.path.exists(static_dir):
        print(f"Directory not found: {static_dir}")
        return

    actual_files = os.listdir(static_dir)
    actual_files_lower = [f.lower() for f in actual_files]
    file_map = {f.lower(): f for f in actual_files}
    
    fixed_count = 0
    missing_count = 0
    
    for p in Product.objects.all():
        if p.image:
            filename = urllib.parse.unquote(p.image.split('/')[-1])
            if filename not in actual_files:
                # Need to fix
                base_name = os.path.splitext(filename)[0].lower()
                
                # First try exact match without extension
                matches = [f for f in actual_files if os.path.splitext(f)[0].lower() == base_name]
                
                if matches:
                    correct_filename = matches[0]
                else:
                    # Try fuzzy matching
                    close_matches = difflib.get_close_matches(filename.lower(), actual_files_lower, n=1, cutoff=0.8)
                    if close_matches:
                        correct_filename = file_map[close_matches[0]]
                    else:
                        correct_filename = None
                        
                if correct_filename:
                    p.image = f"/static/products/{urllib.parse.quote(correct_filename)}"
                    p.save(update_fields=['image'])
                    fixed_count += 1
                    print(f"Fixed: {filename} -> {correct_filename}")
                else:
                    missing_count += 1
                    print(f"Could not find match for: {filename}")
                    
    print(f"\nSuccessfully fixed {fixed_count} DB paths using advanced matching.")
    print(f"Still broken: {missing_count} paths.")

if __name__ == '__main__':
    fix_images_advanced()
