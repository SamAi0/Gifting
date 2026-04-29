from rest_framework import generics, permissions
from inquiries.models import BulkInquiry, ContactMessage
from company_info.models import Testimonial, Settings
from .serializers import (
    BulkInquirySerializer,
    ContactMessageSerializer, TestimonialSerializer, SettingsSerializer
)

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
