"""
Agent admin configuration
"""

from django.contrib import admin
from .models import AgentTask, AgentSuggestion, AgentWorkflow


@admin.register(AgentTask)
class AgentTaskAdmin(admin.ModelAdmin):
    """Admin interface for Agent Task model"""
    
    list_display = [
        'id', 'task_type', 'status', 'user', 'foia_request',
        'created_at', 'tokens_used'
    ]
    list_filter = ['task_type', 'status', 'agent_model']
    search_fields = ['user__email', 'foia_request__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at']
    
    fieldsets = (
        ('Task Information', {
            'fields': ('task_type', 'status', 'user', 'foia_request')
        }),
        ('Data', {
            'fields': ('input_data', 'output_data')
        }),
        ('Processing', {
            'fields': ('started_at', 'completed_at', 'error_message')
        }),
        ('Agent Metadata', {
            'fields': ('agent_model', 'tokens_used')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AgentSuggestion)
class AgentSuggestionAdmin(admin.ModelAdmin):
    """Admin interface for Agent Suggestion model"""
    
    list_display = [
        'title', 'user', 'foia_request', 'suggestion_type',
        'is_accepted', 'is_rejected', 'created_at'
    ]
    list_filter = ['suggestion_type', 'is_accepted', 'is_rejected']
    search_fields = ['title', 'description', 'user__email', 'foia_request__title']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Suggestion', {
            'fields': ('user', 'foia_request', 'suggestion_type', 'title', 'description')
        }),
        ('Content', {
            'fields': ('suggested_text',)
        }),
        ('User Response', {
            'fields': ('is_accepted', 'is_rejected', 'feedback')
        }),
    )


@admin.register(AgentWorkflow)
class AgentWorkflowAdmin(admin.ModelAdmin):
    """Admin interface for Agent Workflow model"""
    
    list_display = [
        'name', 'trigger_event', 'is_active',
        'execution_count', 'success_count', 'failure_count'
    ]
    list_filter = ['is_active', 'trigger_event']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Workflow Configuration', {
            'fields': ('name', 'description', 'trigger_event', 'actions', 'is_active')
        }),
        ('Statistics', {
            'fields': ('execution_count', 'success_count', 'failure_count'),
            'classes': ('collapse',)
        }),
    )
