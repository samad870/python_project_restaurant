"""
Main URL Configuration for Restaurant Management System.
All routes are routed to the 'management' app.
Includes explicit static serving fallback for production/Vercel environments.
"""

from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.http import HttpResponse

def serve_css(request):
    """Explicitly serve style.css with text/css MIME type."""
    css_file = settings.BASE_DIR / 'static' / 'css' / 'style.css'
    try:
        content = css_file.read_text(encoding='utf-8')
    except Exception:
        content = ''
    return HttpResponse(content, content_type='text/css; charset="utf-8"')

urlpatterns = [
    # Direct endpoint ensuring style.css is ALWAYS served with text/css
    path('static/css/style.css', serve_css, name='serve_style_css'),
    path('', include('management.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]
