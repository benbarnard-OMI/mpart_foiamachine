# Generated migration for Statute enhancements
# This migration adds enhanced response time and residency fields to the Statute model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statute',
            name='response_time_days',
            field=models.IntegerField(blank=True, help_text='Specific response time in days', null=True),
        ),
        migrations.AddField(
            model_name='statute',
            name='response_time_type',
            field=models.CharField(
                choices=[
                    ('specific', 'Specific number of days'),
                    ('prompt', 'Prompt response required'),
                    ('reasonable', 'Reasonable time'),
                    ('none', 'No specific limit'),
                ],
                default='specific',
                help_text='Type of response time requirement',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='statute',
            name='residency_required',
            field=models.BooleanField(default=False, help_text='Whether state residency is required'),
        ),
        migrations.AddField(
            model_name='statute',
            name='fee_structure',
            field=models.TextField(blank=True, help_text='Fee information (JSON format)', null=True),
        ),
        migrations.AddField(
            model_name='statute',
            name='exemptions',
            field=models.TextField(blank=True, help_text='Common exemptions (JSON format)', null=True),
        ),
        migrations.AlterField(
            model_name='statute',
            name='fees_exemptions',
            field=models.ManyToManyField(blank=True, to='government.feeexemptionother'),
        ),
        migrations.AlterField(
            model_name='statute',
            name='updates',
            field=models.ManyToManyField(blank=True, to='government.update'),
        ),
        migrations.AlterField(
            model_name='update',
            name='author',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AlterField(
            model_name='government',
            name='nation',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, to='government.nation'),
        ),
        migrations.AlterField(
            model_name='government',
            name='statutes',
            field=models.ManyToManyField(blank=True, related_name='related_statutes', to='government.statute'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='primary_language',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='primary_language_nations', to='government.language'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='foi_languages',
            field=models.ManyToManyField(blank=True, to='government.language'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='admin_0_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='admin_0_nations', to='government.adminname'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='admin_1_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='admin_1_nations', to='government.adminname'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='admin_2_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='admin_2_nations', to='government.adminname'),
        ),
        migrations.AlterField(
            model_name='nation',
            name='admin_3_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='admin_3_nations', to='government.adminname'),
        ),
    ]
