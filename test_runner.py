import os
from pathlib import Path


def main():
    os.chdir(Path(__file__).resolve().parent)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polofeedback.settings")

    import django

    django.setup()
    from django.core.management import call_command

    call_command(
        "test",
        "feedback.tests.FeedbackViewsTests.test_dashboard_autenticado_get",
        verbosity=2,
    )


if __name__ == "__main__":
    main()
