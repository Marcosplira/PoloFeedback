# ===================================================
# Dockerfile — PoloFeedback (Django)
# ===================================================

# Imagem base Python leve e segura
FROM python:3.12-slim

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala somente a biblioteca de runtime necessária pelo driver PostgreSQL.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python primeiro (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Executa a aplicação sem privilégios de root e prepara os diretórios persistentes.
RUN groupadd --system app && useradd --system --gid app --home-dir /app app \
    && mkdir -p /app/media /app/staticfiles \
    && chown -R app:app /app/media /app/staticfiles \
    && chown -R app:app /app

# Coleta os arquivos estáticos (requer SECRET_KEY mas não precisa do DB)
RUN SECRET_KEY="collectstatic-temp-key" DEBUG="False" \
    DATABASE_URL="postgres://build:build@127.0.0.1:5432/build" \
    python manage.py collectstatic --noinput --skip-checks

USER app

# Porta que o gunicorn vai expor
EXPOSE 8000

# Aplica migrações no início e substitui o shell pelo Gunicorn para receber sinais.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py setup_dashboard_users && exec gunicorn polofeedback.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60 --log-level info --access-logfile -"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)" || exit 1
