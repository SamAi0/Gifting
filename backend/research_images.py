import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def research_images():
    base_dir = r'C:\Users\Asus\OneDrive\Desktop\A HRTECHINFO\sohamgift\Soham_Gift\backend\static\products'
    if not os.path.exists(base_dir):
        print("Directory does not exist")
        return
        
    files = set(os.listdir(base_dir))
    print(f"Total files in static/products: {len(files)}")
    
    products = Product.objects.exclude(image__isnull=True).exclude(image='')
    print(f"Total products with image in DB: {products.count()}")
    
    mismatches = 0
    missing_files = 0
    
    for p in products:
        img_name = os.path.basename(p.image)
        if img_name in files:
            expected_name = f"{p.name}{os.path.splitext(img_name)[1]}"
            # Replace invalid filename characters
            for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                expected_name = expected_name.replace(char, '_')
                
            if img_name != expected_name and img_name.lower() != expected_name.lower():
                mismatches += 1
        else:
            missing_files += 1
            
    print(f"Mismatches to rename: {mismatches}")
    print(f"Products pointing to missing files: {missing_files}")

if __name__ == '__main__':
    research_images()
