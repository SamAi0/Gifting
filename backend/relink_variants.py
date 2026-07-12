import os
import django
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import ProductVariant

def relink():
    static_dir = os.path.abspath('static/products')
    actual_files = os.listdir(static_dir)
    
    actual_files_no_ext = {os.path.splitext(f)[0].lower(): f for f in actual_files}
    fuzzy_map = {os.path.splitext(f)[0].lower().replace('_', ' '): f for f in actual_files}

    updated_count = 0

    for v in ProductVariant.objects.select_related('product').all():
        p_name = v.product.name
        c_name = v.color_name
        
        if not p_name or not c_name:
            continue
            
        p_name_uscore = p_name.replace(' ', '_')
        c_name_uscore = c_name.replace(' ', '_')
        
        # Generate possible precise names the user might have used
        candidates = [
            f"{p_name}_{c_name}",
            f"{p_name} {c_name}",
            f"{p_name}-{c_name}",
            f"{p_name_uscore}_{c_name}",
            f"{p_name_uscore}_{c_name_uscore}",
            f"{p_name_uscore}{c_name_uscore}",
            f"{p_name}{c_name}",
        ]
        
        for cand in candidates:
            cand_lower = cand.lower()
            ideal_file = None
            
            if cand_lower in actual_files_no_ext:
                ideal_file = actual_files_no_ext[cand_lower]
            else:
                cand_fuzzy = cand_lower.replace('_', ' ')
                if cand_fuzzy in fuzzy_map:
                    ideal_file = fuzzy_map[cand_fuzzy]
                    
            if ideal_file:
                current_file = urllib.parse.unquote(v.image.split('/')[-1]) if v.image else ""
                if current_file != ideal_file:
                    v.image = ideal_file
                    v.save(update_fields=['image'])
                    updated_count += 1
                    print(f"Updated variant '{p_name} ({c_name})' to image: {ideal_file}")
                break

    print(f"Total variants updated to specific color files: {updated_count}")

if __name__ == '__main__':
    relink()
