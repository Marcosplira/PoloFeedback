import unicodedata

from django.db import migrations


NOMES_RECEPCAO = {
    "micheli priscila",
    "micheli priscilla",
    "jaqueline lima",
    "jessica karla",
    "jesica klarla",
}


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(
        caractere
        for caractere in texto
        if not unicodedata.combining(caractere)
    )


def classificar_recepcao(apps, schema_editor):
    Funcao = apps.get_model("feedback", "Funcao")
    Funcionario = apps.get_model("feedback", "Funcionario")
    banco = schema_editor.connection.alias

    funcao_recepcao, _ = Funcao.objects.using(banco).get_or_create(
        nome="Recepção",
        defaults={"grupo": "recepcao"},
    )
    if funcao_recepcao.grupo != "recepcao":
        funcao_recepcao.grupo = "recepcao"
        funcao_recepcao.save(using=banco, update_fields=("grupo",))

    for funcionario in Funcionario.objects.using(banco).iterator():
        nome_normalizado = " ".join(normalizar(funcionario.nome).split())
        if nome_normalizado not in NOMES_RECEPCAO and not nome_normalizado.startswith(
            "jaqueline "
        ):
            continue

        for funcao in funcionario.funcoes.all():
            if normalizar(funcao.nome).strip() in {"funcionario", "funcionaria"}:
                funcionario.funcoes.remove(funcao.pk)
        funcionario.funcoes.add(funcao_recepcao)


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0013_enquete_multiplas_escolhas"),
    ]

    operations = [
        migrations.RunPython(
            classificar_recepcao,
            migrations.RunPython.noop,
        ),
    ]
