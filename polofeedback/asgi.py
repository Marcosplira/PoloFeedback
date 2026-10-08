"""
ASGI config for polofeedback project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polofeedback.settings')

application = get_asgi_application()

from feedback.apps import ensure_default_dashboard_access

ensure_default_dashboard_access()
