"""
Agent API URL patterns
"""

from django.urls import path
from . import views

app_name = 'agents_api'

urlpatterns = [
    path('draft-request/', views.draft_request_with_agent, name='draft_request'),
    path('analyze-response/<int:request_id>/', views.analyze_response_with_agent, name='analyze_response'),
    path('generate-followup/<int:request_id>/', views.generate_followup_with_agent, name='generate_followup'),
]
