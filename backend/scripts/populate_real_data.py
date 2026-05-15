import os
import django
import json
import sys

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def populate_data():
    products = Product.objects.all()
    print(f"Found {products.count()} products to update.")

    templates = {
        "Stationery Set": {
            "key_features": [
                "Premium A5 Hardcover Notebook with PU Leather Finish",
                "Sleek Metal Ballpoint Pen with Smooth Ink Flow",
                "Matching Designer Keychain with Metal Accent",
                "Elegant Gift Box Packaging with Molded Interior",
                "Ideal for Corporate Gifting and Employee Onboarding"
            ],
            "specifications": {
                "Notebook Size": "A5 (21 x 14.8 cm)",
                "Notebook Pages": "160 Pages, 80 GSM Natural Shade Paper",
                "Pen Material": "High-grade Metal with Matte Finish",
                "Keychain Material": "Metal & PU Leather",
                "Packaging": "Premium Rigid Gift Box",
                "Branding Options": "Laser Engraving, Screen Printing, UV Printing"
            }
        },
        "Notebook": {
            "key_features": [
                "Premium PU Leather Soft/Hard Cover",
                "High-quality Acid-free Paper (No Ink Bleed)",
                "Elastic Closure and Silk Ribbon Bookmark",
                "Rear Expandable Pocket for Loose Notes",
                "Lays Flat 180° for Easy Writing"
            ],
            "specifications": {
                "Size": "A5",
                "Paper Quality": "80-100 GSM",
                "Sheet Count": "192 Sheets / 96 Leaves",
                "Cover Material": "Eco-friendly PU Leather",
                "Binding": "Section Sewn"
            }
        },
        "Pen": {
            "key_features": [
                "Ergonomic Design for Fatigue-free Writing",
                "Premium Metallic Body with Chrome Accents",
                "Quick-drying Japanese Ink Technology",
                "Refillable for Long-lasting Use",
                "Comes in a Stylish Presentation Case"
            ],
            "specifications": {
                "Type": "Ballpoint / Rollerball",
                "Body Material": "Brass / Aluminium with Lacquer Coating",
                "Ink Color": "Blue / Black",
                "Refill Type": "Standard Global Refill",
                "Weight": "25g - 35g"
            }
        },
        "Mug": {
            "key_features": [
                "High-quality Ceramic with Glossy Finish",
                "Microwave and Dishwasher Safe",
                "Large Ergonomic Handle for Comfortable Grip",
                "Vibrant Full-color Printing Capability",
                "Lead and Cadmium Free"
            ],
            "specifications": {
                "Capacity": "325ml / 11oz",
                "Material": "Super White Ceramic",
                "Height": "9.5 cm",
                "Diameter": "8 cm",
                "Weight": "350g"
            }
        },
        "Corporate Set": {
            "key_features": [
                "Curated Selection of Premium Business Essentials",
                "Unified Design Aesthetic Across All Items",
                "High-utility Items for Modern Professionals",
                "Luxury Unboxing Experience for Clients",
                "Durable Construction for Daily Office Use"
            ],
            "specifications": {
                "Components": "Varies by Set (Notebook, Pen, Keychain, Flask, etc.)",
                "Material Quality": "Premium Grade",
                "Branding Area": "Available on All Individual Items",
                "Gift Box": "Magnetic Closure Rigid Box",
                "Customization": "Logo and Individual Name Personalization"
            }
        }
    }

    updated_count = 0
    for product in products:
        name_lower = product.name.lower()
        template = None

        if "set" in name_lower or "trio" in name_lower or "duo" in name_lower:
            template = templates["Corporate Set"]
            if "notebook" in name_lower or "pen" in name_lower:
                template = templates["Stationery Set"]
        elif "notebook" in name_lower or "diary" in name_lower:
            template = templates["Notebook"]
        elif "pen" in name_lower:
            template = templates["Pen"]
        elif "mug" in name_lower:
            template = templates["Mug"]
        else:
            # Default to Corporate Set if unsure
            template = templates["Corporate Set"]

        if template:
            # Only update if fields are empty strings or '[]'/'{}'
            if not product.key_features or product.key_features in ['[]', '']:
                product.key_features = json.dumps(template["key_features"])
            
            if not product.specifications or product.specifications in ['{}', '']:
                product.specifications = json.dumps(template["specifications"])
            
            # Auto-generate SEO meta if missing
            if not product.meta_title:
                product.meta_title = f"{product.name} | Premium Corporate Gift"
            
            if not product.meta_description:
                product.meta_description = f"Buy {product.name} online at Soham Gift. High-quality corporate gifting solution with custom branding options. Perfect for employees and clients."

            product.save()
            updated_count += 1

    print(f"Successfully updated {updated_count} products.")

if __name__ == "__main__":
    populate_data()
