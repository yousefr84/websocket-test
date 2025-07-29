"""
ASGI config for DjangoProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# تنظیم DJANGO_SETTINGS_MODULE و لود اپلیکیشن‌ها
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

# لود اپلیکیشن‌های جنگو قبل از هر چیز
django_asgi_app = get_asgi_application()

# حالا import ماژول‌های وابسته
import testsocket.routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(testsocket.routing.websocket_urlpatterns)
    ),
})