# Próximos Passos — FeedbackPro SaaS

## ✅ O que já foi feito

1. **Landing Page Comercial** (`/landing/`)
   - Página profissional para vender o sistema
   - Botão flutuante de WhatsApp (seu número: 5583986719438)
   - Planos e preços bem definidos
   - Formulário de demonstração

2. **Sistema White-Label**
   - Modelo `ConfiguracaoAcademia` para personalização
   - Cada academia pode ter logo, cores e nome próprios
   - Context processor injeta configurações em todos os templates

3. **Setup Wizard** (`/setup/`)
   - 3 passos simples para configurar nova academia
   - Upload de logo
   - Escolha de cores
   - Informações de contato

4. **Segurança Melhorada**
   - Sistema de auditoria de acessos (`AuditoriaAcesso`)
   - Middleware de segurança adicional
   - Rate limiting para prevenir abuso
   - Security headers

5. **Documentação de Vendas**
   - Contrato SaaS profissional
   - FAQ completo para clientes
   - Planos e preços detalhados
   - SLA definido

6. **Git**
   - Todas as alterações commitadas e pushadas
   - Repositório atualizado no GitHub

---

## 🚀 Próximos Passos Imediatos

### 1. Publicar ou atualizar no PythonAnywhere

Endereço oficial da aplicação: <https://polofeedback.pythonanywhere.com/>.

O projeto exige `DEBUG=False`, uma `SECRET_KEY` privada e um banco PostgreSQL persistente quando executado em produção. Antes de iniciar, configure um PostgreSQL acessível a partir da conta PythonAnywhere e confirme que o plano/provedor permite essa conexão. Não tente usar o SQLite local como banco de produção.

Siga estes passos no Bash Console do PythonAnywhere:

```bash
# 1. Clonar o repositório
git clone https://github.com/Marcosplira/PoloFeedback.git
cd PoloFeedback

# 2. Criar ambiente virtual
python3.12 -m venv ~/.virtualenvs/feedback-env
source ~/.virtualenvs/feedback-env/bin/activate
pip install -r requirements.txt

# 3. Criar superusuário (opcional; as contas gerenciais não precisam ser superusuárias)
python manage.py createsuperuser
```

Na aba **Web** do PythonAnywhere:
- Adicionar novo app: Manual Configuration → Python 3.12 (o Django deste projeto requer Python 3.12 ou superior)
- Virtualenv: `/home/SEU_USUARIO/.virtualenvs/feedback-env`
- Static files: `/static/` → `/home/SEU_USUARIO/PoloFeedback/staticfiles`
- Media files: `/media/` → `/home/SEU_USUARIO/PoloFeedback/media`
- Crie o diretório `media` se necessário, confirme que o usuário da aplicação pode gravar nele e inclua-o na rotina de backup. As fotos e logos são armazenadas nesse diretório.
- WSGI config (substituir tudo):

```python
import os
import sys

path = '/home/SEU_USUARIO/PoloFeedback'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'polofeedback.settings'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'SUBSTITUA_POR_UMA_CHAVE_FORTE_E_PRIVADA'
os.environ['ALLOWED_HOSTS'] = 'polofeedback.pythonanywhere.com'
os.environ['CSRF_TRUSTED_ORIGINS'] = 'https://polofeedback.pythonanywhere.com'
os.environ['DATABASE_URL'] = 'postgresql://USUARIO:SENHA@HOST:5432/NOME_DO_BANCO?sslmode=require'
os.environ['DASHBOARD_MANAGER_USERNAME'] = 'SEU_USUARIO_GERENTE'
os.environ['DASHBOARD_MANAGER_PASSWORD'] = 'SENHA_FORTE_PRIVADA'
os.environ['DASHBOARD_OWNER_USERNAME'] = 'SEU_USUARIO_RESPONSAVEL'
os.environ['DASHBOARD_OWNER_PASSWORD'] = 'OUTRA_SENHA_FORTE_PRIVADA'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Substitua todos os valores de exemplo pelos dados privados do provedor. Nunca salve esse conteúdo no repositório, tire capturas de tela com segredos ou compartilhe a URL PostgreSQL. Gere a chave Django com `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` e guarde-a somente na configuração WSGI privada do PythonAnywhere. Se estiver atualizando uma instalação existente, faça backup do banco e da pasta `media` antes de aplicar migrações.

#### Configurar alertas WhatsApp (opcional)

O modelo da Meta precisa estar aprovado antes de ativar esta etapa. No **PythonAnywhere → Files**, crie/edite `~/PoloFeedback/.env` (a pasta pessoal da conta) ou `~/PoloFeedback/PoloFeedback/.env` (a raiz do projeto). O Django carrega os dois locais tanto na aplicação quanto no comando de alertas. O `.env` está no `.gitignore`; mantenha a permissão privada:

```bash
chmod 600 ~/PoloFeedback/.env
```

O arquivo precisa conter os parâmetros privados de produção para o comando usar o mesmo banco que o site (`DEBUG=False`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` e `DATABASE_URL`) e os parâmetros abaixo:

