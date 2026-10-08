import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Funcao(models.Model):
    GRUPO_RECEPCAO = "recepcao"
    GRUPO_LIMPEZA = "limpeza"
    GRUPO_ESTAGIARIOS_PROFESSORES = "estagiarios_professores"
    GRUPO_DIRECAO = "direcao_coordenacao"
    GRUPO_CHOICES = [
        (GRUPO_RECEPCAO, "Recepção"),
        (GRUPO_LIMPEZA, "Time de limpeza"),
        (GRUPO_ESTAGIARIOS_PROFESSORES, "Estagiários e professores"),
        (GRUPO_DIRECAO, "Direção e coordenação"),
    ]

    nome = models.CharField(max_length=100, unique=True, verbose_name="Função")
    grupo = models.CharField(
        max_length=32,
        choices=GRUPO_CHOICES,
        blank=True,
        verbose_name="Grupo da equipe",
    )

    class Meta:
        verbose_name = "Função"
        verbose_name_plural = "Funções"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='funcionarios/', null=True, blank=True)
    ativo = models.BooleanField(default=True)
    funcoes = models.ManyToManyField(
        Funcao,
        blank=True,
        related_name="funcionarios",
        verbose_name="Funções",
    )

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def funcoes_display(self):
        funcoes = list(self.funcoes.all())
        if funcoes:
            return ", ".join(funcao.nome for funcao in funcoes)
        return self.cargo


class Avaliacao(models.Model):
    CATEGORIA_CHOICES = [
        ("atendimento", "Atendimento"),
        ("limpeza", "Limpeza"),
        ("equipamentos", "Equipamentos"),
        ("professores", "Professores"),
        ("estrutura", "Estrutura"),
        ("geral", "Geral"),
    ]
    TIPO_CHOICES = [
        ("elogio", "Elogio"),
        ("reclamacao", "Reclamação"),
        ("sugestao", "Sugestão"),
    ]
    TIPO_FEEDBACK_CHOICES = TIPO_CHOICES  # alias para compatibilidade
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("em_analise", "Em Análise"),
        ("resolvida", "Resolvida"),
    ]
    ORIGEM_CHOICES = [
        ("aluno", "Aluno (QR)"),
        ("gerente", "Gerente/Admin"),
    ]

    categoria = models.CharField(
        max_length=20, choices=CATEGORIA_CHOICES, default="geral"
    )
    categorias = models.JSONField(null=True, blank=True)

    nota = models.IntegerField(default=5)

    tipo_feedback = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default="elogio"
    )
    tipos_feedback = models.JSONField(null=True, blank=True)

    localizacao = models.CharField(max_length=100, blank=True)
    comentario = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    origem = models.CharField(max_length=10, choices=ORIGEM_CHOICES, default="aluno")

    # Funcionário avaliado
    funcionario = models.ForeignKey(
        Funcionario,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="avaliacoes",
        verbose_name="Funcionário avaliado",
    )
    funcionarios = models.ManyToManyField(
        Funcionario,
        blank=True,
        related_name="avaliacoes_multiplas",
        verbose_name="Funcionários avaliados",
    )

    criado_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="avaliacoes_criadas",
    )
    resolvido_por = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="avaliacoes_resolvidas",
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_resolucao = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-data_criacao"]

    def save(self, *args, **kwargs):
        if self.status == "resolvida" and not self.data_resolucao:
            self.data_resolucao = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.categoria} - {self.nota}★ - {self.status}"

    @property
    def funcionarios_avaliados(self):
        funcionarios = list(self.funcionarios.all())
        if self.funcionario_id and all(
            funcionario.pk != self.funcionario_id for funcionario in funcionarios
        ):
            funcionarios.insert(0, self.funcionario)
        return funcionarios


