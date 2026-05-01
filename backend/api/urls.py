from django.urls import path
from .views import (
    TestimonialListView, SettingsDetailView, ContactCreateView, 
    BulkInquiryCreateView, AdminStatsView
)

urlpatterns = [
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('settings/', SettingsDetailView.as_view(), name='settings-detail'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('bulk-inquiry/', BulkInquiryCreateView.as_view(), name='bulk-inquiry-create'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
]
