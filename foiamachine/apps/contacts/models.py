"""
Contact models
"""

from django.db import models
from foiamachine.apps.core.models import TimeStampedModel


class Contact(TimeStampedModel):
    """
    Contact person at a government agency
    """
    agency = models.ForeignKey(
        'agency.Agency',
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True)
    
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    is_foia_officer = models.BooleanField(
        default=False,
        help_text="Is this person a FOIA officer?"
    )
    
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.agency.name})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
