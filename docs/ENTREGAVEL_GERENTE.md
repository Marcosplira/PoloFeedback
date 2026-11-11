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
- fila opcional de alertas de novas avaliações pelo WhatsApp Business

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
Com os alertas WhatsApp habilitados, a avaliação também entra em uma fila para envio separado pelo processador; o formulário não espera a API externa.

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

Esse recurso de IA é diferente do robô de testes: o gerente solicita o resumo ou faz uma pergunta, e a ferramenta responde com base nos dados disponíveis. Ela não acompanha o site continuamente, não detecta sozinha que uma página caiu e não executa correções. Sem uma chave Gemini válida, o sistema pode apresentar um resumo local baseado nos registros, identificado como tal.

Quando a integração Gemini está habilitada, o contexto inclui indicadores agregados, nomes e funções dos funcionários e textos livres recentes de avaliações/enquetes. Um comentário pode conter informação pessoal mesmo sem um campo de nome; por isso, a academia deve revisar a política de privacidade e orientar a equipe a não encaminhar dados identificáveis desnecessários.

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
- código de alertas WhatsApp preparado, mas desligado por padrão e ainda dependente da configuração do ambiente

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

### Como explicar as quatro telas do painel

#### 1. Treinos por QR Code — tela “Treinos”

Esta área organiza o piloto dos treinos digitais. A equipe pode abrir **Aparelhos e QR** para conferir os códigos dos equipamentos e **Novo plano** para cadastrar um treino individual.

Explique o fluxo mostrado na tela:

1. **O aluno escaneia:** o QR identifica o aparelho, não a pessoa nem o plano.
2. **O aluno entra na própria conta:** a autenticação protege os dados do treino.
3. **O aluno consulta a orientação:** vê os exercícios daquele aparelho que o professor incluiu em seus planos ativos, com séries, repetições, descanso e instruções cadastradas.

O checklist orienta a preparação do piloto: escolher a área e os aparelhos, pedir aos professores que revisem o conteúdo, cadastrar alunos de teste e avaliar os resultados. **Os quadrinhos desse checklist são apenas visuais e não salvam o progresso.** O desenho de celular também é uma ilustração: marcar séries como concluídas e guardar um histórico de execução ainda não faz parte deste MVP. O QR não substitui a orientação do professor, e o sistema não prescreve exercícios nem calcula cargas.

**Como dizer ao gerente:** “Podemos começar em uma área pequena. A equipe revisa os aparelhos e as orientações, alguns alunos testam o acesso pelo celular e, com o retorno deles e dos professores, decidimos se vale ampliar.”

#### 2. Compartilhar o Polo Feedback — tela “Divulgação”

O campo **Link atual** mostra o endereço da página inicial no domínio que está servindo o painel. **Compartilhar pelo WhatsApp** abre uma mensagem com esse endereço. O texto sugerido pode ser editado, copiado e compartilhado; as instruções ao lado dão ideias para uma publicação no Instagram.

Essa tela ajuda a divulgar o produto, mas **não publica conteúdo automaticamente no Instagram nem envia mensagens em massa**. Antes de compartilhar, confirme que o link abre para pessoas fora da rede da academia e que usa o endereço público HTTPS correto. Não divulgue endereços `localhost`, telas de erro, dados pessoais ou informações de alunos.

**Como dizer ao gerente:** “Esta área facilita copiar o link e apresentar o sistema. A mensagem é revisável antes do envio; a divulgação em redes sociais continua sendo feita pela equipe.”

#### 3. QR Codes para avaliação — tela “QR Codes”

Esta página cria cartazes para receber avaliações, não os QR Codes dos aparelhos do módulo de treinos. A equipe escolhe um dos locais disponíveis — como musculação, academia principal, treinamento funcional, Pilates, vestiários, recepção ou enquete — e confere a prévia do cartaz. Também pode informar um local personalizado.

Nos locais de avaliação, o QR abre o formulário com o local já indicado. A opção **Enquete de aulas** abre a enquete. O aluno pode apontar a câmera do celular e responder no navegador, sem baixar um aplicativo.

**Como dizer ao gerente:** “Podemos colocar um cartaz em cada ponto da academia. Assim, a resposta já indica o local escolhido no QR e fica mais fácil comparar as opiniões por ambiente.”

#### 4. Imprimir, salvar e distribuir os cartazes

Na prévia do QR de avaliação, os botões permitem:

- **Imprimir cartaz:** abrir a impressão do navegador, adequada para papel A4.
- **Salvar imagem:** baixar o arquivo PNG do QR para uso digital ou impressão.
- **Copiar link:** copiar o endereço de destino para compartilhar ou testar.

Depois de imprimir, coloque o cartaz em um ponto visível e seguro, próximo ao local correspondente. Faça um teste com um celular antes de fixá-lo. Os QRs são gerados com o domínio atualmente aberto no painel; para uso fora da rede, confirme que o endereço é público e HTTPS. O desempenho dos cartazes pode ser acompanhado pelo painel, filtrando as avaliações pelo local.

#### Diferença entre os dois tipos de QR

| QR Code | Para que serve | O que acontece ao ler |
| --- | --- | --- |
| QR de avaliação | Ouvir a opinião sobre um local ou abrir a enquete | Abre o formulário ou a enquete no navegador |
| QR de treino | Identificar um aparelho de musculação | Solicita o acesso à conta e mostra somente os exercícios daquele aparelho que estão nos planos ativos do aluno |

#### Fala curta para apresentar as telas

