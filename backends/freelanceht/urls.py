"""
URL configuration for FreelanceHT project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls', namespace='core')),
    path('compte/', include('apps.accounts.urls', namespace='accounts')),
    path('freelancers/', include('apps.freelancers.urls', namespace='freelancers')),
    path('projets/', include('apps.projects.urls', namespace='projects')),
    path('contrats/', include('apps.contracts.urls', namespace='contracts')),
    path('messages/', include('apps.messaging.urls', namespace='messaging')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
