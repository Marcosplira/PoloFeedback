"""
Módulo de auditoria para registro de acessos e ações sensíveis.
"""
from django.utils import timezone
from .models import AuditoriaAcesso


def registrar_acesso(
    request,
    acao,
    sucesso=True,
    detalhes=None,
    usuario=None
):
    """
    Registra uma ação de auditoria.

    Args:
        request: Objeto HttpRequest
        acao: Tipo de ação (login, logout, criar_avaliacao, etc.)
        sucesso: Se a ação foi bem-sucedida
        detalhes: Dicionário com detalhes adicionais
        usuario: Objeto User (se None, usa request.user)
    """
    if not usuario:
        usuario = getattr(request, 'user', None)

    # Não registrar ações de usuários anônimos para login falho
    # a menos que seja especificamente um registro de tentativa
    if not usuario or not usuario.is_authenticated:
        if acao != "login":
            return

    ip_address = None
    user_agent = ""

    if request:
        # Obter IP do cliente
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # Obter User Agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]  # Limitar tamanho

    AuditoriaAcesso.objects.create(
        usuario=usuario if usuario and usuario.is_authenticated else None,
        acao=acao,
        ip_address=ip_address,
        user_agent=user_agent,
        detalhes=detalhes or {},
        sucesso=sucesso,
        timestamp=timezone.now()
    )


def get_client_ip(request):
    """
    Obtém o endereço IP do cliente de forma segura.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
