"""
Agency models - Government agencies and departments
"""

from django.db import models
from foiamachine.apps.core.models import TimeStampedModel, SoftDeleteModel


class Agency(TimeStampedModel, SoftDeleteModel):
    """
    Represents a government agency that can receive FOIA requests
    """
    LEVEL_CHOICES = [
        ('federal', 'Federal'),
        ('state', 'State'),
        ('local', 'Local'),
    ]
    
    name = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=500)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_agencies'
    )
    
    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    
    # FOIA-specific information
    foia_contact_email = models.EmailField(blank=True)
    foia_portal_url = models.URLField(blank=True)
    
    # Processing information
    average_response_days = models.IntegerField(
        default=20,
        help_text="Average number of days to respond to FOIA requests"
    )
    
    # Metadata
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Agencies'
        ordering = ['name']
    
    def __str__(self):
        return self.name
