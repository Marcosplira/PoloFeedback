import json
import re
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from django.conf import settings

from .models import Avaliacao


class WhatsAppConfigurationError(ValueError):
    pass


class WhatsAppDeliveryError(Exception):
    def __init__(self, message, retryable):
        super().__init__(message)
        self.retryable = retryable


@dataclass(frozen=True)
class WhatsAppConfig:
    api_version: str
    phone_number_id: str
    access_token: str
    recipient: str
    template_name: str
    template_language: str
    public_base_url: str


def validate_whatsapp_settings():
    if not settings.WHATSAPP_ALERTS_ENABLED:
        raise WhatsAppConfigurationError(
            "Ative WHATSAPP_ALERTS_ENABLED para processar os avisos."
        )

    required = {
        "WHATSAPP_CLOUD_API_VERSION": settings.WHATSAPP_CLOUD_API_VERSION,
        "WHATSAPP_PHONE_NUMBER_ID": settings.WHATSAPP_PHONE_NUMBER_ID,
        "WHATSAPP_ACCESS_TOKEN": settings.WHATSAPP_ACCESS_TOKEN,
        "WHATSAPP_BUSINESS_NUMBER": settings.WHATSAPP_BUSINESS_NUMBER,
        "WHATSAPP_ALERT_RECIPIENT": settings.WHATSAPP_ALERT_RECIPIENT,
        "WHATSAPP_ALERT_TEMPLATE_NAME": settings.WHATSAPP_ALERT_TEMPLATE_NAME,
        "WHATSAPP_ALERT_TEMPLATE_LANGUAGE": (
            settings.WHATSAPP_ALERT_TEMPLATE_LANGUAGE
        ),
        "SITE_PUBLIC_URL": settings.SITE_PUBLIC_URL,
    }
    missing = [name for name, value in required.items() if not value.strip()]
    if missing:
        raise WhatsAppConfigurationError(
            "Configure as variáveis obrigatórias: " + ", ".join(missing)
        )

    if not re.fullmatch(r"v[0-9]+\.[0-9]+", settings.WHATSAPP_CLOUD_API_VERSION):
        raise WhatsAppConfigurationError(
            "WHATSAPP_CLOUD_API_VERSION deve seguir o formato vNN.N."
        )

    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID.strip()
    if not re.fullmatch(r"[0-9]+", phone_number_id):
        raise WhatsAppConfigurationError(
            "WHATSAPP_PHONE_NUMBER_ID deve conter somente dígitos."
        )
    access_token = settings.WHATSAPP_ACCESS_TOKEN.strip()
    if not re.fullmatch(r"[!-~]+", access_token):
        raise WhatsAppConfigurationError(
            "WHATSAPP_ACCESS_TOKEN deve ser um token sem espaços ou quebras de linha."
        )

    phone_values = {
        "WHATSAPP_BUSINESS_NUMBER": settings.WHATSAPP_BUSINESS_NUMBER,
        "WHATSAPP_ALERT_RECIPIENT": settings.WHATSAPP_ALERT_RECIPIENT,
    }
    for name, value in phone_values.items():
        if not re.fullmatch(r"\+?[0-9\s().-]+", value.strip()):
            raise WhatsAppConfigurationError(
                f"{name} deve conter somente dígitos e formatação telefônica."
            )
    business_number = re.sub(
        r"[^0-9]", "", phone_values["WHATSAPP_BUSINESS_NUMBER"]
    )
    recipient = re.sub(r"[^0-9]", "", phone_values["WHATSAPP_ALERT_RECIPIENT"])
    for name, number in (
        ("WHATSAPP_BUSINESS_NUMBER", business_number),
        ("WHATSAPP_ALERT_RECIPIENT", recipient),
    ):
        if not re.fullmatch(r"[0-9]{8,15}", number):
            raise WhatsAppConfigurationError(
                f"{name} deve ser um telefone internacional com 8 a 15 dígitos."
            )
    if business_number == recipient:
        raise WhatsAppConfigurationError(
            "O remetente e o destinatário dos avisos devem ser números distintos."
        )

    template_name = settings.WHATSAPP_ALERT_TEMPLATE_NAME.strip()
    if not re.fullmatch(r"[a-z0-9_]+", template_name):
        raise WhatsAppConfigurationError(
            "WHATSAPP_ALERT_TEMPLATE_NAME deve usar letras minúsculas, "
            "números e sublinhados."
        )

    template_language = settings.WHATSAPP_ALERT_TEMPLATE_LANGUAGE.strip()
    if not re.fullmatch(r"[a-z]{2}_[A-Z]{2}", template_language):
        raise WhatsAppConfigurationError(
            "WHATSAPP_ALERT_TEMPLATE_LANGUAGE deve seguir o formato pt_BR."
        )

    public_base_url = settings.SITE_PUBLIC_URL.strip().rstrip("/")
    parsed_url = urlsplit(public_base_url)
    if (
        parsed_url.scheme != "https"
        or not parsed_url.netloc
        or parsed_url.username
        or parsed_url.password
        or parsed_url.path
        or parsed_url.query
        or parsed_url.fragment
    ):
        raise WhatsAppConfigurationError(
            "SITE_PUBLIC_URL deve ser a origem pública HTTPS, sem caminho."
        )

    return WhatsAppConfig(
        api_version=settings.WHATSAPP_CLOUD_API_VERSION.strip(),
        phone_number_id=phone_number_id,
        access_token=access_token,
        recipient=recipient,
        template_name=template_name,
        template_language=template_language,
        public_base_url=public_base_url,
    )


