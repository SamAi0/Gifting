from django.contrib import admin
from django.utils.html import format_html
from .models import Address, Cart, CartItem, Order, OrderItem
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin

import json
from django_json_widget.widgets import JSONEditorWidget

class SafeJSONEditorWidget(JSONEditorWidget):
    def format_value(self, value):
        if value is None or value == "" or (isinstance(value, str) and not value.strip()):
            return []
        try:
            if isinstance(value, str):
                return json.loads(value)
            return value
        except (ValueError, TypeError, json.JSONDecodeError):
            return []

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_link', 'quantity', 'price', 'customization_text', 'customization_image_preview', 'logo_image_preview')
    fields = ('product_link', 'quantity', 'price', 'customization_text', 'customization_image_preview', 'logo_image_preview', 'customization_data')
    can_delete = False

    def product_link(self, obj):
        if obj.product:
            from django.urls import reverse
            url = reverse('admin:products_product_change', args=[obj.product.id])
            return format_html('<a href="{}" style="font-weight: bold; color: #3498db;">{}</a>', url, obj.product.name)
        return "-"
    
    product_link.short_description = 'Product'
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'customization_data':
            kwargs['widget'] = SafeJSONEditorWidget(mode='view')
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def customization_image_preview(self, obj):
        if obj.customization_image:
            try:
                return format_html(
                    '<div style="margin-bottom: 10px;">'
                    '<a href="{0}" target="_blank">'
                    '<img src="{0}" style="width: 250px; height: auto; max-height: 300px; object-fit: contain; border: 2px solid #3498db; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" />'
                    '</a>'
                    '<p style="font-size: 10px; color: #666; margin-top: 5px;">Click image to view full size</p>'
                    '</div>',
                    obj.customization_image.url
                )
            except Exception as e:
                return f"Error loading mockup: {str(e)}"
        return format_html('<span style="color: #95a5a6; font-style: italic;">No Mockup Generated</span>')
    
    customization_image_preview.short_description = '🎨 Mockup Preview'

    def logo_image_preview(self, obj):
        if obj.logo_image:
            try:
                return format_html(
                    '<div style="margin-bottom: 10px;">'
                    '<a href="{0}" target="_blank">'
                    '<img src="{0}" style="width: 150px; height: auto; max-height: 200px; object-fit: contain; border: 2px solid #e67e22; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);" />'
                    '</a>'
                    '<p style="font-size: 10px; color: #666; margin-top: 5px;">Original Logo Uploaded</p>'
                    '</div>',
                    obj.logo_image.url
                )
            except Exception as e:
                return f"Error loading logo: {str(e)}"
        return format_html('<span style="color: #95a5a6; font-style: italic;">No Logo Uploaded</span>')
    
    logo_image_preview.short_description = '🖼️ Original Logo'

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    def status_colored(self, obj):
        colors = {
            'PENDING': '#f39c12',
            'PLACED': '#8e44ad',
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
    readonly_fields = ('product', 'customization_text', 'customization_image_preview', 'logo_image_preview')
    fields = ('product', 'quantity', 'customization_text', 'customization_image_preview', 'logo_image_preview', 'customization_data')

    def customization_image_preview(self, obj):
        if obj.customization_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px;" />', obj.customization_image.url)
        return "-"
    
    def logo_image_preview(self, obj):
        if obj.logo_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px;" />', obj.logo_image.url)
        return "-"

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'customization_data':
            kwargs['widget'] = SafeJSONEditorWidget(mode='view')
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    list_display = ('user', 'total_price', 'updated_at')
    inlines = [CartItemInline]
