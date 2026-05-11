from rest_framework import serializers
from products.models import Product, Category, ProductVariant, Review, Wishlist, AttributeValue, Attribute
from inquiries.models import BulkInquiry, ContactMessage
from company_info.models import Testimonial, Settings

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute', 'attribute_name', 'value']

class ProductVariantSerializer(serializers.ModelSerializer):
    attribute_values_details = AttributeValueSerializer(source='attribute_values', many=True, read_only=True)
    class Meta:
        model = ProductVariant
        fields = ['id', 'attribute_values', 'attribute_values_details', 'color_name', 'image', 'stock', 'is_active']

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = [
            'id', 'product', 'user', 'user_name', 'rating', 'comment', 
            'image', 'is_verified_purchase', 'helpful_votes', 'created_at'
        ]
        read_only_fields = ['user', 'is_verified_purchase', 'helpful_votes']

class WishlistSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_details', 'added_at']
        read_only_fields = ['user']

    def get_product_details(self, obj):
        return {
            "id": obj.product.id,
            "name": obj.product.name,
            "price": obj.product.price,
            "image": obj.product.image,
            "slug": obj.product.slug
        }

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    customization_zones = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'slug', 'description', 'price', 'discount_price', 
            'category', 'category_name', 
            'image', 'variants', 'customization_zones', 
            'is_trending', 'is_bulk_only', 'is_active', 'stock', 'weight', 
            'badge_text', 'badge_color', 'tags', 'meta_title', 'meta_description',
            'popularity_score', 'average_rating', 'review_count', 'created_at', 'updated_at'
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
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        if not obj.image:
            return None
        return obj.image

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
