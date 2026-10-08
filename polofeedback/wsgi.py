"""
WSGI config for polofeedback project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polofeedback.settings')

application = get_wsgi_application()

from feedback.apps import ensure_default_dashboard_access

ensure_default_dashboard_access()
