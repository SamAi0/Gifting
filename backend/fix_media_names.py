import os
import django
import re
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def safe_filename(filename):
    """
    Converts a filename to a safe version:
    - Lowercase
    - Replaces spaces and special characters with underscores
    - Preserves the extension
    """
    name, ext = os.path.splitext(filename)
    # Remove special characters like &
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[-\s]+', '_', name)
    return f"{name}{ext}"

def fix_media_names():
    media_root = 'media/products'
    if not os.path.exists(media_root):
        print(f"Directory {media_root} not found.")
        return

    print("Checking products in database...")
    products = Product.objects.all()
    
    for product in products:
        if not product.image:
            continue
            
        old_path = product.image.name # e.g., 'products/Sr 240 Pen & Keychain.png'
        old_filename = os.path.basename(old_path)
        new_filename = safe_filename(old_filename)
        
        if old_filename == new_filename:
            continue
            
        new_path = os.path.join('products', new_filename).replace('\\', '/')
        
        actual_old_file_path = os.path.join('media', old_path)
        actual_new_file_path = os.path.join('media', new_path)
        
        print(f"Renaming: {old_filename} -> {new_filename}")
        
        # Rename on disk if it exists
        if os.path.exists(actual_old_file_path):
            try:
                # If new file already exists, don't overwrite it
                if os.path.exists(actual_new_file_path) and actual_old_file_path != actual_new_file_path:
                    print(f"  Warning: {new_filename} already exists on disk. Just updating DB.")
                else:
                    os.rename(actual_old_file_path, actual_new_file_path)
            except Exception as e:
                print(f"  Error renaming file: {e}")
        else:
            print(f"  Warning: File {actual_old_file_path} not found on disk.")
            
        # Update database
        product.image.name = new_path
        product.save()
        print(f"  Updated DB: {old_path} -> {new_path}")

    # Also check for any files on disk that are NOT in the DB but need renaming
    print("\nChecking for remaining files on disk...")
    for filename in os.listdir(media_root):
        new_filename = safe_filename(filename)
        if filename != new_filename:
            old_file_path = os.path.join(media_root, filename)
            new_file_path = os.path.join(media_root, new_filename)
            
            if not os.path.exists(new_file_path):
                print(f"Renaming orphaned file: {filename} -> {new_filename}")
                os.rename(old_file_path, new_file_path)

if __name__ == "__main__":
    fix_media_names()
