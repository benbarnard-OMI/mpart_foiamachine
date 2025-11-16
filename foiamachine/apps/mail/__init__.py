"""
Mail app - Handles email communications
"""

from django.apps import AppConfig


class MailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.mail'
    verbose_name = 'Mail'
