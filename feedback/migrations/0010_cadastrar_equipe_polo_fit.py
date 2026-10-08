from django.db import migrations


FUNCIONARIOS = (
    ("Alan Araújo", "Gerente"),
    ("Anderson Adriel", "Funcionário"),
    ("Douglas Augusto", "Funcionário"),
    ("Italo Kelps", "Funcionário"),
    ("Janderson Fernandes", "Funcionário"),
    ("Jaqueline Lima", "Funcionária"),
    ("Jefferson Tauin", "Proprietário"),
    ("Jessica Karla", "Funcionária"),
    ("João Matheus", "Funcionário"),
    ("José Ivanildo", "Funcionário"),
    ("Maria da Conceição", "Funcionária"),
    ("Mary Carla", "Funcionária"),
    ("Micheli Priscila", "Funcionária"),
    ("Thalyson Pablo", "Funcionário"),
    ("Vitória Bruna", "Funcionária"),
    ("Vivia Gabriella", "Funcionária"),
)


def cadastrar_funcionarios(apps, schema_editor):
    Funcionario = apps.get_model("feedback", "Funcionario")
    for nome, cargo in FUNCIONARIOS:
        Funcionario.objects.get_or_create(
            nome=nome,
            defaults={"cargo": cargo, "ativo": True},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0009_equipamento_exercicio_planotreino_itemplanotreino_and_more"),
    ]

    operations = [
        migrations.RunPython(cadastrar_funcionarios, migrations.RunPython.noop),
    ]
