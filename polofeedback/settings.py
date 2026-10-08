"""
Django settings for polofeedback project.

Variáveis de ambiente suportadas:
  SECRET_KEY           — Chave secreta Django (obrigatória em produção)
  DEBUG                — "True" para desenvolvimento, "False" para produção
  ALLOWED_HOSTS        — Hosts separados por vírgula (usado quando DEBUG=False)
  DATABASE_URL         — URL do PostgreSQL (ex: postgres://user:pass@host:5432/db)
  CSRF_TRUSTED_ORIGINS — Origens CSRF separadas por vírgula
  GEMINI_API_KEY       — Chave da API Google Gemini
  GEMINI_MODEL         — Modelo Gemini (padrão: gemini-1.5-flash)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

_secret_key = os.environ.get("SECRET_KEY") or os.environ.get("DJANGO_SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "True") == "True"

if not _secret_key:
    if DEBUG:
        # Somente aceitável em desenvolvimento local
        _secret_key = "django-insecure-dev-only-nao-use-em-producao-troque-pela-env-SECRET_KEY"
    else:
        raise RuntimeError(
            "Variável de ambiente SECRET_KEY não definida. "
            "Configure SECRET_KEY no ambiente de produção."
        )

SECRET_KEY = _secret_key



ALLOWED_HOSTS = (
    ["*"]
    if DEBUG
    else [
        "127.0.0.1",
        "localhost",
        "0.0.0.0",
        ".onrender.com",
        ".render.com",
        "192.168.102.114",
        "192.168.3.17",
    ]
    + [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]
)

# Origens confiáveis para CSRF em produção (Render / Docker / proxy reverso)
_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        "https://*.onrender.com",
        "https://*.render.com",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "feedback",
]

# Middleware — whitenoise só em produção
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
]
if not DEBUG:
    MIDDLEWARE += ["whitenoise.middleware.WhiteNoiseMiddleware"]
MIDDLEWARE += [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "feedback.middleware.DatabaseErrorPageMiddleware",
]

ROOT_URLCONF = "polofeedback.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "polofeedback.wsgi.application"

# Banco de dados — usa DATABASE_URL se disponível (Docker/Railway), senão SQLite local
_db_url = os.environ.get("DATABASE_URL", "")
if _db_url:
    from urllib.parse import parse_qs, unquote, urlparse

    _parsed = urlparse(_db_url)
    if _parsed.scheme not in {"postgres", "postgresql"}:
        raise RuntimeError("DATABASE_URL deve apontar para um banco PostgreSQL.")

    _database_name = unquote(_parsed.path.lstrip("/"))
    if not _database_name:
        raise RuntimeError("DATABASE_URL precisa informar o nome do banco PostgreSQL.")

    _query_params = parse_qs(_parsed.query)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": _database_name,
            "USER": unquote(_parsed.username or ""),
            "PASSWORD": unquote(_parsed.password or ""),
            "HOST": _parsed.hostname,
            "PORT": _parsed.port or 5432,
            "OPTIONS": {
                "sslmode": _query_params.get("sslmode", ["require"])[0],
            },
        }
    }
else:
    if not DEBUG:
        raise RuntimeError(
            "DATABASE_URL não definida. Configure um banco PostgreSQL "
            "persistente antes de iniciar em produção."
        )
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Whitenoise para servir static em produção (só quando DEBUG=False)
if not DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# Media files (fotos dos funcionários)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"

# Configurações de segurança (ativas apenas em produção)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "same-origin"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "Lax"
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# Modelo padrão: gemini-1.5-flash (rápido, barato, amplamente disponível)
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
