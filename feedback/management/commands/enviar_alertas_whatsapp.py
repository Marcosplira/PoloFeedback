from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db.models import F
from django.utils import timezone

from feedback.models import WhatsAppAviso
from feedback.whatsapp import (
    WhatsAppConfigurationError,
    WhatsAppDeliveryError,
    send_whatsapp_alert,
    validate_whatsapp_settings,
)


MAX_ATTEMPTS = 5
STALE_LOCK_MINUTES = 15


class Command(BaseCommand):
    help = "Envia avisos pendentes de avaliações pela WhatsApp Business Cloud API."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=25)
        parser.add_argument(
            "--retry-failed",
            action="store_true",
            help="Recoloca avisos com falha na fila; pode gerar mensagens duplicadas.",
        )

    def handle(self, *args, **options):
        limit = options["limit"]
        if limit < 1:
            raise CommandError("--limit precisa ser maior que zero.")

        try:
            config = validate_whatsapp_settings()
        except WhatsAppConfigurationError as error:
            raise CommandError(str(error)) from error

        if options["retry_failed"]:
            WhatsAppAviso.objects.filter(status=WhatsAppAviso.STATUS_FALHOU).update(
                status=WhatsAppAviso.STATUS_PENDENTE,
                ultimo_erro="",
                iniciado_em=None,
            )

        stale_before = timezone.now() - timedelta(minutes=STALE_LOCK_MINUTES)
        stale_count = WhatsAppAviso.objects.filter(
            status=WhatsAppAviso.STATUS_ENVIANDO,
            iniciado_em__lt=stale_before,
        ).update(
            status=WhatsAppAviso.STATUS_FALHOU,
            ultimo_erro=(
                "Processo interrompido; confirme a entrega antes de reenviar."
            ),
            iniciado_em=None,
        )
        if stale_count:
            self.stderr.write(
                self.style.WARNING(
                    f"{stale_count} aviso(s) interrompido(s) foram marcados "
                    "para conferência manual."
                )
            )

        pending_ids = list(
            WhatsAppAviso.objects.filter(status=WhatsAppAviso.STATUS_PENDENTE)
            .order_by("criado_em")
            .values_list("pk", flat=True)[:limit]
        )
        sent = 0
        failed = 0

        for aviso_id in pending_ids:
            claimed = WhatsAppAviso.objects.filter(
                pk=aviso_id,
                status=WhatsAppAviso.STATUS_PENDENTE,
            ).update(
                status=WhatsAppAviso.STATUS_ENVIANDO,
                tentativas=F("tentativas") + 1,
                iniciado_em=timezone.now(),
                ultimo_erro="",
            )
            if not claimed:
                continue

            aviso = WhatsAppAviso.objects.select_related("avaliacao").get(
                pk=aviso_id
            )
            try:
                provider_id = send_whatsapp_alert(aviso.avaliacao, config=config)
            except WhatsAppDeliveryError as error:
                terminal = not error.retryable or aviso.tentativas >= MAX_ATTEMPTS
                WhatsAppAviso.objects.filter(pk=aviso_id).update(
                    status=(
                        WhatsAppAviso.STATUS_FALHOU
                        if terminal
                        else WhatsAppAviso.STATUS_PENDENTE
                    ),
                    ultimo_erro=str(error)[:250],
                    iniciado_em=None,
                )
                failed += 1
                self.stderr.write(
                    self.style.ERROR(
                        f"Aviso {aviso_id}: {error} "
                        f"({'falha final' if terminal else 'tentará novamente'})."
                    )
                )
                continue

            WhatsAppAviso.objects.filter(pk=aviso_id).update(
                status=WhatsAppAviso.STATUS_ENVIADO,
                identificador_api=provider_id[:200],
                ultimo_erro="",
                enviado_em=timezone.now(),
                iniciado_em=None,
            )
            sent += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Processamento concluído: {sent} aceito(s) pela API, "
                f"{failed} falha(s), {len(pending_ids)} selecionado(s)."
            )
        )
