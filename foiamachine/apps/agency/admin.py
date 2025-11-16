from django.contrib import admin
from django.utils.html import format_html

from .models import Agency


class AgencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'government', 'medicaid_agency_name', 'foia_officer_name', 
                    'statutory_response_days', 'requires_residency', 'is_territory']
    list_filter = ['is_territory', 'requires_residency', 'government', 'statutory_response_days']
    search_fields = ['name', 'medicaid_agency_name', 'government__name', 
                     'foia_officer_name', 'foia_officer_email', 
                     'contacts__emails__content', 'contacts__last_name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'government', 'creator', 'hidden')
        }),
        ('Medicaid Agency Information', {
            'fields': ('medicaid_agency_name', 'foia_website', 'is_territory')
        }),
        ('FOIA Officer Contact', {
            'fields': ('foia_officer_name', 'foia_officer_email', 'foia_officer_phone', 
                       'foia_officer_fax', 'foia_mailing_address')
        }),
        ('Submission & Response', {
            'fields': ('submission_methods', 'statutory_response_days', 
                       'requires_residency', 'legal_notes')
        }),
        ('Territory Information', {
            'fields': ('cms_region', 'cms_region_contact'),
            'classes': ('collapse',)
        }),
        ('Contacts', {
            'fields': ('contacts',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('pub_contact_cnt', 'editor_contact_cnt'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['slug', 'pub_contact_cnt', 'editor_contact_cnt']
    
    filter_horizontal = ['contacts']
    
    def get_queryset(self, request):
        """Optimize queryset with prefetch_related"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('government', 'contacts', 'contacts__emails')
    
    def response_time_display(self, obj):
        """Display response time in a readable format"""
        if obj.statutory_response_days is None:
            return format_html('<span style="color: #999;">No limit</span>')
        elif obj.statutory_response_days == -1:
            return format_html('<span style="color: #ff9800;">Prompt</span>')
        elif obj.statutory_response_days == -2:
            return format_html('<span style="color: #ff9800;">Reasonable</span>')
        elif obj.statutory_response_days == -3:
            return format_html('<span style="color: #999;">No limit</span>')
        else:
            return f"{obj.statutory_response_days} days"
    
    response_time_display.short_description = 'Response Time'
    
    def get_list_display(self, request):
        """Add response_time_display to list_display"""
        display = list(super().get_list_display(request))
        if 'response_time_display' not in display:
            display.insert(display.index('statutory_response_days'), 'response_time_display')
            display.remove('statutory_response_days')
        return display


admin.site.register(Agency, AgencyAdmin)
