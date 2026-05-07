import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product

def update_customization_zones():
    # Load customization data from frontend
    try:
        with open('../frontend/src/data/customization.json', 'r') as f:
            custom_data_lookup = json.load(f)
        print(f"Loaded {len(custom_data_lookup)} customization configs from JSON")
    except Exception as e:
        print(f"Error loading customization.json: {e}")
        return

    # Update each product in the database
    updated_count = 0
    for custom_data in custom_data_lookup:
        product_id = custom_data.get('productId')
        zones = custom_data.get('zones', [])
        
        try:
            product = Product.objects.get(id=product_id)
            product.customization_config = json.dumps(zones)
            product.save()
            print(f"✅ Updated {product.name} (ID: {product_id}) with {len(zones)} zone(s)")
            updated_count += 1
        except Product.DoesNotExist:
            print(f"⚠️  Product with ID {product_id} not found in database")
        except Exception as e:
            print(f"❌ Error updating product {product_id}: {e}")

    print(f"\n🎉 Successfully updated {updated_count}/{len(custom_data_lookup)} products")

if __name__ == '__main__':
    print("Starting customization zones update...\n")
    update_customization_zones()
