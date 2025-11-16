"""
Core app for MPART FOIA Machine
Provides base functionality and utilities
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.core'
    verbose_name = 'Core'
