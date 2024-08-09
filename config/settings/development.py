# import os
# from dotenv import load_dotenv

# load_dotenv()
# # Import all code from base.py
# from .base import *

# DEBUG = True


# environment = os.environ.get("DJANGO_ENV", "development")

# EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
# EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"
# EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
# EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
# EMAIL_PORT = os.environ.get("EMAIL_PORT", "")

# DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")


# DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE", "")

# DATABASES = {
#     "default": {
#         'ENGINE': os.environ.get("DATABASE_ENGINE", ""),
#         'NAME': os.environ.get("DATABASE_NAME", ""),
#         'USER': os.environ.get("DATABASE_USER", ""),
#         'PASSWORD': os.environ.get("DATABASE_PASSWORD", ""),
#         'HOST': os.environ.get("DATABASE_HOST", ""),
#         'PORT': os.environ.get("DATABASE_PORT", ""),
#     },
#     'replica': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "test_db.sqlite3",
#     },
# }


# # ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
# ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
# print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS},'hello")

# CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
# CORS_ALLOW_ALL_ORIGINS = os.environ.get(
#     "CORS_ALLOW_ALL_ORIGINS", "True") == "True"


# USE_X_FORWARDED_HOST = True
# CSRF_COOKIE_SECURE = True

# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True



import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.sample')

# Import all code from base.py
from .base import *

DEBUG = True

# Override the DATABASES setting for development to use SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}



# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# print(ALLOWED_HOSTS,'allow host')

ALLOWED_HOSTS=['localhost','127.0.0.1']
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_ALL_ORIGINS = os.environ.get(
    "CORS_ALLOW_ALL_ORIGINS", "True") == "True"

USE_X_FORWARDED_HOST = True
CSRF_COOKIE_SECURE = False  # Set to False for development
SECURE_CONTENT_TYPE_NOSNIFF = False  # Disable in development
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Disable in development
SECURE_HSTS_PRELOAD = False  # Disable in development

# Email settings
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")

# Static and Media files
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
