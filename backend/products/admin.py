from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product
from import_export.admin import ImportExportModelAdmin
from django.db import models
from rangefilter.filters import DateRangeFilter
from simple_history.admin import SimpleHistoryAdmin
from django_json_widget.widgets import JSONEditorWidget
import json

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

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'customization_config':
            kwargs['widget'] = SafeJSONEditorWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def image_preview(self, obj):
        try:
            if obj.image:
                return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />', obj.image.url)
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
            if obj.image:
                return format_html('<img src="{}" style="width: 200px; height: 200px; object-fit: cover; border-radius: 12px; border: 2px solid #ddd;" />', obj.image.url)
        except Exception:
            return "Error loading image"
        return "No Image"

    fieldsets = (
        ('General Info', {
            'fields': (('name', 'category'), 'description', ('image', 'image_preview_large'))
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
