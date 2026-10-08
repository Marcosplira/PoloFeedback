from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import inlineformset_factory

from .models import Exercicio, ItemPlanoTreino, PlanoTreino


class CadastroAlunoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "username": "Usuário para entrar",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a senha"


class AlunoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, aluno):
        nome = aluno.get_full_name() or aluno.username
        return f"{nome} (@{aluno.username})"


class PlanoTreinoForm(forms.ModelForm):
    aluno = AlunoModelChoiceField(
        queryset=User.objects.none(),
        label="Aluno",
        empty_label="Selecione um aluno",
    )

    class Meta:
        model = PlanoTreino
        fields = ("aluno", "nome", "observacoes", "ativo")
        labels = {
            "nome": "Nome do plano",
            "observacoes": "Orientações gerais",
            "ativo": "Plano ativo e visível para o aluno",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        alunos = User.objects.filter(is_active=True, is_staff=False)
        if self.instance and self.instance.pk:
            alunos = User.objects.filter(
                Q(is_active=True, is_staff=False)
                | Q(pk=self.instance.aluno_id)
            )
        self.fields["aluno"].queryset = alunos.order_by(
            "first_name",
            "last_name",
            "username",
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full rounded-xl border border-slate-600 bg-slate-950 "
                "px-3 py-2 text-white focus:border-lime-300 focus:outline-none"
            )
        self.fields["ativo"].widget.attrs["class"] = "h-4 w-4 accent-lime-300"


class ItemPlanoTreinoForm(forms.ModelForm):
    class Meta:
        model = ItemPlanoTreino
        fields = (
            "exercicio",
            "ordem",
            "series",
            "repeticoes",
            "descanso_segundos",
            "carga",
            "observacoes",
        )
        labels = {
            "exercicio": "Exercício",
            "ordem": "Ordem",
            "series": "Séries",
            "repeticoes": "Repetições",
            "descanso_segundos": "Descanso (segundos)",
            "carga": "Carga orientada",
            "observacoes": "Orientação específica",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["exercicio"].queryset = Exercicio.objects.filter(
            ativo=True,
            equipamento__ativo=True,
        ).select_related("equipamento")
        self.fields["exercicio"].empty_label = "Selecione um exercício"
        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "w-full rounded-lg border border-slate-600 bg-slate-950 "
                "px-3 py-2 text-white focus:border-lime-300 focus:outline-none"
            )

ItemPlanoTreinoFormSet = inlineformset_factory(
    PlanoTreino,
    ItemPlanoTreino,
    form=ItemPlanoTreinoForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
