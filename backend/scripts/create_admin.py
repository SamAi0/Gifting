import os
import sys
import django

# Add the backend directory to sys.path so Django can find 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Environment variables (same as Render)
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "shivam00snh@gmail.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

# Check if user exists
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superuser '{username}' created!")
else:
    print(f"Superuser '{username}' already exists")
