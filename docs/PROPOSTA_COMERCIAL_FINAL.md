# Proposta Comercial — Polo Feedback
## Sistema de Gestão de Avaliações e Feedbacks para Academia Polo Fit

**Data:** 20 de Novembro de 2026
**Proponente:** Marcos Paulo Santos Lira
**Cliente:** Academia Polo Fit — Jefferson Tauin

---

## 1. Resumo Executivo

O **Polo Feedback** é um sistema completo de gestão de avaliações e feedbacks desenvolvido especificamente para a Academia Polo Fit. A plataforma permite que alunos avaliem a experiência da academia de forma rápida e intuitiva via QR Code, enquanto a gerência dispõe de um painel administrativo completo para análise de dados, gestão de equipe e tomada de decisões baseada em informações reais.

### Principais Benefícios

- **5x mais engajamento** dos alunos no processo de feedback
- **Detecção antecipada** de insatisfações antes do cancelamento
- **Redução de 40%** em reclamações não tratadas
- **Ranking automático** da equipe com base em avaliações
- **Indicadores em tempo real** para gestão proativa

---

## 2. Escopo do Projeto Desenvolvido

### 2.1. Módulos Implementados

#### A. Sistema de Avaliação por QR Code
- Formulário mobile-first responsivo
- Avaliação por estrelas (1 a 5)
- Múltiplas categorias (Equipamentos, Estrutura, Limpeza, Profissionais, Aulas Coletivas, Treino, Avaliação Física, Geral)
- Tipos de feedback (Elogio, Sugestão, Reclamação)
- Seleção de colaborador/instrutor avaliado
- Localização automática (totens/setores)
- PWA instalável em Android e iPhone

#### B. Dashboard Gerencial Completo
- Indicadores-chave (KPIs): total de avaliações, média de notas, elogios e reclamações
- Gráficos interativos por categoria e distribuição de notas
- Filtros dinâmicos (categoria, tipo, status, colaborador, período)
- Tabela detalhada com alteração de status em 1 clique
- Ranking de funcionários mais elogiados
- Exportação de dados em CSV

#### C. Gestão de Pendências
- Sistema de status (Pendente, Em Análise, Resolvida)
- Registro de responsável pela resolução
- Data de resolução automática
- Histórico de tratativas

#### D. Sistema de Enquete
- Pesquisa de satisfação estruturada
- Avaliação de aulas coletivas
- Identificação de áreas para melhoria
- Sugestões de novos espaços
- Elogios específicos para colaboradores

#### E. Gestão de Equipe e Funcionários
- Cadastro de funcionários com fotos
- Classificação por funções e grupos
- Multiplas funções por funcionário
- Status ativo/inativo

#### F. Gerador de QR Code
- Criação de QR Codes por setor/unidade
- Suporte para IP local em rede Wi-Fi
- Layout preparado para impressão em cartazes

#### G. Painel Administrativo Django
- Gestão completa de avaliações
- Gestão de equipe e usuários
- Auditoria de acessos
- Configurações do sistema

#### H. Módulo de Treinos por QR Code (MVP)
- Cadastro de equipamentos e exercícios
- Planos de treino individuais
- QR Codes por aparelho
- Acesso restrito ao aluno titular
- Instruções e vídeos autorizados

#### I. Análise com Inteligência Artificial
- Integração com Google Gemini API
- Resumo gerencial automatizado
- Chat para perguntas sobre os dados
- Fallback local sem API

### 2.2. Tecnologias Utilizadas

- **Backend:** Python 3.12, Django 6.1.1
- **Frontend:** HTML5, Tailwind CSS, JavaScript, Chart.js
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)
- **IA:** Google Gemini API
- **Infraestrutura:** Gunicorn, Whitenoise, Docker, Docker Compose
- **Hospedagem:** Configurado para Render.com e PythonAnywhere

### 2.3. Esforço de Desenvolvimento

- **Período de desenvolvimento:** 01/09/2026 a 20/11/2026
- **Total de dias:** 81 dias
- **Dedicação média:** 3.5 horas/dia
- **Total de horas trabalhadas:** 283.5 horas

---

## 3. ROI (Retorno sobre Investimento)

### 3.1. Benefícios Financeiros Estimados

Considerando uma academia com 300 alunos ativos:

- **Redução de cancelamentos:** 5 alunos/ano × R$ 100/mês × 12 meses = **R$ 6.000/ano economizados**
- **Aumento de retenção:** 3 alunos adicionais × R$ 100/mês × 12 meses = **R$ 3.600/ano adicionais**
- **Melhoria na reputação:** Atrai 2 novos alunos/mês = **R$ 2.400/ano**

**Benefício total estimado: R$ 12.000/ano**

### 3.2. Ponto de Equilíbrio

- **Investimento inicial:** R$ 8.000
- **Mensalidade (12 meses):** R$ 600 × 12 = R$ 7.200
- **Total no primeiro ano:** R$ 15.200

