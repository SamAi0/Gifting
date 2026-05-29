from django.contrib import admin
from .models import Settings, Testimonial
from import_export.admin import ImportExportModelAdmin

@admin.register(Settings)
class SettingsAdmin(ImportExportModelAdmin):
    list_display = ('company_name', 'email', 'phone1')
    
    def has_add_permission(self, request):
        # Only allow one instance of settings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Testimonial)
class TestimonialAdmin(ImportExportModelAdmin):
    list_display = ('name', 'designation', 'company')
    search_fields = ('name', 'company')
