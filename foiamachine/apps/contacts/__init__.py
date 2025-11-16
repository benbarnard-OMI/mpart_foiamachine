"""
Contacts app - Manages agency contacts
"""

from django.apps import AppConfig


class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.contacts'
    verbose_name = 'Contacts'
