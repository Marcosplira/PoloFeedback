# Roadmap profissional — Polo Fit

Este roadmap separa funcionalidades existentes de ideias ainda não implementadas. Prazos e custos devem ser estimados com a gerência após validação do escopo.

## Base existente no Polo Feedback

- Avaliação de satisfação por formulário e QR Code por localização.
- Dashboard protegido por login, filtros, indicadores, avaliações e status.
- Pesquisa de satisfação para aulas e espaços.
- Resumo e chat com suporte Gemini opcional e fallback local limitado.
- PWA instalável e configuração de deploy em Docker/Render.

O sistema atual não possui atualização instantânea via WebSocket, armazenamento/sincronização de avaliações offline, módulo de treinos, mensagens automáticas por WhatsApp, nem publicação validada de produção. O usuário deve atualizar o painel para buscar dados recentes. A configuração de deploy é uma base, não uma confirmação de publicação.

## Prioridade 0 — Preparação operacional e segurança

1. Configurar domínio, `SECRET_KEY`, `DEBUG=False`, hosts, banco, backups e HTTPS em ambiente administrado pela academia.
2. Criar contas individuais para gerente e demais perfis; remover credenciais compartilhadas e validar controle de acesso.
3. Executar testes e validar formulários, QR Codes, fluxo de status, mídia, PWA e recuperação de backup.
4. Definir canal de suporte, responsável pela triagem e prazo interno para responder às reclamações.
5. Documentar aviso de privacidade, minimização de dados, retenção e acesso aos comentários.

## Prioridade 1 — Uso real do feedback

- Incluir canal claro de contato com a academia (WhatsApp atual abre conversa manual).
- Definir rotina de revisão de pendências e responsáveis pela tratativa.
- Medir volume, nota, categorias, tempo de resposta e resolução com uma linha de base.
- Avaliar melhoria no mobile com alunos e funcionários antes de alterar o fluxo.
- Planejar relatórios exportáveis conforme as decisões reais da gerência.

## Prioridade 2 — Proposta de treino por QR Code

O novo sistema de treino não deve ser iniciado diretamente pela implementação. Primeiro validar o problema e o escopo com gerente, professores e alunos, prototipar telas, definir piloto, aprovar custos e especificar critérios de aceite.

### MVP proposto

- Equipamentos com QR Codes aleatórios que identifiquem apenas a máquina.
- Login de alunos, professores e gerência com permissões distintas.
- Exercícios e vídeos próprios ou autorizados, revisados por um professor.
- Planos individuais consultáveis somente pelo aluno autenticado.
- Séries, repetições, intervalos e carga definidos pelo profissional.
- Histórico de alterações e testes contra acesso a plano de outra pessoa.

Este módulo ainda não está implementado. Leia [PROJETO-TREINO-QR.md](./PROJETO-TREINO-QR.md) para o roteiro de descoberta, segurança, conteúdo e piloto. Next Fit e MFIT são referências de fluxo, não fontes para copiar vídeos, marca ou conteúdo protegido.

## Prioridade 3 — Notificações WhatsApp

O contato direto abre uma conversa iniciada pelo usuário. Alertas automáticos exigem aprovação e integração à WhatsApp Business Platform/API oficial, credenciais guardadas com segurança, avaliação de custo, opt-in/opt-out, definição de destinatários e auditoria. Começar com um alerta gerencial mínimo; não enviar automaticamente dados pessoais ou conteúdo de treino.

## Prioridade 4 — Escala

Após validação do uso em uma unidade e da operação:

- automação de atualização do painel, caso haja demanda;
- exportação e relatórios gerenciais;
- integrações com sistemas da academia;
- gestão de múltiplas unidades;
- notificações push ou offline, somente com requisitos claros de privacidade e suporte.

## Indicadores de sucesso

Combinar as metas com a academia antes do piloto. Exemplos: participação dos alunos, tempo de resposta, percentual de pendências resolvidas, satisfação de alunos e equipe, disponibilidade dos QR Codes e número de incidentes de acesso (meta: zero).

Não prometer retenção, receita, economia ou retorno financeiro sem uma medição apropriada.
