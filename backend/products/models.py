import json
from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

def default_customization_config():
    return json.dumps([
        {
            "id": "text-zone-1",
            "type": "text",
            "x": 400,
            "y": 470,
            "originX": "center",
            "originY": "center",
            "angle": 0,
            "maxWidth": 300,
            "maxChars": 12,
            "fontFamily": "Outfit, sans-serif",
            "fontSize": 12,
            "minFontSize": 14,
            "fill": "#ffffff",
            "opacity": 0.9,
            "placeholder": "CUSTOM TEXT"
        }
    ])

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.CharField(max_length=255, null=True, blank=True, help_text="Path to image relative to static (e.g. products/pen.png)")
    image_file = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Upload a new product image (overrides static path)")
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
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
