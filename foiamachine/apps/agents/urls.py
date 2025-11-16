"""
Agent URL patterns
"""

from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('', views.agent_dashboard, name='dashboard'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('suggestions/<int:suggestion_id>/accept/', views.accept_suggestion, name='accept_suggestion'),
    path('suggestions/<int:suggestion_id>/reject/', views.reject_suggestion, name='reject_suggestion'),
]
