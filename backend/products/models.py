import json
import io
import random
import string
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.base import ContentFile
from simple_history.models import HistoricalRecords
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, null=True, blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """Generic attribute like Size, Color, RAM, Material."""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

def default_customization_config():
    zones = []
    for i in range(1, 8):
        zones.append({
            "id": f"zone-{i}",
            "name": f"Zone {i}",
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

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Product(models.Model):
    objects = ProductManager()
    all_objects = models.Manager()
    
    name = models.CharField(max_length=200, db_index=True)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    
    # Image management
    image = models.CharField(max_length=255, null=True, blank=True, help_text="Default image path")
    image_file = models.ImageField(upload_to='products/', null=True, blank=True, help_text="Upload default image")
    
    customization_config = models.TextField(
        default=default_customization_config,
        help_text="JSON structure for customization zones"
    )
    stock = models.IntegerField(default=10)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.5, help_text="Weight in KG")
    
    # Flags
    is_trending = models.BooleanField(default=False, db_index=True)
    is_bulk_only = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    # UI Elements
    badge_text = models.CharField(max_length=50, null=True, blank=True)
    badge_color = models.CharField(max_length=20, default="#D91656")
    
    # Search & SEO
    tags = models.CharField(max_length=255, null=True, blank=True, help_text="Comma separated tags")
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    
    # Metrics
    popularity_score = models.IntegerField(default=0, db_index=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, db_index=True)
    review_count = models.IntegerField(default=0, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    history = HistoricalRecords()
    
    def compress_image(self, image_field):
        if not image_field:
            return
        img = Image.open(image_field)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=70, optimize=True)
        output.seek(0)
        
        name = image_field.name.split('.')[0] + '.jpg'
        image_field.save(name, ContentFile(output.read()), save=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.all_objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        
        if not self.sku:
            # Robust auto-SKU generation with collision check
            cat_code = self.category.name[:3].upper() if self.category else "UNC"
            base_sku = f"SG-{cat_code}-{self.slug[:5].upper()}"
            
            while True:
                rand_code = random.randint(1000, 9999)
                new_sku = f"{base_sku}-{rand_code}"
                if not Product.all_objects.filter(sku=new_sku).exists():
                    self.sku = new_sku
                    break

        # Compress image before saving
        if self.image_file and not self.id: # Only compress on first upload
            self.compress_image(self.image_file)
            
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def get_price_for_quantity(self, quantity):
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

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=200, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    attribute_values = models.ManyToManyField(AttributeValue, related_name='variants')
    # For backward compatibility and easy access
    color_name = models.CharField(max_length=50, blank=True) 
    
    image = models.CharField(max_length=255, null=True, blank=True)
    image_file = models.ImageField(upload_to='products/variants/', null=True, blank=True)
    stock = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.image_file and not self.id:
            # Compress variant image
            img = Image.open(self.image_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=70, optimize=True)
            output.seek(0)
            name = self.image_file.name.split('.')[0] + '.jpg'
            self.image_file.save(name, ContentFile(output.read()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - Variant {self.id}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    helpful_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Review)
def update_product_stats(sender, instance, **kwargs):
    from django.db.models import Avg, Count
    product = instance.product
    stats = product.reviews.aggregate(
        avg_rating=Avg('rating'),
        total_count=Count('id')
    )
    product.average_rating = stats['avg_rating'] or 0
    product.review_count = stats['total_count'] or 0
    product.save()
