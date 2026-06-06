from django.contrib import admin
from .models import BulkInquiry, ContactMessage
from import_export.admin import ImportExportModelAdmin

@admin.register(BulkInquiry)
class BulkInquiryAdmin(ImportExportModelAdmin):
    list_display = ('company_name', 'contact_person', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('company_name', 'contact_person', 'email')
    readonly_fields = ('created_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)