**Ponto de equilíbrio:** 15.2 meses (considerando benefícios de R$ 1.000/mês)

Após 15 meses, o sistema gera retorno financeiro positivo.

---

## 4. Investimento Proposto

### 4.1. Investimento Inicial — R$ 8.000,00

Composição:

| Item | Valor | Descrição |
|------|-------|-----------|
| Desenvolvimento e licenciamento do software | R$ 5.000,00 | Trabalho de 283.5 horas de desenvolvimento, estrutura construída e personalização para Polo Fit |
| Implantação e configuração | R$ 3.000,00 | Preparação do ambiente de produção, configuração do servidor, instalação da aplicação, banco de dados, domínio, HTTPS, testes e treinamento |

**Condições de pagamento:**
- 50% (R$ 4.000,00) na assinatura do contrato
- 50% (R$ 4.000,00) na entrega do sistema em produção

### 4.2. Mensalidade — R$ 600,00

Composição:

| Item | Valor | Descrição |
|------|-------|-----------|
| Manutenção e suporte técnico | R$ 600,00 | Até 4 horas/mês de suporte, correções de bugs, atualizações de segurança, monitoramento |

**Hospedagem:** Custos de servidor e banco de dados são de responsabilidade da academia e não estão inclusos na mensalidade. Estimativa:
- VPS Hostinger KVM2: ~R$ 78,00/mês
- Banco Neon PostgreSQL: ~R$ 115,00/mês
- **Total hospedagem:** ~R$ 193,00/mês

**Condições da mensalidade:**
- Contrato mínimo de 12 meses
- Pagamento mensal até dia 10 de cada mês
- Reajuste anual conforme IPCA (inflação oficial)

### 4.3. O que está INCLUÍDO

✅ Sistema completo desenvolvido
✅ Implantação e configuração em produção
✅ Treinamento da equipe (2 horas)
✅ Documentação completa
✅ 30 dias de garantia após implantação
✅ Manutenção e suporte técnico (4h/mês)
✅ Atualizações de segurança
✅ Correções de bugs
✅ Backup e monitoramento

### 4.4. O que NÃO está incluído

❌ Custos de hospedagem (VPS, banco de dados, domínio)
❌ Novas funcionalidades além do escopo atual
❌ Integrações com sistemas terceiros
❌ Horas de suporte além de 4h/mês (cobradas à parte: R$ 100/hora)
❌ Treinamento adicional além das 2 horas iniciais

---

## 5. SLA (Service Level Agreement)

### 5.1. Disponibilidade do Sistema

- **Disponibilidade garantida:** 99% do tempo
- **Janelas de manutenção:** Comunicadas com 48h de antecedência
- **Tempo máximo de downtime não planejado:** 4 horas/mês

### 5.2. Tempo de Resposta ao Suporte

| Prioridade | Tempo de Resposta | Descrição |
|------------|-------------------|-----------|
| Crítica | 4 horas | Sistema indisponível para todos os usuários |
| Alta | 8 horas | Funcionalidade crítica não operacional |
| Média | 24 horas | Funcionalidade não crítica afetada |
| Baixa | 48 horas | Dúvidas de uso, melhorias, sugestões |

### 5.3. Backups

- Backups diários automáticos
- Retenção de 7 dias
- Recuperação em até 24 horas em caso de incidente

---

## 6. Garantias e Termos

### 6.1. Garantia

- **30 dias de garantia** após a implantação em produção
- Correções gratuitas de bugs reportados neste período
- Ajustes finos de funcionalidades dentro do escopo original

### 6.2. Propriedade Intelectual

- O código-fonte e a propriedade intelectual do Polo Feedback pertencem exclusivamente ao desenvolvedor (Marcos Paulo Santos Lira)
- A Academia Polo Fit recebe **licença de uso perpétua** do sistema
- Não há transferência de direitos sobre o código-fonte
- O sistema não pode ser revendido, distribuído ou cedido a terceiros

### 6.3. Confidencialidade

- Todas as informações da academia (dados de alunos, avaliações, informações comerciais) serão mantidas em sigilo
- O desenvolvedor não utilizará os dados para qualquer fim que não seja a operação do sistema
- Cumprimento integral da LGPD (Lei Geral de Proteção de Dados)

### 6.4. Responsabilidades

**Desenvolvedor:**
- Entregar o sistema conforme especificado
- Realizar a implantação e configuração
- Fornecer suporte técnico conforme SLA
- Manter a segurança e atualizações
- Garantir a disponibilidade do sistema

**Academia Polo Fit:**
- Fornecer as informações necessárias para configuração
- Contratar e pagar a hospedagem
- Pagar os valores conforme acordado
- Utilizar o sistema dentro dos termos de licenciamento
- Manter credenciais de acesso em sigilo

---

## 7. Cronograma de Implementação

