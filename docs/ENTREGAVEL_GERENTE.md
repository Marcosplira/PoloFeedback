# Entregável para o Gerente — Polo Feedback

## Visão geral do software

O Polo Feedback é um sistema digital pensado para transformar a forma como a academia gerencia a experiência dos alunos. Em vez de depender apenas de reclamações informais, a gestão passa a contar com uma plataforma organizada, rápida e profissional para coletar, analisar e responder ao feedback dos clientes.

O sistema foi desenhado para conectar três momentos importantes:
- avaliação do cliente
- acompanhamento da gestão
- apoio inteligente da IA para decisões

A solução reúne:
- formulário de avaliação rápido e responsivo
- dashboard executivo para a gestão
- análise com inteligência artificial
- geração automática de QR Code
- organização por status e filtros
- chatbot para suporte à decisão do gerente

---

## Como funciona o software

### 1. Cliente avalia em poucos segundos
O aluno entra na página de avaliação, escolhe a categoria e envia sua opinião em um processo simples. O formulário contempla:
- nota de 1 a 5
- categorias de avaliação
- tipo de feedback
- comentário opcional
- funcionário avaliado, quando necessário
- localização do ponto de coleta

### 2. Os dados entram no sistema
As respostas são armazenadas com organização automática e ficam disponíveis para análise pela gestão.

### 3. O gerente acompanha o desempenho
No painel administrativo, o gerente consegue visualizar:
- total de avaliações
- média geral
- elogios e reclamações
- ranking dos funcionários
- categoria mais citada
- status das pendências
- filtros por período, setor, tipo e colaborador

### 4. A IA ajuda a interpretar a operação
O sistema gera um resumo executivo para apoiar a gestão. Também existe um chatbot que pode responder perguntas como:
- quais áreas estão mais elogiadas?
- o que está gerando reclamação?
- quem está sendo melhor avaliado?
- o que a equipe deve melhorar?

### 5. O QR Code automatiza a coleta
A academia pode imprimir QR Codes em pontos estratégicos. Quando o aluno escaneia, o sistema já direciona para a avaliação correta e registra a localização automaticamente.

---

## Benefícios para a academia

### Benefícios operacionais
- gestão mais organizada das avaliações
- identificação rápida de problemas recorrentes
- priorização de ações corretivas
- acompanhamento visual do que está pendente

### Benefícios estratégicos
- melhoria contínua da experiência do cliente
- tomada de decisão com base em dados reais
- atenção mais profissional ao atendimento
- fortalecimento da reputação da academia

### Benefícios financeiros
- oportunidade de acompanhar insatisfações antes que se agravem
- indicadores para avaliar tendências de satisfação e possíveis impactos
- melhora na percepção da marca
- apoio a decisões que impactam operação e produtividade

> Retenção, economia e retorno financeiro são resultados a medir em piloto; não são garantidos apenas pela implantação do sistema.

---

## Fluxo principal de uso

1. O aluno escaneia um QR Code na academia.
2. O sistema direciona para a avaliação.
3. A opinião é registrada no banco de dados.
4. O gerente acessa o painel principal.
5. O dashboard exibe métricas e feedbacks.
6. A IA gera o resumo executivo e responde dúvidas.
7. A gestão toma medidas de melhoria e reconhecimento.

---

## Funcionalidades implementadas

### Página inicial e avaliação
- formulário responsivo para celular
- experiência simples e profissional
- destaque para avaliação e painel do gerente
- apresentação moderna para o cliente

### Dashboard do gerente
- indicadores principais
- gráficos por categoria e nota
- filtros inteligentes
- ranking dos colaboradores
- modal com detalhes das avaliações
- alteração de status com organização da operação

### IA e chatbot
- resumo executivo de desempenho
- suporte para perguntas do gerente
- resposta em linguagem natural
- diagnóstico rápido da operação da academia

### QR Code
- geração automática por local
- uso em recepção, vestiários, recepção e outros setores
- facilidade para captar feedback em pontos estratégicos

### Segurança e produção
- ambiente e configuração mais seguros
- uso de variáveis de ambiente
- proteção de dados e cookies
- estrutura mais adequada para deploy profissional

---

## Como apresentar ao gerente

Ao mostrar o software ao gerente, o foco da apresentação deve ser este:

### 1. O software resolve um problema real
A academia precisa saber como os alunos estão percebendo a experiência, e isso pode ser transformado em ação.

### 2. Ele reduz a dependência de reclamações informais
O sistema organiza tudo em um só lugar.

### 3. Ele ajuda a tornar a gestão mais objetiva
O gerente deixa de “adivinhar” e passa a decidir com dados.

### 4. Ele organiza o acompanhamento
Problemas e elogios passam a ser monitorados com mais clareza.

### 5. Ele é escalável
O sistema pode evoluir para novas unidades, alertas, relatórios e integração com outras ferramentas.

---

## Demonstração prática recomendada

Durante a apresentação, o gerente pode ver:
- a página inicial funcionando
- a avaliação do cliente sendo enviada
- o painel mostrando resultados automáticos
- os gráficos e filtros em uso
- a IA gerando análise
- o chatbot respondendo perguntas sobre o negócio

Essa sequência transmite muito bem o valor do produto e facilita a compreensão do software como uma solução de gestão, e não apenas um formulário.

---

## Próximos passos de evolução

A solução já está funcional e pronta para apresentação, e pode evoluir para:
- evolução do MVP de treinos por QR Code, com piloto supervisionado
- notificações automáticas por WhatsApp Business API oficial, após aprovação
- alertas para pendências críticas
- relatórios por unidade
- exportação de dados para PDF
- integração com CRM ou painel interno
- app mobile mais completo

