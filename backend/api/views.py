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

        revenue = Order.objects.filter(status__in=['CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED']).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Get 5 most recent orders with related data
        recent_orders_queryset = Order.objects.select_related('user', 'address').prefetch_related('items', 'items__product').all().order_by('-created_at')[:5]
        recent_orders = OrderSerializer(recent_orders_queryset, many=True, context={'request': request}).data

        # Get top 5 products by order count (Popular Products)
        popular_products_queryset = Product.objects.annotate(
            num_orders=Count('orderitem')
        ).order_by('-num_orders')[:5]
        popular_products = ProductSerializer(popular_products_queryset, many=True, context={'request': request}).data

        data = {
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status='PENDING').count(),
            "total_inquiries": BulkInquiry.objects.count(),
            "total_revenue": float(revenue),
            "recent_orders": recent_orders,
            "popular_products": popular_products,
        }
        return Response(data)
