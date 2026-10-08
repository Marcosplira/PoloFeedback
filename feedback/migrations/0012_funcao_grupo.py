import unicodedata

from django.db import migrations, models


GRUPOS = (
    ("recepcao", ("recep", "balcao")),
    ("limpeza", ("limpeza", "servicos gerais")),
    (
        "direcao_coordenacao",
        ("gerente", "propriet", "diretor", "direcao", "coorden"),
    ),
    (
        "estagiarios_professores",
        (
            "funcionario",
            "funcionaria",
            "professor",
            "instrutor",
            "estagi",
            "educador",
            "musculacao",
            "pilates",
        ),
    ),
)


def classificar_funcoes_existentes(apps, schema_editor):
    Funcao = apps.get_model("feedback", "Funcao")
    banco = schema_editor.connection.alias

    for funcao in Funcao.objects.using(banco).iterator():
        nome_normalizado = unicodedata.normalize("NFKD", funcao.nome.casefold())
        nome_normalizado = "".join(
            caractere
            for caractere in nome_normalizado
            if not unicodedata.combining(caractere)
        )
        for grupo, termos in GRUPOS:
            if any(termo in nome_normalizado for termo in termos):
                funcao.grupo = grupo
                funcao.save(update_fields=("grupo",))
                break


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0011_multiplas_funcoes_e_funcionarios"),
    ]

    operations = [
        migrations.AddField(
            model_name="funcao",
            name="grupo",
            field=models.CharField(
                blank=True,
                choices=[
                    ("recepcao", "Recepção"),
                    ("limpeza", "Time de limpeza"),
                    ("estagiarios_professores", "Estagiários e professores"),
                    ("direcao_coordenacao", "Direção e coordenação"),
                ],
                max_length=32,
                verbose_name="Grupo da equipe",
            ),
        ),
        migrations.RunPython(
            classificar_funcoes_existentes,
            migrations.RunPython.noop,
        ),
    ]
