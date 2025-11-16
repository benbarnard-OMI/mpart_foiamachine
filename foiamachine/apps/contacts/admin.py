"""
Contact admin configuration
"""

from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model"""
    
    list_display = ['full_name', 'title', 'agency', 'email', 'is_foia_officer', 'is_active']
    list_filter = ['is_foia_officer', 'is_active', 'agency__level']
    search_fields = ['first_name', 'last_name', 'email', 'title', 'agency__name']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title')
        }),
        ('Agency', {
            'fields': ('agency', 'is_foia_officer')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_active'),
            'classes': ('collapse',)
        }),
    )
