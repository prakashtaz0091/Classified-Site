"""
ASGI config for configs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings.settings')

# application = get_asgi_application()

import os
from django.core.asgi import get_asgi_application

# Fetch the DJANGO_ENV environment variable, defaulting to "production" if not set
environment = os.environ.get("DJANGO_ENV", "production")

# Set the DJANGO_SETTINGS_MODULE environment variable based on the DJANGO_ENV
if environment == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.production")
elif environment == "development":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.development")
else:
    raise ValueError(f"Unknown DJANGO_ENV: {environment}")

# Initialize the ASGI application
application = get_asgi_application()
