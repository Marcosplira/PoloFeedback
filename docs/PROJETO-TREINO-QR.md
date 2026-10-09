# Projeto Polo Fit — Treinos orientados por QR Code

## Proposta para apresentação à gerência

**Responsável pela proposta e desenvolvimento:** Marcos Paulo Santos Lira  
**Instituição:** Instituto Federal de Educação, Ciência e Tecnologia da Paraíba (IFPB), Campus Picuí — PB  
**Tecnologias previstas:** Python, Django, JavaScript, HTML, CSS e Tailwind CSS

> **Status do projeto:** já foi criado um MVP inicial dentro do Polo Feedback. A implementação cobre cadastro administrativo de aparelhos, exercícios e planos, QR Codes para impressão e visualização autenticada dos exercícios do próprio aluno. Ainda exige cadastro real, revisão profissional, permissões do Django Admin e validação num piloto antes de uso pela academia.

## Resumo executivo para apresentar à gerência

**Proposta:** criar um módulo web responsivo da Academia Polo Fit para o aluno escanear o QR Code de um aparelho, assistir a uma demonstração aprovada e, após autenticação, consultar o exercício e o plano individual elaborado pelo professor.

**Problema:** dúvidas sobre regulagem e execução, explicações repetidas, fichas perdidas ou desatualizadas e falta de padronização das orientações.

**Benefício esperado:** facilitar o acesso às orientações e apoiar o trabalho dos professores, mantendo o acompanhamento profissional. Os resultados devem ser medidos num piloto; não se promete redução de custos ou melhora de retenção antes de haver evidências.

**Pedido de decisão:** aprovar a etapa de descoberta e protótipo, indicar um gerente patrocinador e professores revisores, e escolher uma área pequena para o piloto. A programação, custos e prazo só devem ser confirmados depois de validar os requisitos e a infraestrutura.

**Importante:** trata-se de um MVP técnico para demonstração e validação. Não é uma implantação oficial nem substitui o acompanhamento do professor.

## MVP inicial já implementado

- Modelos para equipamento com identificador QR aleatório, exercício, plano por aluno e itens com séries, repetições, descanso e carga informada pelo professor.
- Cadastro e manutenção de aparelhos e exercícios pelo Django Admin, incluindo edição dos itens do plano dentro do próprio plano.
- Contas privadas de gerente recebem permissões mínimas para cadastrar/editar aparelhos e exercícios; exclusão continua reservada a um administrador.
- Página de QR Codes para impressão, acessível à equipe pelo Dashboard em **QR Treinos** ou diretamente em `/treinos/qrs/`.
- Página de apresentação do projeto e roteiro para iniciar o piloto, acessível pelo Dashboard em **Projeto Academia** (`/dashboard/projeto-treino/`).
- Rota do aparelho exige login; depois de autenticado, o aluno vê somente itens dos próprios planos ativos que correspondem àquele equipamento.
- Instruções gerais do aparelho, observações de segurança, orientações por exercício e link de vídeo externo.
- Contas sem permissão de gerência não acessam Dashboard, análise/chat de IA ou gerador de QR de avaliação.

Para iniciar a demonstração local, aplique `python manage.py migrate`, crie um administrador com `python manage.py createsuperuser` e siga o roteiro **Cadastrar o MVP de treinos por QR Code** no README. O aluno pode criar uma conta pela página `/cadastro/aluno/`; a equipe cria e revisa os planos. As contas privadas de gerente recebem permissões para cadastrar e editar aparelhos e exercícios, mas não para excluí-los pelo Admin. O domínio escolhido para produção é `https://app.polofitacademias.com.br`, mas ele ainda precisa ser conectado ao serviço de hospedagem e configurado no DNS. Gere os QRs somente depois de confirmar que o domínio abre com HTTPS, acessando a página `/treinos/qrs/` por esse endereço.

## 1. Problema a resolver

- O aluno pode ter dúvida sobre a regulagem e a execução correta dos aparelhos.
- O professor precisa explicar repetidamente instruções semelhantes.
- A ficha impressa pode ser esquecida, perdida ou ficar desatualizada.
- A academia precisa padronizar as orientações sem substituir o acompanhamento profissional.

## 2. Solução proposta

Cada aparelho terá um QR Code que abre uma página móvel com instruções daquele equipamento. Depois de entrar em sua conta, o aluno poderá consultar os exercícios e o plano de treino que um professor habilitado atribuiu a ele.

Uma orientação de exercício pode incluir:

- nome do exercício e do equipamento;
- vídeo próprio da academia ou vídeo de terceiro com autorização de uso;
- instruções de preparação, execução e encerramento;
- séries, repetições, intervalo e observações prescritas pelo professor;
- carga prescrita ou carga de referência sugerida e aprovada pelo professor, nunca calculada automaticamente pelo sistema;
- alertas de segurança e indicação para chamar o professor em caso de dúvida ou desconforto.

