"""
Core API URL patterns
"""

from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('requests/', include('foiamachine.apps.requests.api_urls')),
    path('agencies/', include('foiamachine.apps.agency.api_urls')),
    path('agents/', include('foiamachine.apps.agents.api_urls')),
]
