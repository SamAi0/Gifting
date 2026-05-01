from rest_framework import serializers
from products.models import Product, Category
from inquiries.models import BulkInquiry, ContactMessage
from company_info.models import Testimonial, Settings

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(source='products.count', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'product_count']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    customization_zones = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'discount_price', 
            'category', 'category_name', 'image', 'customization_zones', 
            'customization_config', 'is_trending', 'is_bulk_only', 
            'stock', 'weight', 'badge_text', 'badge_color', 'created_at'
        ]
    
    def validate_customization_config(self, value):
        import json
        if not value:
            return "[]"
        try:
            json.loads(value)
        except ValueError:
            raise serializers.ValidationError("Invalid JSON format for customization config.")
        return value

    def get_customization_zones(self, obj):
        import json
        if obj.customization_config:
            try:
                return json.loads(obj.customization_config)
            except:
                return []
        return []
    
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        elif obj.image:
            return obj.image.url
        return None

class BulkInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkInquiry
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = '__all__'
