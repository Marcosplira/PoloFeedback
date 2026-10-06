from django.contrib import admin
from django.utils.html import format_html
from .models import Avaliacao, Funcionario, RespostaEnquete


admin.site.site_header = "Polo Fit — Painel Administrativo"
admin.site.site_title = "Polo Feedback"
admin.site.index_title = "Gestão de Avaliações e Equipe"


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "cargo", "foto_preview", "ativo")
    list_editable = ("ativo",)
    search_fields = ("nome", "cargo")
    ordering = ("nome",)

    @admin.display(description="Foto")
    def foto_preview(self, obj):
        if obj.foto:
            try:
                return format_html(
                    '<img src="{}" style="width:40px;height:40px;object-fit:cover;border-radius:50%;" />',
                    obj.foto.url,
                )
            except Exception:
                return "—"
        return "—"


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_categorias",
        "nota",
        "get_tipos",
        "funcionario",
        "localizacao",
        "status",
        "origem",
        "criado_por",
        "resolvido_por",
        "data_criacao",
    )
    list_filter = ("nota", "status", "origem", "funcionario", "localizacao", "data_criacao")
    search_fields = ("comentario", "localizacao", "funcionario__nome")
    list_editable = ("status",)
    ordering = ("-data_criacao",)

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
        "aula_melhoria",
        "novo_espaco",
        "data_criacao",
    )
    list_filter = ("participa_aulas", "aula_melhoria", "novo_espaco", "data_criacao")
    search_fields = ("aula_falta", "sugestao_valor", "elogio_colaborador", "aulas_favoritas_outra")
    ordering = ("-data_criacao",)

    @admin.display(description="Aulas Favoritas")
    def get_favoritas(self, obj):
        itens = list(obj.aulas_favoritas or [])
        if obj.aulas_favoritas_outra:
            itens.append(f"Outra: {obj.aulas_favoritas_outra}")
        return ", ".join(itens) or "—"
