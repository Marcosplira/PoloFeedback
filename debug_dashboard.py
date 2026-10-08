import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polofeedback.settings")

import django

django.setup()

from django.core.management import call_command


if __name__ == "__main__":
    call_command(
        "test",
        "feedback.tests.FeedbackViewsTests.test_dashboard_autenticado_get",
        verbosity=2,
    )
