# 🏋️ Polo Feedback — Polo Fit

Sistema moderno de coleta, análise e gestão de avaliações e satisfação dos alunos da Academia Polo Fit.

## Acesso ao sistema

🌐 **Polo Feedback:**  
https://polofeedback.pythonanywhere.com/

## 📌 Visão Geral

O **Polo Feedback** foi desenvolvido para aproximar os alunos da gestão da academia, permitindo:
- **Alunos:** Avaliar a experiência rapidamente via celular escaneando um QR Code nos totens ou setores da academia.
- **Gerentes e Supervisores:** Consultar indicadores ao acessar ou atualizar o painel, filtrar feedbacks, gerenciar pendências, visualizar rankings e usar recursos de IA com **Google Gemini** opcional.

---

## 🚀 Principais Funcionalidades

1. **📱 Formulário de Avaliação Mobile-First (`/avaliar/`):**
   - Rápido, intuitivo e responsivo.
   - Nome do aluno opcional. Com os alertas WhatsApp desligados, nome e comentário ficam no sistema para acesso da equipe autorizada; quando os alertas são ligados, a tela informa que também serão encaminhados pelo WhatsApp Business da Meta.
   - Avaliação por estrelas (1 a 5).
   - Múltiplas categorias (Atendimento, Limpeza, Equipamentos, Professores, Estrutura, Geral).
   - Ao escolher **Aulas Coletivas**, o aluno seleciona a modalidade específica (Glúteo, Step, HIIT, Abdominais, Dança, Jump, Funcional, Spinning ou Pump) antes de dar a nota.
   - A enquete também permite informar o nome opcionalmente, visível apenas para a equipe autorizada.
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
   - Integração com a API Google Gemini (`gemini-2.5-flash`) com histórico curto para conversas de múltiplos turnos.
   - Resumo gerencial inclui avaliações, categorias e notas, funcionários, locais e todos os tópicos da enquete.
   - **Fallback local identificado:** sem uma chave Gemini válida, o painel sinaliza o modo local e responde com regras e dados registrados; isso não equivale a um modelo generativo.
   - Quando Gemini está configurado, o contexto enviado inclui dados agregados, nomes/funções de funcionários e textos livres recentes de avaliações e enquetes. Esses textos podem conter dados pessoais; avalie a política de privacidade e evite inserir informações identificáveis nos comentários.

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
   - Fotos e logos passam por validação de imagem e limite de 5 MB.
   - Gestão e auditoria de avaliações.
   - Lista e cadastro de usuários/alunos, ativação/inativação e redefinição de senha; senhas não são exibidas e contas gerenciais não podem conceder privilégios administrativos por essa tela.

7. **📲 Acesso rápido, QR Codes e ajuda no painel:**
   - A página inicial oferece QR Codes para avaliação e pesquisa; cada código aponta para o host HTTPS/local usado para abrir o site.
   - A pedido do proprietário, a página inicial prioriza avaliação e satisfação no celular; os detalhes e valores dos planos ficam recolhidos até o visitante tocar para consultá-los. Nesse painel, é possível marcar um ou mais planos e enviar a seleção à recepção pelo WhatsApp para tirar dúvidas; isso não confirma matrícula.
   - A página inicial também exibe a foto da academia e o vídeo de apresentação incorporado do Google Drive. Para os visitantes assistirem, o arquivo precisa permitir acesso a qualquer pessoa com o link.
   - O Dashboard oferece atalhos de diagnóstico de migrações (`/dashboard/configuracao/`), material para compartilhar (`/dashboard/divulgacao/`) e apresentação do projeto de treinos (`/dashboard/projeto-treino/`).
   - A tela de instalação adiciona o PWA à tela inicial do dispositivo. O aplicativo ainda não está publicado na Google Play Store; não compartilhe links como se houvesse um app listado na loja.

8. **📨 Alertas de avaliação pelo WhatsApp (opcional e desligado por padrão):**
   - Processador no backend para encaminhar avaliações públicas ao número configurado da gerência usando modelo aprovado da WhatsApp Business Cloud API.
   - A fila evita que uma falha externa interrompa o envio do formulário; o comando de processamento precisa ser agendado pela equipe.
   - Não recebe mensagens nem responde aos alunos; exige revisão de privacidade, segredos no provedor e aprovação do modelo antes da ativação.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.12, Django 6.1.1 |
