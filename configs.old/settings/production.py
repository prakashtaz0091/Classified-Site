# production.py for now demo settings not actual

from common.common import *

# Debug mode
DEBUG = False

# Allowed hosts for production
ALLOWED_HOSTS = ['yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Security settings (optional)
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
