from rest_framework import serializers
from products.models import Product, Category, ProductVariant, Review, Wishlist, AttributeValue, Attribute, Brand, ProductImage
from inquiries.models import BulkOrder, ContactMessage
from company_info.models import Testimonial, Settings

class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)
    subcategories = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count', 'parent', 'subcategories']

    def get_subcategories(self, obj):
        # We limit depth to avoid recursion issues if any
        return CategorySerializer(obj.subcategories.all(), many=True).data

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'logo', 'description']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name']


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
            "slug": obj.product.slug,
            "price": obj.product.price,
            "discount_price": obj.product.discount_price,
            "image": obj.product.image or (obj.product.image_file.url if obj.product.image_file else None)
        }

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_details = BrandSerializer(source='brand', read_only=True)
    customization_zones = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'slug', 'description', 'price', 'discount_price', 
            'category', 'category_name', 'brand', 'brand_details',
            'image', 'image_file', 'images', 'variants', 'customization_zones', 'customization_config',
            'key_features', 'specifications',
            'is_trending', 'is_bulk_only', 'is_active', 'stock', 'weight', 
            'badge_text', 'badge_color', 'tags', 'meta_title', 'meta_description',
            'popularity_score', 'average_rating', 'review_count', 'created_at', 'updated_at'
        ]
    
    def validate(self, data):
        # Validate that discount price is less than price
        price = data.get('price')
        discount_price = data.get('discount_price')
        
        # Check against instance for PATCH requests where fields might be omitted
        if price is None and self.instance:
            price = self.instance.price
            
        if discount_price is None and self.instance:
            discount_price = self.instance.discount_price

        if price is not None and discount_price is not None:
            if discount_price >= price:
                raise serializers.ValidationError({"discount_price": "Discount price must be less than regular price."})
                
        return data
    
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

    def to_representation(self, instance):
        import json
        data = super().to_representation(instance)
        # Parse key_features and specifications from JSON strings if they are strings
        if isinstance(data.get('key_features'), str):
            try:
                data['key_features'] = json.loads(data['key_features'])
            except:
                data['key_features'] = []
        
        if isinstance(data.get('specifications'), str):
            try:
                data['specifications'] = json.loads(data['specifications'])
            except:
                data['specifications'] = {}
        return data
    
    def get_image(self, obj):
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        if not obj.image:
            return None
        return obj.image

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'slug', 'price', 'discount_price',
            'category_name', 'image', 'image_file',
            'is_trending', 'is_bulk_only', 'stock',
            'badge_text', 'badge_color', 'popularity_score', 'average_rating', 'review_count'
        ]
        
    def get_image(self, obj):
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        if not obj.image:
            return None
        return obj.image

class BulkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkOrder
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
