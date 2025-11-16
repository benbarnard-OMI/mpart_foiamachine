"""
Custom User model for MPART FOIA Machine
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from foiamachine.apps.core.models import TimeStampedModel


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Set username to email if not provided
        if 'username' not in extra_fields:
            extra_fields['username'] = email
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


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
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required as USERNAME_FIELD
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        """Returns the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.email
