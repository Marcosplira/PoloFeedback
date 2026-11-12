# 📖 GUIA DO USUÁRIO — PLATAFORMA POLO FIT
**Academia Polo Fit — Picuí, PB**  
*Manual Operacional Ilustrado e Passo a Passo*

---

## 1. INTRODUÇÃO & ACESSO AO SISTEMA

A plataforma **Polo Feedback & Treinos** pode ser acessada de qualquer smartphone, tablet ou computador pelo navegador web.
Além disso, ela funciona como um **PWA (Progressive Web App)**: ao acessar o site pelo celular, basta tocar em *"Instalar no celular"* para adicionar o ícone da Polo Fit diretamente na tela inicial, funcionando como um aplicativo nativo.

* **Endereço Oficial em Produção**: `https://polofeedback.pythonanywhere.com/`
* **Formulário de Avaliação**: `https://polofeedback.pythonanywhere.com/avaliar/`
* **Área da Equipe**: `https://polofeedback.pythonanywhere.com/dashboard/`
* **Treinos do Aluno**: `https://polofeedback.pythonanywhere.com/treinos/meus/`
* **Painel Administrativo**: `https://polofeedback.pythonanywhere.com/admin/`

---

## 2. GUIA DO ALUNO

### 2.1. Como Consultar o Treino no Aparelho (Via QR Code)
1. No salão de musculação, vá até o equipamento que deseja utilizar (ex: *Leg Press 45°*).
2. Abra a câmera do celular e aponte para o **QR Code** colado no aparelho.
3. Toque no link que surge na tela.
4. Entre com sua conta de aluno. O QR identifica o aparelho, não identifica você nem contém seu plano.
5. O sistema procura os exercícios daquele aparelho nos seus planos ativos e mostra somente os que o professor atribuiu à sua conta:
   - Nome do exercício e do aparelho.
   - Séries, repetições e intervalo de descanso prescritos.
   - Carga orientada, quando cadastrada pelo professor.
   - Instruções, observações e vídeo demonstrativo, quando disponíveis.
6. Siga a orientação profissional. Em caso de dúvida, desconforto ou diferença entre a tela e a orientação presencial, peça ajuda ao professor.

**Importante:** nesta versão, o sistema exibe a prescrição, mas não marca séries como concluídas nem guarda um histórico de execução. Ele não calcula carga ou treino automaticamente.

### 2.2. Como Fazer uma Avaliação de Atendimento
1. Aponte a câmera para os cartazes espalhados pela academia (Recepção, Salão de Musculação, Vestiários).
2. Escolha sua nota de **1 a 5 estrelas**.
3. Selecione a categoria da sua opinião (ex: *Equipamentos, Climatização, Limpeza, Atendimento*).
   - Para avaliar uma aula coletiva, escolha **Aulas Coletivas** e depois selecione a modalidade, como *Spinning* ou *Dança*.
4. *(Opcional)* Escreva um comentário sincero ou deixe um elogio nominal a um colaborador.
5. Se quiser, informe seu nome. Ele será visto apenas pela equipe autorizada; deixe o campo em branco para não se identificar.
6. Clique em **Enviar Avaliação**. O processo leva menos de 1 minuto.

### 2.3. Como Participar da Enquete de Novas Aulas
1. Acesse o menu **Enquete** na página inicial ou pelo QR Code da pesquisa.
2. Responda às 5 perguntas rápidas sobre preferências de aulas coletivas (Cross, Pilates, Spinning, Dança).
3. Indique os melhores horários para sua rotina.
4. Envie suas respostas para a gerência planejar as próximas grades horárias.

### 2.4. Como consultar opções de planos
1. Na página inicial, abra **Planos que se encaixam no seu estilo de vida**.
2. Escolha um único plano para consultar. As opções adicionais ficam dentro de **Ver outras opções de planos**.
3. Use o botão para perguntar sobre esse plano à recepção pelo WhatsApp.

Essa seleção serve apenas para iniciar uma conversa. Ela não faz matrícula, não reserva vaga e não confirma a contratação de nenhum plano.

---

## 3. GUIA DO PROFESSOR / INSTRUTOR

