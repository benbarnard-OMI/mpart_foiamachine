"""
Agents app - AI-powered automation for FOIA request management
This app provides intelligent agents that assist with:
- Drafting FOIA requests
- Analyzing responses
- Generating follow-ups
- Workflow automation
"""

from django.apps import AppConfig


class AgentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foiamachine.apps.agents'
    verbose_name = 'AI Agents'
