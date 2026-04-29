import razorpay
from django.conf import settings
from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from .models import Cart, CartItem, Order, OrderItem, Address
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, AddressSerializer

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = request.user.cart
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data.get('address_id')
        try:
            address = Address.objects.get(id=address_id, user=request.user)
        except Address.DoesNotExist:
            return Response({"error": "Invalid address"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = cart.total_price
        
        # Create Razorpay Order
        razorpay_order = client.order.create({
            "amount": int(total_amount * 100), # amount in paise
            "currency": "INR",
            "payment_capture": "1"
        })

        # Create local Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            total_amount=total_amount,
            razorpay_order_id=razorpay_order['id']
        )

        # Move items from cart to order
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                customization_text=item.customization_text,
                customization_image=item.customization_image
            )
        
        # Clear cart
        cart.items.all().delete()

        return Response({
            "order_id": order.id,
            "razorpay_order_id": razorpay_order['id'],
            "amount": total_amount,
            "key": settings.RAZORPAY_KEY_ID
        })

class VerifyPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = 'PAID'
            order.razorpay_payment_id = razorpay_payment_id
            order.save()
            return Response({"message": "Payment successful"})
        except Exception as e:
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)
