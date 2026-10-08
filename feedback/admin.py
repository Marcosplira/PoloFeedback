from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Avaliacao,
    Equipamento,
    Exercicio,
    Funcao,
    Funcionario,
    ItemPlanoTreino,
    PlanoTreino,
    RespostaEnquete,
)


admin.site.site_header = "Polo Fit | Painel Administrativo"
admin.site.site_title = "Polo Fit | Gestão"
admin.site.index_title = "Gestão de equipe, avaliações e treinos"


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "funcoes_display", "foto_preview", "ativo")
    list_editable = ("ativo",)
    search_fields = ("nome", "funcoes__nome")
    list_filter = ("ativo", "funcoes")
    filter_horizontal = ("funcoes",)
    exclude = ("cargo",)
    ordering = ("nome",)

    @admin.display(description="Funções", ordering="funcoes__nome")
    def funcoes_display(self, obj):
        return obj.funcoes_display or "—"

    @admin.display(description="Foto")
    def foto_preview(self, obj):
        if not obj.foto_url:
            return "—"
        return format_html(
            '<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:50%;" />',
            obj.foto_url,
        )


@admin.register(Funcao)
class FuncaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "grupo")
    list_editable = ("grupo",)
    list_filter = ("grupo",)
    search_fields = ("nome",)
    ordering = ("nome",)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_categorias",
        "nota",
        "get_tipos",
        "get_funcionarios",
        "localizacao",
        "status",
        "origem",
        "criado_por",
        "resolvido_por",
        "data_criacao",
    )
    list_filter = ("nota", "status", "origem", "funcionarios", "localizacao", "data_criacao")
    search_fields = ("comentario", "localizacao", "funcionario__nome", "funcionarios__nome")
    list_editable = ("status",)
    ordering = ("-data_criacao",)
    exclude = ("funcionario",)

    @admin.display(description="Funcionários")
    def get_funcionarios(self, obj):
        return ", ".join(
            funcionario.nome for funcionario in obj.funcionarios_avaliados
        ) or "—"

    @admin.display(description="Categorias")
    def get_categorias(self, obj):
        if obj.categorias:
            return ", ".join(obj.categorias)
        return obj.categoria

    @admin.display(description="Tipo")
    def get_tipos(self, obj):
        if obj.tipos_feedback:
            return ", ".join(obj.tipos_feedback)
        return obj.tipo_feedback

    # AQUI FICA AUTOMÁTICO
    def save_model(self, request, obj, form, change):
        # Se está criando novo no admin, é gerente
        if not change:
            obj.origem = "gerente"
            obj.criado_por = request.user

        # Se marcou como resolvida, grava quem resolveu
        if obj.status == "resolvida" and not obj.resolvido_por:
            from django.utils import timezone

            obj.resolvido_por = request.user
            obj.data_resolucao = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(RespostaEnquete)
class RespostaEnqueteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "participa_aulas",
        "get_favoritas",
        "get_funcionarios",
        "get_aulas_melhoria",
        "get_novos_espacos",
        "data_criacao",
    )
    list_filter = ("participa_aulas", "data_criacao")
    search_fields = ("aula_falta", "sugestao_valor", "elogio_colaborador", "aulas_favoritas_outra")
    ordering = ("-data_criacao",)

    @admin.display(description="Aulas Favoritas")
    def get_favoritas(self, obj):
        itens = list(obj.aulas_favoritas or [])
        if obj.aulas_favoritas_outra:
            itens.append(f"Outra: {obj.aulas_favoritas_outra}")
        return ", ".join(itens) or "—"

    @admin.display(description="Aulas para melhorias")
    def get_aulas_melhoria(self, obj):
        return ", ".join(obj.aula_melhoria or []) or "—"

    @admin.display(description="Novos espaços")
    def get_novos_espacos(self, obj):
        return ", ".join(obj.novo_espaco or []) or "—"

    @admin.display(description="Funcionários elogiados")
    def get_funcionarios(self, obj):
        return ", ".join(
            funcionario.nome for funcionario in obj.funcionarios_elogiados.all()
        ) or "—"


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "localizacao", "ativo", "atualizado_em")
    list_filter = ("ativo", "localizacao")
    search_fields = ("nome", "localizacao")
    readonly_fields = ("identificador_qr", "criado_em", "atualizado_em")


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ("nome", "equipamento", "ativo", "atualizado_em")
    list_filter = ("ativo", "equipamento")
    search_fields = ("nome", "equipamento__nome")
    autocomplete_fields = ("equipamento",)
    readonly_fields = ("criado_em", "atualizado_em")


class ItemPlanoTreinoInline(admin.TabularInline):
    model = ItemPlanoTreino
    extra = 1
    autocomplete_fields = ("exercicio",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "exercicio":
            kwargs["queryset"] = Exercicio.objects.filter(ativo=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PlanoTreino)
class PlanoTreinoAdmin(admin.ModelAdmin):
    list_display = ("nome", "aluno", "professor", "ativo", "atualizado_em")
    list_filter = ("ativo", "atualizado_em")
    search_fields = ("nome", "aluno__username", "aluno__first_name", "aluno__last_name")
    readonly_fields = ("criado_em", "atualizado_em")
    inlines = (ItemPlanoTreinoInline,)
