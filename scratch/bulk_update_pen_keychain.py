import os
import django
import sys
import json

# Set up Django environment
sys.path.append(r"c:\Users\Asus\Downloads\New folder\Gifting\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

# Base details from Amazon
BASE_DETAILS = {
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
    "Body Shape": "Round",
    "Pattern": "Classic",
    "Recommended Uses For Product": "Writing",
    "Country of Origin": "India",
    "Manufacturer": "Gold&Key",
    "Item Type": "Retractable Ballpoint Pens",
    "Material Type": "Metal",
    "Ink Base": "Oil",
    "Unit Count": "1.0 Count"
  }
}

def main():
    # 1. Fetch exact IDs specified by user (55, 56, 57)
    specified_ids = [55, 56, 57]
    products_by_id = list(Product.objects.filter(id__in=specified_ids))
    
    # 2. Query for products containing "Pen" and "Keychain"
    # But filter out other combos like Bottle, Cardholder, Diary, etc. to match user intent
    all_candidates = Product.objects.filter(name__icontains="Pen").filter(name__icontains="Keychain")
    
    filtered_products = []
    exclude_keywords = ["bottle", "diary", "cardholder", "card holder", "purse", "magnet", "crock", "wooden", "mouse", "organizer", "elastic"]
    
    for p in all_candidates:
        name_lower = p.name.lower()
        # If it matches user intent and doesn't contain heavy combo keywords, or is in the specified list
        is_excluded = any(kw in name_lower for kw in exclude_keywords)
        if p.id in specified_ids or not is_excluded:
            filtered_products.append(p)
            
    print(f"Found {len(filtered_products)} products to update:")
    for p in filtered_products:
        print(f"- ID: {p.id} | Name: {p.name}")
        
    print("\nStarting bulk update with dynamic product details variations...")
    
    updated_count = 0
    for product in filtered_products:
        # Create a dynamic organic description using the actual product name
        description = (
            f"Introduce style and sophistication to your professional routine with the {product.name}. "
            "Featuring a double-walled premium customizable metal corporate gifting pen and a matching durable metallic keychain. "
            "Both items can be elegantly custom-engraved with your personalized name. "
            "Perfect for corporate events, colleague appreciation, graduation, and personal gifts. "
            "Packaged inside a beautiful premium classic presentation case."
        )
        
        # Make key features slightly customized for the product name
        features = list(BASE_DETAILS["key_features"])
        if "premium" in product.name.lower():
            features[1] = "Comes as an ultra-premium combo: High-grade Metal Pen & Custom Metal Keychain"
        elif "executive" in product.name.lower():
            features[1] = "Comes as a executive class 2-in-1 combo: Sleek Metal Pen & Custom Metal Keychain"
            
        # Customize specifications
        specs = dict(BASE_DETAILS["specifications"])
        specs["Style Name"] = product.name
        
        # Save to product
        product.description = description
        product.key_features = json.dumps(features)
        product.specifications = json.dumps(specs)
        product.save()
        
        updated_count += 1
        print(f"Updated product ID {product.id} successfully.")
        
    print(f"\nDone! Successfully updated {updated_count} products with customized descriptions and specs.")

if __name__ == "__main__":
    main()
