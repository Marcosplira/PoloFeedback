# Documentação Técnica - Polo Feedback

## Índice
1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Modelos de Dados](#modelos-de-dados)
6. [Views e URLs](#views-e-urls)
7. [Integração com IA (Google Gemini)](#integração-com-ia-google-gemini)
8. [Configuração de Ambiente](#configuração-de-ambiente)
9. [Deploy](#deploy)
10. [Segurança](#segurança)
11. [Testes](#testes)
12. [Troubleshooting](#troubleshooting)

---

## Visão Geral

O **Polo Feedback** é um sistema profissional de gestão de feedback para academias, desenvolvido em Django. O sistema permite:

- Coleta de avaliações dos alunos através de QR Codes
- Enquetes sobre preferências de aulas e espaços
- Painel gerencial com métricas e dashboards
- Sistema de treinos por QR Code
- Análise inteligente com Google Gemini
- Gestão de equipe e funcionários

### Características Principais

- **Framework**: Django 5.0+
- **Banco de Dados**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Frontend**: Django Templates com CSS customizado + Tailwind CSS
- **IA**: Google Gemini para análise de feedbacks
- **Deploy**: Docker Compose + Render (cloud)
- **PWA**: Progressive Web App para instalação em dispositivos móveis

---

## Arquitetura do Sistema

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Avaliação   │  │   Enquete    │  │   Dashboard  │      │
│  │  (Mobile)    │  │  (Pesquisa)  │  │  (Gerencial) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Django Backend                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Views     │  │    Models    │  │    Admin     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Banco de Dados                            │
│              PostgreSQL / SQLite                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Serviços Externos                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Google Gemini│  │   QR Code    │  │   PWA Service│      │
│  │      (IA)     │  │  Generation  │  │   (Offline)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Padrões de Projeto

- **MVC**: Model-View-Controller (Django: Model-View-Template)
- **Middleware**: Custom middleware para tratamento de erros de banco
- **Decorators**: `@staff_required` para proteção de views administrativas
- **Signals**: Para eventos de criação/atualização de dados

---

## Tecnologias Utilizadas

### Backend

- **Python 3.12**: Linguagem principal
- **Django 5.0+**: Framework web
- **PostgreSQL**: Banco de dados relacional (produção)
- **SQLite**: Banco de dados (desenvolvimento)
- **Gunicorn**: Servidor WSGI (produção)
- **WhiteNoise**: Servidor de arquivos estáticos

### Frontend

- **Django Templates**: Motor de templates
- **Tailwind CSS**: Framework CSS (via CDN)
- **Inter (Google Fonts)**: Tipografia
- **Chart.js**: Gráficos no dashboard

### Integrações

- **Google Gemini API**: Análise de feedbacks com IA
- **qrcode (Python)**: Geração de QR Codes
- **PWA Service Worker**: Funcionalidade offline

### DevOps

- **Docker**: Containerização
- **Docker Compose**: Orquestração de containers
- **Render**: Plataforma de deploy (cloud)
- **Locaweb**: Servidor VPS (alternativa)

---

## Estrutura do Projeto

```
PoloFeedback/
├── feedback/                  # App principal
│   ├── __init__.py
│   ├── admin.py             # Configuração do admin Django
│   ├── apps.py
│   ├── middleware.py        # Middleware customizado
│   ├── models.py           # Modelos de dados
│   ├── tests.py            # Testes automatizados
│   ├── urls.py             # URLs do app
│   └── views.py            # Views e lógica de negócio
│
├── feedback/templates/      # Templates HTML
│   ├── feedback/
│   │   ├── avaliar.html          # Página de avaliação
│   │   ├── dashboard.html        # Painel gerencial
│   │   ├── enquete.html          # Enquete de pesquisas
│   │   ├── inicio.html           # Homepage
│   │   ├── rodape.html           # Footer compartilhado
│   │   ├── qrcode.html           # Geração de QR Codes
│   │   ├── configuracao_sistema.html  # Configurações
│   │   ├── pwa_meta.html         # Meta tags PWA
│   │   ├── pwa_install.html      # Página de instalação PWA
│   │   └── ...                   # Outros templates
│   └── registration/             # Templates de autenticação
│
├── feedback/static/         # Arquivos estáticos
│   └── feedback/
│       ├── LOGO.png
│       ├── academia1.png
│       ├── academia2.png
│       └── planos-polofit.jpg
│
├── polofeedback/            # Configuração do projeto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Configurações principais
│   ├── urls.py              # URLs raiz
│   └── wsgi.py
│
├── docs/                    # Documentação
│   ├── DOCUMENTACAO_TECNICA_COMPLETA.md
│   ├── GUIA_DO_USUARIO.md
│   └── DEPLOY_VPS.md
│
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Orquestração Docker
├── render.yaml              # Configuração Render
├── requirements.txt         # Dependências Python
├── manage.py                # CLI Django
└── README.md                # Documentação geral
```

---

## Modelos de Dados

### Modelos Principais

#### 1. Funcionario
Representa os funcionários/colaboradores da academia.

```python
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    foto_url = models.URLField(blank=True, null=True)
    funcoes = models.ManyToManyField(Funcao)
    # ... outros campos
```

#### 2. Avaliacao
Avaliações dos alunos sobre a academia.

```python
class Avaliacao(models.Model):
    CATEGORIA_CHOICES = [
        ('atendimento', 'Atendimento'),
        ('professores', 'Professores'),
        ('equipamentos', 'Equipamentos'),
        ('limpeza', 'Limpeza'),
        ('estrutura', 'Estrutura'),
        ('geral', 'Geral'),
    ]
    
    TIPO_FEEDBACK_CHOICES = [
        ('elogio', 'Elogio'),
        ('reclamacao', 'Reclamação'),
        ('sugestao', 'Sugestão'),
    ]
    
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em análise'),
        ('resolvida', 'Resolvida'),
    ]
    
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    tipo_feedback = models.CharField(max_length=20, choices=TIPO_FEEDBACK_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    nota = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    funcionarios = models.ManyToManyField(Funcionario, related_name='avaliacoes')
    data_criacao = models.DateTimeField(auto_now_add=True)
    # ... outros campos
```

#### 3. RespostaEnquete
Respostas da enquete de preferências dos alunos.

```python
class RespostaEnquete(models.Model):
    participa_aulas = models.CharField(max_length=50, blank=True)
    aulas_favoritas = models.JSONField(default=list, blank=True)
    novo_espaco = models.JSONField(default=list, blank=True)
    aula_melhoria = models.JSONField(default=list, blank=True)
    sugestao_valor = models.TextField(blank=True)
    elogio_colaborador = models.TextField(blank=True)
    aula_falta = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
```

#### 4. Equipamento
Equipamentos da academia para o sistema de treinos.

```python
class Equipamento(models.Model):
    identificador_qr = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=100, blank=True)
    instrucoes = models.TextField(blank=True)
    observacoes_seguranca = models.TextField(blank=True)
```

#### 5. PlanoTreino e ItemPlanoTreino
Planos de treino para os alunos.

```python
class PlanoTreino(models.Model):
    nome = models.CharField(max_length=100)
    observacoes = models.TextField(blank=True)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

class ItemPlanoTreino(models.Model):
    plano = models.ForeignKey(PlanoTreino, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    series = models.IntegerField()
    repeticoes = models.CharField(max_length=50)
    descanso_segundos = models.IntegerField(default=60)
    carga = models.CharField(max_length=50, blank=True)
```

---

## Views e URLs

### Views Principais

#### Avaliação
- `avaliar()`: Formulário de avaliação (múltiplos passos)
- `processar_avaliacao()`: Processamento do formulário

#### Enquete
- `enquete()`: Formulário de enquete (múltiplos passos)
- `processar_enquete()`: Processamento da enquete

#### Dashboard
- `dashboard()`: Painel gerencial com métricas
- `atualizar_status_avaliacao()`: Atualização de status via POST

#### IA
- `ia_analisar()`: Análise de feedbacks com Gemini
- `ia_chat()`: Chat conversacional com IA

#### Treinos
- `gestao_treinos()`: Gestão de planos de treino
- `form_plano_treino()`: Criação/edição de planos
- `meus_treinos()`: Visualização dos treinos do aluno
- `treino_equipamento()`: Instruções do equipamento via QR

#### QR Codes
- `gerar_qrcode()`: Geração de QR Codes de avaliação
- `qrcodes_treinos()`: Geração de QR Codes de treinos

### URLs

```python
# Avaliação
path('avaliar/', views.avaliar, name='avaliar')

# Enquete
path('enquete/', views.enquete, name='enquete')

# Dashboard
path('dashboard/', views.dashboard, name='dashboard')

# IA
path('ia/analisar/', views.ia_analisar, name='ia_analisar')
path('ia/chat/', views.ia_chat, name='ia_chat')

# Treinos
path('treinos/', views.gestao_treinos, name='gestao_treinos')
path('treinos/plano/<int:plano_id>/', views.form_plano_treino, name='form_plano_treino')
path('meus-treinos/', views.meus_treinos, name='meus_treinos')
path('treino/<str:qr_id>/', views.treino_equipamento, name='treino_equipamento')

# QR Codes
path('qrcode/', views.gerar_qrcode, name='gerar_qrcode')
path('qrcodes-treinos/', views.qrcodes_treinos, name='qrcodes_treinos')

# Configuração
path('configuracao/', views.configuracao_sistema, name='configuracao_sistema')
```

---

## Integração com IA (Google Gemini)

### Configuração

A API do Google Gemini é configurada via variável de ambiente:

```python
# settings.py
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
```

### Funcionalidades

#### 1. Análise de Avaliações

A view `ia_analisar()` coleta dados gerenciais e envia para o Gemini:

```python
@staff_required(permission="feedback.view_avaliacao")
def ia_analisar(request):
    dados = _coletar_dados_gerenciais_ia()
    
    system_instruction = (
        "Você é o assistente executivo da Academia Polo Fit. "
        "Gere em português brasileiro um resumo gerencial objetivo "
        "com pontos fortes, pontos de atenção e ações práticas."
    )
    
    resposta = _solicitar_resposta_gemini(
        system_instruction,
        [{"role": "user", "parts": [{"text": prompt}]}],
    )
    
    return JsonResponse({"analise": resposta})
```

#### 2. Chat Conversacional

A view `ia_chat()` permite perguntas em linguagem natural:

```python
@staff_required(permission="feedback.view_avaliacao")
def ia_chat(request):
    pergunta = request.GET.get('pergunta', '')
    dados = _coletar_dados_gerenciais_ia()
    
    # Tenta resposta com Gemini
    resposta_gemini = _solicitar_resposta_gemini(...)
    
    # Fallback para resposta local
    if not resposta_gemini:
        resposta = _gerar_resposta_conversacional_local(pergunta, dados)
    
    return JsonResponse({"resposta": resposta})
```

### Uso no Dashboard

O dashboard inclui um botão "Gerar resumo" que chama a API de IA:

```javascript
const response = await fetch('/ia/analisar/', {
    method: 'GET',
    headers: { 'Accept': 'application/json' }
});
const data = await response.json();
document.getElementById('resumo-ia-conteudo').innerHTML = data.analise;
```

---

## Configuração de Ambiente

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=polofeedback.onrender.com,app.polofitacademias.com.br

# Banco de Dados (Produção)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Google Gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash

# Senhas (Use variáveis de ambiente, NÃO hardcode!)
DASHBOARD_MANAGER_PASSWORD=secure-password
DASHBOARD_OWNER_PASSWORD=secure-password
ADMIN_PASSWORD=secure-password
```

### Configuração de Desenvolvimento

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar banco (SQLite)
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

### Configuração de Produção

```bash
# Usar PostgreSQL
export DATABASE_URL=postgresql://...

# Migrar banco
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic

# Rodar com Gunicorn
gunicorn polofeedback.wsgi:application
```

---

## Deploy

### Opção 1: Render (Cloud)

O arquivo `render.yaml` configura o deploy no Render:

```yaml
services:
  - type: web
    name: polofeedback
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn polofeedback.wsgi:application
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: polofeedback-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: GEMINI_API_KEY
        sync: false
```

### Opção 2: Docker Compose

Usar `docker-compose.yml` para deploy local ou VPS:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: polofeedback
      POSTGRES_USER: polofit
      POSTGRES_PASSWORD: secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn polofeedback.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://polofit:secure-password@db:5432/polofeedback
      - SECRET_KEY=your-secret-key

volumes:
  postgres_data:
```

Comandos:

```bash
# Construir e iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Opção 3: VPS (Locaweb/Outros)

Veja o guia completo em `docs/DEPLOY_VPS.md`.

---

## Segurança

### Boas Práticas Implementadas

1. **Variáveis de Ambiente**: Senhas e chaves nunca no código
2. **HTTPS**: SSL em produção (SECURE_SSL_REDIRECT=True)
3. **Cookies Seguros**: SECURE_SSL_REDIRECT, CSRF_COOKIE_SECURE
4. **HSTS**: HSTS_INCLUDE_SUBDOMAINS em produção
5. **Autenticação**: `@staff_required` para views administrativas
6. **CSRF**: Proteção CSRF ativada
7. **XSS**: Templates Django escapam HTML por padrão

### Atenção: Senhas Hardcoded

⚠️ **CRÍTICO**: O arquivo `render.yaml` contém senhas hardcoded que devem ser removidas:

```yaml
# NÃO FAÇA ISSO:
envVars:
  - key: DASHBOARD_MANAGER_PASSWORD
    value: PoloFitGerente2026!
```

**Correção**:

```yaml
# FAÇA ISSO:
envVars:
  - key: DASHBOARD_MANAGER_PASSWORD
    sync: false  # Definir manualmente no painel do Render
```

### Permissões

- Usuários com `is_staff=True` podem acessar o dashboard
- Permissões granulares via Django Admin
- Views protegidas com `@staff_required(permission="feedback.view_avaliacao")`

---

## Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test feedback.tests.TestAvaliacao

# Com verbosidade
python manage.py test --verbosity=2
```

### Estrutura de Testes

O arquivo `tests.py` contém:

- Testes de views (avaliar, enquete, dashboard)
- Testes de modelos
- Testes de middleware
- Testes de autenticação
- Testes de IA (mock)

### Exemplo de Teste

```python
def test_inicio_carrega_template_correto(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'feedback/inicio.html')
```

---

## Troubleshooting

### Erro: "no such table"

**Causa**: Migrações não aplicadas

**Solução**:
```bash
python manage.py migrate
```

### Erro: "SECRET_KEY not set"

**Causa**: Variável de ambiente não configurada

**Solução**:
```bash
export SECRET_KEY=your-secret-key
# Ou adicionar ao .env
```

### Erro: Gemini API falha

**Causa**: API key inválida ou quota excedida

**Solução**:
- Verificar `GEMINI_API_KEY` no .env
- Verificar quota no Google Cloud Console
- O sistema usa fallback local se Gemini falhar

### Erro: Static files não carregam

**Causa**: WhiteNoise não configurado ou collectstatic não executado

**Solução**:
```bash
python manage.py collectstatic --noinput
```

### Performance lenta

**Causas**:
- N+1 queries
- Falta de índices
- Banco não otimizado

**Soluções**:
- Usar `select_related()` e `prefetch_related()`
- Adicionar índices no models.py
- Usar cache (Redis/Django cache)

---

## Suporte

Para dúvidas ou problemas:

- 📧 Email: marcos.paulo@email.com
- 📱 WhatsApp: (83) 98671-9438
- 🌐 Instagram: @polofitacademias

---

**Versão**: 1.0.0  
**Última atualização**: 2026-10-18  
**Desenvolvido por**: Marcos Paulo Santos Lira
