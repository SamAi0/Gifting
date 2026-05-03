import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Category, Product

def seed_products():
    # Ensure categories exist
    office_gifts, _ = Category.objects.get_or_create(name="Office Gifts")
    stationery, _ = Category.objects.get_or_create(name="Stationery")
    gift_sets, _ = Category.objects.get_or_create(name="Corporate Gift Sets")
    drinkware, _ = Category.objects.get_or_create(name="Drinkware")

    # Load customization data from frontend
    import json
    try:
        with open('../frontend/src/data/customization.json', 'r') as f:
            custom_data_lookup = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load customization.json: {e}")
        custom_data_lookup = []

    def get_config_for_product(product_id):
        # Match by productId from customization.json
        for c in custom_data_lookup:
            if c.get('productId') == product_id:
                return json.dumps(c.get('zones', []))
        return None

    products_data = [
        {
            "name": "Premium Ceramic Mug",
            "description": "High-quality ceramic mug perfect for office use. Can be personalized with company logo or employee name.",
            "price": 499.00,
            "discount_price": 399.00,
            "category": office_gifts,
            "image": "products/mug.png",
            "stock": 150,
            "weight": 0.35,
            "is_trending": True,
            "badge_text": "BESTSELLER",
            "badge_color": "#D91656",
            "customization_config": get_config_for_product(1)
        },
        {
            "name": "Luxury Leather Notebook",
            "description": "Executive black leather-bound notebook with premium 100 GSM paper. Ideal for corporate branding.",
            "price": 899.00,
            "discount_price": 749.00,
            "category": stationery,
            "image": "products/notebook.png",
            "stock": 100,
            "weight": 0.45,
            "is_trending": True,
            "badge_text": "NEW",
            "badge_color": "#10B981",
            "customization_config": get_config_for_product(2)
        },
        {
            "name": "Silver Metallic Pen",
            "description": "Sleek silver metallic pen with smooth ink flow. A classic corporate gift.",
            "price": 299.00,
            "category": stationery,
            "image": "products/pen.png",
            "stock": 200,
            "weight": 0.05,
            "is_trending": False,
            "customization_config": get_config_for_product(3)
        },
        {
            "name": "Classic Pen & Keychain Duo",
            "description": "Timeless combination of a sleek pen and a durable keychain in a premium gift box.",
            "price": 1100.00,
            "discount_price": 950.00,
            "category": gift_sets,
            "image": "products/pen_and_keychain.png",
            "stock": 75,
            "weight": 0.25,
            "is_trending": True,
            "badge_text": "50% OFF",
            "badge_color": "#F59E0B",
            "customization_config": get_config_for_product(4)
        },
        {
            "name": "Stylish Pen & Keyring",
            "description": "A trendy pen and keyring set that makes for a perfect promotional gift.",
            "price": 950.00,
            "category": gift_sets,
            "image": "products/pen_key.png",
            "stock": 80,
            "weight": 0.20,
            "is_trending": False,
            "customization_config": get_config_for_product(5)
        },
        {
            "name": "Executive Trio (Sr 125)",
            "description": "Premium Pen, Keychain, and Cardholder set for the discerning executive.",
            "price": 1599.00,
            "discount_price": 1399.00,
            "category": gift_sets,
            "image": "products/sr_125_pen_keychain_cardholder.png",
            "stock": 60,
            "weight": 0.40,
            "is_trending": True,
            "badge_text": "PREMIUM",
            "badge_color": "#8B5CF6",
            "customization_config": get_config_for_product(6)
        },
        {
            "name": "Corporate Gift Set (Sr 126)",
            "description": "A sophisticated combination of a luxury pen, keychain, and cardholder.",
            "price": 1499.00,
            "category": gift_sets,
            "image": "products/sr_126_pen_keychain_cardholder.png",
            "stock": 55,
            "weight": 0.38,
            "is_trending": False,
            "customization_config": get_config_for_product(7)
        },
        {
            "name": "Perfumo Luxury Set (Sr 135)",
            "description": "Exclusive set including a wallet, perfume, pen, and cardholder.",
            "price": 2999.00,
            "discount_price": 2599.00,
            "category": gift_sets,
            "image": "products/sr_135_perfumo_set_wallet_perfume_pen_cardholder.png",
            "stock": 40,
            "weight": 0.65,
            "is_trending": True,
            "badge_text": "LUXURY",
            "badge_color": "#EC4899",
            "customization_config": get_config_for_product(8)
        },
        {
            "name": "Red Elastic Notebook Set (Sr 139)",
            "description": "Stylish red notebook with matching elastic pen holder.",
            "price": 799.00,
            "category": stationery,
            "image": "products/sr_139_red_elastic_pen_diary.png",
            "stock": 90,
            "weight": 0.35,
            "is_trending": False,
            "customization_config": get_config_for_product(9)
        },
        {
            "name": "Black Mars Notebook Set (Sr 144)",
            "description": "Professional black notebook and pen set with high-quality paper.",
            "price": 849.00,
            "discount_price": 699.00,
            "category": stationery,
            "image": "products/sr_144_black_mars_pen_diary.png",
            "stock": 85,
            "weight": 0.40,
            "is_trending": True,
            "badge_text": "TRENDING",
            "badge_color": "#3B82F6",
            "customization_config": get_config_for_product(10)
        },
        {
            "name": "Premium Pen & Keychain (Sr 238)",
            "description": "Classic pairing of a metallic pen and a durable keychain.",
            "price": 699.00,
            "category": gift_sets,
            "image": "products/sr_238_pen_keychain.png",
            "stock": 100,
            "weight": 0.18,
            "is_trending": False,
            "customization_config": get_config_for_product(11)
        },
        {
            "name": "Elegant Pen & Cardholder (Sr 242)",
            "description": "Sleek pen and cardholder set, perfect for networking events.",
            "price": 899.00,
            "category": gift_sets,
            "image": "products/sr_242_pen_cardholder.png",
            "stock": 70,
            "weight": 0.22,
            "is_trending": False,
            "customization_config": get_config_for_product(12)
        },
        {
            "name": "Male & Female Perfume Set (Sr 243)",
            "description": "A dual-scent perfume set presented in a premium gift box.",
            "price": 1899.00,
            "discount_price": 1599.00,
            "category": gift_sets,
            "image": "products/sr_243_2_in_1_perfumes_set_male_female_perfumes.png",
            "stock": 45,
            "weight": 0.55,
            "is_trending": True,
            "badge_text": "GIFT IDEA",
            "badge_color": "#EF4444",
            "customization_config": get_config_for_product(13)
        },
        {
            "name": "Copper Hydration Set (Sr 264)",
            "description": "Luxury copper bottle and two matching mugs for healthy hydration.",
            "price": 3499.00,
            "category": drinkware,
            "image": "products/sr_264_copper_bottle_mug_sets_blue500_ml_copper_bottle_2_mugs.png",
            "stock": 30,
            "weight": 1.20,
            "is_trending": True,
            "badge_text": "PREMIUM",
            "badge_color": "#B45309",
            "customization_config": get_config_for_product(14)
        },
        {
            "name": "HydroX Black Gift Set (Sr 294)",
            "description": "Black HydroX insulated bottle with matching pen and keychain.",
            "price": 2299.00,
            "discount_price": 1999.00,
            "category": gift_sets,
            "image": "products/sr_294_hydrox_black_bottle_pen_keychain.png",
            "stock": 50,
            "weight": 0.60,
            "is_trending": True,
            "badge_text": "HOT",
            "badge_color": "#DC2626",
            "customization_config": get_config_for_product(15)
        },
        {
            "name": "HydroX White Gift Set (Sr 295)",
            "description": "White HydroX insulated bottle with matching pen and keychain.",
            "price": 2299.00,
            "category": gift_sets,
            "image": "products/sr_295_hydrox_white_bottle_pen_keychain.png",
            "stock": 48,
            "weight": 0.58,
            "is_trending": False,
            "customization_config": get_config_for_product(16)
        },
        {
            "name": "Red Elastic Diary Set (Sr 140)",
            "description": "Premium red diary with pen loop and elastic closure.",
            "price": 799.00,
            "discount_price": 649.00,
            "category": stationery,
            "image": "products/sr_140_red_elastic_pen_diary.png",
            "stock": 95,
            "weight": 0.36,
            "is_trending": False,
            "customization_config": get_config_for_product(17)
        },
        {
            "name": "Black Mars Diary Set (Sr 145)",
            "description": "Elegant black diary set with matching pen.",
            "price": 849.00,
            "category": stationery,
            "image": "products/sr_145_black_mars_pen_diary.png",
            "stock": 88,
            "weight": 0.42,
            "is_trending": False,
            "customization_config": get_config_for_product(18)
        },
        {
            "name": "Executive Pen & Keychain (Sr 240)",
            "description": "Premium executive pen with matching metal keychain.",
            "price": 749.00,
            "discount_price": 599.00,
            "category": gift_sets,
            "image": "products/sr_240_pen_keychain.png",
            "stock": 92,
            "weight": 0.19,
            "is_trending": True,
            "badge_text": "VALUE",
            "badge_color": "#059669",
            "customization_config": get_config_for_product(19)
        },
        {
            "name": "Professional Pen & Cardholder (Sr 247)",
            "description": "Sleek pen and leather cardholder combination for professionals.",
            "price": 949.00,
            "category": gift_sets,
            "image": "products/sr_247_pen_cardholder.png",
            "stock": 65,
            "weight": 0.24,
            "is_trending": False,
            "customization_config": get_config_for_product(20)
        },
    ]

    for p_data in products_data:
        prod, created = Product.objects.get_or_create(
            name=p_data["name"],
            defaults={
                "description": p_data["description"],
                "price": p_data["price"],
                "discount_price": p_data.get("discount_price"),
                "category": p_data["category"],
                "image": p_data["image"],
                "stock": p_data.get("stock", 10),
                "weight": p_data.get("weight", 0.5),
                "is_trending": p_data.get("is_trending", False),
                "badge_text": p_data.get("badge_text"),
                "badge_color": p_data.get("badge_color", "#D91656"),
                "customization_config": p_data.get("customization_config")
            }
        )
        if not created:
             prod.description = p_data["description"]
             prod.price = p_data["price"]
             prod.discount_price = p_data.get("discount_price")
             prod.category = p_data["category"]
             prod.image = p_data["image"]
             prod.stock = p_data.get("stock", 10)
             prod.weight = p_data.get("weight", 0.5)
             prod.is_trending = p_data.get("is_trending", False)
             prod.badge_text = p_data.get("badge_text")
             prod.badge_color = p_data.get("badge_color", "#D91656")
             prod.customization_config = p_data.get("customization_config")
             prod.save()
    
    print(f"Successfully seeded {len(products_data)} products.")


if __name__ == "__main__":
    seed_products()