```dotenv
WHATSAPP_ALERTS_ENABLED=True
WHATSAPP_CLOUD_API_VERSION=vXX.X
WHATSAPP_PHONE_NUMBER_ID=ID_DO_NUMERO_NA_META
WHATSAPP_ACCESS_TOKEN=TOKEN_PRIVADO_DA_META
WHATSAPP_BUSINESS_NUMBER=55DDDNUMERODOREMETENTE
WHATSAPP_ALERT_RECIPIENT=55DDDNUMERODAGESTAO
WHATSAPP_ALERT_TEMPLATE_NAME=polo_feedback_nova_avaliacao
WHATSAPP_ALERT_TEMPLATE_LANGUAGE=pt_BR
SITE_PUBLIC_URL=https://polofeedback.pythonanywhere.com
```

Troque os exemplos pelos valores reais, sem colchetes ou aspas: use uma versão Graph API suportada, o nome/idioma exatamente como aparecem no modelo aprovado e telefones internacionais distintos. Não compartilhe o `.env`, o token nem capturas mostrando esses valores. Não deixe variáveis WhatsApp antigas/vazias no WSGI sobrescreverem o arquivo.

No Bash Console, atualize as dependências no mesmo virtualenv configurado na aba Web. No caso desta instalação, as capturas indicam Python 3.12 e o ambiente `feedback-env312`; confirme o caminho na aba **Web → Virtualenv**:

```bash
/home/PoloFeedback/.virtualenvs/feedback-env312/bin/python -m pip install -r /home/PoloFeedback/PoloFeedback/requirements.txt
```

Na aba **Web**, clique em **Reload**. Entre no dashboard e confira o quadro **Robô de alertas pelo WhatsApp**; **Credenciais configuradas** confirma que o arquivo foi lido, mas não consulta a aprovação na Meta nem confirma que a tarefa está agendada.

Para processar a fila, configure em **Tasks** uma tarefa agendada com o mesmo Python 3.12 virtualenv e projeto, usando os caminhos reais da sua conta. O Django carrega o `.env` automaticamente; não use `source .env` (a URL do banco contém caracteres que o shell pode interpretar):

```bash
/home/PoloFeedback/.virtualenvs/feedback-env312/bin/python /home/PoloFeedback/PoloFeedback/manage.py enviar_alertas_whatsapp --limit 25
```

Se seu usuário, virtualenv ou pastas tiverem outros nomes, substitua os caminhos pelos valores da aba **Web** e de `echo $VIRTUAL_ENV` no console. Escolha a frequência disponível no seu plano. Antes de deixar a tarefa recorrente, confira o nome do modelo e faça um processamento controlado: o comando pode enviar mensagens reais que estiverem pendentes. Se o processo não conseguir ler as configurações ou conectar ao banco de produção, não agende/reexecute até corrigir a configuração. Não é necessário rodar migrações novamente para esta etapa.

Para executar migrações e coletar estáticos no Bash Console, carregue a mesma `DATABASE_URL` de forma interativa (sem incluí-la no comando salvo no histórico):

```bash
read -s -p "DATABASE_URL: " DATABASE_URL; echo
export DATABASE_URL
source ~/.virtualenvs/feedback-env/bin/activate
cd ~/PoloFeedback
python manage.py migrate
python manage.py collectstatic --noinput
```

Para criar/atualizar as contas gerenciais, informe os dados de forma interativa no Bash Console e execute o comando na mesma sessão:

```bash
read -r -p "Usuário gerente: " DASHBOARD_MANAGER_USERNAME
read -s -p "Senha gerente: " DASHBOARD_MANAGER_PASSWORD; echo
read -r -p "Usuário responsável: " DASHBOARD_OWNER_USERNAME
read -s -p "Senha responsável: " DASHBOARD_OWNER_PASSWORD; echo
export DASHBOARD_MANAGER_USERNAME DASHBOARD_MANAGER_PASSWORD
export DASHBOARD_OWNER_USERNAME DASHBOARD_OWNER_PASSWORD
python manage.py setup_dashboard_users
unset DASHBOARD_MANAGER_USERNAME DASHBOARD_MANAGER_PASSWORD
unset DASHBOARD_OWNER_USERNAME DASHBOARD_OWNER_PASSWORD
```

Esse comando concede permissões específicas de equipe, incluindo a configuração da academia; não compartilhe nem reutilize senhas de exemplo.

