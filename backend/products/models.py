from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/')
    customization_config = models.TextField(null=True, blank=True, help_text="JSON string for customization zones (coordinates, font, etc.)")
    stock = models.IntegerField(default=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.5, help_text="Weight in KG")
    is_trending = models.BooleanField(default=False)
    is_bulk_only = models.BooleanField(default=False, help_text="If True, product is only available for bulk orders")
    badge_text = models.CharField(max_length=50, null=True, blank=True, help_text="e.g. NEW, 50% OFF, BESTSELLER")
    badge_color = models.CharField(max_length=20, default="#D91656", help_text="Hex code or Tailwind color name")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