class RespostaEnquete(models.Model):
    # 1. Sobre as aulas coletivas - Participação
    participa_aulas = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Participa das aulas coletivas",
    )
    # 2. Aulas que mais gosta ou participa (múltipla escolha)
    aulas_favoritas = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Aulas favoritas",
    )
    aulas_favoritas_outra = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Outra aula favorita",
    )
    # 3. Qual aula precisa de mais atenção ou melhorias
    aula_melhoria = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Aula que precisa de melhorias",
    )
    # 4. Qual aula sente falta na academia (resposta aberta)
    aula_falta = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Aula que sente falta",
    )
    # 5. Sobre novos espaços na academia
    novo_espaco = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Novo espaço mais desejado",
    )
    novo_espaco_outro = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Outro novo espaço",
    )
    # 6. O que agregaria mais valor à academia (resposta aberta)
    sugestao_valor = models.TextField(
        blank=True,
        verbose_name="O que agregaria mais valor",
    )
    # Elogio para colaboradores
    elogio_colaborador = models.TextField(
        blank=True,
        verbose_name="Elogio para colaboradores",
    )
    funcionarios_elogiados = models.ManyToManyField(
        Funcionario,
        blank=True,
        related_name="elogios_enquetes",
        verbose_name="Funcionários elogiados",
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Resposta da Enquete"
        verbose_name_plural = "Respostas da Enquete"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Enquete #{self.id} - {self.data_criacao.strftime('%d/%m/%Y %H:%M')}"


class Equipamento(models.Model):
    nome = models.CharField(max_length=120, unique=True, verbose_name="Equipamento")
    identificador_qr = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Identificador do QR Code",
    )
    localizacao = models.CharField(max_length=120, blank=True, verbose_name="Localização")
    instrucoes = models.TextField(blank=True, verbose_name="Instruções gerais")
    observacoes_seguranca = models.TextField(
        blank=True,
        verbose_name="Orientações de segurança",
    )
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Equipamento de treino"
        verbose_name_plural = "Equipamentos de treino"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Exercicio(models.Model):
    nome = models.CharField(max_length=120, verbose_name="Exercício")
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name="exercicios",
        verbose_name="Equipamento",
    )
    instrucoes = models.TextField(verbose_name="Como executar")
    video_url = models.URLField(blank=True, verbose_name="Link do vídeo autorizado")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Exercício"
        verbose_name_plural = "Exercícios"
        ordering = ["equipamento__nome", "nome"]
        constraints = [
            models.UniqueConstraint(
                fields=("equipamento", "nome"),
                name="feedback_unique_exercise_per_equipment",
            )
        ]

    def __str__(self):
        return f"{self.nome} — {self.equipamento.nome}"


class PlanoTreino(models.Model):
    aluno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="planos_treino",
        verbose_name="Aluno",
    )
    professor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="planos_criados",
        verbose_name="Professor responsável",
    )
    nome = models.CharField(max_length=120, default="Meu treino", verbose_name="Nome do plano")
    observacoes = models.TextField(blank=True, verbose_name="Observações")
    ativo = models.BooleanField(default=True, verbose_name="Plano ativo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Plano de treino"
        verbose_name_plural = "Planos de treino"
        ordering = ["aluno__username", "nome"]

    def __str__(self):
        return f"{self.nome} — {self.aluno.get_full_name() or self.aluno.username}"


class ItemPlanoTreino(models.Model):
    plano = models.ForeignKey(
        PlanoTreino,
        on_delete=models.CASCADE,
        related_name="itens",
        verbose_name="Plano",
    )
    exercicio = models.ForeignKey(
        Exercicio,
        on_delete=models.PROTECT,
        related_name="itens_plano",
        verbose_name="Exercício",
    )
    ordem = models.PositiveSmallIntegerField(default=1, verbose_name="Ordem")
    series = models.PositiveSmallIntegerField(default=3, verbose_name="Séries")
    repeticoes = models.CharField(max_length=40, default="10", verbose_name="Repetições")
    descanso_segundos = models.PositiveSmallIntegerField(
        default=60,
        verbose_name="Descanso (segundos)",
    )
    carga = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="Carga orientada pelo professor",
        help_text="Ex.: 15 kg. O sistema não calcula nem recomenda carga.",
    )
    observacoes = models.CharField(max_length=255, blank=True, verbose_name="Observações")

    class Meta:
        verbose_name = "Exercício do plano"
        verbose_name_plural = "Exercícios do plano"
        ordering = ["ordem", "id"]

    def __str__(self):
        return f"{self.ordem}. {self.exercicio.nome} — {self.plano}"