| **Frontend** | HTML5, Tailwind CSS (CDN), JavaScript, Chart.js |
| **Banco de Dados** | SQLite (desenvolvimento local) / PostgreSQL (produção, Docker e Render alternativo) |
| **Inteligência Artificial** | Google Gemini API (`gemini-2.5-flash`) |
| **Infraestrutura** | Gunicorn, Whitenoise, Docker, Docker Compose |
| **Hospedagem** | PythonAnywhere (produção) |

---

## 🤖 Verificações automatizadas

O GitHub Actions executa testes da seleção e gravação de aulas coletivas e do processador WhatsApp (com chamadas externas simuladas) quando há atualizações no código; também pode ser iniciado manualmente. Um monitor separado verifica diariamente se a página inicial, avaliação, enquete, login, manifest PWA e Service Worker continuam respondendo no endereço público.

O monitor faz apenas requisições HTTPS de leitura: não entra em contas, não envia avaliações, não altera dados e não rastreia visitantes. Falhas aparecem como execução malsucedida na aba **Actions** do GitHub; o monitor não corrige erros automaticamente nem garante a disponibilidade do provedor. Para executar localmente:

```powershell
python scripts/monitor_public_site.py
```

Opcionalmente, defina `SITE_URL` para apontar o monitor a outro domínio HTTPS.

### Robô e IA: o que existe e o que pode evoluir

Os testes e o monitor automático verificam comportamento técnico; o resumo/chat com Gemini é uma ferramenta gerencial acionada pelo usuário. **A IA não recebe alertas do monitor, não vigia o código continuamente e não corrige bugs.**

Também existe um processador opcional de alertas de avaliações para a WhatsApp Business Cloud API. Ele fica **desligado por padrão** e não envia nada enquanto não for configurado e executado pela equipe. Quando habilitado, coloca cada nova avaliação pública em uma fila no banco, sem esperar por uma chamada externa durante o envio do formulário. Um comando Django separado processa a fila; o agendamento periódico desse comando precisa ser configurado no provedor de hospedagem. A integração não recebe mensagens nem responde a alunos.

O painel gerencial exibe o quadro **Robô de alertas pelo WhatsApp**, que informa se a função está desativada, se faltam variáveis de configuração ou se as credenciais foram preenchidas. Mesmo com credenciais presentes, a equipe deve confirmar a aprovação do modelo na Meta e agendar o comando de envio.

No PythonAnywhere, as configurações podem ficar no arquivo `.env` privado na pasta pessoal (`~/PoloFeedback/.env`) ou na raiz do projeto (`~/PoloFeedback/PoloFeedback/.env`). O Django carrega ambos os locais tanto no site quanto no comando agendado, sem colocar credenciais na linha do comando. O `.env` já está excluído do Git; restrinja sua leitura ao usuário da conta (`chmod 600 ~/PoloFeedback/.env`) e nunca envie seu conteúdo em capturas de tela ou mensagens. Para a tarefa agendada conectar ao mesmo banco de produção, o `.env` também precisa conter a configuração Django/produção necessária, especialmente `DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` e `DATABASE_URL`. Variáveis de ambiente já definidas no WSGI têm precedência sobre os valores do `.env`; remova de lá variáveis WhatsApp antigas/vazias ou outros valores que deveriam vir do `.env`.

