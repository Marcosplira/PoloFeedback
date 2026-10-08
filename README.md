# 🏋️ Polo Feedback — Polo Fit

Sistema moderno de coleta, análise e gestão de avaliações e satisfação dos alunos da **Academia Polo Fit**.

---

## 📌 Visão Geral

O **Polo Feedback** foi desenvolvido para aproximar os alunos da gestão da academia, permitindo:
- **Alunos:** Avaliar a experiência rapidamente via celular escaneando um QR Code nos totens ou setores da academia.
- **Gerentes e Supervisores:** Consultar indicadores ao acessar ou atualizar o painel, filtrar feedbacks, gerenciar pendências, visualizar rankings e usar recursos de IA com **Google Gemini** opcional.

---

## 🚀 Principais Funcionalidades

1. **📱 Formulário de Avaliação Mobile-First (`/avaliar/`):**
   - Rápido, intuitivo e responsivo.
   - Avaliação por estrelas (1 a 5).
   - Múltiplas categorias (Atendimento, Limpeza, Equipamentos, Professores, Estrutura, Geral).
   - Tipos de feedback (Elogio 👍, Sugestão 💡, Reclamação ⚠️).
   - Opção de selecionar o colaborador/instrutor avaliado.
   - Retenção inteligente de dados em caso de avisos de validação.

2. **📊 Dashboard Gerencial (`/dashboard/`):**
   - Indicadores-chave (KPIs): Total de avaliações, média de notas, total de elogios e reclamações.
   - Gráficos interativos (Chart.js) por Categoria e por Distribuição de Notas.
   - Filtros dinâmicos por categoria, tipo de feedback, status e colaborador.
   - Tabela detalhada com modal interativo e alteração de status em 1 clique (*Pendente*, *Em Análise*, *Resolvida* com registro de quem resolveu).
   - **Ranking de Funcionários:** Destaque para instrutores mais elogiados e suas médias.

3. **🤖 Análise Inteligente com IA (`/ia/analisar/` e chat em `/ia/chat/`):**
   - Integração com a API Google Gemini (`gemini-1.5-flash`).
   - Gera um resumo executivo com pontos fortes, alertas operacionais e recomendações práticas para a gerência com base nos dados reais coletados.
   - **Fallback local limitado:** sem a API, algumas respostas são geradas por regras e indicadores do sistema; não equivale a um modelo generativo.

4. **🖨️ Gerador de QR Code com Impressão de Cartaz (`/qrcode/`):**
   - Permite criar QR Codes para qualquer setor ou unidade (ex: *Musculação*, *Recepção*, *Polo Centro*).
   - Suporte inteligente para IP local na rede Wi-Fi, permitindo testes práticos em smartphones.
   - Layout preparado para impressão direta em cartazes para totens e balcões.

5. **📲 PWA instalável em Android e iPhone:**
   - No Android, o navegador pode instalar o Polo Feedback como aplicativo.
   - No iPhone, o Safari orienta a adicionar o sistema à Tela de Início.
   - Sem conexão, mostra uma tela informativa; avaliações e dados privados não são armazenados offline.
   - A instalação exige que o site esteja publicado em um domínio com HTTPS. Esta PWA não é, por si só, um pacote publicado na Play Store ou App Store.

6. **🛡️ Painel Administrativo Completo (`/admin/`):**
   - Gestão de colaboradores com fotos e status ativo.
   - Gestão e auditoria de avaliações.

7. **📲 Acesso rápido, QR Codes e ajuda no painel:**
   - A página inicial oferece QR Codes para avaliação e pesquisa; cada código aponta para o host HTTPS/local usado para abrir o site.
   - A página inicial também exibe a foto da academia e o vídeo de apresentação incorporado do Google Drive. Para os visitantes assistirem, o arquivo precisa permitir acesso a qualquer pessoa com o link.
   - O Dashboard oferece atalhos de diagnóstico de migrações (`/dashboard/configuracao/`) e material para compartilhar (`/dashboard/divulgacao/`).
   - A tela de instalação adiciona o PWA à tela inicial do dispositivo. O aplicativo ainda não está publicado na Google Play Store; não compartilhe links como se houvesse um app listado na loja.

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

