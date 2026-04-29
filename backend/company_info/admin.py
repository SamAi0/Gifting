from django.contrib import admin
from .models import Testimonial, Settings

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'designation')
    search_fields = ('name', 'company', 'message')

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'phone1')
    
    def has_add_permission(self, request):
        # Only allow one instance of Settings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