### Próximo projeto: treinos por QR Code

O aluno poderá escanear o QR Code de uma máquina, autenticar-se e consultar apenas o próprio treino e as instruções aprovadas pelo professor. A carga, as séries e as repetições serão definidas pelo profissional; o sistema não deve prescrever exercícios automaticamente. É necessário validar requisitos, segurança, conteúdo autorizado, custos e piloto antes de iniciar a programação. Consulte [PROJETO-TREINO-QR.md](./PROJETO-TREINO-QR.md).

### WhatsApp

O botão de contato do sistema abre uma conversa iniciada pela pessoa com a academia. Ele não envia notificações automáticas. Para avisos automáticos, será necessária integração futura com a WhatsApp Business API, aprovação da academia, análise de custos e definição de preferências de comunicação e privacidade.

---

## Módulo Polo Fit Treinos por QR Code

> **Status:** MVP inicial implementado no código; falta cadastrar conteúdo real, revisar permissões e validar um piloto com a academia antes de uso oficial.

### Desafio da rotina

Alunos podem ter dúvidas sobre os aparelhos e a execução dos exercícios. Professores repetem orientações, enquanto fichas impressas podem ser esquecidas ou ficar desatualizadas. A proposta é facilitar a consulta sem substituir o professor nem automatizar prescrição de treino.

### Como funciona o MVP

1. A equipe cadastra o aparelho, instruções gerais e observações de segurança.
2. A equipe cadastra exercícios associados ao equipamento e adiciona instruções e link de vídeo autorizado.
3. O professor ou gerente cria um plano para o usuário/aluno e inclui séries, repetições, descanso e carga orientada.
4. A equipe imprime um QR Code que contém apenas um identificador aleatório do equipamento.
5. O aluno escaneia o código e entra em sua conta para ver as instruções e apenas os exercícios daquele aparelho que estão em seus próprios planos ativos.

### Recursos sugeridos

**Implementado:** cadastro de aparelhos e exercícios no Django Admin; QR Code imprimível; links de vídeo e instruções; login; plano individual com séries, repetições, descanso e carga preenchida pelo professor; verificação de titularidade do plano; interface adaptada ao celular; testes de privacidade.

**Possíveis melhorias após o piloto:** marcar séries concluídas, cronômetro de descanso, histórico de treinos, favoritos, busca, alternativas autorizadas pelo professor, legenda e controles de acessibilidade, lembretes internos configuráveis e pesquisa breve sobre clareza das instruções.

### O que precisa ser aprovado antes do piloto real

- gerente patrocinador, professor(es) responsáveis pela revisão e área/equipamentos do piloto;
- perfis de acesso, dados necessários, aviso de privacidade e retenção;
- autoria/licença dos vídeos e aprovação das instruções;
- alternativa de atendimento para aluno sem celular ou sem conexão;
- custo de hospedagem e mídia, operação, manutenção e suporte;
- metas do piloto, por exemplo: alunos que encontram a instrução, clareza do conteúdo, dúvidas recorrentes e QR/vídeos indisponíveis.

O código do MVP já existe. O próximo passo é cadastrar uma amostra de conteúdo aprovado, entrevistar os perfis, validar o fluxo no protótipo/página e executar um piloto pequeno supervisionado. Estime prazo e investimento das próximas melhorias depois de validar o escopo e as condições técnicas. Não se deve prometer economia, retenção ou resultados de saúde sem avaliação apropriada.

### Texto curto para apresentar ao gerente

> “Preparei um MVP de treinos por QR Code para a Polo Fit. A equipe cadastra aparelhos e vídeos autorizados; o aluno entra com sua conta e vê apenas os exercícios daquele aparelho que pertencem ao próprio plano. O professor define séries, repetições e carga — o sistema não prescreve automaticamente. Proponho validarmos o conteúdo e as permissões, escolhermos uma área pequena e fazermos um piloto supervisionado antes de decidir as próximas melhorias e investimentos.”

O escopo detalhado, as etapas de descoberta e desenvolvimento, os riscos de privacidade e os critérios de piloto estão em [PROJETO-TREINO-QR.md](./PROJETO-TREINO-QR.md).

---

## Conclusão

O Polo Feedback é uma ferramenta prática, moderna e estratégica para a gestão da academia. Ele permite que a empresa entenda melhor sua operação, reduza ruídos, valorize os pontos fortes e tenha um processo mais profissional para atender clientes.

Com dashboard, QR Code, IA e chatbot, o sistema deixa claro que a academia tem uma solução inteligente para acompanhar a experiência do cliente e agir com mais rapidez e qualidade.

---

## Mensagem final para apresentação

“Com o Polo Feedback, a academia organiza os feedbacks para ouvir os alunos, analisar temas recorrentes e acompanhar as ações de melhoria.”

---

## Contato e autoria

**Academia Polo Fit**
Rua Antônio dos Santos, nº 62, Bairro Cenecista, Picuí - PB, CEP 58187-000
Telefone/WhatsApp: (83) 98671-9438
Instagram: [@polofitacademias](https://www.instagram.com/polofitacademias/)
Horários: segunda a sexta, 05h às 22h; sábado, 11h às 19h.

**Software e proposta:** Marcos Paulo Santos Lira

- Tecnologia em Sistemas para Internet — Tecnólogo, IFPB, Campus Picuí — PB; concluído em 2026.
- Técnico em Eletrônica — Subsequente, IFPB, Campus Picuí — PB.
- Técnico em Informática, IFPB, Campus Picuí — PB.
