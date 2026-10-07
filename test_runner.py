import os

ROOT = r"C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main"
os.chdir(ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polofeedback.settings")

import django

django.setup()
from django.core.management import call_command

call_command('test', 'feedback.tests.FeedbackViewsTests.test_dashboard_autenticado_get', verbosity=2)
