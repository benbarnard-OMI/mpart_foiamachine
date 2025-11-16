"""
Agency app - Manages government agencies
"""

from django.apps import AppConfig


class AgencyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.agency'
    verbose_name = 'Agencies'
