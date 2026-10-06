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

admin_password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin123')
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@polofit.com', admin_password)
    print(f'Superuser admin criado com sucesso (senha definida: {\"personalizada via env\" if os.environ.get(\"DJANGO_ADMIN_PASSWORD\") else \"admin123\"})!')
else:
    # Atualiza a senha se já existir (útil para rotação de credenciais)
    user = User.objects.get(username='admin')
    user.set_password(admin_password)
    user.save()
    print('Superuser admin verificado e senha atualizada.')
"
echo ">>> Build concluído com sucesso!"
