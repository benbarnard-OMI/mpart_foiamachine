from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import AutoSlugField
from apps.government.models import Government
from apps.core.models import BaseData
from apps.contacts.models import Contact
from datetime import datetime
from django.utils import timezone
import json


class AgencyManager(models.Manager):
    def all_them(self):
        return super(AgencyManager, self).get_queryset().filter(deprecated__isnull=True).prefetch_related("government", "creator")

    def get_queryset(self):
        return super(AgencyManager, self).get_queryset().filter(deprecated__isnull=True, hidden=False).prefetch_related("government", "creator")

class Agency(BaseData):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=('name', ), overwrite=False)
    government = models.ForeignKey(Government, on_delete=models.CASCADE)
    contacts = models.ManyToManyField(Contact, blank=True, related_name='agency_related_contacts')
    objects = AgencyManager()
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    hidden = models.BooleanField(default=False)
    pub_contact_cnt = models.IntegerField(default=0)
    editor_contact_cnt = models.IntegerField(default=0)
    
    # Medicaid-specific fields
    medicaid_agency_name = models.CharField(max_length=255, blank=True, null=True, help_text="Official Medicaid agency name")
    foia_officer_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of FOIA officer")
    foia_officer_email = models.EmailField(blank=True, null=True, help_text="FOIA officer email address")
    foia_officer_phone = models.CharField(max_length=255, blank=True, null=True, help_text="FOIA officer phone number")
    foia_officer_fax = models.CharField(max_length=255, blank=True, null=True, help_text="FOIA officer fax number")
    foia_mailing_address = models.TextField(blank=True, null=True, help_text="Mailing address for FOIA requests")
    foia_website = models.URLField(blank=True, null=True, help_text="Agency website for FOIA information")
    submission_methods = models.TextField(blank=True, null=True, help_text="How to submit requests (JSON or comma-separated)")
    statutory_response_days = models.IntegerField(null=True, blank=True, help_text="Response time in days (-1 for 'prompt', -2 for 'reasonable', -3 for 'no limit')")
    requires_residency = models.BooleanField(default=False, help_text="Whether state residency is required")
    legal_notes = models.TextField(blank=True, null=True, help_text="Special legal considerations and notes")
    is_territory = models.BooleanField(default=False, help_text="Whether this is a US territory")
    cms_region = models.CharField(max_length=50, blank=True, null=True, help_text="CMS Regional Office if territory")
    cms_region_contact = models.TextField(blank=True, null=True, help_text="CMS Regional Office contact information")


    class Meta:
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

    def has_editable_contact(self, usr):
        for contact in self.contacts.all():
            if contact.creator == usr:
                return True
        return False

    @property
    def late_requests(self):
        """
        How many requests have FAILED to meet their deadlines?
        """
        num_late_requests = 0
        for r in self.related_agencies.all():
            if r.is_late_naive: num_late_requests += 1
        return num_late_requests

    @property
    def average_time_outstanding(self):
        days_late = 0
        for r in self.related_agencies.all():
            days_late += r.time_outstanding
        return days_late 

    def save(self, *args, **kw):
        if self.pk is not None:
            self.pub_contact_cnt = self.contacts.filter(hidden=False).count()
            self.editor_contact_cnt = self.contacts.all().count()
        else:
            self.pub_contact_cnt = 0
            self.editor_contact_cnt = 0
        super(Agency, self).save(*args, **kw)
