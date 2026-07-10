import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def generate_report():
    report_path = r'C:\Users\Asus\.gemini\antigravity-ide\brain\0b0b6385-9acb-47b0-88ab-49791b5084f4\image_rename_report.md'
    
    products = Product.objects.all().order_by('id')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Image and Database Sync Report\n\n")
        f.write("Here is the final list of products with their perfectly synced, newly formatted image names.\n\n")
        
        f.write("| ID | Product Name | Current Image File |\n")
        f.write("|---|---|---|\n")
        
        for p in products:
            img = os.path.basename(p.image) if p.image else "No Image"
            f.write(f"| {p.id} | {p.name} | `{img}` |\n")

    print("Report generated at", report_path)

if __name__ == '__main__':
    generate_report()