def _template_parameters(avaliacao, config):
    categorias = avaliacao.categorias or [avaliacao.categoria]
    categoria_labels = dict(Avaliacao.CATEGORIA_CHOICES)
    categoria = ", ".join(
        categoria_labels.get(item, item) for item in categorias
    )
    aula_label = dict(Avaliacao.AULA_COLETIVA_CHOICES).get(
        avaliacao.aula_coletiva,
        "Não se aplica",
    )
    comentario = avaliacao.comentario.strip() or "Sem comentário"
    if len(comentario) > 900:
        comentario = comentario[:900].rstrip() + " [truncado]"

    values = [
        f"#{avaliacao.pk}",
        str(avaliacao.nota),
        categoria,
        aula_label,
        avaliacao.nome_respondente.strip() or "Anônimo",
        comentario,
        f"{config.public_base_url}/dashboard/",
    ]
    return [
        {"type": "text", "text": value}
        for value in values
    ]


def send_whatsapp_alert(avaliacao, config=None):
    config = config or validate_whatsapp_settings()
    url = (
        f"https://graph.facebook.com/{config.api_version}/"
        f"{config.phone_number_id}/messages"
    )
    payload = {
        "messaging_product": "whatsapp",
        "to": config.recipient,
        "type": "template",
        "template": {
            "name": config.template_name,
            "language": {"code": config.template_language},
            "components": [
                {
                    "type": "body",
                    "parameters": _template_parameters(avaliacao, config),
                }
            ],
        },
    }
    request = Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            response_data = json.loads(response.read(65536))
    except HTTPError as error:
        retryable = error.code in {408, 429} or error.code >= 500
        error.close()
        raise WhatsAppDeliveryError(
            f"A API do WhatsApp respondeu com HTTP {error.code}.",
            retryable=retryable,
        ) from None
    except (URLError, TimeoutError, OSError):
        raise WhatsAppDeliveryError(
            "Falha temporária de comunicação com a API do WhatsApp.",
            retryable=True,
        ) from None
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise WhatsAppDeliveryError(
            "A API do WhatsApp retornou uma resposta inválida.",
            retryable=False,
        ) from None

    if not isinstance(response_data, dict):
        raise WhatsAppDeliveryError(
            "A API do WhatsApp retornou uma resposta inválida.",
            retryable=False,
        )
    messages = response_data.get("messages", [])
    if (
        not isinstance(messages, list)
        or not messages
        or not isinstance(messages[0], dict)
        or not isinstance(messages[0].get("id"), str)
        or not messages[0]["id"]
    ):
        raise WhatsAppDeliveryError(
            "A API não confirmou o recebimento do aviso.",
            retryable=False,
        )
    return messages[0]["id"]