> “O painel tem três usos principais: acompanhar e preparar o piloto de treinos por aparelho, gerar cartazes de avaliação para os diferentes locais e compartilhar o endereço público do sistema. O QR de avaliação abre um formulário rápido; o QR de treino identifica um equipamento e exige que o aluno entre na própria conta. Vamos validar os cartazes e o conteúdo dos treinos com a equipe antes de ampliar o uso.”

---

## Próximos passos de evolução

A solução já está funcional e pronta para apresentação, e pode evoluir para:
- evolução do MVP de treinos por QR Code, com piloto supervisionado
- configuração e teste controlado dos alertas WhatsApp já preparados antes de ativá-los
- alertas para pendências críticas
- relatórios por unidade
- exportação de dados para PDF
- integração com CRM ou painel interno
- app mobile mais completo

### Módulo de treinos por QR Code

O MVP já permite que o aluno escaneie o QR Code de um aparelho, entre na própria conta e consulte os exercícios correspondentes aos seus planos ativos. O professor define séries, repetições e carga; o sistema não prescreve exercícios automaticamente. Antes do uso oficial, ainda é necessário revisar o conteúdo, as permissões e os procedimentos do piloto. Consulte [PROJETO-TREINO-QR.md](./PROJETO-TREINO-QR.md).

### WhatsApp

O botão de contato continua abrindo uma conversa manual. Separadamente, foi preparado um processador de alertas que pode encaminhar cada nova avaliação pública ao número da gerência usando a WhatsApp Business Cloud API oficial. O recurso fica **desligado por padrão** e não está publicado/ativado automaticamente.

Quando ativo, o aviso inclui nota, categoria, aula coletiva (quando houver), nome (se informado), comentário e link do painel. O formulário avisa o aluno sobre esse encaminhamento antes do envio. O processamento ocorre em segundo plano por comando agendado, para que uma indisponibilidade da Meta não impeça o registro da avaliação. A base local guarda o estado e o identificador técnico do envio, não uma cópia extra do comentário.

**O que falta antes de usar em produção:**

1. A academia deve revisar a política de privacidade, porque nome e comentário passam pelo serviço da Meta e são compartilhados no aparelho/número de gestão configurado.
2. Na Meta, confirmar o número remetente, credenciais e versão suportada da API; o destinatário deve ser diferente do remetente.
3. Criar e aprovar o modelo `polo_feedback_nova_avaliacao` em português, com sete parâmetros no corpo, na ordem documentada no README.
4. Cadastrar os segredos e `SITE_PUBLIC_URL` nas variáveis do ambiente de hospedagem, aplicar as migrações e agendar o comando `python manage.py enviar_alertas_whatsapp --limit 25`.
5. Testar primeiro em ambiente controlado. O status de sucesso indica que a API aceitou a mensagem, não que ela foi entregue; a confirmação final exigiria webhook, ainda não incluído.

O comando não é executado pelo HTML e os testes usam apenas chamadas simuladas; nenhuma mensagem real foi enviada. A opção `--retry-failed` pode duplicar um alerta em caso de resultado ambíguo e deve ser usada apenas após conferência manual.

### Robô de testes com apoio de IA — proposta segura

**O que está ativo:** o robô técnico faz verificações HTTPS de leitura nas páginas públicas e o GitHub Actions executa testes automatizados para a seleção e o registro de aulas coletivas. Uma execução pode ser iniciada manualmente; o monitor público também está agendado. Os resultados ficam nas execuções do GitHub Actions. Esse robô não faz login, não envia avaliações e não altera dados.

**O que ainda não está integrado:** a IA do Gemini não recebe os alertas do monitor e não analisa automaticamente o código, os logs ou as falhas dos testes. A IA atual é um recurso separado, iniciado pelo gerente.

Uma próxima etapa pode fazer o robô, quando falhar, produzir um resumo técnico com a página verificada, horário, resposta HTTP e duração; a IA poderia então sugerir causas e passos de investigação. A recomendação seria apenas uma hipótese para a equipe revisar — não uma confirmação de bug nem uma ordem para alterar o sistema.

**Salvaguardas recomendadas antes de conectar IA ao robô:**

- enviar somente metadados técnicos necessários; remover cookies, tokens, senhas, endereço IP, conteúdo de formulários e dados pessoais;
- usar uma chave de API armazenada como segredo no provedor, nunca no código, nos logs ou em mensagens;
- limitar o uso a falhas de teste/monitoramento e identificar claramente a resposta como produzida por IA;
- exigir aprovação humana antes de abrir ou alterar dados operacionais, corrigir código, publicar uma versão ou avisar alunos;
- registrar a falha e a decisão da equipe, sem armazenar dados sensíveis no relatório.

**Evolução sugerida:** primeiro ampliar os testes automatizados da avaliação por modalidade e das telas móveis; depois avaliar um alerta técnico; somente após revisão de privacidade e custos, considerar resumo assistido por IA. Não recomendamos um robô que faça login como gerente, altere avaliações, mude senhas, edite treinos ou publique código sem supervisão.

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

- Rua Antônio dos Santos, nº 62, Bairro Cenecista, Picuí - PB, 
- CEP 58187-000
- Telefone/WhatsApp: (83) 98671-9438
- Instagram: [@polofitacademias](https://www.instagram.com/polofitacademias/)
- Horários: segunda a sexta, 05h às 22h; sábado, 11h às 19h.

**Software e proposta:** Marcos Paulo Santos Lira
