from django.contrib import admin
from django.utils.html import format_html
from .models import Address, Cart, CartItem, Order, OrderItem
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'customization_text', 'customization_image_preview', 'logo_image_preview', 'customization_data')
    fields = ('product', 'quantity', 'price', 'customization_text', 'customization_image_preview', 'logo_image_preview', 'customization_data')
    can_delete = False

    def customization_image_preview(self, obj):
        if obj.customization_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />', obj.customization_image.url)
        return "No Mockup"
    
    customization_image_preview.short_description = 'Mockup Preview'

    def logo_image_preview(self, obj):
        if obj.logo_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />', obj.logo_image.url)
        return "No Logo"
    
    logo_image_preview.short_description = 'Original Logo'

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    def status_colored(self, obj):
        colors = {
            'PENDING': '#f39c12',
            'PAID': '#2ecc71',
            'SHIPPED': '#3498db',
            'DELIVERED': '#16a085',
            'CANCELLED': '#e74c3c',
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 12px; font-weight: bold; font-size: 10px;">{}</span>',
            colors.get(obj.status, '#95a5a6'),
            obj.status
        )
    
    status_colored.short_description = 'Status'

    list_display = ('id', 'user', 'total_amount', 'status', 'status_colored', 'created_at')
    list_filter = (
        'status', 
        ('created_at', DateRangeFilter),
    )
    search_fields = ('user__username', 'razorpay_order_id')
    readonly_fields = ('created_at', 'total_amount', 'razorpay_order_id', 'razorpay_payment_id')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    list_per_page = 15

    fieldsets = (
        ('Order Overview', {
            'fields': (('user', 'status'), ('total_amount', 'created_at'))
        }),
        ('Payment Details', {
            'fields': (('razorpay_order_id', 'razorpay_payment_id'),),
            'classes': ('collapse',)
        }),
        ('Shipping Address', {
            'fields': ('address',),
        }),
    )

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
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
