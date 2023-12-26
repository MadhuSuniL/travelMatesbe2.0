"""
ASGI config for lead_management project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os,time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travelmate_project.settings')

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import OriginValidator
django.setup()
from .ws_urls import urlpatterns
from channels.auth import AuthMiddlewareStack
from helper.MiddleWares import WSAuthMiddleware
from .settings import ASGI_ALLOWED_HOSTS
application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket':OriginValidator(
            AuthMiddlewareStack(
                WSAuthMiddleware(
                    URLRouter(urlpatterns)
                )
            )
        ,ASGI_ALLOWED_HOSTS+['*']
        ),
    }
)
