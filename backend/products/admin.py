from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static
from .models import Category, Product
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from django.db import models
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin
from core.widgets import SafeJSONEditorWidget

# Removed local SafeJSONEditorWidget definition


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ImportExportMixin, SimpleHistoryAdmin):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'customization_config':
            kwargs['widget'] = SafeJSONEditorWidget(mode='view')
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def image_preview(self, obj):
        try:
            if obj.image_file:
                url = obj.image_file.url
            elif obj.image:
                # Use the path directly if it starts with /static/ or /media/
                url = obj.image
                if not (url.startswith('/static/') or url.startswith('/media/') or url.startswith('http')):
                     url = static(url)
            else:
                return "No Image"
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />', url)
        except Exception:
            return "Error loading image"
        return "No Image"
    
    image_preview.short_description = 'Preview'

    list_display = ('image_preview', 'name', 'category', 'price', 'stock', 'is_trending', 'is_bulk_only')
    list_filter = (
        'category', 
        'is_trending', 
        'is_bulk_only', 
        ('created_at', DateRangeFilter),
    )
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_trending', 'is_bulk_only')
    readonly_fields = ('created_at', 'image_preview_large')
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
            'fields': (('name', 'category'), 'description', ('image', 'image_file', 'image_preview_large'))
        }),
        ('Pricing & Inventory', {
            'fields': (('price', 'discount_price'), ('stock', 'weight'), ('is_trending', 'is_bulk_only')),
            'classes': ('extrapretty',),
        }),
        ('Branding & Customization', {
            'fields': ('customization_config', ('badge_text', 'badge_color')),
            'description': 'Configure the live branding engine zones here using the interactive JSON editor.'
        }),
        ('System Info', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
