# Guia de Deploy em VPS com Docker

## Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Escolha da VPS](#escolha-da-vps)
3. [Configuração Inicial da VPS](#configuração-inicial-da-vps)
4. [Instalação do Docker](#instalação-do-docker)
5. [Preparação do Projeto](#preparação-do-projeto)
6. [Configuração de Variáveis de Ambiente](#configuração-de-variáveis-de-ambiente)
7. [Deploy com Docker Compose](#deploy-com-docker-compose)
8. [Configuração de Domínio e SSL](#configuração-de-domínio-e-ssl)
9. [Monitoramento e Manutenção](#monitoramento-e-manutenção)
10. [Backup e Segurança](#backup-e-segurança)

---

## Pré-requisitos

### Conhecimentos Necessários

- Linux básico (comandos de terminal)
- Git (clonar repositório)
- Docker e Docker Compose
- Conceitos de VPS (Virtual Private Server)
- Editor de texto (nano, vim, ou VS Code Remote)

### Ferramentas Necessárias

- Cliente SSH (PuTTY, Terminal, ou VS Code Remote)
- Cliente Git
- Editor de texto

---

## Escolha da VPS

### Opções Recomendadas

#### 1. Locaweb (Brasil)
- **Vantagens**: Servidor no Brasil, suporte em português
- **Plano recomendado**: Cloud Server Flex 2GB RAM / 1 vCPU
- **Custo**: ~R$ 50-100/mês
- **Link**: https://www.locaweb.com.br/

#### 2. DigitalOcean
- **Vantagens**: Fácil configuração, bom preço
- **Plano recomendado**: Basic Droplet 2GB RAM / 1 vCPU
- **Custo**: ~$12/mês (~R$ 60)
- **Link**: https://www.digitalocean.com/

#### 3. AWS Lightsail
- **Vantagens**: Integração AWS, escalável
- **Plano recomendado**: 2GB RAM / 1 vCPU
- **Custo**: ~$10/mês (~R$ 50)
- **Link**: https://aws.amazon.com/lightsail/

#### 4. Linode
- **Vantagens**: Bom desempenho, preço competitivo
- **Plano recomendado**: Nanode 2GB
- **Custo**: ~$10/mês (~R$ 50)
- **Link**: https://www.linode.com/

### Sistema Operacional

Recomendado: **Ubuntu 22.04 LTS** ou **Ubuntu 24.04 LTS**

- Suporte de longo prazo
- Pacotes atualizados
- Comunidade ativa
- Docker bem suportado

---

## Configuração Inicial da VPS

### 1. Acesso via SSH

```bash
ssh root@seu-ip-vps
```

Primeiro acesso? Será solicitado a senha fornecida pela VPS.

### 2. Atualizar o Sistema

```bash
apt update && apt upgrade -y
```

### 3. Criar Usuário (Segurança)

**NÃO** use sempre o usuário root. Crie um usuário comum:

```bash
# Criar usuário
adduser polofit

# Adicionar ao grupo sudo
usermod -aG sudo polofit

# Testar login
su - polofit
```

### 4. Configurar SSH (Chaves Públicas)

No seu computador local:

```bash
# Gerar chave SSH (se não tiver)
ssh-keygen -t rsa -b 4096

# Copiar chave para VPS
ssh-copy-id polofit@seu-ip-vps
```

### 5. Desabilitar Login Root (Opcional, mas recomendado)

Edite `/etc/ssh/sshd_config`:

```bash
sudo nano /etc/ssh/sshd_config
```

Alterar:
```
PermitRootLogin no
PasswordAuthentication no
```

Reiniciar SSH:
```bash
sudo systemctl restart sshd
```

### 6. Configurar Firewall (UFW)

```bash
# Permitir SSH
sudo ufw allow OpenSSH

# Permitir HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Ativar firewall
sudo ufw enable

# Ver status
sudo ufw status
```

---

## Instalação do Docker

### 1. Instalar Docker

```bash
# Remover versões antigas
sudo apt remove docker docker-engine docker.io containerd runc

# Atualizar índice
sudo apt update

# Instalar dependências
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Adicionar chave GPG do Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Adicionar repositório
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Atualizar e instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verificar instalação
docker --version
```

### 2. Configurar Docker sem sudo

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Fazer logout e login novamente
# Ou executar:
newgrp docker
```

### 3. Testar Docker

```bash
docker run hello-world
```

Deve aparecer mensagem de sucesso.

---

## Preparação do Projeto

### 1. Clonar Repositório

```bash
# Navegar para diretório home
cd ~

# Clonar repositório (substitua pelo seu)
git clone https://github.com/seu-usuario/PoloFeedback.git
cd PoloFeedback
```

### 2. Verificar Dockerfile

O `Dockerfile` deve estar assim:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar projeto
COPY . .

# Coletar estáticos
RUN python manage.py collectstatic --noinput

# Expor porta
EXPOSE 8000

# Comando de execução
CMD ["gunicorn", "polofeedback.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### 3. Verificar docker-compose.yml

O `docker-compose.yml` deve estar assim:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: polofeedback_db
    environment:
      POSTGRES_DB: polofeedback
      POSTGRES_USER: polofit
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  web:
    build: .
    container_name: polofeedback_web
    command: gunicorn polofeedback.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://polofit:${DB_PASSWORD}@db:5432/polofeedback
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ALLOWED_HOSTS=${ALLOWED_HOSTS}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
```

---

## Configuração de Variáveis de Ambiente

### 1. Criar arquivo .env

```bash
nano .env
```

### 2. Adicionar variáveis

```bash
# Django
SECRET_KEY=gerar-uma-chave-secreta-aqui-usar-comando-python
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com.br,www.seu-dominio.com.br,seu-ip-vps

# Banco de Dados
DB_PASSWORD=senha-forte-aqui

# Google Gemini
GEMINI_API_KEY=sua-chave-gemini-aqui
GEMINI_MODEL=gemini-2.5-flash

# Senhas do Sistema (Use senhas fortes!)
DASHBOARD_MANAGER_PASSWORD=senha-forte-aqui
DASHBOARD_OWNER_PASSWORD=senha-forte-aqui
ADMIN_PASSWORD=senha-forte-aqui
```

### 3. Gerar SECRET_KEY

No seu computador local:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copie o resultado e cole no .env.

---

## Deploy com Docker Compose

### 1. Construir Imagens

```bash
docker-compose build
```

### 2. Executar Migrações

```bash
docker-compose run web python manage.py migrate
```

### 3. Criar Superusuário

```bash
docker-compose run web python manage.py createsuperuser
```

Siga as instruções para criar o usuário admin.

### 4. Iniciar Serviços

```bash
docker-compose up -d
```

### 5. Verificar Status

```bash
docker-compose ps
```

Todos os serviços devem estar "Up".

### 6. Verificar Logs

```bash
# Todos os logs
docker-compose logs

# Logs específicos
docker-compose logs web
docker-compose logs db
```

### 7. Testar Acesso

No navegador:
```
http://seu-ip-vps:8000
```

Deve carregar a aplicação.

---

## Configuração de Domínio e SSL

### 1. Comprar Domínio

Compre domínio em:
- Registro.br (para .com.br)
- Namecheap
- GoDaddy
- Cloudflare Registrar

### 2. Configurar DNS

No painel do registrador, aponte o domínio para o IP da VPS:

```
Tipo: A
Nome: @ (ou www)
Valor: seu-ip-vps
TTL: 3600 (ou padrão)
```

### 3. Instalar Nginx

```bash
sudo apt install nginx -y
```

### 4. Configurar Nginx

Criar arquivo de configuração:

```bash
sudo nano /etc/nginx/sites-available/polofeedback
```

Conteúdo:

```nginx
server {
    listen 80;
    server_name seu-dominio.com.br www.seu-dominio.com.br;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/polofit/PoloFeedback/staticfiles/;
    }
}
```

### 5. Ativar Configuração

```bash
sudo ln -s /etc/nginx/sites-available/polofeedback /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Instalar Certbot (SSL)

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 7. Obter Certificado SSL

```bash
sudo certbot --nginx -d seu-dominio.com.br -d www.seu-dominio.com.br
```

Siga as instruções. Escolha "Redirect" quando perguntado.

### 8. Renovação Automática

Certbot configura renovação automática. Verificar:

```bash
sudo certbot renew --dry-run
```

---

## Monitoramento e Manutenção

### 1. Monitorar Logs

```bash
# Docker logs
docker-compose logs -f web

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Reiniciar Serviços

```bash
# Reiniciar Docker Compose
docker-compose restart

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 3. Atualizar Aplicação

```bash
# Parar serviços
docker-compose down

# Pull do git
git pull origin main

# Reconstruir
docker-compose build

# Migrar (se necessário)
docker-compose run web python manage.py migrate

# Iniciar
docker-compose up -d
```

### 4. Backup do Banco de Dados

Criar script de backup:

```bash
nano ~/backup-db.sh
```

Conteúdo:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/polofit/backups"
mkdir -p $BACKUP_DIR

docker-compose exec -T db pg_dump -U polofit polofeedback > $BACKUP_DIR/backup_$DATE.sql

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete
```

Tornar executável:

```bash
chmod +x ~/backup-db.sh
```

Adicionar ao crontab:

```bash
crontab -e
```

Adicionar linha para backup diário às 3h:

```
0 3 * * * /home/polofit/backup-db.sh
```

---

## Backup e Segurança

### 1. Backup Automático

#### Banco de Dados

Usar script acima (crontab).

#### Arquivos Estáticos

```bash
tar -czf backups/static_$(date +%Y%m%d).tar.gz staticfiles/
```

#### Mídia (uploads)

```bash
tar -czf backups/media_$(date +%Y%m%d).tar.gz media/
```

### 2. Backup Off-site

Enviar backups para serviço externo:
- AWS S3
- Google Cloud Storage
- Dropbox
- Outro servidor

Exemplo com rclone:

```bash
rclone copy /home/polofit/backups remote:polofeedback-backups
```

### 3. Segurança Adicional

#### Atualizações Automáticas

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure -plow unattended-upgrades
```

#### Fail2Ban (Proteção contra brute force)

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

#### Monitoramento (Opcional)

- Uptime Robot (grátis)
- Pingdom
- New Relic
- Datadog

---

## Troubleshooting

### Erro: "Connection refused"

**Causa**: Serviço não está rodando ou porta errada.

**Solução**:
```bash
docker-compose ps
docker-compose logs web
```

### Erro: "Database connection refused"

**Causa**: Banco não iniciou ou credenciais erradas.

**Solução**:
```bash
docker-compose logs db
# Verificar .env
```

### Erro: "502 Bad Gateway"

**Causa**: Nginx não consegue conectar ao Docker.

**Solução**:
```bash
# Verificar se web está rodando
docker-compose ps web

# Verificar configuração Nginx
sudo nginx -t
```

### Erro: "SSL certificate expired"

**Causa**: Certificado não renovou.

**Solução**:
```bash
sudo certbot renew
sudo systemctl restart nginx
```

### Erro: "Out of memory"

**Causa**: VPS sem RAM suficiente.

**Solução**:
- Upgrade do plano VPS
- Adicionar swap
- Otimizar Docker (limitar recursos)

Adicionar swap:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Resumo de Comandos Úteis

### Docker

```bash
docker-compose up -d           # Iniciar
docker-compose down            # Parar
docker-compose restart         # Reiniciar
docker-compose logs -f         # Logs em tempo real
docker-compose ps              # Status
docker-compose exec web bash   # Acessar container
```

### Nginx

```bash
sudo systemctl restart nginx  # Reiniciar
sudo systemctl status nginx   # Status
sudo nginx -t                 # Testar configuração
```

### Sistema

```bash
sudo apt update && sudo apt upgrade -y  # Atualizar
df -h                          # Espaço em disco
free -h                        # Uso de RAM
htop                           # Monitoramento (instalar primeiro)
```

---

## Custo Estimado

### VPS (Mensal)
- Locaweb: R$ 50-100
- DigitalOcean: ~R$ 60
- AWS Lightsail: ~R$ 50
- Linode: ~R$ 50

### Domínio (Anual)
- .com.br: ~R$ 40 (Registro.br)
- .com: ~R$ 60-120

### Total Estimado
- **Mínimo**: R$ 90-120/mês
- **Recomendado**: R$ 120-150/mês

---

## Suporte

Para dúvidas:

- 📧 Email: marcos.paulo@email.com
- 📱 WhatsApp: (83) 98671-9438
- 🌐 Instagram: @polofitacademias

---

**Versão**: 1.0.0  
**Última atualização**: 2026-10-18  
**Desenvolvido por**: Marcos Paulo Santos Lira
