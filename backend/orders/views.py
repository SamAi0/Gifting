from django.conf import settings
from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem, CartItemLogo, Order, OrderItem, OrderItemLogo, Address, Coupon
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, AddressSerializer
from products.models import Product
from .utils import is_maharashtra_pincode
from decimal import Decimal

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

class MergeCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        guest_items = request.data.get('items', [])
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        for item_data in guest_items:
            try:
                product_id = item_data.get('product_id')
                product = Product.objects.get(id=product_id)
                quantity = int(item_data.get('quantity', 1))
                customization_text = item_data.get('customization_text', '')
                customization_data = item_data.get('customization_data', '')

                # Check if item with same product and customization already exists in user cart
                existing_item = CartItem.objects.filter(
                    cart=cart, 
                    product=product,
                    customization_text=customization_text,
                    customization_data=customization_data
                ).first()

                if existing_item:
                    existing_item.quantity += quantity
                    existing_item.save()
                else:
                    CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=quantity,
                        customization_text=customization_text,
                        customization_data=customization_data
                    )
            except (Product.DoesNotExist, ValueError, TypeError):
                continue
                
        return Response({"message": "Cart merged successfully"})

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
from django.db.models import F

class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Use get_or_create to avoid RelatedObjectDoesNotExist if cart hasn't been initialized
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        # Pre-check stock for all items
        for item in cart.items.all():
            if item.product.stock < item.quantity:
                return Response({
                    "error": f"Insufficient stock for {item.product.name}. Available: {item.product.stock}"
                }, status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data.get('address_id')
        payment_method = request.data.get('payment_method', 'ONLINE')
        try:
            address = Address.objects.get(id=address_id, user=request.user)
            if not is_maharashtra_pincode(address.pincode):
                return Response({"error": "Selected address is outside Maharashtra. Delivery not available."}, status=status.HTTP_400_BAD_REQUEST)
        except Address.DoesNotExist:
            return Response({"error": "Invalid address"}, status=status.HTTP_400_BAD_REQUEST)

        business_name = request.data.get('business_name')
        gst_number = request.data.get('gst_number')
        coupon_code = request.data.get('coupon_code')
        
        subtotal = cart.total_price
        shipping_charges = Decimal('0.00') if subtotal > Decimal('5000.00') else Decimal('250.00')
        tax_amount = (subtotal * Decimal('0.18')).quantize(Decimal('0.01'))
        total_amount = subtotal + shipping_charges + tax_amount
        
        coupon = None
        if coupon_code:
            from django.utils import timezone
            coupon = Coupon.objects.filter(
                code=coupon_code, 
                active=True, 
                valid_from__lte=timezone.now(), 
                valid_to__gte=timezone.now()
            ).first()

        if coupon:
            discount = (total_amount * Decimal(coupon.discount_percent) / Decimal('100.00')).quantize(Decimal('0.01'))
            total_amount -= discount

        razorpay_order_id = None
        
        if payment_method == 'ONLINE':
            try:
                client = get_razorpay_client()
                razorpay_order = client.order.create({
                    "amount": int(total_amount * 100),
                    "currency": "INR",
                    "payment_capture": "1"
                })
                razorpay_order_id = razorpay_order['id']
            except Exception as e:
                logger.error(f"Razorpay Error: {str(e)}")
                return Response({"error": "Failed to create Razorpay order"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            with transaction.atomic():
                # Create local Order
                order = Order.objects.create(
                    user=request.user,
                    address=address,
                    total_amount=total_amount,
                    payment_method=payment_method,
                    razorpay_order_id=razorpay_order_id,
                    business_name=business_name,
                    gst_number=gst_number,
                    shipping_charges=shipping_charges,
                    tax_amount=tax_amount,
                    coupon=coupon,
                    status='CONFIRMED' if payment_method == 'COD' else 'PENDING'
                )

                for item in cart.items.all():
                    # Atomic stock decrement
                    updated = Product.objects.filter(id=item.product.id, stock__gte=item.quantity).update(stock=F('stock') - item.quantity)
                    if not updated:
                        raise Exception(f"Insufficient stock for {item.product.name} during final processing.")

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
                    
                    for logo in item.logos.all():
                        OrderItemLogo.objects.create(order_item=order_item, file=logo.file)
                
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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            order.status = 'CONFIRMED' # Fixed: 'PAID' was not in STATUS_CHOICES
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

from django.http import FileResponse
from .utils import generate_invoice_pdf

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for admins to manage orders, and users to view/download invoices.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-created_at')

    def get_permissions(self):
        if self.action == 'invoice':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    @action(detail=True, methods=['get'])
    def invoice(self, request, pk=None):
        order = self.get_object()
        # Security: Only admin or the order owner can download the invoice
        if not request.user.is_staff and order.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        pdf_buffer = generate_invoice_pdf(order)
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"Invoice_Order_{order.id}.pdf")

class ValidateCouponView(views.APIView):
    permission_classes = [permissions.AllowAny] # Allow guests to check coupons too

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"error": "Coupon code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.utils import timezone
        coupon = Coupon.objects.filter(
            code=code, 
            active=True, 
            valid_from__lte=timezone.now(), 
            valid_to__gte=timezone.now()
        ).first()
        
        if not coupon:
            return Response({"error": "Invalid or expired coupon"}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            "id": coupon.id,
            "code": coupon.code,
            "discount_percent": coupon.discount_percent,
        })
