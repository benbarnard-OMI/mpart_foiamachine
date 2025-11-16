"""
Requests app - Manages FOIA requests
"""

from django.apps import AppConfig


class RequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.requests'
    verbose_name = 'FOIA Requests'
