# Projeto Polo Fit — Treinos orientados por QR Code

## Proposta para apresentação à gerência

**Responsável pela proposta e desenvolvimento:** Marcos Paulo Santos Lira  
**Instituição:** Instituto Federal de Educação, Ciência e Tecnologia da Paraíba (IFPB), Campus Picuí — PB  
**Tecnologias previstas:** Python, Django, JavaScript, HTML, CSS e Tailwind CSS

> Este é um módulo proposto para uma nova etapa. O sistema Polo Feedback existente ainda não cadastra treinos, máquinas ou alunos e não oferece instruções de exercícios por QR Code.

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
- carga definida pelo professor, sem cálculo ou prescrição automática pelo sistema.

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
5. A página explica a máquina e solicita login para mostrar o treino individual.
6. O aluno confere a orientação e realiza o exercício; dúvidas e desconfortos devem ser tratados com o professor.
7. O professor revisa o plano periodicamente e altera suas prescrições quando necessário.

## 5. Escopo recomendado para o primeiro MVP

**Incluir**

- cadastro de equipamentos, exercícios, categorias e vídeos;
- geração e impressão de QR Codes por máquina;
- login dos alunos e dos professores;
- plano individual com ordenação de exercícios;
- séries, repetições, intervalo, observações e carga prescrita;
- tela mobile-first com controles grandes, vídeo e instruções legíveis;
- histórico simples de alterações e identificação do profissional responsável;
- interface administrativa para ativar/inativar conteúdo desatualizado;
- testes de autenticação, autorização e privacidade entre contas.

**Deixar para versões posteriores**

- integração com o sistema comercial/ERP da academia;
- pagamentos, agenda de aulas e chat entre professor e aluno;
- integração com relógios, sensores ou máquinas;
- recomendação automática de carga ou treino;
- aplicativo nativo publicado nas lojas;
- notificações automáticas por WhatsApp.

## 6. Como iniciar antes de programar

### Etapa 1 — Aprovar o problema e o responsável

Converse com gerente, professores e alunos. Registre quais aparelhos geram mais dúvidas, como os treinos são entregues atualmente, quais informações cada perfil precisa e quem aprovará o conteúdo técnico.

### Etapa 2 — Delimitar o piloto

Escolha em conjunto uma área e um conjunto pequeno de equipamentos para testar. Defina o que não fará parte do MVP e como será feito o suporte quando um QR estiver danificado ou um vídeo ficar indisponível.

### Etapa 3 — Validar os requisitos e a segurança

Confirme os papéis e permissões, os dados realmente necessários, a política de acesso e atualização dos planos e os procedimentos para alunos sem celular ou sem conexão. Não coloque nome, matrícula, diagnóstico, carga ou plano individual dentro do QR Code ou da URL pública.

### Etapa 4 — Fazer protótipos

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

Só depois da aprovação dos requisitos, protótipos e critérios de aceite, iniciar a implementação e criar tarefas técnicas.

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
