"""
Celery configuration for MPART FOIA Machine
"""

import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foiamachine.config.settings')

app = Celery('foiamachine')

# Load config from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Periodic task schedule
app.conf.beat_schedule = {
    'auto-followup-overdue-requests': {
        'task': 'foiamachine.apps.agents.tasks.auto_followup_overdue_requests',
        'schedule': crontab(hour=9, minute=0),  # Run daily at 9 AM
    },
    'analyze-new-responses': {
        'task': 'foiamachine.apps.agents.tasks.analyze_new_responses',
        'schedule': crontab(hour='*/6'),  # Run every 6 hours
    },
}
