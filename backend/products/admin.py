from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_trending', 'is_bulk_only', 'created_at')
    list_filter = ('category', 'is_trending', 'is_bulk_only', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_trending', 'is_bulk_only')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image', 'price', 'discount_price')
        }),
        ('Inventory & Availability', {
            'fields': ('stock', 'weight', 'is_trending', 'is_bulk_only')
        }),
        ('Customization Config', {
            'fields': ('customization_config',),
            'description': 'JSON configuration for customization zones.'
        }),
        ('Badges & Labels', {
            'fields': ('badge_text', 'badge_color')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
