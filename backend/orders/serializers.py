from rest_framework import serializers
from .models import Cart, CartItem, CartItemLogo, Order, OrderItem, OrderItemLogo, Address
from .utils import is_maharashtra_pincode
from api.serializers import ProductSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

    def validate_pincode(self, value):
        if not is_maharashtra_pincode(value):
            raise serializers.ValidationError("Delivery available only in Maharashtra.")
        return value

class CartItemLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemLogo
        fields = ('id', 'file', 'uploaded_at')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if instance.file and request:
            ret['file'] = request.build_absolute_uri(instance.file.url)
        return ret

class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customization_image = serializers.ImageField(required=False, allow_null=True)
    logo_image = serializers.ImageField(required=False, allow_null=True)
    logos = CartItemLogoSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_details', 'quantity', 'customization_text', 'customization_image', 'customization_data', 'logo_image', 'logos', 'subtotal')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if instance.customization_image and request:
            ret['customization_image'] = request.build_absolute_uri(instance.customization_image.url)
        if instance.logo_image and request:
            ret['logo_image'] = request.build_absolute_uri(instance.logo_image.url)
        return ret

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price')

class OrderItemLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemLogo
        fields = ('id', 'file')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if instance.file and request:
            ret['file'] = request.build_absolute_uri(instance.file.url)
        return ret

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    customization_image = serializers.ImageField(required=False, allow_null=True)
    logo_image = serializers.ImageField(required=False, allow_null=True)
    logos = OrderItemLogoSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_details', 'quantity', 'price', 'customization_text', 'customization_image', 'customization_data', 'logo_image', 'logos')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if instance.customization_image and request:
            ret['customization_image'] = request.build_absolute_uri(instance.customization_image.url)
        if instance.logo_image and request:
            ret['logo_image'] = request.build_absolute_uri(instance.logo_image.url)
        return ret

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    address_details = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'user_name', 'address', 'address_details', 'total_amount', 'status', 'razorpay_order_id', 'created_at', 'items')
        read_only_fields = ('total_amount', 'razorpay_order_id', 'created_at')
