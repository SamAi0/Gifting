from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
from .models import Category, Product, ProductVariant, Attribute, AttributeValue, Brand, ProductImage
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin
from core.widgets import SafeJSONEditorWidget

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color_name', 'image', 'image_file', 'stock', 'is_active')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'parent', 'id')
    list_filter = ('parent',)
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)

@admin.register(Product)
class ProductAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'customization_config':
            kwargs['widget'] = SafeJSONEditorWidget(mode='code')
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def image_preview(self, obj):
        try:
            if obj.image_file:
                url = obj.image_file.url
            elif obj.image:
                url = obj.image
                if not (url.startswith('/static/') or url.startswith('/media/') or url.startswith('http')):
                     url = static(url)
            else:
                return "No Image"
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />', url)
        except Exception:
            return "Error loading image"
    
    image_preview.short_description = 'Preview'

    list_display = ('image_preview', 'name', 'sku', 'category', 'brand', 'price', 'stock', 'is_active', 'is_trending')
    list_filter = (
        'category', 
        'brand',
        'is_trending', 
        'is_active',
        'is_bulk_only', 
        ('created_at', DateRangeFilter),
    )
    search_fields = ('name', 'sku', 'description', 'tags')
    list_editable = ('price', 'stock', 'is_active', 'is_trending')
    readonly_fields = ('created_at', 'updated_at', 'image_preview_large')
    list_per_page = 20
    
    def image_preview_large(self, obj):
        try:
            if obj.image_file:
                url = obj.image_file.url
            elif obj.image:
                url = obj.image
                if not (url.startswith('/static/') or url.startswith('/media/') or url.startswith('http')):
                     url = static(url)
            else:
                return "No Image"
            return format_html('<img src="{}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 12px; border: 2px solid #ddd;" />', url)
        except Exception:
            return "Error loading image"
        return "No Image"

    fieldsets = (
        ('General Info', {
            'fields': (('name', 'sku'), ('category', 'brand'), 'description', 'tags', ('image', 'image_file', 'image_preview_large'))
        }),
        ('Pricing & Inventory', {
            'fields': (('price', 'discount_price'), ('stock', 'weight'), ('is_trending', 'is_bulk_only', 'is_active', 'is_deleted')),
        }),
        ('SEO Info', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('Branding & Customization', {
            'fields': ('customization_config', ('badge_text', 'badge_color')),
            'description': 'Configure the live branding engine zones here using the interactive JSON editor.'
        }),
        ('System Info', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'stock', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('product__name',)
    filter_horizontal = ('attribute_values',)
