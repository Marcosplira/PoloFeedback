# 🏋️ Polo Feedback — Polo Fit

Sistema moderno de coleta, análise e gestão de avaliações e satisfação dos alunos da **Academia Polo Fit**.

---

## 📌 Visão Geral

O **Polo Feedback** foi desenvolvido para aproximar os alunos da gestão da academia, permitindo:
- **Alunos:** Avaliar a experiência rapidamente via celular escaneando um QR Code nos totens ou setores da academia.
- **Gerentes e Supervisores:** Acompanhar métricas de satisfação em tempo real, filtrar feedbacks, gerenciar pendências de atendimento, visualizar rankings dos instrutores e gerar relatórios executivos instantâneos com Inteligência Artificial (**Google Gemini**).

---

## 🚀 Principais Funcionalidades

1. **📱 Formulário de Avaliação Mobile-First (`/avaliar/`):**
   - Rápido, intuitivo e responsivo.
   - Avaliação por estrelas (1 a 5).
   - Múltiplas categorias (Atendimento, Limpeza, Equipamentos, Professores, Estrutura, Geral).
   - Tipos de feedback (Elogio 👍, Sugestão 💡, Reclamação ⚠️).
   - Opção de selecionar o colaborador/instrutor avaliado.
   - Retenção inteligente de dados em caso de avisos de validação.

2. **📊 Dashboard Gerencial em Tempo Real (`/dashboard/`):**
   - Indicadores-chave (KPIs): Total de avaliações, média de notas, total de elogios e reclamações.
   - Gráficos interativos (Chart.js) por Categoria e por Distribuição de Notas.
   - Filtros dinâmicos por categoria, tipo de feedback, status e colaborador.
   - Tabela detalhada com modal interativo e alteração de status em 1 clique (*Pendente*, *Em Análise*, *Resolvida* com registro de quem resolveu).
   - **Ranking de Funcionários:** Destaque para instrutores mais elogiados e suas médias.

3. **🤖 Análise Inteligente com IA (`/ia/analisar/` e chat em `/ia/chat/`):**
   - Integração com a API Google Gemini (`gemini-1.5-flash`).
   - Gera um resumo executivo com pontos fortes, alertas operacionais e recomendações práticas para a gerência com base nos dados reais coletados.
   - **Fallback inteligente:** funciona mesmo sem a chave da API, gerando análise automaticamente a partir dos dados do banco.

4. **🖨️ Gerador de QR Code com Impressão de Cartaz (`/qrcode/`):**
   - Permite criar QR Codes para qualquer setor ou unidade (ex: *Musculação*, *Recepção*, *Polo Centro*).
   - Suporte inteligente para IP local na rede Wi-Fi, permitindo testes práticos em smartphones.
   - Layout preparado para impressão direta em cartazes para totens e balcões.

5. **🛡️ Painel Administrativo Completo (`/admin/`):**
   - Gestão de colaboradores com fotos e status ativo.
   - Gestão e auditoria de avaliações.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.12, Django 6.1.1 |
| **Frontend** | HTML5, Tailwind CSS (CDN), JavaScript, Chart.js |
| **Banco de Dados** | SQLite (Desenvolvimento local) / PostgreSQL (Produção / Docker) |
| **Inteligência Artificial** | Google Gemini API (`gemini-1.5-flash`) |
| **Infraestrutura** | Gunicorn, Whitenoise, Docker, Docker Compose |
| **Hospedagem** | Render.com (configuração pronta) |

---

## 💻 Como Rodar o Projeto Localmente

### 1. Pré-requisitos
- Python 3.12+ instalado
- Git

### 2. Clonar e ativar o Ambiente Virtual

