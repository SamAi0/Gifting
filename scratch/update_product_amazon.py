import os
import django
import sys
import json

# Set up Django environment
sys.path.append(r"c:\Users\Asus\Downloads\New folder\Gifting\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Data scraped from Amazon
AMAZON_DATA = {
  "description": "Double-walled premium customizable metal corporate gifting pen and keychain set. Features golden flakes embedded within a clear window in the pen, and a high-durability sleek metal keychain. Both items can be custom engraved with a personalized name. Comes packaged in a premium classic presentation case.",
  "key_features": [
    "Elegant metal body with a transparent golden-flakes section",
    "Comes as a premium 2-in-1 combo: Sleek Metal Pen & Custom Metal Keychain",
    "Ideal corporate and personal gifting item with customized name engraving",
    "Packaged elegantly in a classic presentation case"
  ],
  "specifications": {
    "Brand": "Tempt",
    "Writing Instrument Form": "Ballpoint Pen",
    "Ink Colour": "Blue",
    "Drill Point / Nib Size": "Ballpoint",
    "Special Features": "Personalized",
    "Hand Orientation": "Ambidextrous",
    "Grip Type": "Smooth",
    "Closure Type": "Twist",
    "Colour": "Gold",
    "Subject Character": "Personalized Name",
    "Style Name": "Keychain Pen",
    "Body Shape": "Round",
    "Pattern": "Classic",
    "Recommended Uses For Product": "Writing",
    "Country of Origin": "India",
    "Manufacturer": "Gold&Key",
    "Item Type": "Retractable Ballpoint Pens",
    "ASIN": "B0BT9H7NX7",
    "Material Type": "Metal",
    "Ink Base": "Oil",
    "Unit Count": "1.0 Count"
  }
}

def update_product():
    # Search for product containing "Pen" and "Keychain" in name
    query = Product.objects.filter(name__icontains="Pen").filter(name__icontains="Keychain")
    
    if not query.exists():
        # Fallback to loose search
        query = Product.objects.filter(name__icontains="Pen")
        
    if not query.exists():
        print("ERROR: No product matching 'Pen & Keychain' found in the database.")
        # List first 10 products so we know what is available
        print("\nAvailable products in database:")
        for p in Product.objects.all()[:10]:
            print(f"- ID: {p.id} | Name: {p.name}")
        return

    # Print matching products
    print("Found matching products:")
    for p in query:
        print(f"- ID: {p.id} | Name: {p.name}")

    # Select the first matching product
    product = query.first()
    print(f"\nUpdating Product: ID {product.id} - {product.name}")
    
    # Update fields
    product.description = AMAZON_DATA["description"]
    product.key_features = json.dumps(AMAZON_DATA["key_features"])
    product.specifications = json.dumps(AMAZON_DATA["specifications"])
    
    product.save()
    print("SUCCESS: Product details updated successfully!")

if __name__ == "__main__":
    update_product()
