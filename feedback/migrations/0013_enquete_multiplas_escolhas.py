from django.db import migrations, models


def copiar_respostas_existentes(apps, schema_editor):
    RespostaEnquete = apps.get_model("feedback", "RespostaEnquete")
    banco = schema_editor.connection.alias

    for resposta in RespostaEnquete.objects.using(banco).iterator():
        resposta.aula_melhoria_opcoes = (
            [resposta.aula_melhoria] if resposta.aula_melhoria else []
        )
        resposta.novo_espaco_opcoes = (
            [resposta.novo_espaco] if resposta.novo_espaco else []
        )
        resposta.save(
            using=banco,
            update_fields=("aula_melhoria_opcoes", "novo_espaco_opcoes"),
        )


def restaurar_respostas_antigas(apps, schema_editor):
    RespostaEnquete = apps.get_model("feedback", "RespostaEnquete")
    banco = schema_editor.connection.alias

    for resposta in RespostaEnquete.objects.using(banco).iterator():
        resposta.aula_melhoria = (resposta.aula_melhoria_opcoes or [""])[0]
        resposta.novo_espaco = (resposta.novo_espaco_opcoes or [""])[0]
        resposta.save(
            using=banco,
            update_fields=("aula_melhoria", "novo_espaco"),
        )


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0012_funcao_grupo"),
    ]

    operations = [
        migrations.AddField(
            model_name="respostaenquete",
            name="aula_melhoria_opcoes",
            field=models.JSONField(
                blank=True,
                default=list,
                verbose_name="Aulas que precisam de melhorias",
            ),
        ),
        migrations.AddField(
            model_name="respostaenquete",
            name="novo_espaco_opcoes",
            field=models.JSONField(
                blank=True,
                default=list,
                verbose_name="Novos espaços desejados",
            ),
        ),
        migrations.RunPython(
            copiar_respostas_existentes,
            restaurar_respostas_antigas,
        ),
        migrations.RemoveField(
            model_name="respostaenquete",
            name="aula_melhoria",
        ),
        migrations.RemoveField(
            model_name="respostaenquete",
            name="novo_espaco",
        ),
        migrations.RenameField(
            model_name="respostaenquete",
            old_name="aula_melhoria_opcoes",
            new_name="aula_melhoria",
        ),
        migrations.RenameField(
            model_name="respostaenquete",
            old_name="novo_espaco_opcoes",
            new_name="novo_espaco",
        ),
    ]
