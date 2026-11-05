"""
Django settings for Restaurant Management System.

This configuration is designed with CSV-based data storage:
- No SQLite database
- No MySQL / PostgreSQL / MongoDB
- No Django ORM
- All permanent data is stored in CSV files inside the data/ folder.
- Uses CookieStorage for flash messages.
- Uses WhiteNoise to reliably serve static CSS files on Vercel and production.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-restaurant-management-system-secret-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition - ONLY lightweight apps, NO auth/admin/session/contenttypes
INSTALLED_APPS = [
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurant.wsgi.application'

# Database configuration: EMPTY (Strict requirement - CSV files only)
DATABASES = {}

# Flash messages storage using browser cookies (No database session needed)
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
WHITENOISE_USE_FINDERS = True

# Path to the CSV storage directory
DATA_DIR = BASE_DIR / 'data'
