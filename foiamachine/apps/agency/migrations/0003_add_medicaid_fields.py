# Generated migration for Medicaid fields
# This migration adds Medicaid-specific fields to the Agency model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0002_auto__add_field_agency_pub_contact_cnt__add_field_agency_editor_contac'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='medicaid_agency_name',
            field=models.CharField(blank=True, help_text='Official Medicaid agency name', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='foia_officer_name',
            field=models.CharField(blank=True, help_text='Name of FOIA officer', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='foia_officer_email',
            field=models.EmailField(blank=True, help_text='FOIA officer email address', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='foia_officer_phone',
            field=models.CharField(blank=True, help_text='FOIA officer phone number', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='foia_officer_fax',
            field=models.CharField(blank=True, help_text='FOIA officer fax number', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='foia_mailing_address',
            field=models.TextField(blank=True, help_text='Mailing address for FOIA requests', null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='foia_website',
            field=models.URLField(blank=True, help_text='Agency website for FOIA information', null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='submission_methods',
            field=models.TextField(blank=True, help_text='How to submit requests (JSON or comma-separated)', null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='statutory_response_days',
            field=models.IntegerField(blank=True, help_text="Response time in days (-1 for 'prompt', -2 for 'reasonable', -3 for 'no limit')", null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='requires_residency',
            field=models.BooleanField(default=False, help_text='Whether state residency is required'),
        ),
        migrations.AddField(
            model_name='agency',
            name='legal_notes',
            field=models.TextField(blank=True, help_text='Special legal considerations and notes', null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='is_territory',
            field=models.BooleanField(default=False, help_text='Whether this is a US territory'),
        ),
        migrations.AddField(
            model_name='agency',
            name='cms_region',
            field=models.CharField(blank=True, help_text='CMS Regional Office if territory', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='agency',
            name='cms_region_contact',
            field=models.TextField(blank=True, help_text='CMS Regional Office contact information', null=True),
        ),
        migrations.AlterField(
            model_name='agency',
            name='government',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, to='government.government'),
        ),
        migrations.AlterField(
            model_name='agency',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, to='auth.user'),
        ),
    ]
