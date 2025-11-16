"""
URL Configuration for MPART FOIA Machine
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include('foiamachine.apps.core.api_urls')),
    path('requests/', include('foiamachine.apps.requests.urls')),
    path('agencies/', include('foiamachine.apps.agency.urls')),
    path('contacts/', include('foiamachine.apps.contacts.urls')),
    path('agents/', include('foiamachine.apps.agents.urls')),
    path('', include('foiamachine.apps.core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Customize admin site
admin.site.site_header = "MPART FOIA Machine Administration"
admin.site.site_title = "MPART FOIA Admin"
admin.site.index_title = "Welcome to MPART FOIA Machine"
