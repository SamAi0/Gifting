import os
import django
import urllib.parse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, ProductVariant

def fix_images():
    static_dir = os.path.abspath('static/products')
    actual_files = os.listdir(static_dir)
    
    base_name_map = {os.path.splitext(f)[0].lower(): f for f in actual_files}
    full_name_map = {f.lower(): f for f in actual_files}

    # Also fuzzy map replacing underscores with spaces
    fuzzy_map = {os.path.splitext(f)[0].lower().replace('_', ' '): f for f in actual_files}
    
    # And mapping spaces to underscores
    fuzzy_map2 = {os.path.splitext(f)[0].lower().replace(' ', '_'): f for f in actual_files}

    def try_fix(model_instance, field_name='image'):
        val = getattr(model_instance, field_name)
        if not val: return False
        db_filename = urllib.parse.unquote(val.split('/')[-1])
        if db_filename in actual_files: return False
        
        base_db_original = os.path.splitext(db_filename)[0].lower()
        candidates_to_try_base = [base_db_original]
        
        # If it's a variant, try falling back by stripping the color suffix or using the product name
        if hasattr(model_instance, 'color_name') and model_instance.color_name:
            color = model_instance.color_name.lower()
            if base_db_original.endswith('_' + color):
                candidates_to_try_base.append(base_db_original[:-(len(color)+1)])
            if base_db_original.endswith(' ' + color):
                candidates_to_try_base.append(base_db_original[:-(len(color)+1)])
            if base_db_original.endswith('-' + color):
                candidates_to_try_base.append(base_db_original[:-(len(color)+1)])
                
            if hasattr(model_instance, 'product') and model_instance.product:
                candidates_to_try_base.append(model_instance.product.name.lower())

        for base_db in candidates_to_try_base:
            if base_db in base_name_map:
                setattr(model_instance, field_name, base_name_map[base_db])
                model_instance.save(update_fields=[field_name])
                return True
                
            # Check fuzzy space/underscore
            if base_db.replace('_', ' ') in fuzzy_map:
                setattr(model_instance, field_name, fuzzy_map[base_db.replace('_', ' ')])
                model_instance.save(update_fields=[field_name])
                return True
                
            if base_db.replace(' ', '_') in fuzzy_map2:
                setattr(model_instance, field_name, fuzzy_map2[base_db.replace(' ', '_')])
                model_instance.save(update_fields=[field_name])
                return True

        if db_filename.lower() in full_name_map:
            setattr(model_instance, field_name, full_name_map[db_filename.lower()])
            model_instance.save(update_fields=[field_name])
            return True
            
        return False

    fixed_count = 0
    missing_count = 0

    for p in Product.objects.all():
        if try_fix(p):
            fixed_count += 1
        elif p.image and urllib.parse.unquote(p.image.split('/')[-1]) not in actual_files:
            missing_count += 1

    var_fixed = 0
    var_missing = 0
    for v in ProductVariant.objects.all():
        if try_fix(v):
            var_fixed += 1
        elif v.image and urllib.parse.unquote(v.image.split('/')[-1]) not in actual_files:
            var_missing += 1

    print(f"Products: Fixed {fixed_count}, Missing {missing_count}")
    print(f"Variants: Fixed {var_fixed}, Missing {var_missing}")

    # Write missing report
    missing_items = []
    for p in Product.objects.all():
        if p.image and urllib.parse.unquote(p.image.split('/')[-1]) not in actual_files:
            missing_items.append({'name': p.name, 'file': urllib.parse.unquote(p.image.split('/')[-1])})
    
    for v in ProductVariant.objects.all():
        if v.image and urllib.parse.unquote(v.image.split('/')[-1]) not in actual_files:
            missing_items.append({'name': f"{v.product.name} ({v.color_name})", 'file': urllib.parse.unquote(v.image.split('/')[-1])})

    lines = ["# Missing Images Report", f"Total Missing: {len(missing_items)}", "", "| Item Name | Expected File |", "|---|---|"]
    for item in missing_items:
        lines.append(f"| {item['name']} | `{item['file']}` |")
        
    with open('../missing_images_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    fix_images()
