# Proposta comercial — Polo Feedback

**Data:** 3 de novembro de 2026  
**Proponente:** Marcos Paulo Santos Lira  
**Cliente:** Academia Polo Fit — Picuí/PB  
**Contato do cliente:** Jefferson

## 1. Objetivo

Implantar e disponibilizar para a Academia Polo Fit a versão personalizada do Polo Feedback, sistema web para receber avaliações dos alunos por QR Code e apoiar o acompanhamento gerencial.

## 2. Escopo incluído

Pelo valor indicado na seção 3, estão incluídos:

- disponibilização da versão acordada do sistema, com formulário de avaliação, pesquisa/enquete, painel gerencial e geração de QR Codes;
- configuração inicial da aplicação em um servidor Linux VPS da Locaweb, após a contratação e confirmação de compatibilidade do plano;
- configuração inicial de domínio e HTTPS, desde que o cliente forneça o domínio e os acessos necessários ao DNS e ao servidor;
- aplicação das migrações e configuração inicial do banco de dados;
- testes de aceite dos fluxos principais antes da liberação para uso oficial.

A publicação será concluída somente depois que os critérios técnicos e os testes de aceite forem atendidos. Esta proposta não declara que a hospedagem atual ou uma nova VPS já esteja configurada ou validada.

## 3. Valor do desenvolvimento e implantação inicial

**Valor total: R$ 1.500,00 (mil e quinhentos reais), em pagamento integral na aprovação da proposta.**

O valor cobre o escopo descrito nesta proposta para uma implantação inicial em um servidor e um domínio. Funcionalidades novas, integrações, migrações adicionais ou mudanças de escopo serão avaliadas e orçadas separadamente.

## 4. Hospedagem e despesas de terceiros

O custo recorrente do servidor, domínio, serviços de terceiros e eventuais recursos adicionais não está incluído nos R$ 1.500,00. A contratação e o pagamento desses serviços serão feitos diretamente pelo cliente ao respectivo fornecedor.

Na consulta à [página oficial de VPS da Locaweb](https://www.locaweb.com.br/servidor-vps/), em 3 de novembro de 2026, o plano inicial era anunciado com **2 vCPUs e 40 GB SSD por R$ 15,90/mês no equivalente de uma contratação por 24 meses**, total de **R$ 381,60 pelo período**, com renovação anunciada de **R$ 23,92/mês**. Preços, recursos e condições podem mudar e devem ser confirmados no checkout.

**A memória RAM do plano não ficou especificada na informação consultada.** Como foi mencionada a necessidade de avaliar uma configuração com 4 GB de RAM, esse requisito deve ser confirmado por escrito com a Locaweb antes de contratar. Não se recomenda comprar o plano de entrada sem essa confirmação e sem conferir o valor total, o prazo e a renovação.

## 5. Condições e responsabilidades

- O cliente contratará o VPS e o domínio e fornecerá os acessos técnicos necessários de forma segura, sem enviar senhas por canais públicos.
- A configuração inicial depende de o plano contratado atender aos requisitos técnicos da aplicação.
- O banco de dados de produção deverá ser persistente, e a estratégia de backup deverá ser combinada antes da liberação.
- O código-fonte, a licença de uso, eventual exclusividade e a titularidade dos direitos serão definidos expressamente em contrato separado; esta proposta não transfere o código-fonte.
- O prazo de implantação será combinado após a confirmação da contratação do servidor, do domínio e dos acessos.

## 6. Suporte e serviços não incluídos

Suporte contínuo, monitoramento, manutenção recorrente, operação de backups, atualizações futuras e novas funcionalidades não estão incluídos no valor acima. Se necessários, serão objeto de contratação ou orçamento separados.

## 7. Critérios para liberação oficial

Antes de divulgar o sistema para uso oficial, será necessário:

1. confirmar o plano VPS, seus recursos, preço total e renovação;
2. configurar o domínio e confirmar HTTPS válido, redirecionamento de HTTP para HTTPS e cookies seguros;
3. configurar o banco persistente, variáveis privadas, permissões e backups;
4. executar os testes de regressão e os testes de aceite dos fluxos de avaliação, painel e QR Codes;
5. corrigir eventuais bloqueios encontrados antes de liberar o acesso aos alunos.

## 8. Aceite comercial

Esta proposta registra os valores e o escopo comercial para discussão entre as partes. A contratação será formalizada por instrumento separado, com identificação completa das partes, responsabilidades, condições de pagamento e demais termos acordados.

**Pelo proponente**

Nome: Marcos Paulo Santos Lira  
Assinatura: ____________________________________  
Data: ____ / ____ / ______

**Pela Academia Polo Fit**

Nome e cargo: __________________________________  
Assinatura: ____________________________________  
Data: ____ / ____ / ______
