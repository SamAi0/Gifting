import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Product
from company_info.models import Settings

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'corporate@sohamgift.com', 'admin123')
    print("Superuser created: admin / admin123")

# Create initial settings
if not Settings.objects.exists():
    Settings.objects.create(
        company_name="Soham Gift",
        tagline="Exclusive Corporate Gifting Solutions",
        description="Premium bulk gifting for employees, clients, and partners.",
        address="Shop C, Jai Ganesh Society, Opp. Railway Station, Sector 3, Airoli, Navi Mumbai, Maharashtra – 400708",
        phone1="8169975287",
        phone2="7021495439",
        email="corporate@sohamgift.com"
    )
    print("Initial settings created.")

# Create categories
categories = [
    "Gift Hampers", "Office Gifts", "Stationery", "Tech Gadgets", 
    "Accessories", "Flowers & Cakes", "Gift Sets", "Packaging"
]

for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)
print(f"Created/Verified {len(categories)} categories.")
