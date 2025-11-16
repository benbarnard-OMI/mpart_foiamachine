"""
FOIA Request admin configuration
"""

from django.contrib import admin
from .models import FOIARequest, RequestCommunication, RequestDocument


class RequestCommunicationInline(admin.TabularInline):
    """Inline admin for request communications"""
    model = RequestCommunication
    extra = 0
    fields = ['direction', 'communication_type', 'subject', 'date', 'agent_generated']
    readonly_fields = ['date']


class RequestDocumentInline(admin.TabularInline):
    """Inline admin for request documents"""
    model = RequestDocument
    extra = 0
    fields = ['title', 'file', 'is_request_document', 'is_response_document', 'agent_processed']


@admin.register(FOIARequest)
class FOIARequestAdmin(admin.ModelAdmin):
    """Admin interface for FOIA Request model"""
    
    list_display = [
        'title', 'user', 'agency', 'status', 'submitted_date', 
        'agent_assisted', 'response_received'
    ]
    list_filter = [
        'status', 'agent_assisted', 'response_received', 
        'requires_followup', 'is_deleted'
    ]
    search_fields = ['title', 'description', 'request_body', 'tracking_number']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'status', 'user', 'agency')
        }),
        ('Request Content', {
            'fields': ('request_body',)
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'submitted_date', 'due_date')
        }),
        ('Agent Assistance', {
            'fields': ('agent_assisted', 'agent_improvements'),
            'classes': ('collapse',)
        }),
        ('Response', {
            'fields': ('response_received', 'response_date', 'response_summary')
        }),
        ('Follow-up', {
            'fields': ('requires_followup', 'followup_notes'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [RequestCommunicationInline, RequestDocumentInline]


@admin.register(RequestCommunication)
class RequestCommunicationAdmin(admin.ModelAdmin):
    """Admin interface for Request Communication model"""
    
    list_display = ['request', 'direction', 'communication_type', 'subject', 'date', 'agent_generated']
    list_filter = ['direction', 'communication_type', 'agent_generated']
    search_fields = ['subject', 'content']
    date_hierarchy = 'date'


@admin.register(RequestDocument)
class RequestDocumentAdmin(admin.ModelAdmin):
    """Admin interface for Request Document model"""
    
    list_display = [
        'title', 'request', 'file_size', 
        'is_request_document', 'is_response_document', 
        'agent_processed'
    ]
    list_filter = [
        'is_request_document', 'is_response_document', 
        'agent_processed'
    ]
    search_fields = ['title', 'description', 'agent_summary']
    date_hierarchy = 'created_at'