Na página **Web** do PythonAnywhere, ative **Force HTTPS** e clique em **Reload**. O host `pythonanywhere.com` fornece HTTPS para subdomínios próprios; consulte a [documentação de HTTPS](https://help.pythonanywhere.com/pages/HTTPSSetup/) e a [orientação para forçar HTTPS](https://help.pythonanywhere.com/pages/ForcingHTTPS/). Depois, valide externamente:

```bash
curl -I http://polofeedback.pythonanywhere.com/login/
curl -sS -D - -o /dev/null https://polofeedback.pythonanywhere.com/login/
```

A primeira chamada deve redirecionar para HTTPS. Na segunda, confira `Strict-Transport-Security` e, quando a resposta definir cookies, o atributo `Secure`. Não considere a implantação segura enquanto HTTP servir a página sem redirecionar ou os cookies seguros não estiverem presentes.

Clique em **Reload** no topo da página.

### 2. Configurar Domínio (Opcional)

- Comprar domínio barato no Registro.br (R$ 40/ano)
- Ex: `feedbackpro.com.br` ou `academiafeedback.com.br`
- Configurar no PythonAnywhere em **Web → Custom domain**

### 3. Testar o Sistema

1. Abrir a avaliação em `https://polofeedback.pythonanywhere.com/avaliar/`.
2. Entrar no dashboard em `https://polofeedback.pythonanywhere.com/dashboard/` com uma conta autorizada.
3. Testar o fluxo de feedback pelo celular e confirmar o recebimento no painel.
4. Gerar QR Codes somente pelo domínio HTTPS publicado e testá-los com um celular conectado à internet.

### 4. Primeiras Vendas

**Abordagem para academias:**

```
"Olá! Sou Marcos Paulo, desenvolvedor aqui da Paraíba.
Desenvolvi o FeedbackPro, um sistema inteligente por QR Code onde os alunos avaliam aparelhos, limpeza e professores em menos de 1 minuto direto pelo celular.

Isso ajuda a academia a descobrir insatisfações antes do aluno cancelar a matrícula e ranqueia sua equipe de instrutores.

Estou liberando 14 dias grátis para você testar com seus alunos sem compromisso e ver o resultado na prática.
Posso criar seu acesso de teste hoje?"
```

**Canais de divulgação:**
- Instagram: Pesquisar "academia [cidade]" e seguir/dar like
- WhatsApp: Contatar donos de academias
- Google Maps: Buscar academias na região e entrar em contato
- Facebook: Grupos de empresários locais

**Meta inicial:**
- 10 academias testando (grátis 14 dias)
- 3 academias convertendo para pagantes
- Renda recorrente: 3 × R$ 149 = R$ 447/mês

---

## 📊 Estratégia de Crescimento

### Fase 1: Validação (Mês 1)
- Focar em academias de Picuí, Cuité, Campina Grande
- Oferecer trial grátis de 14 dias
- Coletar feedback e melhorias
- Meta: 5 academias pagantes

### Fase 2: Expansão (Mês 2-3)
- Expandir para outras cidades da Paraíba
- Criar casos de sucesso (testimonials)
- Melhorar sistema com base no feedback
- Meta: 15 academias pagantes

### Fase 3: Escala (Mês 4-6)
- Investir em marketing digital
- Criar conteúdo para YouTube/Instagram
- Parcerias com consultores fitness
- Meta: 50 academias pagantes (R$ 7.450/mês)

---

## 💡 Dicas Importantes

### Sobre o Jefferson e Polo Fit
- Não leve para o pessoal. É negócio.
- Você tem a tecnologia, agora é seu produto.
- Se eles quiserem depois, serão apenas mais um cliente pagando R$ 149/mês como qualquer outro.

### Sobre Preços
- Não cobre barato demais. Desvaloriza seu trabalho.
- Se alguém reclamar do preço, não é seu cliente ideal.
- Foque em academias que valorizam tecnologia e crescimento.

### Sobre Suporte
- Responda rápido (WhatsApp é ideal)
- Seja paciente no começo
- Documente dúvidas recorrentes
- Melhore o sistema baseado no feedback

### Sobre Marketing
- Fale em benefícios, não funcionalidades
- "Melhorar satisfação" > "Sistema de avaliação"
- "Evitar cancelamentos" > "Coletar feedback"
- Use números: "5x mais engajamento", "+40% satisfação"

---

## 🔧 Manutenção Futura

### Semanal
- Verificar logs de erro
- Verificar os backups do PostgreSQL e da pasta `media`
- Responder suporte

### Mensal
- Renovar domínio (se comprou)
- Revisar métricas de uso
- Planejar melhorias

### Trimestral
- Atualizar dependências Python
- Renovar PythonAnywhere (plano grátis)
- Revisar segurança

---

## 📞 Contato de Suporte

Se precisar de ajuda:
- WhatsApp: 5583986719438
- Email: [seu email]
- GitHub: https://github.com/Marcosplira/PoloFeedback

---

## 🎉 Parabéns, Marcos!

Você transformou um projeto específico para uma academia em um produto SaaS profissional que pode ser vendido para centenas de academias pelo Brasil.

A chave agora é:
1. **Colocar no ar** (PythonAnywhere - já tem o guia)
2. **Falar com academias** (WhatsApp/Instagram)
3. **Oferecer teste grátis** (14 dias)
4. **Converter em pagantes** (após verem o valor)

Não desista! O produto está excelente. É só questão de tempo até ter sua primeira venda.

Boa sorte! 🚀