### 3.1. Como Montar um Novo Plano de Treino para um Aluno
1. Faça login com seu usuário da equipe.
2. Acesse a **Área da Equipe** no topo da página e clique em **Treinos** (`/treinos/gestao/`).
3. Clique no botão **➕ Novo plano**.
4. Preencha os campos principais:
   - **Nome do Plano**: ex: *Treino A - Hipertrofia Pernas & Glúteos*.
   - **Aluno**: Selecione o aluno cadastrado na lista suspensa.
   - **Professor Responsável**: Selecione o seu nome.
   - **Observações Gerais**: Orientações de aquecimento ou restrições médicas.
   - Marque a caixa **Ativo**.
5. Na seção **Exercícios do Plano**:
   - Selecione o **Exercício / Aparelho**.
   - Defina as **Séries**, **Repetições**, **Carga** (kg) e **Tempo de Descanso** (segundos).
   - Escreva uma instrução curta de postura (ex: *"Não travar os joelhos na extensão máxima"*).
   - Se desejar incluir mais exercícios, clique em **+ Adicionar outro exercício**.
6. Clique no botão **Salvar plano de treino**. O aluno já poderá consultar imediatamente.

### 3.2. Como Editar ou Atualizar Cargas de um Treino
1. Na lista de planos em `/treinos/gestao/`, localize o aluno desejado.
2. Clique no botão **Editar plano**.
3. Altere as cargas, repetições ou substitua exercícios conforme a evolução do aluno.
4. Clique em **Salvar plano de treino**.

### 3.3. Como entender a demonstração de treinos por QR Code

O QR Code funciona como uma etiqueta digital do equipamento. Por exemplo, o código do Leg Press identifica essa máquina. Depois que o aluno entra com a própria conta, o sistema verifica os planos ativos atribuídos a ele e apresenta os exercícios vinculados àquele aparelho. Outro aluno que escaneie o mesmo código só verá os itens do próprio plano.

A equipe cadastra aparelhos e exercícios, e o professor monta o plano individual com séries, repetições, descanso, carga e observações. A página **Projeto da Academia PoloFit**, no painel da equipe, explica esse fluxo e apresenta o roteiro para um piloto.

O módulo atual é um MVP para demonstração: não calcula cargas, não registra séries concluídas e não substitui a orientação do professor. Antes de usar oficialmente, a academia deve cadastrar conteúdo real, revisar as instruções e vídeos com os profissionais e testar o fluxo com um grupo pequeno.

---

## 4. GUIA DO GERENTE GERAL

### 4.1. Como Acompanhar o Painel Executivo (Dashboard)
1. Acesse `/dashboard/`.
2. No topo, visualize em cartões destacados:
   - **Nota Média (NPS)** da academia de 1.0 a 5.0.
   - **Total de Avaliações** recebidas no período.
   - **Total de Elogios** e **Total de Reclamações**.
3. Na seção **"Para Resolver"**:
   - Acompanhe cada feedback pendente.
   - Altere o status de cada item para *Em análise* ou *Resolvido* após tomar a providência necessária.
4. Clique em **"Diagnóstico Inteligente com IA"** para receber um resumo executivo gerado automaticamente pelo Google Gemini, destacando pontos críticos e planos de ação.

### 4.2. Como Gerenciar Usuários, Funcionários e Alunos
1. Acesse o **Admin do Django** (`/admin/`) através do botão no topo do painel executivo.
2. Na seção **Autenticação e Autorização > Usuários**:
   - Para cadastrar um novo aluno: clique em **Adicionar Usuário**, defina username e senha.
   - Associe o usuário ao grupo **Alunos** para garantir que ele só acesse a área do aluno.
3. Na seção **Feedback > Funcionários**:
   - Cadastre os colaboradores (professores, recepcionistas, gestores) para que seus nomes apareçam nos relatórios e nos formulários de avaliação.
4. Na seção **Feedback > Equipamentos**:
   - Cadastre novas máquinas com nome e localização (ex: *Crossover - Musculação*). O QR Code do aparelho é gerado automaticamente pelo sistema.
