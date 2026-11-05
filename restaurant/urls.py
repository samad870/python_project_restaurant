"""
Main URL Configuration for Restaurant Management System.
All routes are routed to the 'management' app.
"""

from django.urls import path, include

urlpatterns = [
    path('', include('management.urls')),
]

