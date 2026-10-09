import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Cria ou atualiza as duas contas privadas de acesso ao painel e gestão de usuários."

    legacy_usernames = ("gerente", "marcos")
    accounts = (
        ("DASHBOARD_MANAGER_USERNAME", "DASHBOARD_MANAGER_PASSWORD"),
        ("DASHBOARD_OWNER_USERNAME", "DASHBOARD_OWNER_PASSWORD"),
    )
    permission_codenames = (
        "view_avaliacao",
        "change_avaliacao",
        "view_funcionario",
        "add_funcionario",
        "change_funcionario",
        "view_funcao",
        "add_funcao",
        "change_funcao",
        "view_respostaenquete",
        "view_equipamento",
        "add_equipamento",
        "change_equipamento",
        "view_exercicio",
        "add_exercicio",
        "change_exercicio",
        "view_planotreino",
        "add_planotreino",
        "change_planotreino",
        "delete_planotreino",
        "view_itemplanotreino",
        "add_itemplanotreino",
        "change_itemplanotreino",
        "delete_itemplanotreino",
    )
    user_permission_codenames = ("view_user", "add_user", "change_user")

    def _disable_legacy_accounts(self, keep_usernames=()):
        user_model = get_user_model()
        for username in self.legacy_usernames:
            if username in keep_usernames:
                continue
            user = user_model.objects.filter(username=username).first()
            if user is None or not user.is_active:
                continue
            user.set_unusable_password()
            user.is_active = False
            user.is_staff = False
            user.is_superuser = False
            user.save(
                update_fields=(
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            )
            user.groups.clear()
            user.user_permissions.clear()

    def handle(self, *_args, **_options):
        configured_accounts = []
        missing_variables = []
        for username_key, password_key in self.accounts:
            username = os.environ.get(username_key, "").strip()
            password = os.environ.get(password_key, "")
            if not username or not password:
                missing_variables.extend(
                    key for key, value in ((username_key, username), (password_key, password))
                    if not value
                )
                continue
            if any(existing[0] == username for existing in configured_accounts):
                raise CommandError("As duas contas precisam ter usuários diferentes.")
            configured_accounts.append((username, password))

        if missing_variables:
            self._disable_legacy_accounts()
            self.stderr.write(
                self.style.WARNING(
                    "Contas do dashboard não atualizadas; configure estas variáveis "
                    "privadas para criá-las: " + ", ".join(missing_variables)
                )
            )
            return

        permissions_feedback = Permission.objects.filter(
            content_type__app_label="feedback",
            codename__in=self.permission_codenames,
        )
        permissions_users = Permission.objects.filter(
            content_type__app_label="auth",
            codename__in=self.user_permission_codenames,
        )
        found_codenames = set(permissions_feedback.values_list("codename", flat=True))
        missing_codenames = set(self.permission_codenames) - found_codenames
        found_user_codenames = set(permissions_users.values_list("codename", flat=True))
        missing_user_codenames = (
            set(self.user_permission_codenames) - found_user_codenames
        )
        if missing_codenames or missing_user_codenames:
            raise CommandError(
                "Permissões de usuários ou do dashboard ausentes. Execute as "
                "migrações antes de configurar as contas."
            )
        permissions = permissions_feedback | permissions_users

        user_model = get_user_model()
        users_to_save = []
        for username, password in configured_accounts:
            user = user_model.objects.filter(username=username).first()
            if user is None:
                user = user_model(username=username)
            try:
                validate_password(password, user=user)
            except ValidationError as error:
                raise CommandError(
                    f"A senha configurada para {username} não atende aos "
                    "requisitos de segurança: " + "; ".join(error.messages)
                ) from error
            users_to_save.append((user, password))

        self._disable_legacy_accounts(
            keep_usernames={username for username, _ in configured_accounts}
        )
        for user, password in users_to_save:
            user.set_password(password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = False
            user.save()
            user.groups.clear()
            user.user_permissions.set(permissions)

        admin_password = os.environ.get("ADMIN_PASSWORD", "").strip()
        if admin_password:
            admin_user = user_model.objects.filter(username="admin").first()
            if admin_user is None:
                admin_user = user_model(username="admin")
            admin_user.set_password(admin_password)
            admin_user.is_active = True
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()

        self.stdout.write(
            self.style.SUCCESS("As duas contas do dashboard foram configuradas.")
        )
