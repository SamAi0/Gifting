import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def execute():
    base_dir = r'C:\Users\Asus\OneDrive\Desktop\A HRTECHINFO\sohamgift\Soham_Gift\backend\static\products'
    json_path = r'C:\Users\Asus\OneDrive\Desktop\A HRTECHINFO\sohamgift\Soham_Gift\frontend\src\data\customization.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        
    products = Product.objects.exclude(image__isnull=True).exclude(image='')
    files_on_disk = set(os.listdir(base_dir))
    
    renamed_count = 0
    json_updates = 0
    
    for p in products:
        old_img_name = os.path.basename(p.image)
        if old_img_name in files_on_disk:
            # 1. Determine new name
            ext = os.path.splitext(old_img_name)[1]
            new_name = f"{p.name}{ext}"
            for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                new_name = new_name.replace(char, '_')
                
            if old_img_name != new_name and old_img_name.lower() != new_name.lower():
                old_path = os.path.join(base_dir, old_img_name)
                new_path = os.path.join(base_dir, new_name)
                
                # If target file exists, it's a conflict, just skip for safety
                if os.path.exists(new_path):
                    continue
                    
                # 2. Rename on disk
                os.rename(old_path, new_path)
                
                # Update files_on_disk tracker so we don't trip over ourselves
                files_on_disk.remove(old_img_name)
                files_on_disk.add(new_name)
                
                # 3. Update database
                new_db_path = f"/static/products/{new_name}"
                p.image = new_db_path
                p.save(update_fields=['image'])
                
                # 4. Update JSON
                for item in json_data:
                    if item.get('productId') == p.id:
                        item['baseImage'] = new_db_path
                        json_updates += 1
                        
                renamed_count += 1

    # Save JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
        
    print(f"Successfully renamed {renamed_count} image files!")
    print(f"Updated DB and made {json_updates} changes in customization.json.")

if __name__ == '__main__':
    execute()
