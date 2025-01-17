import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.message import routing


# Fetch the DJANGO_ENV environment variable, defaulting to "production" if not set
environment = os.environ.get("DJANGO_ENV", "production")
print(environment,'===.')

# Set the DJANGO_SETTINGS_MODULE environment variable based on the DJANGO_ENV
if environment == "production":
    print('i am productions===========================+++>')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.production")
elif environment == "development":
    print('i am developemtn==================.>')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.development")
else:
    raise ValueError(f"Unknown DJANGO_ENV: {environment}")

# Initialize the ASGI application
# application = get_asgi_application() #previous

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