Configure `WHATSAPP_ALERTS_ENABLED=True`, `WHATSAPP_CLOUD_API_VERSION`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_BUSINESS_NUMBER`, `WHATSAPP_ALERT_RECIPIENT`, `WHATSAPP_ALERT_TEMPLATE_NAME`, `WHATSAPP_ALERT_TEMPLATE_LANGUAGE` e `SITE_PUBLIC_URL`. Use o nome/idioma exatos do modelo aprovado na Meta, o ID do número conectado à Cloud API e números internacionais distintos para remetente e destinatário. A versão da API deve ser uma versão ainda suportada pela Meta. O corpo aprovado do modelo deve usar os parâmetros nesta ordem:

```text
Nova avaliação {{1}}. Nota {{2}}/5; categoria {{3}}; aula {{4}};
nome {{5}}; comentário {{6}}. Painel: {{7}}
```

1. identificador da avaliação;
2. nota;
3. categoria(s);
4. aula coletiva ou “Não se aplica”;
5. nome ou “Anônimo”;
6. comentário (limitado a 900 caracteres);
7. link HTTPS do painel.

A tela do aluno informa esse encaminhamento quando a função está ativa. O modelo não armazena cópia do comentário, e os logs não incluem nome nem comentário.

Após configurar, atualize as dependências no ambiente virtual do PythonAnywhere (`pip install -r requirements.txt`), reinicie a aplicação na aba **Web** e confira se o painel mostra **Credenciais configuradas**. O arquivo `.env` não precisa de migrações novas. Configure uma tarefa agendada com o Python 3.12 virtualenv e a raiz do projeto. As configurações do `.env` são carregadas pelo próprio Django, inclusive fora do WSGI:

```bash
/home/SEU_USUARIO/.virtualenvs/feedback-env312/bin/python /home/SEU_USUARIO/PoloFeedback/PoloFeedback/manage.py enviar_alertas_whatsapp --limit 25
```

Substitua `SEU_USUARIO` e `feedback-env312` pelos caminhos exibidos na sua aba **Web**; o `.env` pode ficar em `/home/SEU_USUARIO/PoloFeedback/.env` ou dentro da raiz do projeto. Antes de deixar a tarefa recorrente, faça um primeiro processamento controlado: o comando pode enviar mensagens reais da fila.

Falhas temporárias são tentadas novamente até cinco vezes; uma interrupção ou timeout pode deixar dúvida sobre a aceitação pela API e resultar em duplicidade. A opção `--retry-failed` também pode duplicar mensagens; use-a somente depois de conferir o histórico no WhatsApp. O status **Aceito pela API** não comprova entrega ao aparelho; confirmação de entrega exigiria um webhook de status, que não faz parte desta implementação. Nenhuma mensagem real é enviada pelos testes automatizados.

**Limites:** o recurso encaminha dados pessoais à Meta e ao número oficial configurado; antes de habilitá-lo em produção, a academia deve validar a política de privacidade, a necessidade do conteúdo, os acessos ao aparelho e os requisitos aplicáveis. A integração não altera código ou banco automaticamente, não entra em contas e não publica atualizações. Para conectar IA ao robô técnico no futuro, enviar somente metadados sanitizados e exigir revisão humana.

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

O Django carrega automaticamente um `.env` local na raiz do projeto; sem esse arquivo ou variáveis de ambiente, usa SQLite local e fallback da IA. Para entrar no dashboard local, crie uma conta com `python manage.py createsuperuser`.

### 5. Executar Migrações do Banco

```powershell
python manage.py migrate
```

As migrações incluem os 17 funcionários informados para a lista de avaliações (Alan Araújo como gerente, Jefferson Tauin como proprietário e os demais como funcionários). Os cargos legados são convertidos em funções selecionáveis e classificados em quatro grupos para a pergunta de elogios da enquete: **Recepção**, **Time de limpeza**, **Estagiários e professores** e **Direção e coordenação**. Jaqueline Lima, Jessica Karla e Micheli Priscila são inicialmente classificadas em **Recepção**; os demais cargos genéricos de funcionário ficam em **Estagiários e professores**. Confirme e ajuste essa classificação conforme a equipe real.

No Django Admin, abra **Funções** para ajustar o grupo de cada cargo e **Funcionários** para associar uma ou mais funções às pessoas. A pergunta 6 da enquete exibe as pessoas agrupadas por esses grupos e permite selecionar várias. Nas perguntas sobre espaços desejados e aulas que precisam de melhorias, os alunos também podem marcar várias opções; a pergunta de frequência das aulas continua aceitando apenas uma resposta.

Se o Admin mostrar `no such table: feedback_equipamento` ou `feedback_planotreino`, pare o servidor e execute `python manage.py migrate` na pasta exata do projeto e com o mesmo ambiente Python usado para iniciar o servidor. Depois, inicie novamente com `python manage.py runserver`. Executar a migração em outra cópia do projeto ou em outro banco não corrige o banco que está servindo a página.

Se o servidor já estiver usando um banco, a tela de erro mostra instruções em vez do traceback amarelo do Django e registra a exceção no log. A tela **Diagnóstico** do Dashboard exibe migrações pendentes quando a conexão com o banco está disponível. Em hospedagem, configure `DATABASE_URL` primeiro; as migrações são aplicadas pelo comando de inicialização.

### 6. Criar o usuário administrador (primeira vez)

```powershell
python manage.py createsuperuser
```

Para configurar as duas contas privadas do dashboard, defina estas variáveis no ambiente de hospedagem:
- `DASHBOARD_MANAGER_USERNAME` (usuário inicial sugerido: `gerente`)
- `DASHBOARD_MANAGER_PASSWORD` (senha privada, forte e não compartilhada)
- `DASHBOARD_OWNER_USERNAME` (usuário inicial sugerido: `marcos`)
- `DASHBOARD_OWNER_PASSWORD` (outra senha privada e forte)

O comando `python manage.py setup_dashboard_users` cria/atualiza as contas com acesso ao dashboard, à gestão de funcionários, à configuração da academia, ao cadastro/edição de aparelhos e exercícios e à consulta/cadastro/edição básica de usuários, sem torná-las superusuárias nem permitir exclusões pelo Admin. A tela de usuários oculta campos de privilégios; senhas existentes nunca são exibidas. No Render alternativo, o `startCommand` executa as migrações e esse comando antes de iniciar o servidor. No PythonAnywhere, configure as variáveis no WSGI e execute o comando pelo Bash Console se precisar criar ou atualizar essas contas. Se as variáveis não estiverem preenchidas, as contas gerenciais não são criadas. Não há credenciais padrão no código nem na tela de login.

### 7. Cadastrar o MVP de treinos por QR Code

No endereço `/admin/`, entre com uma conta da equipe autorizada (ou com o superusuário local) e:

1. Oriente cada aluno a criar a própria conta em `/cadastro/aluno/`; ela será uma conta comum, sem acesso à equipe.
2. Cadastre cada máquina em **Equipamentos de treino**, com instruções e avisos de segurança.
3. Cadastre os exercícios em **Exercícios**, relacionando o equipamento e, se aprovado, um link para vídeo.
4. Crie um **Plano de treino**, selecione o aluno e o professor responsável e inclua os exercícios, séries, repetições, descanso e carga orientada pelo professor.
5. Um membro da equipe imprime os QR Codes em `/treinos/qrs/` ou pelo link **QR Treinos** no Dashboard.

O QR Code identifica apenas o equipamento. O aluno entra com sua conta para ver os exercícios vinculados ao aparelho que pertencem aos próprios planos ativos. Para usar as telas de gestão, o professor deve ter conta da equipe (`is_staff`). As contas privadas criadas por `setup_dashboard_users` também recebem permissões para visualizar, adicionar e alterar equipamentos e exercícios pelo Admin, sem permissão para excluí-los. A equipe pode imprimir os QR Codes dos aparelhos sem a permissão de visualizar avaliações. O gerente deve ter a permissão `feedback.view_avaliacao` (ou ser superusuário) para abrir Dashboard, IA e QR Codes de avaliação.

A apresentação com o problema, solução, fluxo e etapas sugeridas do piloto também está acessível no Dashboard pelo botão **Projeto da Academia PoloFit**.

O link do QR é montado usando o host acessado pelo membro da equipe. Em produção, use `https://polofeedback.pythonanywhere.com/`, confirme que abre com HTTPS e gere os códigos nesse endereço. Não imprima QRs gerados por `localhost` para uso pelos alunos. Vídeos externos precisam ser próprios ou licenciados. Carga, séries e repetições são configuradas pelo professor; o sistema não calcula nem prescreve treino.

