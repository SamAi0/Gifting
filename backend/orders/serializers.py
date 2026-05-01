from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Address
from api.serializers import ProductSerializer

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ('user',)

class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customization_image = serializers.ImageField(required=False, allow_null=True)
    logo_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_details', 'quantity', 'customization_text', 'customization_image', 'customization_data', 'logo_image', 'subtotal')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price')

class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    customization_image = serializers.ImageField(read_only=True)
    logo_image = serializers.ImageField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_details', 'quantity', 'price', 'customization_text', 'customization_image', 'customization_data', 'logo_image')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    address_details = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'user_name', 'address', 'address_details', 'total_amount', 'status', 'razorpay_order_id', 'created_at', 'items')
        read_only_fields = ('total_amount', 'razorpay_order_id', 'created_at')
