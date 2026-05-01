from django.contrib import admin
from .models import Address, Cart, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'customization_text', 'customization_image')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'razorpay_order_id')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]
    list_editable = ('status',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'pincode', 'is_default')
    list_filter = ('city', 'state')
    search_fields = ('user__username', 'street_address')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_price', 'updated_at')
    inlines = [CartItemInline]