### 8. Iniciar o Servidor de Desenvolvimento

```powershell
python manage.py runserver
```

Para liberar o acesso a smartphones na mesma rede Wi-Fi:
```powershell
python manage.py runserver 0.0.0.0:8000
```

Acesse a versão publicada no PythonAnywhere:
- **Avaliação do Aluno:** [https://polofeedback.pythonanywhere.com/avaliar/](https://polofeedback.pythonanywhere.com/avaliar/)
- **Dashboard Gerencial:** [https://polofeedback.pythonanywhere.com/dashboard/](https://polofeedback.pythonanywhere.com/dashboard/) (requer login autorizado)
- **Gerador de QR Code:** [https://polofeedback.pythonanywhere.com/qrcode/](https://polofeedback.pythonanywhere.com/qrcode/) (requer permissão gerencial)
- **QR Codes dos aparelhos:** [https://polofeedback.pythonanywhere.com/treinos/qrs/](https://polofeedback.pythonanywhere.com/treinos/qrs/) (requer login da equipe)
- **Administração Django:** [https://polofeedback.pythonanywhere.com/admin/](https://polofeedback.pythonanywhere.com/admin/) (requer login autorizado)

Os endereços `localhost:8000` são somente para desenvolvimento e funcionam apenas enquanto o servidor local estiver aberto. Se o computador ou celular não estiver executando o projeto, o navegador pode mostrar a página **“Sem conexão com a internet”**; isso não significa que o endereço publicado esteja fora do ar. Use os links PythonAnywhere acima para acessar a produção.

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

Com os containers em execução, abra `http://localhost:8000` no navegador do mesmo computador onde o Docker está rodando. Esse endereço local não é um link público e não funciona em outro aparelho. Para acessar o sistema publicado, use <https://polofeedback.pythonanywhere.com/>.

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

## ☁️ Deploy alternativo no Render.com

O ambiente de produção documentado acima é o PythonAnywhere. O arquivo `render.yaml` é uma opção alternativa de hospedagem; não é necessário para acessar o sistema publicado no PythonAnywhere.

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
| `DASHBOARD_MANAGER_USERNAME` / `DASHBOARD_MANAGER_PASSWORD` | *(não configurados)* | Credenciais privadas da primeira conta gerencial |
| `DASHBOARD_OWNER_USERNAME` / `DASHBOARD_OWNER_PASSWORD` | *(não configurados)* | Credenciais privadas da segunda conta gerencial |
| `GEMINI_API_KEY` | *(vazio — usa fallback local)* | Chave da API Gemini para IA |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Modelo Gemini utilizado |
| `WHATSAPP_ALERTS_ENABLED` | `False` | Habilita a criação de alertas para avaliações públicas |
| `WHATSAPP_CLOUD_API_VERSION` | *(vazio)* | Versão da Graph API suportada pela aplicação Meta |
| `WHATSAPP_PHONE_NUMBER_ID` | *(vazio)* | ID do número conectado à WhatsApp Business Cloud API |
| `WHATSAPP_ACCESS_TOKEN` | *(vazio)* | Token de acesso protegido; nunca versionar ou registrar em logs |
| `WHATSAPP_BUSINESS_NUMBER` | *(vazio)* | Número remetente em formato internacional |
| `WHATSAPP_ALERT_RECIPIENT` | *(vazio)* | Número da gerência que receberá os avisos, diferente do remetente |
| `WHATSAPP_ALERT_TEMPLATE_NAME` / `WHATSAPP_ALERT_TEMPLATE_LANGUAGE` | `polo_feedback_nova_avaliacao` / `pt_BR` | Nome e idioma do modelo aprovado na Meta |
| `SITE_PUBLIC_URL` | *(vazio)* | Origem HTTPS usada no link do painel enviado no modelo |

---

## 📁 Estrutura do Projeto

```
PoloFeedback/
├── feedback/                   # App principal
│   ├── management/commands/     # Comando do processador de alertas WhatsApp
│   ├── migrations/             # Migrações do banco
│   ├── static/feedback/        # Imagens, ícones e arquivos da PWA
│   ├── templates/
│   │   ├── feedback/           # Templates: avaliar, dashboard, qrcode, sucesso
│   │   └── registration/       # Template de login
│   ├── admin.py                # Configuração do painel admin
│   ├── models.py               # Modelos: Funcionario, Avaliacao, WhatsAppAviso
│   ├── tests.py                # Testes automatizados
│   ├── whatsapp.py             # Integração de saída com WhatsApp Cloud API
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
9. Alertas WhatsApp já preparados, mas desligados — configurar Meta, privacidade e agendamento antes de ativar

### Documentação complementar
- [docs/ANALISE_AUDITORIA.md](docs/ANALISE_AUDITORIA.md)
- [docs/ROADMAP_PROFISSIONAL.md](docs/ROADMAP_PROFISSIONAL.md)
- [docs/ENTREGAVEL_GERENTE.md](docs/ENTREGAVEL_GERENTE.md)
- [docs/SLIDES-APRESENTACAO.md](docs/SLIDES-APRESENTACAO.md)
- [docs/SLIDE_APRESENTACAO.html](docs/SLIDE_APRESENTACAO.html)
- [docs/PROJETO-TREINO-QR.md](docs/PROJETO-TREINO-QR.md)
- [docs/ENTREGAVEL_GERENTE.md](docs/ENTREGAVEL_GERENTE.md) — roteiro para explicar as telas de treinos, divulgação e QR Codes ao gerente

---

## 👨‍💻 Desenvolvedor

**Marcos Paulo Santos Lira**

Projeto desenvolvido para contribuir com a divulgação e organização da Academia Polo Fit de **Picuí-PB** através da tecnologia.

*© 2026 Polo Fit — Sua opinião faz a diferença.*
