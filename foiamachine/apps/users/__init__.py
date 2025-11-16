"""
Users app for MPART FOIA Machine
Custom user model and authentication
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.users'
    verbose_name = 'Users'
