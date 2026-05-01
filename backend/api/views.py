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
        from django.db.models import Sum
        revenue = Order.objects.filter(status='PAID').aggregate(total=Sum('total_amount'))['total'] or 0
        data = {
            "total_products": Product.objects.count(),
            "total_orders": Order.objects.count(),
            "pending_orders": Order.objects.filter(status='PENDING').count(),
            "total_inquiries": BulkInquiry.objects.count(),
            "total_revenue": float(revenue),
        }
        return Response(data)