Para usar Docker Compose, copie o arquivo de exemplo e preencha os valores:
```powershell
copy .env.example .env
```

O `runserver` local não carrega `.env` automaticamente: sem variáveis de ambiente, usa SQLite local e fallback da IA. Para entrar no dashboard local, crie uma conta com `python manage.py createsuperuser`.

### 5. Executar Migrações do Banco

```powershell
python manage.py migrate
```

As migrações incluem os 16 funcionários informados para a lista de avaliações (Alan Araújo como gerente, Jefferson Tauin como proprietário e os demais como funcionários). Os cargos legados são convertidos em funções selecionáveis e classificados em quatro grupos para a pergunta de elogios da enquete: **Recepção**, **Time de limpeza**, **Estagiários e professores** e **Direção e coordenação**. Jaqueline Lima, Jessica Karla e Micheli Priscila são inicialmente classificadas em **Recepção**; os demais cargos genéricos de funcionário ficam em **Estagiários e professores**. Confirme e ajuste essa classificação conforme a equipe real.

No Django Admin, abra **Funções** para ajustar o grupo de cada cargo e **Funcionários** para associar uma ou mais funções às pessoas. A pergunta 6 da enquete exibe as pessoas agrupadas por esses grupos e permite selecionar várias. Nas perguntas sobre espaços desejados e aulas que precisam de melhorias, os alunos também podem marcar várias opções; a pergunta de frequência das aulas continua aceitando apenas uma resposta.

Se o Admin mostrar `no such table: feedback_equipamento` ou `feedback_planotreino`, pare o servidor e execute `python manage.py migrate` na pasta exata do projeto e com o mesmo ambiente Python usado para iniciar o servidor. Depois, inicie novamente com `python manage.py runserver`. Executar a migração em outra cópia do projeto ou em outro banco não corrige o banco que está servindo a página.

Se o servidor já estiver usando um banco, a tela de erro mostra instruções em vez do traceback amarelo do Django e registra a exceção no log. A tela **Diagnóstico** do Dashboard exibe migrações pendentes quando a conexão com o banco está disponível. Em hospedagem, configure `DATABASE_URL` primeiro; as migrações são aplicadas pelo comando de inicialização.

### 6. Criar o usuário administrador (primeira vez)

```powershell
python manage.py createsuperuser
```

Para configurar as duas contas privadas do dashboard no Render, defina no painel **Environment**:
- `DASHBOARD_MANAGER_USERNAME` (usuário inicial sugerido: `gerente`)
- `DASHBOARD_MANAGER_PASSWORD` (senha privada, forte e não compartilhada)
- `DASHBOARD_OWNER_USERNAME` (usuário inicial sugerido: `marcos`)
- `DASHBOARD_OWNER_PASSWORD` (outra senha privada e forte)

O comando `python manage.py setup_dashboard_users` cria/atualiza as contas com acesso ao dashboard e à gestão de funcionários, sem torná-las superusuárias. O `startCommand` do Render executa as migrações e esse comando antes de iniciar o servidor. Se as variáveis ainda não estiverem preenchidas, o serviço continua no ar e registra um aviso; as contas só são criadas depois de configurar as senhas e reiniciar o serviço. Não há credenciais padrão no código nem na tela de login.

### 7. Cadastrar o MVP de treinos por QR Code

No endereço `/admin/`, entre com o administrador e:

1. Cadastre os alunos como usuários comuns (sem marcar **Equipe** / `is_staff`).
2. Cadastre cada máquina em **Equipamentos de treino**, com instruções e avisos de segurança.
3. Cadastre os exercícios em **Exercícios**, relacionando o equipamento e, se aprovado, um link para vídeo.
4. Crie um **Plano de treino**, selecione o aluno e o professor responsável e inclua os exercícios, séries, repetições, descanso e carga orientada pelo professor.
5. Um membro da equipe imprime os QR Codes em `/treinos/qrs/` ou pelo link **QR Treinos** no Dashboard.

