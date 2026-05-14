from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
from simple_history.models import HistoricalRecords

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    def __str__(self):
        return self.code

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.city}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id} ({self.user.username if self.user else 'Guest'})"

    @property
    def total_price(self):
        from decimal import Decimal
        return sum((item.subtotal for item in self.items.all()), Decimal('0'))

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customization_text = models.CharField(max_length=255, null=True, blank=True)
    customization_image = models.ImageField(upload_to='cart_customizations/', null=True, blank=True)
    customization_data = models.TextField(null=True, blank=True)
    logo_image = models.ImageField(upload_to='cart_logos/', null=True, blank=True) # Keeping for backward compat

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.product.get_price_for_quantity(self.quantity) * self.quantity

class CartItemLogo(models.Model):
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='logos')
    file = models.FileField(upload_to='cart_logos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SaveForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_items', null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved: {self.product.name} ({self.user.username if self.user else 'Guest'})"

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('CUSTOMIZED', 'Customized'),
        ('PACKED', 'Packed'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    PAYMENT_METHOD_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='ONLINE')
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    
    # New fields for Business and Logistics
    business_name = models.CharField(max_length=200, null=True, blank=True)
    gst_number = models.CharField(max_length=15, null=True, blank=True)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    preferred_delivery_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase
    customization_text = models.CharField(max_length=255, null=True, blank=True)
    customization_image = models.ImageField(upload_to='order_customizations/', null=True, blank=True)
    customization_data = models.TextField(null=True, blank=True)
    logo_image = models.ImageField(upload_to='order_logos/', null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

class OrderItemLogo(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='logos')
    file = models.FileField(upload_to='order_logos/')
