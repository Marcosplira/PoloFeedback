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

echo ">>> Build concluído com sucesso!"