O QR Code identifica apenas o equipamento. O aluno entra com sua conta para ver os exercícios vinculados ao aparelho que pertencem aos próprios planos ativos. Para administrar os planos, o professor deve ter conta da equipe (`is_staff`) e as permissões de visualizar/adicionar/alterar Equipamento, Exercício, Plano de treino e Exercício do plano. A equipe pode imprimir os QR Codes dos aparelhos sem a permissão de visualizar avaliações. O gerente deve ter a permissão `feedback.view_avaliacao` (ou ser superusuário) para abrir Dashboard, IA e QR Codes de avaliação.

O link do QR é montado usando o host acessado pelo membro da equipe. O domínio escolhido para a implantação é `https://app.polofitacademias.com.br`; ele já está incluído nos hosts e origens CSRF permitidos do Render. Para que funcione, configure esse domínio personalizado no serviço do Render e cadastre no provedor DNS os registros que o Render indicar. Depois do deploy, confirme que o domínio abre com HTTPS, cadastre os equipamentos e gere os códigos acessando `/treinos/qrs/` por esse domínio. Não imprima QRs gerados por `localhost` para uso pelos alunos. Vídeos externos precisam ser próprios ou licenciados. Carga, séries e repetições são configuradas pelo professor; o sistema não calcula nem prescreve treino.

