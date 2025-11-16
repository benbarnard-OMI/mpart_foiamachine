"""
ASGI config for MPART FOIA Machine project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foiamachine.config.settings')

application = get_asgi_application()
