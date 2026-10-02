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

# Instala dependências do sistema necessárias para psycopg2 e pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python primeiro (aproveita cache do Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o restante do projeto
COPY . .

# Cria as pastas de media e staticfiles com permissões corretas
RUN mkdir -p /app/media /app/staticfiles

# Coleta os arquivos estáticos (requer SECRET_KEY mas não precisa do DB)
RUN SECRET_KEY="collectstatic-temp-key" DEBUG="False" python manage.py collectstatic --noinput

# Porta que o gunicorn vai expor
EXPOSE 8000

# Comando de inicialização: aplica migrations e sobe o servidor com configurações de produção
CMD ["sh", "-c", "python manage.py migrate && gunicorn polofeedback.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 60 --log-level info --access-logfile -"]