Funcionalidades adicionais podem ser avaliadas após a validação do MVP: marcar séries/exercícios como concluídos, cronômetro de descanso, histórico de treinos concluídos, favoritos, busca e filtros, alternativas de exercício previamente aprovadas pelo professor, acessibilidade (texto ampliado e vídeos legendados), aviso de treino desatualizado e retorno do aluno sobre a clareza da instrução. Esses recursos não devem alterar a prescrição profissional nem incentivar treino com dor.

O QR identifica a máquina, não a pessoa. As informações particulares do treino só ficam disponíveis após autenticação e verificação de que o plano pertence ao aluno autenticado.

## 3. Perfis e responsabilidades

| Perfil | Acesso proposto |
| --- | --- |
| Gerente/administrador | Gerencia unidades, máquinas, usuários e indicadores operacionais. |
| Professor | Cadastra exercícios e atribui ou atualiza treinos de seus alunos. |
| Aluno | Consulta o próprio plano e as instruções públicas da máquina. |

O sistema não deve permitir que um aluno consulte treinos de outra pessoa. Permissões e separação de dados devem ser testadas em cada endpoint, não apenas escondidas na interface.

## 4. Fluxo de uso

1. O gerente cadastra os equipamentos e associa um QR Code único a cada um.
2. Um profissional cadastra ou revisa as instruções e adiciona um vídeo autorizado.
3. O professor cria o plano individual, escolhe os exercícios e registra séries, repetições, intervalos e carga.
4. O aluno escaneia o QR Code do equipamento.
5. Se necessário, o aluno entra na conta; depois o sistema exibe as orientações da máquina e somente os itens daquele equipamento nos próprios planos ativos.
6. O aluno confere a orientação e realiza o exercício; dúvidas e desconfortos devem ser tratados com o professor.
7. O professor revisa o plano periodicamente e altera suas prescrições quando necessário.

## 5. Escopo recomendado para o primeiro MVP

**Incluído no MVP atual**

- cadastro de equipamentos, exercícios, categorias e vídeos;
- geração e impressão de QR Codes por máquina;
- login dos alunos e dos professores;
- plano individual com ordenação de exercícios;
- séries, repetições, intervalo, observações e carga prescrita;
- tela mobile-first com controles grandes, vídeo e instruções legíveis;
- estado atual do plano, data de atualização e professor responsável;
- cadastro e ativação/inativação de equipamento e exercício;
- registro do professor responsável no plano;
- testes de login, autorização e separação entre alunos.

**Próximas melhorias para piloto/versões posteriores**

- histórico de alterações do conteúdo e das prescrições;
- tela gerencial para monitorar conteúdo desatualizado e utilização;
- fluxos específicos para revisão/publicação do professor e configuração de permissões;
- acessibilidade do conteúdo, vídeos legendados e roteiro offline para ausência de celular/conexão.

**Deixar para versões posteriores**

- marcação de exercícios concluídos, cronômetro de descanso e histórico de sessões;
- busca, favoritos e alternativas previamente autorizadas pelo professor;
- lembretes internos configuráveis e resumo de progresso, sem exposição pública;
- integração com o sistema comercial/ERP da academia;
- pagamentos, agenda de aulas e chat entre professor e aluno;
- integração com relógios, sensores ou máquinas;
- recomendação automática de carga ou treino (não recomendada sem avaliação e validação profissional específicas);
- aplicativo nativo publicado nas lojas;
- notificações automáticas por WhatsApp.

## 6. Como organizar o projeto e preparar um piloto

### Etapa 1 — Aprovar o problema e o responsável

Converse com gerente, professores e alunos. Registre quais aparelhos geram mais dúvidas, como os treinos são entregues atualmente, quais informações cada perfil precisa e quem aprovará o conteúdo técnico. O código do MVP existe, mas a validação com pessoas da academia ainda precisa acontecer antes do piloto.

### Etapa 2 — Delimitar o piloto

Escolha em conjunto uma área e um conjunto pequeno de equipamentos para testar. Defina o que não fará parte do MVP e como será feito o suporte quando um QR estiver danificado ou um vídeo ficar indisponível.

### Etapa 3 — Validar os requisitos e a segurança

Confirme os papéis e permissões, os dados realmente necessários, a política de acesso e atualização dos planos e os procedimentos para alunos sem celular ou sem conexão. Não coloque nome, matrícula, diagnóstico, carga ou plano individual dentro do QR Code ou da URL pública.

### Etapa 4 — Validar o protótipo disponível

Desenhe no papel ou em ferramenta de prototipação as telas de login, leitura do QR, instrução do aparelho, plano do aluno e edição pelo professor. Peça que pessoas dos três perfis tentem realizar tarefas sem orientação.

