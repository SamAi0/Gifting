from django.urls import path
from .views import (
    TestimonialListView, SettingsDetailView, ContactCreateView, 
    BulkOrderCreateView, AdminStatsView, AdminGlobalSearchView
)

urlpatterns = [
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
    path('settings/', SettingsDetailView.as_view(), name='settings-detail'),
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('bulk-order/', BulkOrderCreateView.as_view(), name='bulk-order-create'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),
    path('admin/search/', AdminGlobalSearchView.as_view(), name='admin-search'),
]
