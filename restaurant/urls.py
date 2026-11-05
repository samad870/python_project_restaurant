"""
Main URL Configuration for Restaurant Management System.
All routes are routed to the 'management' app.
Includes explicit static serving fallback for production/Vercel environments.
"""

from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', include('management.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]