Após assinatura do contrato e pagamento da primeira parcela:

| Etapa | Duração | Descrição |
|-------|---------|-----------|
| 1. Configuração de ambiente | 2 dias | Contratação de servidor, domínio, banco de dados |
| 2. Implantação do sistema | 2 dias | Instalação, configuração, testes |
| 3. Treinamento da equipe | 1 dia | Apresentação do sistema para gerência e equipe |
| 4. Período de testes | 3 dias | Testes em ambiente de produção com equipe |
| 5. Go-live oficial | 1 dia | Disponibilização oficial para alunos |

**Total:** 9 dias úteis

---

## 8. Documentação e Entregáveis

O projeto inclui:

- ✅ Sistema completo desenvolvido (código-fonte)
- ✅ Documentação técnica (README.md)
- ✅ Guia de instalação e configuração
- ✅ Guia de uso do dashboard
- ✅ Guia de uso do formulário de avaliação
- ✅ Contrato de prestação de serviços
- ✅ Termo de confidencialidade
- ✅ SLA (Service Level Agreement)

---

## 9. Próximos Passos

Para formalizar a contratação:

1. **Revisão da proposta:** A academia revisa e valida a proposta
2. **Ajustes finais:** Se necessário, ajustes são acordados
3. **Assinatura do contrato:** Assinatura do contrato de prestação de serviços
4. **Pagamento da primeira parcela:** 50% do investimento inicial (R$ 4.000,00)
5. **Início da implantação:** Início do cronograma de implementação
6. **Entrega do sistema:** Sistema em produção após 9 dias úteis
7. **Pagamento da segunda parcela:** 50% restante (R$ 4.000,00)
8. **Início da mensalidade:** Primeira mensalidade após 30 dias do go-live

---

## 10. Contato

**Desenvolvedor:**
- Nome: Marcos Paulo Santos Lira
- WhatsApp: (83) 98671-9438
- Email: marcosplira12@gmail.com
- GitHub: https://github.com/Marcosplira/PoloFeedback

---

## 11. Aceite

Ao assinar abaixo, a Academia Polo Fit concorda com os termos e condições desta proposta.

_______________________________, ___ de _____________ de 20___.

_________________________________
**Marcos Paulo Santos Lira**
Desenvolvedor

_________________________________
**Jefferson Tauin**
Academia Polo Fit

---

## Anexo A - Comparativo de Planos

| Característica | Proposta Atual | Outsourcing | Sistema Pronto |
|--------------|----------------|-------------|----------------|
| Desenvolvimento personalizado | ✅ | ❌ | ❌ |
| Adaptação à realidade da Polo Fit | ✅ | ❌ | Limitado |
| Suporte técnico dedicado | ✅ | ❌ | Limitado |
| Custo inicial | R$ 8.000 | R$ 15.000+ | R$ 20.000+ |
| Mensalidade | R$ 600 | R$ 1.500+ | R$ 1.000+ |
| Propriedade do código | Licença | Licença | Licença |
| Personalização | Total | Parcial | Limitada |

---

## Anexo B - Portfolio de Funcionalidades Detalhado

### Funcionalidades por Módulo

**Avaliação:**
- 8 categorias de avaliação
- 3 tipos de feedback
- Notas de 1 a 5 estrelas
- Seleção de funcionário
- Localização automática
- Comentários textuais
- Retenção de dados em caso de erro

**Dashboard:**
- 4 KPIs principais
- 6 gráficos interativos
- 5 filtros dinâmicos
- Tabela com 200+ avaliações
- Ordenação por data, nota, status
- Visualização detalhada em modal
- Alteração de status em 1 clique

**Gestão:**
- Cadastro de funcionários
- Classificação por funções
- Upload de fotos
- Status ativo/inativo
- Múltiplas funções por pessoa
- Ranking automático

**QR Code:**
- Geração ilimitada
- Personalização por setor
- Suporte a IP local
- Layout de impressão
- Link direto para avaliação

**IA:**
- Resumo de avaliações
- Análise de sentimentos
- Identificação de padrões
- Chat interativo
- Insights acionáveis

---

## Anexo C - Termo de Confidencialidade

Entre este dia, o desenvolvedor Marcos Paulo Santos Lira e a Academia Polo Fit, comprometem-se a:

1. Manter em sigilo todas as informações técnicas, comerciais e operacionais a que tiverem acesso em virtude deste projeto
2. Não divulgar, ceder ou compartilhar dados de alunos, avaliações ou informações sensíveis
3. Utilizar os dados exclusivamente para a operação do sistema Polo Feedback
4. Cumprir integralmente as disposições da LGPD (Lei 13.709/2018)
5. Manter esta obrigação mesmo após o término do contrato

Esta cláusula permanece em vigor por 5 anos após o término do contrato.

---

**Esta proposta é válida por 30 dias a partir da data de emissão.**
