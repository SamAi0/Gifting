from django.conf import settings
from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from .models import Cart, CartItem, CartItemLogo, Order, OrderItem, OrderItemLogo, Address
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, AddressSerializer
from .utils import is_maharashtra_pincode

import logging
logger = logging.getLogger(__name__)

def get_razorpay_client():
    import razorpay
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

class PincodeCheckView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        pincode = request.query_params.get('pincode')
        if not pincode:
            return Response({"error": "Pincode is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        is_valid = is_maharashtra_pincode(pincode)
        return Response({
            "pincode": pincode,
            "is_serviceable": is_valid,
            "message": "Delivery available!" if is_valid else "Delivery available only in Maharashtra."
        })

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        instance = serializer.save(cart=cart)
        
        # Handle multiple logo images
        logos = self.request.FILES.getlist('logo_image')
        for logo in logos:
            CartItemLogo.objects.create(cart_item=instance, file=logo)

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from django.db import transaction

class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Use get_or_create to avoid RelatedObjectDoesNotExist if cart hasn't been initialized
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data.get('address_id')
        payment_method = request.data.get('payment_method', 'ONLINE') # Default to ONLINE
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            if not is_maharashtra_pincode(address.pincode):
                return Response({"error": "Selected address is outside Maharashtra. Delivery not available."}, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"error": "Invalid address"}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = cart.total_price
        razorpay_order_id = None
        
        if payment_method == 'ONLINE':
            # Create Razorpay Order
            try:
                client = get_razorpay_client()
                razorpay_order = client.order.create({
                    "amount": int(total_amount * 100), # amount in paise
                    "currency": "INR",
                    "payment_capture": "1"
                })
                razorpay_order_id = razorpay_order['id']
            except Exception as e:
                logger.error(f"Razorpay Error: {str(e)}")
                return Response({"error": "Failed to create Razorpay order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Ensure order creation and cart clearing are atomic
        try:
            with transaction.atomic():
                # Create local Order
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_amount=total_amount,
                    payment_method=payment_method,
                    razorpay_order_id=razorpay_order_id,
                    status='PLACED' if payment_method == 'COD' else 'PENDING'
                )

                # Move items from cart to order
                for item in cart.items.all():
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.get_price_for_quantity(item.quantity),
                        customization_text=item.customization_text,
                        customization_image=item.customization_image,
                        customization_data=item.customization_data,
                        logo_image=item.logo_image
                    )
                    
                    # Copy logos
                    for logo in item.logos.all():
                        OrderItemLogo.objects.create(order_item=order_item, file=logo.file)
                
                # Clear cart
                cart.items.all().delete()

            return Response({
                "order_id": order.id,
                "razorpay_order_id": razorpay_order_id,
                "amount": total_amount,
                "payment_method": payment_method,
                "key": settings.RAZORPAY_KEY_ID if payment_method == 'ONLINE' else None
            })
        except Exception as e:
            logger.error(f"Order Creation Error: {str(e)}")
            return Response({"error": "Failed to process order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            client = get_razorpay_client()
            client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.status = 'PAID'
            order.razorpay_payment_id = razorpay_payment_id
            order.save()
            return Response({"message": "Payment successful"})
        except Exception as e:
            logger.error(f"Payment Verification Error: {str(e)}")
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

class UserOrderListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related('items', 'items__product').order_by('-created_at')
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for admins to manage orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all().order_by('-created_at')
