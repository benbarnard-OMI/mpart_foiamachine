"""
WSGI config for MPART FOIA Machine project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foiamachine.config.settings')

application = get_wsgi_application()
