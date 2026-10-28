"""
Middleware de segurança para validações e proteções adicionais.
"""
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils import timezone
from .auditoria import registrar_acesso


class SecurityMiddleware:
    """
    Middleware para adicionar camadas extras de segurança.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Adicionar headers de segurança
        response = self.get_response(request)

        # Header de segurança contra clickjacking
        response['X-Frame-Options'] = 'DENY'

        # Header de segurança contra MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # Header de segurança XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy (ex: desabilitar geolocalização)
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        return response


class AuditoriaLoginMiddleware:
    """
    Middleware para registrar tentativas de login e logout.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar se é uma requisição de login
        path = request.path

        # Registrar login bem-sucedido (após autenticação)
        if request.user.is_authenticated and path == '/dashboard/':
            # Verificar se há um indicador de login recente na sessão
            if not request.session.get('login_registrado'):
                registrar_acesso(
                    request,
                    acao='login',
                    sucesso=True,
                    detalhes={'path': path}
                )
                request.session['login_registrado'] = True

        # Registrar logout
        if path == '/logout/' and request.user.is_authenticated:
            registrar_acesso(
                request,
                acao='logout',
                sucesso=True,
                usuario=request.user
            )

        return self.get_response(request)


class RateLimitMiddleware:
    """
    Middleware básico de rate limiting para prevenir abuso.
    Em produção, usar Redis ou similar para rate limiting distribuído.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Em memória (não escalável) - substituir por Redis em produção
        self.request_counts = {}

    def __call__(self, request):
        # Obter IP do cliente
        ip = self._get_client_ip(request)

        # Rate limiting apenas para endpoints sensíveis
        sensitive_paths = ['/avaliar/', '/ia/chat/', '/ia/analisar/']

        if any(request.path.startswith(path) for path in sensitive_paths):
            if not self._check_rate_limit(ip):
                from django.http import HttpResponseTooManyRequests
                return HttpResponseTooManyRequests(
                    "Muitas requisições. Tente novamente em alguns minutos."
                )

        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _check_rate_limit(self, ip):
        """
        Verifica se o IP excedeu o limite de requisições.
        Limite: 100 requisições por minuto por IP.
        """
        from collections import defaultdict
        import time

        now = int(time.time())
        minute_ago = now - 60

        # Limpar entradas antigas
        if ip in self.request_counts:
            self.request_counts[ip] = [
                timestamp for timestamp in self.request_counts[ip]
                if timestamp > minute_ago
            ]

        # Verificar limite
        if ip in self.request_counts and len(self.request_counts[ip]) >= 100:
            return False

        # Registrar requisição
        if ip not in self.request_counts:
            self.request_counts[ip] = []
        self.request_counts[ip].append(now)

        return True
