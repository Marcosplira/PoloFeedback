# Revisão técnica e de produto — Polo Feedback

## Resumo

O repositório contém um produto web Django para coletar feedback, exibir avaliações e uma enquete, gerar QR Codes e apoiar a gestão com um dashboard e recursos de IA. Esta revisão distingue a base existente das propostas futuras; configurações de deploy, por si só, não comprovam que um serviço foi publicado ou validado em produção.

## Melhorias implementadas nesta revisão

- Separação da página inicial e da página de avaliação para os links terem destinos distintos.
- Inclusão de endereço, telefone, conversa manual por WhatsApp e autoria/créditos no rodapé.
- Remoção da criação/rotação de usuário com senha padrão durante o build. O gerente deve criar uma conta individual.
- Imagem Docker executada como usuário sem privilégios de root; Compose exige segredo e senha de banco definidos e usa volume persistente para mídia, sem mascarar os estáticos coletados.
- Documentação e slides agora distinguem o sistema existente das propostas de treino por QR Code e notificações automáticas.

## Limitação de validação do ambiente

Os testes Django devem ser executados no ambiente Python do projeto. Docker/Compose não está disponível no ambiente desta revisão; portanto, a imagem e a configuração Compose ainda precisam ser validadas por `docker compose config`, build e inicialização em uma máquina com Docker.

## Próximas melhorias prioritárias

### 1. Preparar a operação antes da publicação

- Configurar segredos, HTTPS, domínio, hosts, banco de produção, backups e recuperação.
- Criar contas pessoais e validar permissões de cada perfil.
- Definir responsáveis por triagem e resolução, e política de acesso e retenção de feedback.
- Fazer teste de aceitação com gerente, funcionários e alunos antes de divulgar QR Codes.

### 2. Melhorar análise e acompanhamento

- Conferir filtros, contagens e relatórios com amostras controladas.
- Registrar tempos de resposta e resolução e acordar metas mensuráveis.
- Avaliar atualização automática do dashboard somente se a operação precisar.
- Reduzir o acoplamento do módulo de views gradualmente com testes de caracterização.

### 3. Planejar o módulo de treinos separado

Treinos por aparelho ainda não existem no sistema atual. Validar fluxos, papéis, conteúdo e um piloto antes de programar. Proteger planos individuais por autenticação/autorização, manter QR Codes sem dados pessoais, usar vídeos próprios ou autorizados e deixar séries/carga sob responsabilidade profissional. Detalhes: [PROJETO-TREINO-QR.md](./PROJETO-TREINO-QR.md).

### 4. Planejar WhatsApp automático de forma segura

O link existente abre conversa manual. Notificações futuras dependem de WhatsApp Business API oficial, aprovação, custos, credenciais, consentimento/preferências, minimização de conteúdo e auditoria. Não enviar mensagens a alunos sem uma base apropriada e fluxo de opt-out.

### 5. Melhorias técnicas adicionais

- revisar validação, tamanho e tipo de uploads de fotos;
- configurar monitoramento de erros e logs sem dados pessoais desnecessários;
- revisar limitação e tempo limite das chamadas externas da IA;
- planejar política de atualização de dependências e execução de verificações de segurança;
- confirmar requisitos de acessibilidade e desempenho em celulares com usuários reais.

## Critérios de prontidão para uso oficial

- validação da configuração Docker e/ou do ambiente de hospedagem;
- testes de acesso sem autenticação e por cada perfil;
- teste de restauração de backup e persistência de mídia;
- política de privacidade e canal de contato publicados;
- domínio e HTTPS confirmados;
- critérios e responsáveis pela operação aprovados pela gerência.

Metas de retenção, economia e retorno financeiro precisam de baseline e medição; não devem ser prometidas com base apenas na existência do software.
