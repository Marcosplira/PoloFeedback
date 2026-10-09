import os

ROOT = r"C:\Users\ACER\Downloads\PoloFeedback-main\PoloFeedback-main"
os.chdir(ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "polofeedback.settings")

import django

django.setup()

from django.test import Client
from django.contrib.auth.models import User
from feedback.models import Funcionario, Avaliacao

User.objects.all().delete()
Funcionario.objects.all().delete()
Avaliacao.objects.all().delete()

user = User.objects.create_user(username='gerente_teste', password='senha_segura_123')
func = Funcionario.objects.create(nome='Mariana Instrutora', cargo='Instrutora de Pilates', ativo=True)
Avaliacao.objects.create(
    categoria='estrutura',
    categorias=['estrutura'],
    nota=5,
    tipo_feedback='elogio',
    tipos_feedback=['elogio'],
    comentario='Ambiente climatizado e agradável.',
    funcionario=func,
)

client = Client()
client.force_login(user)
response = client.get('/dashboard/')
print('STATUS', response.status_code)
print('TEMPLATE', getattr(response, 'template_name', None))
print('CONTENT_TYPE', response.get('Content-Type'))
print('HAS_CONTEXT', bool(getattr(response, 'context', None)))
if response.context is not None:
    print('CONTEXT_KEYS', list(response.context.keys())[:20])
    print('MEDIA', response.context.get('media_notas'))
    print('TOTAL', response.context.get('total_avaliacoes'))
    print('RENDERED_SNIPPET', response.content.decode('utf-8', errors='replace')[:800])
