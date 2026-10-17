# 📖 GUIA DO USUÁRIO — PLATAFORMA POLO FIT
**Academia Polo Fit — Picuí, PB**  
*Manual Operacional Ilustrado e Passo a Passo*

---

## 1. INTRODUÇÃO & ACESSO AO SISTEMA

A plataforma **Polo Feedback & Treinos** pode ser acessada de qualquer smartphone, tablet ou computador pelo navegador web.
Além disso, ela funciona como um **PWA (Progressive Web App)**: ao acessar o site pelo celular, basta tocar em *"Instalar no celular"* para adicionar o ícone da Polo Fit diretamente na tela inicial, funcionando como um aplicativo nativo.

* **Endereço Oficial em Produção**: `https://polofeedback.onrender.com/`
* **Área da Equipe**: `https://polofeedback.onrender.com/dashboard/`
* **Área do Aluno**: `https://polofeedback.onrender.com/aluno/`
* **Painel Administrativo**: `https://polofeedback.onrender.com/admin/`

---

## 2. GUIA DO ALUNO

### 2.1. Como Consultar o Treino no Aparelho (Via QR Code)
1. No salão de musculação, vá até o equipamento que deseja utilizar (ex: *Leg Press 45°*).
2. Abra a câmera do celular e aponte para o **QR Code** colado no aparelho.
3. Toque no link que surge na tela.
4. Caso ainda não esteja conectado, faça login com seu **usuário** e **senha** fornecidos pela academia.
5. O sistema identifica instantaneamente o aparelho e exibe na sua tela:
   - Nome do exercício recomendado para seu nível.
   - Quantidade de séries e repetições (ex: `3 x 12`).
   - Carga prescrita pelo professor responsável.
   - Tempo de descanso recomendado com contagem.
   - Dica de postura e execução correta gravada pelo seu professor.
6. Ao terminar cada série, clique em **✓ Série Feita** para registrar seu progresso.

### 2.2. Como Fazer uma Avaliação de Atendimento
1. Aponte a câmera para os cartazes espalhados pela academia (Recepção, Salão de Musculação, Vestiários).
2. Escolha sua nota de **1 a 5 estrelas**.
3. Selecione a categoria da sua opinião (ex: *Equipamentos, Climatização, Limpeza, Atendimento*).
4. *(Opcional)* Escreva um comentário sincero ou deixe um elogio nominal a um colaborador.
5. Clique em **Enviar Avaliação**. O processo leva menos de 1 minuto e é totalmente anônimo.

### 2.3. Como Participar da Enquete de Novas Aulas
1. Acesse o menu **Enquete** na página inicial ou pelo QR Code da pesquisa.
2. Responda às 5 perguntas rápidas sobre preferências de aulas coletivas (Cross, Pilates, Spinning, Dança).
3. Indique os melhores horários para sua rotina.
4. Envie suas respostas para a gerência planejar as próximas grades horárias.

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
