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
