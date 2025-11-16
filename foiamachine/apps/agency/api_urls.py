"""
Agency API URLs
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.agency.api_views import AgencyViewSet

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet, basename='agency')

app_name = 'agency_api'

urlpatterns = [
    path('', include(router.urls)),
]
