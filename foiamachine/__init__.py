"""
MPART FOIA Machine - Main Package
A customized FOIA request management system with integrated AI agent flows
"""

__version__ = "1.0.0"
__author__ = "MPART Team"

# This will make sure the Celery app is always imported when Django starts
from .celery import app as celery_app

__all__ = ('celery_app',)
