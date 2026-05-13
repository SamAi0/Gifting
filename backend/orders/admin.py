from django.contrib import admin
from django.utils.html import format_html
from .models import Address, Cart, CartItem, Order, OrderItem
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin

from core.widgets import SafeJSONEditorWidget

# Removed local SafeJSONEditorWidget definition


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_link', 'quantity', 'price', 'customization_text', 'customization_image_preview', 'all_logos_gallery')
    fields = ('product_link', 'quantity', 'price', 'customization_text', 'customization_image_preview', 'all_logos_gallery', 'customization_data')
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

    def all_logos_gallery(self, obj):
        logos = obj.logos.all()
        if not logos:
            return format_html('<span style="color: #95a5a6; font-style: italic;">No Logos Uploaded</span>')
        
        html = '<div style="display: flex; gap: 15px; flex-wrap: wrap; background: #f8f9fa; padding: 15px; border-radius: 12px; border: 1px solid #e9ecef;">'
        for i, logo in enumerate(logos, 1):
            try:
                url = logo.file.url
                html += format_html(
                    '<div style="text-align: center; width: 120px;">'
                    '<a href="{0}" target="_blank">'
                    '<img src="{0}" style="width: 100px; height: 100px; object-fit: contain; border: 2px solid #e67e22; border-radius: 8px; background: white; margin-bottom: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />'
                    '</a>'
                    '<div style="font-size: 10px; font-weight: bold; color: #d35400;">Logo {1}</div>'
                    '</div>',
                    url, i
                )
            except:
                continue
        html += '</div>'
        return format_html(html)
    
    all_logos_gallery.short_description = '🖼️ Branding Logo Gallery'

@admin.register(Order)
class OrderAdmin(ImportExportMixin, SimpleHistoryAdmin):
    def status_colored(self, obj):
        colors = {
            'PENDING': '#f39c12',
            'CONFIRMED': '#2ecc71',
            'PROCESSING': '#8e44ad',
            'CUSTOMIZED': '#9b59b6',
            'PACKED': '#34495e',
            'SHIPPED': '#3498db',
            'OUT_FOR_DELIVERY': '#1abc9c',
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
    readonly_fields = ('product', 'customization_text', 'customization_image_preview', 'all_logos_gallery')
    fields = ('product', 'quantity', 'customization_text', 'customization_image_preview', 'all_logos_gallery', 'customization_data')

    def customization_image_preview(self, obj):
        if obj.customization_image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: contain; border-radius: 4px;" />', obj.customization_image.url)
        return "-"
    
    def all_logos_gallery(self, obj):
        logos = obj.logos.all()
        if not logos: return "-"
        html = '<div style="display: flex; gap: 5px;">'
        for logo in logos:
            try:
                html += format_html('<img src="{}" style="width: 30px; height: 30px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />', logo.file.url)
            except: continue
        html += '</div>'
        return format_html(html)
    
    all_logos_gallery.short_description = 'Logos'

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'customization_data':
            kwargs['widget'] = SafeJSONEditorWidget(mode='view')
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(Cart)
class CartAdmin(ImportExportModelAdmin):
    list_display = ('user', 'total_price', 'updated_at')
    inlines = [CartItemInline]
