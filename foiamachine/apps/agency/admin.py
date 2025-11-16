"""
Agency admin configuration
"""

from django.contrib import admin
from .models import Agency


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    """Admin interface for Agency model"""
    
    list_display = ['name', 'level', 'is_active', 'foia_contact_email', 'average_response_days']
    list_filter = ['level', 'is_active', 'is_deleted']
    search_fields = ['name', 'email', 'foia_contact_email', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'level', 'parent', 'description', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'fax', 'address', 'website')
        }),
        ('FOIA Information', {
            'fields': ('foia_contact_email', 'foia_portal_url', 'average_response_days')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
