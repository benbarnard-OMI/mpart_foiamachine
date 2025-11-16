"""
Custom User model for MPART FOIA Machine
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from foiamachine.apps.core.models import TimeStampedModel


class User(AbstractUser, TimeStampedModel):
    """
    Custom user model extending Django's AbstractUser
    """
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    # Preferences
    receive_email_notifications = models.BooleanField(default=True)
    enable_agent_assistance = models.BooleanField(
        default=True,
        help_text="Allow AI agents to assist with request drafting and management"
    )
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Returns the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.email
