import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, ProductVariant

def deep_scan():
    static_dir = 'static/products'
    files = [f for f in os.listdir(static_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Get all images from DB
    p_images = set(Product.objects.values_list('image', flat=True))
    v_images = set(ProductVariant.objects.values_list('image', flat=True))
    
    all_db_images = set()
    for img in p_images:
        if img: all_db_images.add(os.path.basename(img))
    for img in v_images:
        if img: all_db_images.add(os.path.basename(img))
        
    missing = []
    for f in files:
        if f not in all_db_images:
            missing.append(f)
            
    print(f"Total files in directory: {len(files)}")
    print(f"Total images in DB (unique basenames): {len(all_db_images)}")
    print(f"Missing files: {len(missing)}")
    
    if missing:
        print("\nMissing files list:")
        for f in missing:
            print(f"- {f}")
            
if __name__ == '__main__':
    deep_scan()
