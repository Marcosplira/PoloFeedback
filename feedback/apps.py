from django.apps import AppConfig

DEFAULT_DASHBOARD_USERS = {
    "gerente": {
        "password": "gerente123",
        "is_staff": True,
        "is_superuser": True,
    },
    "marcos": {
        "password": "marcos123",
        "is_staff": True,
        "is_superuser": True,
    },
}


def ensure_default_dashboard_access():
    """Cria contas de acesso do painel para gerente e responsável do projeto."""
    try:
        from django.contrib.auth import get_user_model

        User = get_user_model()
        for username, data in DEFAULT_DASHBOARD_USERS.items():
            user, created = User.objects.get_or_create(username=username)
            user.is_staff = True
            user.is_superuser = True
            user.set_password(data["password"])
            if not user.email:
                user.email = f"{username}@polofitacademias.com"
            user.save(update_fields=["is_staff", "is_superuser", "password", "email"])
    except Exception:
        # Evita quebrar a inicialização do serviço se a base ainda não estiver pronta.
        pass


class FeedbackConfig(AppConfig):
    name = 'feedback'

    def ready(self):
        # Importado tardia para evitar comportamentos durante as migrações.
        return
