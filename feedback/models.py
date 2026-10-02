from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='funcionarios/', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']

    def __str__(self):
        return self.nome


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