### 8. Iniciar o Servidor de Desenvolvimento

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
- **QR Codes dos aparelhos:** [http://localhost:8000/treinos/qrs/](http://localhost:8000/treinos/qrs/) (equipe)
- **Administração Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🐳 Como Rodar com Docker

Para subir a aplicação completa com banco PostgreSQL em containers:

### 1. Crie o arquivo `.env` a partir do exemplo no PowerShell:
```powershell
Copy-Item .env.example .env
```

Preencha `SECRET_KEY` com uma chave Django exclusiva e `DB_PASSWORD` com uma senha forte antes de iniciar. Não use os valores de exemplo em produção.

### 2. Suba os containers:
```bash
docker compose up --build -d
```

O sistema estará disponível em [http://localhost:8000](http://localhost:8000).

Crie uma conta administrativa individual na primeira execução:
```bash
docker compose exec web python manage.py createsuperuser
```

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

Os testes devem ser executados no ambiente Python configurado para o projeto. Consulte a saída do comando para o resultado atual.

---

## ☁️ Deploy no Render.com

O arquivo `render.yaml` configura somente o serviço Web do Django. O banco PostgreSQL deve ser criado separadamente na Neon para não consumir o limite de bancos do Workspace do Render nem compartilhar dados com outros projetos.

### 1. Criar um banco PostgreSQL separado na Neon

1. Crie uma conta em [neon.tech](https://neon.tech/) e crie um projeto PostgreSQL para o Polo Feedback.
2. No painel da Neon, abra os detalhes de conexão do projeto e copie a connection string PostgreSQL (normalmente começa com `postgresql://`).
3. Trate essa URL como uma senha: não a envie em mensagens, não a coloque no GitHub e não a salve em `render.yaml`.

Confira os limites e eventuais cobranças indicados pela Neon antes de criar o banco.

### 2. Configurar o Render

1. No Blueprint `PoloFeedback`, execute **Manual sync** para criar somente o serviço Web. A configuração não tentará criar um banco no Render.
2. Abra o serviço Web `polofeedback` e entre em **Environment**.
3. Adicione `DATABASE_URL` e cole a connection string da Neon. Salve; o Render poderá solicitar um novo deploy.
4. O Django usa SSL (`sslmode=require`) por padrão para o PostgreSQL. O comando de inicialização executa as migrações antes de iniciar o servidor.
5. Após o deploy concluir, abra o **Shell** do serviço e crie seu usuário administrador com `python manage.py createsuperuser`.

Para o domínio personalizado, adicione `app.polofitacademias.com.br` em **Settings → Custom Domains** no serviço Web e configure no provedor do domínio os registros DNS que o Render mostrar. Só gere QR Codes depois que o endereço estiver publicado e abrir com HTTPS.

### Outras variáveis no painel do Render

Se utilizar a IA com Google Gemini, configure `GEMINI_API_KEY` em **Environment**:

| Variável | Descrição |
| :--- | :--- |
| `GEMINI_API_KEY` | Chave da API Google Gemini (obtenha em [aistudio.google.com](https://aistudio.google.com/app/apikey)) |

> ⚠️ **IMPORTANTE:** Nunca coloque senhas ou chaves de API diretamente no repositório ou no arquivo `render.yaml`. Use as variáveis protegidas do provedor.

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

---

## 📁 Estrutura do Projeto

```
PoloFeedback/
├── feedback/                   # App principal
│   ├── migrations/             # Migrações do banco
│   ├── static/feedback/        # Imagens, ícones e arquivos da PWA
│   ├── templates/
│   │   ├── feedback/           # Templates: avaliar, dashboard, qrcode, sucesso
│   │   └── registration/       # Template de login
│   ├── admin.py                # Configuração do painel admin
│   ├── models.py               # Modelos: Funcionario, Avaliacao
│   ├── tests.py                # Testes automatizados (13 testes)
│   └── views.py                # Views: avaliar, dashboard, qrcode, ia
├── polofeedback/               # Configuração do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example                # Exemplo de variáveis de ambiente
├── .dockerignore               # Arquivos excluídos da imagem Docker
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

O projeto contém avaliação por QR Code, painel administrativo, pesquisa de satisfação, suporte de IA e um MVP inicial de treinos por máquina. O módulo de treinos cadastra aparelhos/exercícios, cria planos por aluno, imprime QR Codes e protege o acesso ao plano com autenticação e verificação de titularidade. Antes de um piloto real, ainda é preciso cadastrar conteúdo aprovado, contas e permissões, validar a URL HTTPS usada nos QRs e testar o fluxo com a gerência e os professores. A implantação em nuvem precisa de configuração e validação específicas por ambiente.

### Status verificado
- sistema de avaliação, painel, enquete e QR Code
- assistente de IA condicionado à configuração da API, com fallback local limitado
- segredos e credenciais devem ser gerados e armazenados por ambiente
- imagem Docker deve ser validada com Docker/Compose antes de publicar

### Principais melhorias recomendadas
1. Atualização automática em tempo real
2. Sincronização offline/on-line para mobile
3. QR Code por setor, unidade e local específico
4. IA para resumo executivo e chatbot do gerente
5. App mobile profissional e branding premium
6. Dashboard executivo com relatórios e alertas
7. Separação de regras de negócio em services e módulos
8. Treinos por QR Code — MVP inicial implementado; avaliar piloto e melhorias (histórico de conclusão, cronômetro, favoritos e acessibilidade)
9. Notificações automáticas WhatsApp — planejar com API oficial, custos, consentimento e auditoria

### Documentação complementar
- [docs/ANALISE_AUDITORIA.md](docs/ANALISE_AUDITORIA.md)
- [docs/ROADMAP_PROFISSIONAL.md](docs/ROADMAP_PROFISSIONAL.md)
- [docs/ENTREGAVEL_GERENTE.md](docs/ENTREGAVEL_GERENTE.md)
- [docs/SLIDES-APRESENTACAO.md](docs/SLIDES-APRESENTACAO.md)
- [docs/SLIDE_APRESENTACAO.html](docs/SLIDE_APRESENTACAO.html)
- [docs/PROJETO-TREINO-QR.md](docs/PROJETO-TREINO-QR.md)

---

*© 2026 Polo Fit — Sua opinião faz a diferença.*
