from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'weight', 'is_trending')
    list_filter = ('category', 'is_trending')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_trending')
