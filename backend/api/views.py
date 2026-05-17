from rest_framework import generics, permissions
from inquiries.models import BulkInquiry, ContactMessage
from company_info.models import Testimonial, Settings
from .serializers import (
    BulkInquirySerializer,
    ContactMessageSerializer, TestimonialSerializer, SettingsSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product
from orders.models import Order
from django.db.models import Q

class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class SettingsDetailView(generics.RetrieveAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    
    def get_object(self):
        obj = Settings.objects.first()
        if not obj:
            from django.http import Http404
            raise Http404("Settings not found. Please run seed_data.py")
        return obj

class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

class BulkInquiryCreateView(generics.CreateAPIView):
    queryset = BulkInquiry.objects.all()
    serializer_class = BulkInquirySerializer

class AdminStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        from django.db.models import Sum, Count
        from orders.serializers import OrderSerializer
        from .serializers import ProductSerializer

        confirmed_statuses = ['CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED']
        revenue = Order.objects.filter(status__in=confirmed_statuses).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get 5 most recent orders with related data
        recent_orders_queryset = Order.objects.select_related('user', 'address').prefetch_related('items', 'items__product').all().order_by('-created_at')[:5]
        recent_orders = OrderSerializer(recent_orders_queryset, many=True, context={'request': request}).data

        # Get top 5 products by order count (Popular Products)
        popular_products_queryset = Product.objects.annotate(
            num_orders=Count('orderitem')
        ).order_by('-num_orders')[:5]
        popular_products = ProductSerializer(popular_products_queryset, many=True, context={'request': request}).data

        return Response({
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status='PENDING').count(),
            "total_inquiries": BulkInquiry.objects.count(),
            "total_revenue": float(revenue),
            "recent_orders": recent_orders,
            "popular_products": popular_products,
        })

class AdminGlobalSearchView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"products": [], "orders": [], "users": []})

        from django.contrib.auth.models import User
        from orders.serializers import OrderSerializer
        from .serializers import ProductSerializer

        # Search Products
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(sku__icontains=query) | Q(description__icontains=query)
        )[:5]
        product_data = ProductSerializer(products, many=True, context={'request': request}).data

        # Search Orders
        orders = Order.objects.filter(
            Q(id__icontains=query) | Q(user__username__icontains=query) | Q(razorpay_order_id__icontains=query)
        )[:5]
        order_data = OrderSerializer(orders, many=True, context={'request': request}).data

        # Search Users
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )[:5]
        user_data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]

        return Response({
            "products": product_data,
            "orders": order_data,
            "users": user_data
        })
