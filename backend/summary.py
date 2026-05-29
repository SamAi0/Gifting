import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, ProductVariant

def get_summary():
    static_dir = 'static/products'
    all_files = set(f for f in os.listdir(static_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg')))
    
    p_imgs = set()
    for p in Product.objects.all():
        if p.image:
            p_imgs.add(os.path.basename(p.image))
            
    v_imgs = set()
    for v in ProductVariant.objects.all():
        if v.image:
            v_imgs.add(os.path.basename(v.image))
            
    all_used = p_imgs | v_imgs
    unused = all_files - all_used
    
    print(f"Total Files in Folder: {len(all_files)}")
    print(f"Total Unique Images used in DB: {len(all_used)}")
    print(f"Main Product Images: {len(p_imgs)}")
    print(f"Variant Images: {len(v_imgs)}")
    print(f"Unused files: {len(unused)}")
    
    if unused:
        print("\nUnused files list:")
        for f in unused:
            print(f"- {f}")
            
    print("\nVariant Breakdown (Example):")
    # Show one product with variants
    multi_variant = Product.objects.filter(variants__isnull=False).distinct()[:3]
    for p in multi_variant:
        variants = p.variants.all()
        print(f"Product: {p.name} | Variants: {variants.count()} ({', '.join([v.color_name for v in variants])})")

if __name__ == '__main__':
    get_summary()