```powershell
# Ative o ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

Se não tiver o `venv` criado ainda:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente (opcional)

Copie o arquivo de exemplo e ajuste os valores:
```powershell
copy .env.example .env
```

> Para desenvolvimento local, o projeto funciona sem configurar nada — usa SQLite e fallback da IA.

### 5. Executar Migrações do Banco

```powershell
python manage.py migrate
```

### 6. Criar superusuário para o Dashboard (primeira vez)

```powershell
python manage.py createsuperuser
```

### 7. Iniciar o Servidor de Desenvolvimento

```powershell
python manage.py runserver
```

Para liberar o acesso a smartphones na mesma rede Wi-Fi:
```powershell
python manage.py runserver 0.0.0.0:8000
```

Acesse no navegador:
- **Avaliação do Aluno:** [http://localhost:8000/](http://localhost:8000/)
- **Dashboard Gerencial:** [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)
- **Gerador de QR Code:** [http://localhost:8000/qrcode/](http://localhost:8000/qrcode/)
- **Administração Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🐳 Como Rodar com Docker

Para subir a aplicação completa com banco PostgreSQL em containers:

### 1. Crie o arquivo `.env` a partir do exemplo:
```bash
cp .env.example .env
# Edite o .env e defina pelo menos: SECRET_KEY, DB_PASSWORD, DJANGO_ADMIN_PASSWORD
```

### 2. Suba os containers:
```bash
docker compose up --build -d
```

O sistema estará disponível em [http://localhost:8000](http://localhost:8000).

### 3. Parar os containers:
```bash
docker compose down
```

---

## 🧪 Executando os Testes Automatizados

O projeto possui suíte de testes cobrindo modelos, validações, autenticação e fluxos gerenciais:

```powershell
python manage.py test
```

> ✅ 10 testes — todos passando.

---

## ☁️ Deploy no Render.com

O arquivo `render.yaml` contém a configuração completa de deploy.

### Configuração necessária no painel do Render:
Após o primeiro deploy, vá em **Environment → Environment Variables** e adicione:

| Variável | Descrição |
| :--- | :--- |
| `GEMINI_API_KEY` | Chave da API Google Gemini (obtenha em [aistudio.google.com](https://aistudio.google.com/app/apikey)) |
| `DJANGO_ADMIN_PASSWORD` | Senha do usuário `admin` para acessar o dashboard |

> ⚠️ **IMPORTANTE:** Nunca coloque senhas ou chaves de API diretamente no arquivo `render.yaml`. Use sempre o painel de variáveis de ambiente.

---

## 🔐 Variáveis de Ambiente Suportadas

| Variável | Padrão | Descrição |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(erro em produção se não definida)* | Chave secreta do Django |
| `DEBUG` | `True` | Modo de depuração (`True` ou `False`) |
| `ALLOWED_HOSTS` | `*` em debug | Hosts permitidos separados por vírgula |
| `DATABASE_URL` | *(SQLite local)* | URL do banco PostgreSQL em produção |
| `GEMINI_API_KEY` | *(vazio — usa fallback local)* | Chave da API Gemini para IA |
| `GEMINI_MODEL` | `gemini-1.5-flash` | Modelo Gemini utilizado |
| `DJANGO_ADMIN_PASSWORD` | *(não cria admin se vazio)* | Senha do superusuário `admin` |

---

## 📁 Estrutura do Projeto

```
PoloFeedback/
├── feedback/                   # App principal
│   ├── migrations/             # Migrações do banco
│   ├── static/feedback/        # Imagens e assets estáticos
│   ├── templates/
│   │   ├── feedback/           # Templates: avaliar, dashboard, qrcode, sucesso
│   │   └── registration/       # Template de login
│   ├── admin.py                # Configuração do painel admin
│   ├── models.py               # Modelos: Funcionario, Avaliacao
│   ├── tests.py                # Testes automatizados (10 testes)
│   └── views.py                # Views: avaliar, dashboard, qrcode, ia
├── polofeedback/               # Configuração do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example                # Exemplo de variáveis de ambiente
├── .gitignore
├── build.sh                    # Script de build para o Render
├── docker-compose.yml          # Orquestração Docker local
├── Dockerfile                  # Imagem Docker da aplicação
├── manage.py
├── render.yaml                 # Configuração de deploy no Render.com
└── requirements.txt            # Dependências Python
```

---

## 🔎 Auditoria e melhorias prioritárias

O projeto já está funcional e com boa base para evoluir. A validação atual foi feita com testes automatizados e o sistema está em estado estável.

### Status verificado
- 10 testes executados com sucesso
- sistema de avaliação funcional
- dashboard operacional com filtros e rankings
- IA com fallback local
- QR Code funcionando para localizações

### Principais melhorias recomendadas
1. Atualização automática em tempo real
2. Sincronização offline/on-line para mobile
3. QR Code por setor, unidade e local específico
4. IA para resumo executivo e chatbot do gerente
5. App mobile profissional e branding premium
6. Dashboard executivo com relatórios e alertas
7. Separação de regras de negócio em services e módulos

### Documentação complementar
- [docs/ANALISE_AUDITORIA.md](docs/ANALISE_AUDITORIA.md)
- [docs/ROADMAP_PROFISSIONAL.md](docs/ROADMAP_PROFISSIONAL.md)
- [docs/ENTREGAVEL_GERENTE.md](docs/ENTREGAVEL_GERENTE.md)
- [docs/SLIDE_APRESENTACAO.html](docs/SLIDE_APRESENTACAO.html)

---

*© 2026 Polo Fit — Sua opinião faz a diferença.*
