#!/usr/bin/env bash
# =============================================================
# build.sh — Script de build para hospedagem (ex: Render.com)
# Executado automaticamente a cada deploy.
# =============================================================
set -o errexit

echo ">>> Instalando dependências Python..."
pip install -r requirements.txt

echo ">>> Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo ">>> Aplicando migrações do banco de dados..."
python manage.py migrate

# Garante que o usuário admin exista para login imediato do gerente.
# A senha é lida da variável de ambiente DJANGO_ADMIN_PASSWORD.
# Configure essa variável no painel do Render (ou provedor usado).
echo ">>> Verificando superusuário admin..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'polofeedback.settings')
django.setup()
from django.contrib.auth.models import User

admin_password = os.environ.get('DJANGO_ADMIN_PASSWORD', '')
if not admin_password:
    print('AVISO: Variável DJANGO_ADMIN_PASSWORD não definida.')
    print('       O usuário admin não será criado/atualizado automaticamente.')
    print('       Configure essa variável de ambiente no painel do Render.')
elif not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@polofit.com', admin_password)
    print('Superuser admin criado com sucesso!')
else:
    # Atualiza a senha se já existir (útil para rotação de credenciais)
    user = User.objects.get(username='admin')
    user.set_password(admin_password)
    user.save()
    print('Superuser admin verificado e senha atualizada.')
"
echo ">>> Build concluído com sucesso!"
