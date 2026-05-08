import json
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

def default_customization_config():
    zones = []
    # Standard positions for a 7-zone set (e.g. Box, Bottle, Pen, Keychain, Cardholder, Diary, Bag)
    # These are placeholders, users can adjust in Admin
    for i in range(1, 8):
        zones.append({
            "id": f"zone-{i}",
            "name": f"Zone {i}", # User requested names with zones
            "type": "text",
            "x": 400,
            "y": 100 + (i * 60), 
            "originX": "center",
            "originY": "center",
            "angle": 0,
            "maxWidth": 300,
            "maxChars": 15,
            "fontFamily": "Outfit, sans-serif",
            "fontSize": 12,
            "fill": "#ffffff",
            "opacity": 0.9,
            "placeholder": f"ZONE {i} TEXT"
        })
    return json.dumps(zones)

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.CharField(max_length=255, null=True, blank=True, help_text="Default image path (e.g. products/pen.png)")
    image_file = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Upload default image")
    customization_config = models.TextField(
        default=default_customization_config,
        help_text="JSON structure for customization zones (coordinates, font, etc.)"
    )
    stock = models.IntegerField(default=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.5, help_text="Weight in KG")
    is_trending = models.BooleanField(default=False)
    is_bulk_only = models.BooleanField(default=False, help_text="If True, product is only available for bulk orders")
    badge_text = models.CharField(max_length=50, null=True, blank=True, help_text="e.g. NEW, 50% OFF, BESTSELLER")
    badge_color = models.CharField(max_length=20, default="#D91656", help_text="Hex code or Tailwind color name")
    created_at = models.DateTimeField(auto_now_add=True)
    
    history = HistoricalRecords()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_price_for_quantity(self, quantity):
        """Calculate unit price based on bulk quantity tiers."""
        base_price = self.price
        discount = Decimal('0')
        if quantity >= 500:
            discount = Decimal('0.15')
        elif quantity >= 250:
            discount = Decimal('0.10')
        elif quantity >= 100:
            discount = Decimal('0.05')
        
        return self.price * (Decimal('1.0') - discount)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color_name = models.CharField(max_length=50)
    image = models.CharField(max_length=255, null=True, blank=True, help_text="Path to variant image (e.g. products/pen_blue.png)")
    image_file = models.ImageField(upload_to='products/variants/', null=True, blank=True, help_text="Upload variant image")
    stock = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"