### Etapa 5 — Preparar os vídeos e o conteúdo

Use demonstrações gravadas pela academia ou material cujo uso esteja autorizado. Next Fit e MFIT Personal podem servir como referências de experiência e organização do fluxo; não copie vídeos, telas, marca ou textos protegidos. Professores devem revisar e aprovar as instruções antes da publicação.

### Etapa 6 — Definir critérios de aceite

Antes do desenvolvimento, escreva como demonstrar que:

- QR inválido/inativo não revela informações privadas;
- aluno autenticado consulta apenas o próprio treino;
- professor autorizado consegue cadastrar e atualizar planos;
- o conteúdo funciona em telas de celular e conexões da academia;
- orientações podem ser atualizadas sem reimprimir o QR;
- o gerente sabe quem publicou ou alterou cada orientação.

### Etapa 7 — Estimar custo e aprovar o piloto

Apresente ao gerente as entregas, custos de hospedagem, domínio, produção/armazenamento de vídeo, suporte, operação e manutenção. Combine prazo, responsável por aprovação técnica, participantes do teste e como decidir a continuidade.

O MVP está implementado no código; antes de usar com alunos reais, aprove requisitos, protótipo, conteúdo e critérios de aceite com a gerência.

### Etapa 8 — Configurar, testar e avaliar em ciclos

Cadastre poucos equipamentos e conteúdos aprovados; crie contas de aluno e equipe com permissões mínimas; gere os QRs no domínio alcançável por celulares. Faça testes com contas de aluno, professor e gerente, incluindo tentativas de acesso indevido. Rode um piloto supervisionado, registre problemas e só então decida com a gerência se amplia o escopo.

## 7. Estrutura técnica sugerida

- **Django:** autenticação, permissões, cadastro, planos, QR Codes e interface administrativa.
- **HTML/CSS/Tailwind/JavaScript:** telas responsivas e interações no navegador.
- **PostgreSQL:** dados persistentes na publicação.
- **Armazenamento de mídia:** vídeos preferencialmente hospedados em serviço apropriado; o banco guarda metadados e links.
- **QR Code:** token aleatório não sequencial que aponta somente para o equipamento. Nunca codificar um identificador de aluno ou o conteúdo do plano.
- **Testes:** cobrir acesso anônimo, aluno, professor, gerente e tentativa de acesso cruzado aos planos.

Entidades candidatas: `Aluno`, `Professor`, `Equipamento`, `Exercicio`, `PlanoTreino`, `ItemPlano`, `VideoInstrucao` e `HistoricoPlano`. A modelagem final deve ser confirmada com os fluxos aprovados antes das migrações.

## 8. Segurança, saúde e LGPD

- Coletar somente dados necessários e explicar ao aluno a finalidade do tratamento.
- Definir base legal, aviso de privacidade, retenção e canal para solicitações do titular com apoio do responsável da academia.
- Limitar o acesso por função, registrar alterações e proteger sessões e credenciais.
- Não armazenar dados de saúde ou limitações físicas sem necessidade, justificativa, proteção e revisão apropriadas.
- Vídeos e instruções são material educativo aprovado pela academia; não substituem avaliação ou orientação presencial.
- A carga e o plano são definidos por profissional responsável. O sistema não deve sugerir cargas automaticamente no MVP.
- Remover ou substituir rapidamente conteúdo incorreto, equipamento interditado ou vídeo sem autorização.

## 9. WhatsApp — etapa futura, não incluída no MVP

O botão de contato atual abre uma conversa iniciada pela pessoa com a academia; ele não envia alertas automáticos ao gerente, professores ou alunos.

Para notificações automáticas, planejar uma integração com a WhatsApp Business Platform/API oficial, sujeita a cadastro, credenciais, regras e custos vigentes. O primeiro caso de uso recomendado é alertar o gerente sobre uma avaliação crítica com o mínimo de dados necessários. Antes de enviar mensagens a alunos ou funcionários, definir finalidade, consentimento/base legal, preferências de comunicação, modelos aprovados, opt-out, controle de acesso e trilha de auditoria. Não enviar automaticamente comentários pessoais ou dados do treino.

## 10. Indicadores para avaliar o piloto

- percentual de alunos que conseguem encontrar o exercício pelo QR;
- tempo para localizar e compreender as instruções;
- dúvidas que ainda precisam ser atendidas pelo professor;
- QR Codes e vídeos indisponíveis;
- satisfação de alunos e professores após o piloto;
- ocorrências de acesso indevido (meta: zero).

Definir uma linha de base e metas com a gerência antes do piloto. Não prometer retenção, economia ou resultado financeiro sem medir esses efeitos.
