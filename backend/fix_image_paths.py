import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product
from django.utils.text import slugify

def fix_image_paths():
    products = Product.objects.all()
    fixed_count = 0
    not_found_count = 0
    
    for p in products:
        if not p.image:
            continue
            
        base_dir = os.path.dirname(os.path.abspath(__file__)) # this is backend/
        relative_path = p.image.lstrip('/')
        full_path = os.path.join(base_dir, relative_path)
        
        if not os.path.exists(full_path):
            ext = os.path.splitext(p.image)[1]
            
            clean_filename = slugify(p.name).replace('-', '_')
            
            new_image_path = f"/static/products/{clean_filename}{ext}"
            new_full_path = os.path.join(base_dir, new_image_path.lstrip('/'))
            
            if os.path.exists(new_full_path):
                p.image = new_image_path
                p.save(update_fields=['image'])
                fixed_count += 1
            else:
                found = False
                for try_ext in ['.png', '.jpg', '.jpeg', '.webp']:
                    new_image_path_alt = f"/static/products/{clean_filename}{try_ext}"
                    new_full_path_alt = os.path.join(base_dir, new_image_path_alt.lstrip('/'))
                    if os.path.exists(new_full_path_alt):
                        p.image = new_image_path_alt
                        p.save(update_fields=['image'])
                        fixed_count += 1
                        found = True
                        break
                        
                if not found:
                    not_found_count += 1
                    
    print(f"[SUCCESS] Fixed {fixed_count} broken image links in the database!")
    if not_found_count > 0:
        print(f"[WARNING] Still could not find images for {not_found_count} products.")

if __name__ == '__main__':
    fix_image_paths()
