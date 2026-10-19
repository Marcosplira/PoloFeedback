import io
import base64
import json
import logging
import re
import socket
import unicodedata
import urllib.request
import urllib.error
import qrcode
from datetime import timedelta
from functools import wraps
from urllib.parse import quote

from collections import Counter, defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.staticfiles import finders
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
    JsonResponse,
)
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

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
from .forms import CadastroAlunoForm, ItemPlanoTreinoFormSet, PlanoTreinoForm

logger = logging.getLogger(__name__)


def staff_required(view_func=None, *, permission=None):
    def decorate(view):
        @wraps(view)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not request.user.is_staff:
                return render(
                    request,
                    "feedback/acesso_negado_equipe.html",
                    {"usuario": request.user},
                    status=403,
                )
            if (
                permission
                and not request.user.is_superuser
                and not request.user.has_perm(permission)
            ):
                return HttpResponseForbidden(
                    "Sua conta não tem permissão para acessar esta área."
                )
            return view(request, *args, **kwargs)

        return wrapped_view

    if view_func is not None:
        return decorate(view_func)
    return decorate


def service_worker(request):
    worker_path = finders.find("feedback/service-worker.js")
    if not worker_path:
        return HttpResponseNotFound()

    with open(worker_path, encoding="utf-8") as worker_file:
        response = HttpResponse(
            worker_file.read(),
            content_type="application/javascript",
        )

    response["Service-Worker-Allowed"] = "/"
    return response


def _obter_ip_local():
    """Detecta o IP do servidor na rede local para facilitar testes via smartphone."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _gerar_qrcode_base64(url, box_size=8):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=3,
    )
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def _selecionar_funcionarios(ids):
    ids_unicos = list(dict.fromkeys(ids))
    if any(not funcionario_id.isdecimal() for funcionario_id in ids_unicos):
        return [], False

    funcionarios_por_id = {
        str(funcionario.pk): funcionario
        for funcionario in Funcionario.objects.filter(
            pk__in=ids_unicos,
            ativo=True,
        ).prefetch_related("funcoes")
    }
    selecao_valida = len(funcionarios_por_id) == len(ids_unicos)
    funcionarios = [
        funcionarios_por_id[funcionario_id]
        for funcionario_id in ids_unicos
        if funcionario_id in funcionarios_por_id
    ]
    return funcionarios, selecao_valida


def avaliar(request):
    funcionarios = Funcionario.objects.filter(ativo=True).prefetch_related("funcoes")

    if request.method == "POST":
        categorias = request.POST.getlist("categorias")
        if not categorias and request.POST.get("categoria"):
            categorias = [request.POST.get("categoria").strip()]

        nota = request.POST.get("nota")

        tipos_feedback = request.POST.getlist("tipos_feedback")
        if not tipos_feedback and request.POST.get("tipo_feedback"):
            tipos_feedback = [request.POST.get("tipo_feedback").strip()]

        # Se o usuário não selecionou o tipo de feedback, deduz pela nota de estrelas
        if not tipos_feedback and nota:
            try:
                n = int(nota)
                if n >= 4:
                    tipos_feedback = ["elogio"]
                elif n == 3:
                    tipos_feedback = ["sugestao"]
                else:
                    tipos_feedback = ["reclamacao"]
            except ValueError:
                tipos_feedback = ["elogio"]

        comentario = request.POST.get("comentario", "").strip()
        localizacao = request.POST.get("localizacao", "").strip()

        funcionario_ids = request.POST.getlist("funcionarios_ids")
        if not funcionario_ids and request.POST.get("funcionario_id"):
            funcionario_ids = [request.POST.get("funcionario_id").strip()]

        funcionarios_selecionados, selecao_valida = _selecionar_funcionarios(
            funcionario_ids
        )

        erros = []

        if not categorias:
            erros.append(
                "Selecione sobre o que você quer opinar."
            )

        if not nota:
            erros.append("Avalie atribuindo uma nota de 1 a 5 estrelas.")

        if not tipos_feedback:
            tipos_feedback = ["elogio"]

        if not selecao_valida:
            erros.append(
                "Um ou mais funcionários selecionados não estão disponíveis. "
                "Revise a seleção e tente novamente."
            )

        if erros:
            return render(
                request,
                "feedback/avaliar.html",
                {
                    "localizacao": localizacao,
                    "erros": erros,
                    "funcionarios": funcionarios,
                    "comentario": comentario,
                    "nota_selecionada": nota,
                    "categorias_selecionadas": categorias,
                    "tipos_selecionados": tipos_feedback,
                    "funcionarios_ids_selecionados": funcionario_ids,
                },
            )

        avaliacao = Avaliacao.objects.create(
            categoria=categorias[0],
            categorias=categorias,
            nota=int(nota),
            tipo_feedback=tipos_feedback[0],
            tipos_feedback=tipos_feedback,
            comentario=comentario,
            localizacao=localizacao,
            funcionario=funcionarios_selecionados[0]
            if funcionarios_selecionados
            else None,
        )
        avaliacao.funcionarios.set(funcionarios_selecionados)

        return render(
            request,
            "feedback/sucesso.html",
            {"localizacao": localizacao},
        )

    localizacao_get = request.GET.get("localizacao", "").strip()

    if not localizacao_get:
        localizacao_get = "Geral"

    return render(
        request,
        "feedback/avaliar.html",
        {
            "localizacao": localizacao_get,
            "funcionarios": funcionarios,
        },
    )


def inicio(request):
    avaliar_url = request.build_absolute_uri(reverse("avaliar"))
    enquete_url = request.build_absolute_uri(reverse("enquete"))
    return render(
        request,
        "feedback/inicio.html",
        {
            "avaliar_url": avaliar_url,
            "avaliar_qr": _gerar_qrcode_base64(avaliar_url),
            "enquete_url": enquete_url,
            "enquete_qr": _gerar_qrcode_base64(enquete_url),
            "link_funciona_publicamente": request.get_host().split(":", 1)[0].lower()
            not in {"localhost", "127.0.0.1"},
        },
    )


def baixar_video(request):
    """
    Redireciona diretamente para o download do vídeo da Polo Fit no Google Drive,
    resolvendo o formulário de confirmação de arquivo grande para iniciar o download
    direto sem a tela de aviso de verificação de vírus.
    """
    file_id = "1dMbcjNqjXwljGSaJdAHkax_5Sy_12_bX"
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            uuid_match = re.search(r'name="uuid"\s+value="([^"]+)"', html)
            if uuid_match:
                uuid_val = uuid_match.group(1)
                direct_url = (
                    f"https://drive.usercontent.google.com/download"
                    f"?id={file_id}&export=download&confirm=t&uuid={uuid_val}"
                )
                return redirect(direct_url)
    except Exception as exc:
        logger.warning("Falha ao obter link direto do vídeo no Google Drive: %s", exc)

    return redirect(
        f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    )


def enquete(request):
    """
    Página da Enquete de Satisfação com as 6 perguntas oficiais.
    """

    funcionarios = list(
        Funcionario.objects.filter(ativo=True)
        .prefetch_related("funcoes")
        .order_by("nome")
    )
    funcionarios_por_grupo = []
    for codigo, nome_grupo in Funcao.GRUPO_CHOICES:
        funcionarios_do_grupo = [
            funcionario
            for funcionario in funcionarios
            if any(funcao.grupo == codigo for funcao in funcionario.funcoes.all())
        ]
        funcionarios_por_grupo.append(
            {
                "codigo": codigo,
                "nome": nome_grupo,
                "funcionarios": funcionarios_do_grupo,
            }
        )

    if request.method == "POST":

        aulas_favoritas = request.POST.getlist("aulas_favoritas")
        aulas_favoritas_outra = request.POST.get(
            "aulas_favoritas_outra",
            "",
        ).strip()

        participa_aulas = request.POST.get(
            "participa_aulas",
            "",
        ).strip()

        novo_espaco = request.POST.getlist(
            "novo_espaco",
        )

        novo_espaco_outro = request.POST.get(
            "novo_espaco_outro",
            "",
        ).strip()

        aula_melhoria = request.POST.getlist(
            "aula_melhoria",
        )

        aula_falta = request.POST.get(
            "aula_falta",
            "",
        ).strip()

        sugestao_valor = request.POST.get(
            "sugestao_valor",
            "",
        ).strip()

        elogio_colaborador = request.POST.get(
            "elogio_colaborador",
            "",
        ).strip()

        funcionario_ids = request.POST.getlist("funcionarios_ids")
        funcionarios_selecionados, selecao_valida = _selecionar_funcionarios(
            funcionario_ids
        )
        if not selecao_valida:
            return render(
                request,
                "feedback/enquete.html",
                {
                    "funcionarios": funcionarios,
                    "funcionarios_por_grupo": funcionarios_por_grupo,
                    "funcionarios_ids_selecionados": funcionario_ids,
                    "erro_funcionarios": (
                        "Um ou mais funcionários selecionados não estão disponíveis. "
                        "Revise a seleção e tente novamente."
                    ),
                },
                status=400,
            )

        resposta = RespostaEnquete.objects.create(
            participa_aulas=participa_aulas,
            aulas_favoritas=aulas_favoritas,
            aulas_favoritas_outra=aulas_favoritas_outra,
            aula_melhoria=aula_melhoria,
            aula_falta=aula_falta,
            novo_espaco=novo_espaco,
            novo_espaco_outro=novo_espaco_outro,
            sugestao_valor=sugestao_valor,
            elogio_colaborador=elogio_colaborador,
        )
        resposta.funcionarios_elogiados.set(funcionarios_selecionados)

        if elogio_colaborador and funcionarios_selecionados:
            avaliacao = Avaliacao.objects.create(
                categoria="professores",
                categorias=["professores"],
                nota=5,
                tipo_feedback="elogio",
                tipos_feedback=["elogio"],
                comentario=f"[Enquete] {elogio_colaborador}",
                funcionario=funcionarios_selecionados[0],
                origem="aluno",
            )
            avaliacao.funcionarios.set(funcionarios_selecionados)

        return render(
            request,
            "feedback/enquete_sucesso.html",
            {"resposta": resposta},
        )

    return render(
        request,
        "feedback/enquete.html",
        {
            "funcionarios": funcionarios,
            "funcionarios_por_grupo": funcionarios_por_grupo,
        },
    )


@staff_required(permission="feedback.view_avaliacao")
def dashboard(request):

    # ==========================================================
    # ATUALIZAÇÃO DE STATUS
    # ==========================================================

    if request.method == "POST":

        avaliacao_id = request.POST.get("avaliacao_id")
        novo_status = request.POST.get("novo_status")

        if avaliacao_id and novo_status in [
            "pendente",
            "em_analise",
            "resolvida",
        ]:

            av = get_object_or_404(
                Avaliacao,
                pk=avaliacao_id,
            )

            av.status = novo_status

            if novo_status == "resolvida":

                if not av.resolvido_por:
                    av.resolvido_por = request.user

                if not av.data_resolucao:
                    av.data_resolucao = timezone.now()

            else:
                av.resolvido_por = None
                av.data_resolucao = None

            av.save()

        params = request.POST.get(
            "filtros_ativos",
            "",
        )

        if params:
            return redirect(f"/dashboard/?{params}")

        return redirect("/dashboard/")

    # ==========================================================
    # FILTROS
    # ==========================================================

    categoria_filtro = request.GET.get(
        "categoria",
        "",
    )

    tipo_filtro = request.GET.get(
        "tipo",
        "",
    )

    status_filtro = request.GET.get(
        "status",
        "",
    )

    funcionario_filtro = request.GET.get(
        "funcionario",
        "",
    )

    periodo_filtro = request.GET.get(
        "periodo",
        "",
    )

    # ==========================================================
    # AVALIAÇÕES
    # ==========================================================

    avaliacoes = (
        Avaliacao.objects.all()
        .select_related("funcionario")
        .prefetch_related(
            "funcionarios",
            "funcionarios__funcoes",
            "funcionario__funcoes",
        )
    )

    if periodo_filtro:

        agora = timezone.localtime()

        if periodo_filtro == "hoje":

            inicio = agora.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )

            avaliacoes = avaliacoes.filter(data_criacao__gte=inicio)

        elif periodo_filtro == "semana":

            inicio = agora - timedelta(days=7)

            avaliacoes = avaliacoes.filter(data_criacao__gte=inicio)

        elif periodo_filtro == "mes":

            inicio = agora - timedelta(days=30)

            avaliacoes = avaliacoes.filter(data_criacao__gte=inicio)

    if categoria_filtro:

        avaliacoes = avaliacoes.filter(
            models.Q(categoria=categoria_filtro)
            | models.Q(categorias__icontains=categoria_filtro)
        )

    if tipo_filtro:

        avaliacoes = avaliacoes.filter(
            models.Q(tipo_feedback=tipo_filtro)
            | models.Q(tipos_feedback__icontains=tipo_filtro)
        )

    if status_filtro:
        avaliacoes = avaliacoes.filter(status=status_filtro)

    if funcionario_filtro:
        avaliacoes = avaliacoes.filter(
            models.Q(funcionario_id=funcionario_filtro)
            | models.Q(funcionarios__id=funcionario_filtro)
        ).distinct()

    avaliacoes = avaliacoes.order_by("-data_criacao")

    # ==========================================================
    # CARDS
    # ==========================================================

    total_avaliacoes = avaliacoes.count()

    media = avaliacoes.aggregate(m=models.Avg("nota"))["m"] or 0

    total_elogios = avaliacoes.filter(
        models.Q(tipo_feedback="elogio") | models.Q(tipos_feedback__icontains="elogio")
    ).count()

    total_reclamacoes = avaliacoes.filter(
        models.Q(tipo_feedback="reclamacao")
        | models.Q(tipos_feedback__icontains="reclamacao")
    ).count()

    # ==========================================================
    # GRÁFICO POR CATEGORIA
    # ==========================================================

    cats = []

    for a in avaliacoes:

        if a.categorias and isinstance(
            a.categorias,
            list,
        ):

            cats.extend([str(x).strip().lower() for x in a.categorias])

        elif a.categoria:

            cats.append(str(a.categoria).strip().lower())

    cont_cat = Counter(cats)

    avaliacoes_categoria = []

    for codigo, nome in Avaliacao.CATEGORIA_CHOICES:

        quantidade = cont_cat.get(
            codigo.lower(),
            0,
        )

        avaliacoes_categoria.append(
            {
                "nome": nome,
                "quantidade": quantidade,
            }
        )

    if sum(x["quantidade"] for x in avaliacoes_categoria) == 0 and cont_cat:

        avaliacoes_categoria = [
            {
                "nome": chave.capitalize(),
                "quantidade": valor,
            }
            for chave, valor in cont_cat.items()
        ]

    # ==========================================================
    # GRÁFICO POR NOTA
    # ==========================================================

    cont_nota = Counter([a.nota for a in avaliacoes if a.nota])

    avaliacoes_nota = [
        {
            "nota": n,
            "quantidade": cont_nota.get(n, 0),
        }
        for n in range(5, 0, -1)
    ]

    # ==========================================================
    # FUNCIONÁRIOS
    # ==========================================================

    todos_funcionarios = Funcionario.objects.filter(ativo=True).prefetch_related("funcoes")

    # ==========================================================
    # RANKING DE FUNCIONÁRIOS
    # ==========================================================

    avaliacoes_por_funcionario = defaultdict(dict)
    avaliacoes_ranking = (
        Avaliacao.objects.only(
            "id",
            "nota",
            "tipo_feedback",
            "funcionario_id",
        )
        .prefetch_related("funcionarios")
    )
    for avaliacao in avaliacoes_ranking:
        funcionarios_ids = {
            funcionario.pk for funcionario in avaliacao.funcionarios.all()
        }
        if avaliacao.funcionario_id:
            funcionarios_ids.add(avaliacao.funcionario_id)
        for funcionario_id in funcionarios_ids:
            avaliacoes_por_funcionario[funcionario_id][avaliacao.pk] = avaliacao

    ranking_funcionarios = []

    for func in todos_funcionarios:
        avs = list(avaliacoes_por_funcionario.get(func.pk, {}).values())
        total = len(avs)
        elogios = sum(avaliacao.tipo_feedback == "elogio" for avaliacao in avs)
        reclamacoes = sum(
            avaliacao.tipo_feedback == "reclamacao" for avaliacao in avs
        )
        sugestoes = sum(avaliacao.tipo_feedback == "sugestao" for avaliacao in avs)
        notas = [avaliacao.nota for avaliacao in avs if avaliacao.nota is not None]
        media_func = sum(notas) / len(notas) if notas else 0

        foto_url = func.foto_url or ""

        ranking_funcionarios.append(
            {
                "funcionario": func,
                "nome": func.nome,
                "funcoes": func.funcoes_display,
                "foto": foto_url,
                "total": total,
                "elogios": elogios,
                "reclamacoes": reclamacoes,
                "sugestoes": sugestoes,
                "media": round(
                    media_func,
                    1,
                ),
            }
        )

    ranking_funcionarios.sort(
        key=lambda x: (
            x["elogios"],
            x["media"],
        ),
        reverse=True,
    )

    # ==========================================================
    # AVALIAÇÕES POR LOCAL
    # ==========================================================

    LOCAIS_DEFINIDOS = [
        ("Geral", "🌐"),
        ("Recepção", "🧑‍💼"),
        ("Academia Principal", "🏋️"),
        ("Vestiários", "🚿"),
        ("Studio de Pilates", "🧘"),
        ("Área de Musculação", "💪"),
        ("Treinamento Funcional", "🏃"),
    ]

    locais_ranking = []

    estatisticas_locais = {
        registro["localizacao"]: registro
        for registro in Avaliacao.objects.values("localizacao").annotate(
            total=models.Count("id"),
            media=models.Avg("nota"),
        )
    }

    for nome_local, icone in LOCAIS_DEFINIDOS:
        estatisticas = estatisticas_locais.get(nome_local, {})
        total_local = estatisticas.get("total", 0)

        if total_local == 0:
            continue

        media_local = estatisticas.get("media") or 0

        locais_ranking.append(
            {
                "nome": nome_local,
                "icone": icone,
                "total": total_local,
                "media": round(
                    media_local,
                    1,
                ),
            }
        )

    locais_ranking.sort(
        key=lambda x: x["total"],
        reverse=True,
    )

    respostas_enquete = RespostaEnquete.objects.all()
    total_enquetes = respostas_enquete.count()
    favoritas_ranking = Counter(
        [
            aula
            for resposta in respostas_enquete.exclude(aulas_favoritas=[])
            for aula in (resposta.aulas_favoritas or [])
        ]
    ).most_common(6)
    espacos_ranking = Counter(
        espaco
        for resposta in respostas_enquete
        for espaco in (resposta.novo_espaco or [])
    ).most_common(6)
    melhorias_ranking = Counter(
        aula
        for resposta in respostas_enquete
        for aula in (resposta.aula_melhoria or [])
    ).most_common(5)
    participacao_ranking = Counter(
        respostas_enquete.exclude(participa_aulas="").values_list(
            "participa_aulas",
            flat=True,
        )
    ).most_common(4)
    ultimas_enquetes = (
        respostas_enquete.filter(
            models.Q(sugestao_valor__gt="")
            | models.Q(elogio_colaborador__gt="")
            | models.Q(aula_falta__gt="")
        )
        .order_by("-data_criacao")[:6]
    )

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    return render(
        request,
        "feedback/dashboard.html",
        {
            "total_avaliacoes": total_avaliacoes,
            "media_notas": round(
                media,
                1,
            ),
            "total_elogios": total_elogios,
            "total_reclamacoes": total_reclamacoes,
            "categoria_filtro": categoria_filtro,
            "tipo_filtro": tipo_filtro,
            "status_filtro": status_filtro,
            "funcionario_filtro": funcionario_filtro,
            "periodo_filtro": periodo_filtro,
            "avaliacoes_categoria": avaliacoes_categoria,
            "avaliacoes_nota": avaliacoes_nota,
            "avaliacoes": avaliacoes,
            "categorias": Avaliacao.CATEGORIA_CHOICES,
            "tipos_feedback": Avaliacao.TIPO_FEEDBACK_CHOICES,
            "status_choices": Avaliacao.STATUS_CHOICES,
            "funcionarios": todos_funcionarios,
            "ranking_funcionarios": ranking_funcionarios,
            "locais_ranking": locais_ranking,
            "total_enquetes": total_enquetes,
            "favoritas_ranking": favoritas_ranking,
            "espacos_ranking": espacos_ranking,
            "melhorias_ranking": melhorias_ranking,
            "participacao_ranking": participacao_ranking,
            "ultimas_enquetes": ultimas_enquetes,
            "principal_oportunidade": melhorias_ranking[0] if melhorias_ranking else None,
            "espaco_mais_desejado": espacos_ranking[0] if espacos_ranking else None,
            "gemini_configured": bool(getattr(settings, "GEMINI_API_KEY", "")),
            "total_funcionarios": todos_funcionarios.count(),
            "total_equipamentos": Equipamento.objects.count(),
        },
    )


@staff_required(permission="feedback.view_avaliacao")
def projeto_treino(request):
    return render(request, "feedback/projeto_treino.html")


@staff_required(permission="feedback.view_avaliacao")
def configuracao_sistema(request):
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    executor = MigrationExecutor(connection)
    pendentes = executor.migration_plan(executor.loader.graph.leaf_nodes())

    total_avaliacoes = Avaliacao.objects.count()
    total_planos = PlanoTreino.objects.count()
    total_respostas_enquete = RespostaEnquete.objects.count()
    total_funcionarios = Funcionario.objects.count()

    User = get_user_model()
    total_usuarios = User.objects.count()
    total_alunos = User.objects.filter(is_staff=False).count()

    ia_gemini_ativo = bool(getattr(settings, "GEMINI_API_KEY", None))

    modulos = [
        {
            "nome": "Treinos por QR Code (Piloto)",
            "descricao": "Aparelhos com QR code para exibição direta da ficha e séries do aluno",
            "status": "Ativo",
            "icone": "📱",
            "url": reverse("gestao_treinos"),
            "badge_color": "emerald",
        },
        {
            "nome": "Avaliações e Satisfação (NPS)",
            "descricao": "Coleta contínua de feedback por totens, cartazes ou link direto",
            "status": "Ativo",
            "icone": "⭐",
            "url": reverse("dashboard"),
            "badge_color": "emerald",
        },
        {
            "nome": "Pesquisa de Demanda e Aulas",
            "descricao": "Enquete interativa para novas modalidades, horários e melhorias",
            "status": "Ativo",
            "icone": "📊",
            "url": reverse("enquete"),
            "badge_color": "emerald",
        },
        {
            "nome": "Inteligência Artificial (Google Gemini)",
            "descricao": "Geração automática de diagnósticos executivos e resumos de gestão",
            "status": "Configurada" if ia_gemini_ativo else "Pronto p/ Ativar",
            "icone": "🤖",
            "url": reverse("dashboard"),
            "badge_color": "emerald" if ia_gemini_ativo else "amber",
        },
        {
            "nome": "PWA & Acesso Mobile",
            "descricao": "Instalação instantânea no celular dos alunos e da equipe sem App Store",
            "status": "Ativo",
            "icone": "📲",
            "url": reverse("inicio"),
            "badge_color": "emerald",
        },
    ]

    contexto = {
        "banco_engine": connection.settings_dict["ENGINE"],
        "migracoes_pendentes": [
            f"{migration.app_label}.{migration.name}"
            for migration, _ in pendentes
        ],
        "migracoes_ok": not pendentes,
        "total_avaliacoes": total_avaliacoes,
        "total_planos": total_planos,
        "total_respostas_enquete": total_respostas_enquete,
        "total_usuarios": total_usuarios,
        "total_alunos": total_alunos,
        "total_funcionarios": total_funcionarios,
        "ia_gemini_ativo": ia_gemini_ativo,
        "modulos": modulos,
        "unidade_nome": "Academia Polo Fit",
        "unidade_cidade": "Picuí - PB",
        "unidade_endereco": "Rua Antônio dos Santos, nº 62, Bairro Cenecista",
        "unidade_telefone": "(83) 98671-9438",
        "unidade_horario": "Seg-Sex: 05h às 22h · Sáb: 11h às 19h",
    }
    return render(request, "feedback/configuracao_sistema.html", contexto)


@staff_required(permission="feedback.view_avaliacao")
def divulgacao(request):
    link_publico = request.build_absolute_uri(reverse("inicio"))
    mensagem = (
        "Conheça o Polo Feedback, uma solução digital para ouvir alunos e "
        "acompanhar oportunidades de melhoria em academias: "
        f"{link_publico}"
    )
    return render(
        request,
        "feedback/divulgacao.html",
        {
            "link_publico": link_publico,
            "mensagem_whatsapp": mensagem,
            "link_whatsapp": (
                "https://wa.me/?text="
                + quote(mensagem)
            ),
            "link_funciona_publicamente": request.get_host().split(":", 1)[0].lower()
            not in {"localhost", "127.0.0.1"},
        },
    )


@staff_required(permission="feedback.view_avaliacao")
def gerar_qrcode(request):

    qrcode_base64 = None
    localizacao = ""
    url_gerada = ""

    ip_local = _obter_ip_local()

    usar_ip = request.GET.get("usar_ip") == "1"

    localizacao = request.GET.get("localizacao", "Área de Musculação").strip()
    if not localizacao:
        localizacao = "Área de Musculação"

    if localizacao:

        if usar_ip and ip_local != "127.0.0.1":

            porta = request.get_port()

            host = (
                f"{ip_local}:{porta}"
                if porta and porta not in ["80", "443"]
                else ip_local
            )

        else:

            host = request.get_host()

        protocolo = "https" if request.is_secure() else "http"

        if "enquete" in localizacao.lower():
            url_gerada = f"{protocolo}://{host}/enquete/"
        else:
            url_gerada = f"{protocolo}://{host}/avaliar/?localizacao={quote(localizacao)}"

        qrcode_base64 = _gerar_qrcode_base64(url_gerada, box_size=10)

    return render(
        request,
        "feedback/qrcode.html",
        {
            "qrcode_base64": qrcode_base64,
            "localizacao": localizacao,
            "url_gerada": url_gerada,
            "ip_local": ip_local,
            "usando_ip": usar_ip,
        },
    )


def treino_equipamento(request, identificador_qr):
    equipamento = get_object_or_404(
        Equipamento,
        identificador_qr=identificador_qr,
        ativo=True,
    )
    exercicios = equipamento.exercicios.filter(ativo=True)
    itens_plano = ItemPlanoTreino.objects.none()

    if request.user.is_authenticated:
        itens_plano = (
            ItemPlanoTreino.objects.filter(
                plano__aluno=request.user,
                plano__ativo=True,
                exercicio__equipamento=equipamento,
                exercicio__ativo=True,
            )
            .select_related("plano", "exercicio")
            .order_by("plano__nome", "ordem", "id")
        )
    else:
        return redirect_to_login(
            request.get_full_path(),
            login_url=reverse("login"),
        )

    return render(
        request,
        "feedback/treino_equipamento.html",
        {
            "equipamento": equipamento,
            "exercicios": exercicios,
            "itens_plano": itens_plano,
        },
    )


def cadastro_aluno(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            destino = (
                "dashboard"
                if request.user.has_perm("feedback.view_avaliacao")
                else "qrcodes_treinos"
            )
            return redirect(destino)
        return redirect("meus_treinos")

    form = CadastroAlunoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        aluno = form.save()
        login(request, aluno)
        return redirect("meus_treinos")

    return render(request, "registration/cadastro_aluno.html", {"form": form})


@login_required
def meus_treinos(request):
    if request.user.is_staff and request.user.has_perm("feedback.view_avaliacao"):
        return redirect("dashboard")

    itens_ativos = (
        ItemPlanoTreino.objects.filter(
            exercicio__ativo=True,
            exercicio__equipamento__ativo=True,
        )
        .select_related("exercicio", "exercicio__equipamento")
        .order_by("ordem", "id")
    )
    planos = PlanoTreino.objects.filter(
        aluno=request.user,
        ativo=True,
    ).prefetch_related(Prefetch("itens", queryset=itens_ativos, to_attr="itens_ativos"))

    return render(request, "feedback/meus_treinos.html", {"planos": planos})


@staff_required
def gestao_treinos(request):
    planos = (
        PlanoTreino.objects.select_related("aluno", "professor")
        .annotate(quantidade_exercicios=models.Count("itens"))
        .order_by("-atualizado_em")
    )
    return render(request, "feedback/gestao_treinos.html", {"planos": planos})


@staff_required
def editar_plano_treino(request, plano_id=None):
    if plano_id is None:
        plano = PlanoTreino(professor=request.user)
    else:
        plano = get_object_or_404(PlanoTreino, pk=plano_id)

    form = PlanoTreinoForm(request.POST or None, instance=plano)
    formset = ItemPlanoTreinoFormSet(request.POST or None, instance=plano)

    form_valido = form.is_valid()
    formset_valido = formset.is_valid()

    if request.method == "POST" and form_valido and formset_valido:
        with transaction.atomic():
            plano = form.save(commit=False)
            if plano.professor_id is None:
                plano.professor = request.user
            plano.save()
            formset.instance = plano
            formset.save()
        return redirect("gestao_treinos")

    return render(
        request,
        "feedback/form_plano_treino.html",
        {
            "form": form,
            "formset": formset,
            "plano": plano,
        },
    )


@staff_required
def qrcodes_treinos(request):
    equipamentos = []
    for equipamento in Equipamento.objects.filter(ativo=True):
        url = request.build_absolute_uri(
            reverse(
                "treino_equipamento",
                kwargs={"identificador_qr": equipamento.identificador_qr},
            )
        )
        equipamentos.append(
            {
                "equipamento": equipamento,
                "url": url,
                "qr_base64": _gerar_qrcode_base64(url),
            }
        )

    return render(
        request,
        "feedback/treinos_qrcodes.html",
        {"equipamentos": equipamentos},
    )


def _coletar_dados_gerenciais_ia():
    usuario_model = get_user_model()
    avaliacoes = list(
        Avaliacao.objects.all()
        .select_related("funcionario")
        .prefetch_related("funcionarios", "funcionarios__funcoes")
        .order_by("-data_criacao")
    )
    categorias = Counter()
    tipos = Counter()
    notas = Counter()
    status = Counter()
    locais = Counter()
    avaliacoes_por_funcionario = defaultdict(list)

    for avaliacao in avaliacoes:
        categorias_avaliacao = (
            avaliacao.categorias
            if isinstance(avaliacao.categorias, list) and avaliacao.categorias
            else [avaliacao.categoria]
        )
        categorias.update(item for item in categorias_avaliacao if item)

        tipos_avaliacao = set(
            avaliacao.tipos_feedback
            if isinstance(avaliacao.tipos_feedback, list)
            else []
        )
        if avaliacao.tipo_feedback:
            tipos_avaliacao.add(avaliacao.tipo_feedback)
        tipos.update(tipo for tipo in tipos_avaliacao if tipo)

        if avaliacao.nota:
            notas[avaliacao.nota] += 1
        status[avaliacao.status] += 1
        if avaliacao.localizacao:
            locais[avaliacao.localizacao] += 1

        funcionarios = {
            funcionario.pk: funcionario
            for funcionario in avaliacao.funcionarios.all()
        }
        if avaliacao.funcionario_id:
            funcionarios[avaliacao.funcionario_id] = avaliacao.funcionario
        for funcionario_id in funcionarios:
            avaliacoes_por_funcionario[funcionario_id].append(avaliacao)

    categoria_labels = dict(Avaliacao.CATEGORIA_CHOICES)
    categoria_texto = ", ".join(
        f"{categoria_labels.get(chave, chave)}: {quantidade}"
        for chave, quantidade in categorias.most_common()
    ) or "sem avaliações por categoria"
    notas_texto = ", ".join(
        f"{nota} estrela(s): {notas[nota]}" for nota in range(1, 6)
    )
    locais_texto = ", ".join(
        f"{local}: {quantidade}" for local, quantidade in locais.most_common(8)
    ) or "sem local informado"

    ranking = []
    elogios_por_funcionario = Counter()
    for funcionario in Funcionario.objects.filter(ativo=True).prefetch_related("funcoes"):
        avaliacoes_funcionario = avaliacoes_por_funcionario.get(funcionario.pk, [])
        funcionario_tipos = Counter(
            tipo
            for avaliacao in avaliacoes_funcionario
            for tipo in (
                set(
                    avaliacao.tipos_feedback
                    if isinstance(avaliacao.tipos_feedback, list)
                    else []
                )
                | ({avaliacao.tipo_feedback} if avaliacao.tipo_feedback else set())
            )
        )
        funcionario_notas = [
            avaliacao.nota
            for avaliacao in avaliacoes_funcionario
            if avaliacao.nota is not None
        ]
        media_funcionario = (
            sum(funcionario_notas) / len(funcionario_notas)
            if funcionario_notas
            else None
        )
        media_funcionario_texto = (
            f"{media_funcionario:.1f}/5" if media_funcionario is not None else "sem avaliações"
        )
        ranking.append(
            f"{funcionario.nome} ({funcionario.funcoes_display or 'Função não informada'}): "
            f"{len(avaliacoes_funcionario)} avaliação(ões), "
            f"{funcionario_tipos['elogio']} elogio(s), "
            f"{funcionario_tipos['reclamacao']} reclamação(ões), "
            f"média {media_funcionario_texto}"
        )
        if funcionario_tipos["elogio"]:
            elogios_por_funcionario[funcionario.nome] = funcionario_tipos["elogio"]
    ranking_texto = "\n".join(ranking) or "Nenhum funcionário ativo cadastrado."

    respostas_enquete = list(
        RespostaEnquete.objects.all()
        .prefetch_related("funcionarios_elogiados")
        .order_by("-data_criacao")
    )
    aulas_favoritas = Counter()
    aulas_melhoria = Counter()
    novos_espacos = Counter()
    participacao = Counter()
    aulas_faltantes = Counter()
    sugestoes_valor = []
    elogios_colaboradores = []
    elogios_colaboradores_nomes = Counter()
    for resposta in respostas_enquete:
        aulas_favoritas.update(resposta.aulas_favoritas or [])
        aulas_melhoria.update(resposta.aula_melhoria or [])
        novos_espacos.update(resposta.novo_espaco or [])
        if resposta.aulas_favoritas_outra:
            aulas_favoritas[resposta.aulas_favoritas_outra.strip()] += 1
        if resposta.novo_espaco_outro:
            novos_espacos[resposta.novo_espaco_outro.strip()] += 1
        if resposta.participa_aulas:
            participacao[resposta.participa_aulas] += 1
        if resposta.aula_falta.strip():
            aulas_faltantes[resposta.aula_falta.strip()] += 1
        if resposta.sugestao_valor.strip():
            sugestoes_valor.append(resposta.sugestao_valor.strip())
        if resposta.elogio_colaborador.strip():
            elogios_colaboradores.append(resposta.elogio_colaborador.strip())
        for funcionario in resposta.funcionarios_elogiados.all():
            elogios_colaboradores_nomes[funcionario.nome] += 1

    def formatar_contagem(contagem):
        return ", ".join(
            f"{nome}: {quantidade}" for nome, quantidade in contagem.most_common(6)
        ) or "sem respostas registradas"

    comentarios = [
        avaliacao.comentario.strip()
        for avaliacao in avaliacoes
        if avaliacao.comentario.strip()
    ][:8]
    
    # Remover tags HTML dos comentários
    import re
    comentarios_limpos = [re.sub(r'<[^>]+>', '', c) for c in comentarios]
    tipos_labels = dict(Avaliacao.TIPO_CHOICES)
    media = (
        sum(avaliacao.nota for avaliacao in avaliacoes) / len(avaliacoes)
        if avaliacoes
        else None
    )
    total_av = len(avaliacoes)
    pct_elogios = round((tipos["elogio"] / total_av) * 100) if total_av else 0
    pct_reclamacoes = round((tipos["reclamacao"] / total_av) * 100) if total_av else 0
    pct_sugestoes = round((tipos["sugestao"] / total_av) * 100) if total_av else 0

    return {
        "total": total_av,
        "media": media,
        "media_texto": f"{media:.1f}/5" if media is not None else "sem avaliações",
        "elogios": tipos["elogio"],
        "reclamacoes": tipos["reclamacao"],
        "sugestoes": tipos["sugestao"],
        "percentual_elogios": pct_elogios,
        "percentual_reclamacoes": pct_reclamacoes,
        "percentual_sugestoes": pct_sugestoes,
        "notas_dict": {nota: notas[nota] for nota in range(1, 6)},
        "categorias_lista": [
            {
                "chave": chave,
                "nome": categoria_labels.get(chave, chave),
                "total": quantidade,
                "percentual": round((quantidade / total_av) * 100) if total_av else 0,
            }
            for chave, quantidade in categorias.most_common()
        ],
        "status": status,
        "status_texto": (
            f"pendentes: {status['pendente']}, em análise: {status['em_analise']}, "
            f"resolvidas: {status['resolvida']}"
        ),
        "categorias": categoria_texto,
        "notas": notas_texto,
        "locais": locais_texto,
        "tipos": ", ".join(
            f"{tipos_labels.get(tipo, tipo)}: {tipos[tipo]}"
            for tipo, _ in Avaliacao.TIPO_CHOICES
        ),
        "ranking": ranking_texto,
        "ranking_funcionarios": ranking,
        "elogios_por_funcionario": elogios_por_funcionario,
        "comentarios": comentarios_limpos,
        "total_enquetes": len(respostas_enquete),
        "alunos_total": usuario_model.objects.filter(is_staff=False).count(),
        "alunos_ativos": usuario_model.objects.filter(
            is_staff=False,
            is_active=True,
        ).count(),
        "equipamentos_ativos": Equipamento.objects.filter(ativo=True).count(),
        "exercicios_ativos": Exercicio.objects.filter(ativo=True).count(),
        "planos_ativos": PlanoTreino.objects.filter(ativo=True).count(),
        "participacao": formatar_contagem(participacao),
        "aulas_favoritas": formatar_contagem(aulas_favoritas),
        "aulas_melhoria": formatar_contagem(aulas_melhoria),
        "aulas_faltantes": formatar_contagem(aulas_faltantes),
        "novos_espacos": formatar_contagem(novos_espacos),
        "sugestoes_valor": sugestoes_valor[:6],
        "elogios_colaboradores": elogios_colaboradores[:6],
        "elogios_colaboradores_nomes": formatar_contagem(elogios_colaboradores_nomes),
    }


def _gerar_html_graficos_ia(dados):
    total = dados.get("total", 0)
    media = dados.get("media") or 0.0
    elogios = dados.get("elogios", 0)
    reclamacoes = dados.get("reclamacoes", 0)
    sugestoes = dados.get("sugestoes", 0)

    pct_elogios = dados.get("percentual_elogios", 0)
    pct_reclamacoes = dados.get("percentual_reclamacoes", 0)
    pct_sugestoes = dados.get("percentual_sugestoes", 0)

    notas_raw = dados.get("notas_dict", {})
    if not notas_raw:
        notas_raw = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        import re
        texto_notas = dados.get("notas", "")
        for n in range(1, 6):
            m = re.search(rf"{n}\s*estrela\(s\):\s*(\d+)", texto_notas)
            if m:
                notas_raw[n] = int(m.group(1))

    categorias_lista = dados.get("categorias_lista", [])
    if not categorias_lista:
        cat_texto = dados.get("categorias", "")
        categorias_lista = []
        if cat_texto and cat_texto != "sem avaliações por categoria":
            for parte in cat_texto.split(","):
                if ":" in parte:
                    nome, qtd = parte.split(":", 1)
                    try:
                        categorias_lista.append({"nome": nome.strip(), "total": int(qtd.strip())})
                    except ValueError:
                        pass

    status_raw = dados.get("status", {})
    pendentes = status_raw.get("pendente", 0)
    em_analise = status_raw.get("em_analise", 0)
    resolvidas = status_raw.get("resolvida", 0)

    linhas_estrelas = []
    cores_estrelas = {
        5: "#22c55e",
        4: "#a3e635",
        3: "#eab308",
        2: "#f97316",
        1: "#ef4444",
    }
    for n in (5, 4, 3, 2, 1):
        qtd = notas_raw.get(n, 0)
        pct = round((qtd / total) * 100) if total else 0
        cor = cores_estrelas.get(n, "#a3e635")
        linhas_estrelas.append(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:0.8rem;">
                <span style="width:32px;color:#cbd5e1;font-weight:700;">{n} ★</span>
                <div style="flex:1;height:8px;background:rgba(255,255,255,0.08);border-radius:999px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{cor};border-radius:999px;"></div>
                </div>
                <span style="width:68px;text-align:right;color:#94a3b8;font-size:0.75rem;">{qtd} ({pct}%)</span>
            </div>
        """)
    html_estrelas = "".join(linhas_estrelas)

    linhas_cat = []
    max_cat = max([c["total"] for c in categorias_lista], default=1)
    icones_cat = {
        "equipamentos": "🏋️",
        "estrutura": "🏢",
        "limpeza": "🧹",
        "professores": "👨‍🏫",
        "profissionais": "👥",
        "atendimento": "🧑‍💼",
        "aulas": "🥊",
        "treino": "💪",
        "avaliacao": "📋",
        "geral": "💡",
    }
    for item in categorias_lista[:5]:
        nome = item["nome"]
        qtd = item["total"]
        pct_bar = round((qtd / max_cat) * 100) if max_cat else 0
        pct_total = round((qtd / total) * 100) if total else 0
        icone = "📌"
        for k, ic in icones_cat.items():
            if k in nome.lower():
                icone = ic
                break
        linhas_cat.append(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;font-size:0.8rem;">
                <span style="width:115px;color:#e2e8f0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;" title="{nome}">{icone} {nome}</span>
                <div style="flex:1;height:8px;background:rgba(255,255,255,0.08);border-radius:999px;overflow:hidden;">
                    <div style="width:{pct_bar}%;height:100%;background:linear-gradient(90deg, #a3e635, #4ade80);border-radius:999px;"></div>
                </div>
                <span style="width:68px;text-align:right;color:#94a3b8;font-size:0.75rem;">{qtd} ({pct_total}%)</span>
            </div>
        """)
    html_categorias = "".join(linhas_cat) if linhas_cat else '<p style="font-size:0.8rem;color:#94a3b8;">Sem dados de categorias.</p>'

    html = f"""
    <div class="ia-graficos-wrapper" style="background:rgba(15,15,15,0.85);border:1px solid rgba(163,230,53,0.25);border-radius:12px;padding:16px;margin:10px 0;box-shadow:0 4px 20px rgba(0,0,0,0.4);">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:10px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:1.15rem;">📊</span>
                <strong style="color:#a3e635;font-size:0.95rem;letter-spacing:-0.01em;">Métricas e Gráficos das Avaliações</strong>
            </div>
            <span style="font-size:0.75rem;padding:3px 8px;border-radius:999px;background:rgba(163,230,53,0.15);color:#a3e635;font-weight:700;">
                {total} avaliações
            </span>
        </div>

        <!-- 4 CARDS RESUMO -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(120px, 1fr));gap:8px;margin-bottom:16px;">
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:900;color:#a3e635;">{media:.1f} ★</div>
                <div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:700;margin-top:2px;">Nota Média</div>
            </div>
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:900;color:#22c55e;">{pct_elogios}%</div>
                <div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:700;margin-top:2px;">Elogios ({elogios})</div>
            </div>
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:900;color:{'#ef4444' if reclamacoes > 0 else '#94a3b8'};">{reclamacoes}</div>
                <div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:700;margin-top:2px;">Reclamações</div>
            </div>
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:10px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:900;color:#eab308;">{sugestoes}</div>
                <div style="font-size:0.7rem;color:#94a3b8;text-transform:uppercase;font-weight:700;margin-top:2px;">Sugestões</div>
            </div>
        </div>

        <!-- GRÁFICO 1: BARRA DE SENTIMENTO -->
        <div style="margin-bottom:16px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:0.78rem;font-weight:700;color:#e2e8f0;">Distribuição de Sentimento</span>
                <span style="font-size:0.72rem;color:#94a3b8;">{pct_elogios}% Positivo</span>
            </div>
            <div style="height:12px;background:rgba(255,255,255,0.08);border-radius:999px;overflow:hidden;display:flex;">
                <div style="width:{pct_elogios}%;background:#22c55e;" title="Elogios: {elogios} ({pct_elogios}%)"></div>
                <div style="width:{pct_sugestoes}%;background:#eab308;" title="Sugestões: {sugestoes} ({pct_sugestoes}%)"></div>
                <div style="width:{pct_reclamacoes}%;background:#ef4444;" title="Reclamações: {reclamacoes} ({pct_reclamacoes}%)"></div>
            </div>
            <div style="display:flex;gap:12px;margin-top:6px;font-size:0.72rem;color:#94a3b8;flex-wrap:wrap;">
                <span style="display:inline-flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:50%;background:#22c55e;"></span> Elogios ({elogios})</span>
                <span style="display:inline-flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:50%;background:#eab308;"></span> Sugestões ({sugestoes})</span>
                <span style="display:inline-flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:50%;background:#ef4444;"></span> Reclamações ({reclamacoes})</span>
            </div>
        </div>

        <!-- GRÁFICO 2 & 3: GRID DE 2 COLUNAS (NOTAS + CATEGORIAS) -->
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(240px, 1fr));gap:14px;margin-bottom:14px;">
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:12px;">
                <div style="font-size:0.8rem;font-weight:700;color:#e2e8f0;margin-bottom:10px;">⭐ Distribuição por Estrelas</div>
                {html_estrelas}
            </div>
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:12px;">
                <div style="font-size:0.8rem;font-weight:700;color:#e2e8f0;margin-bottom:10px;">📍 Setores Mais Avaliados</div>
                {html_categorias}
            </div>
        </div>

        <!-- STATUS DE RESOLUÇÃO -->
        <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:8px 12px;font-size:0.75rem;">
            <span style="color:#94a3b8;font-weight:600;">Status das Ações:</span>
            <div style="display:flex;gap:12px;flex-wrap:wrap;">
                <span style="color:#fbbf24;">⏳ Pendentes: <strong>{pendentes}</strong></span>
                <span style="color:#60a5fa;">🔍 Em análise: <strong>{em_analise}</strong></span>
                <span style="color:#4ade80;">✅ Resolvidas: <strong>{resolvidas}</strong></span>
            </div>
        </div>
    </div>
    """
    return html


def _gerar_resumo_executivo_local(dados):
    # Remover tags HTML dos comentários
    import re
    comentarios_limpos = [re.sub(r'<[^>]+>', '', c) for c in dados["comentarios"]]
    comentarios = "\n".join(f'• "{comentario}"' for comentario in comentarios_limpos)
    sugestoes_valor = "\n".join(
        f"• {sugestao}" for sugestao in dados["sugestoes_valor"]
    )
    elogios = "\n".join(
        f"• {elogio}" for elogio in dados["elogios_colaboradores"]
    )
    if (
        not dados["total"]
        and not dados["total_enquetes"]
        and not dados["ranking_funcionarios"]
        and not dados["alunos_total"]
        and not dados["equipamentos_ativos"]
        and not dados["exercicios_ativos"]
        and not dados["planos_ativos"]
    ):
        return "Ainda não há avaliações nem respostas de enquete para resumir."

    return f"""**Resumo geral da Academia Polo Fit**

**Avaliações:** {dados['total']} registro(s), nota média {dados['media_texto']}; {dados['elogios']} elogio(s), {dados['reclamacoes']} reclamação(ões) e {dados['sugestoes']} sugestão(ões). {dados['status_texto']}.
**Tópicos avaliados:** {dados['categorias']}.
**Distribuição das notas:** {dados['notas']}.
**Locais mais avaliados:** {dados['locais']}.

**Equipe:** {dados['ranking']}

**Enquete:** {dados['total_enquetes']} resposta(s). Participação em aulas: {dados['participacao']}. Aulas favoritas: {dados['aulas_favoritas']}. Aulas indicadas para melhoria: {dados['aulas_melhoria']}. Aulas que os alunos sentem falta: {dados['aulas_faltantes']}. Espaços desejados: {dados['novos_espacos']}. Colaboradores mais elogiados na enquete: {dados['elogios_colaboradores_nomes']}.

**Módulo de treinos:** {dados['alunos_total']} aluno(s) cadastrado(s), {dados['alunos_ativos']} ativo(s); {dados['equipamentos_ativos']} equipamento(s), {dados['exercicios_ativos']} exercício(s) e {dados['planos_ativos']} plano(s) ativo(s).

**Sugestões de valor:** {sugestoes_valor or 'nenhuma sugestão aberta registrada'}.
**Elogios escritos à equipe:** {elogios or 'nenhum elogio aberto registrado'}.
**Comentários recentes das avaliações:** {comentarios or 'nenhum comentário registrado'}.

**Próximos passos:** priorizar as reclamações pendentes, revisar os tópicos e aulas com mais pedidos de melhoria e reconhecer os funcionários elogiados. Os números descrevem os registros disponíveis e não substituem uma análise de contexto."""


def _contexto_dados_gerenciais(dados):
    # Remover tags HTML dos comentários
    import re
    comentarios_limpos = [re.sub(r'<[^>]+>', '', c) for c in dados["comentarios"]]
    comentarios = "\n".join(f'- "{texto}"' for texto in comentarios_limpos)
    sugestoes = "\n".join(f"- {texto}" for texto in dados["sugestoes_valor"])
    elogios = "\n".join(f"- {texto}" for texto in dados["elogios_colaboradores"])
    return f"""Dados atualizados do Polo Fit:
AVALIAÇÕES: total {dados['total']}; média {dados['media_texto']}; {dados['tipos']}; status {dados['status_texto']}.
CATEGORIAS: {dados['categorias']}.
NOTAS: {dados['notas']}.
LOCAIS: {dados['locais']}.
FUNCIONÁRIOS ATIVOS: {dados['ranking']}.
ENQUETE: {dados['total_enquetes']} respostas; participação em aulas: {dados['participacao']}; favoritas: {dados['aulas_favoritas']}; melhorias de aulas: {dados['aulas_melhoria']}; aulas que fazem falta: {dados['aulas_faltantes']}; novos espaços: {dados['novos_espacos']}; funcionários elogiados: {dados['elogios_colaboradores_nomes']}.
MÓDULO DE TREINOS: {dados['alunos_total']} alunos cadastrados ({dados['alunos_ativos']} ativos); {dados['equipamentos_ativos']} equipamentos, {dados['exercicios_ativos']} exercícios e {dados['planos_ativos']} planos ativos.
SUGESTÕES DE VALOR: {sugestoes or 'sem respostas'}.
ELOGIOS ABERTOS À EQUIPE: {elogios or 'sem respostas'}.
COMENTÁRIOS RECENTES: {comentarios or 'sem comentários'}.
Use somente estes dados para afirmações sobre resultados; avise quando algo não estiver disponível."""


def _solicitar_resposta_gemini(system_instruction, contents):
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if not api_key:
        return None

    modelo_cfg = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
    modelos = list(dict.fromkeys((modelo_cfg, "gemini-2.5-flash", "gemini-2.5-flash-lite")))
    for modelo in modelos:
        url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/{modelo}:generateContent?key={api_key}"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": 1000,
                "temperature": 0.4,
            },
        }
        request_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=request_data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            logger.warning(
                "Falha ao consultar Gemini no modelo %s (%s).",
                modelo,
                type(error).__name__,
            )
            continue

        if not isinstance(result, dict):
            logger.warning("Gemini retornou resposta inválida para o modelo %s.", modelo)
            continue
        candidates = result.get("candidates", [])
        if candidates and isinstance(candidates[0], dict):
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts and isinstance(parts[0], dict) and parts[0].get("text"):
                return parts[0]["text"]
        logger.warning("Gemini não retornou texto para o modelo %s.", modelo)
    return None


@csrf_exempt
@staff_required(permission="feedback.view_avaliacao")
def ia_analisar(request):
    dados = _coletar_dados_gerenciais_ia()
    if (
        not dados["total"]
        and not dados["total_enquetes"]
        and not dados["ranking_funcionarios"]
        and not dados["alunos_total"]
        and not dados["equipamentos_ativos"]
        and not dados["exercicios_ativos"]
        and not dados["planos_ativos"]
    ):
        return JsonResponse(
            {
                "analise": "Ainda não há avaliações nem respostas de enquete para resumir.",
                "graficos_html": None,
            }
        )

    graficos_html = _gerar_html_graficos_ia(dados)

    system_instruction = (
        "Você é o assistente executivo da Academia Polo Fit. Gere em português "
        "brasileiro um resumo gerencial objetivo com pontos fortes, pontos de "
        "atenção e ações práticas. Inclua avaliações, categorias, notas, locais, "
        "desempenho de funcionários e todos os tópicos da enquete. Não invente "
        "resultados, não identifique alunos e indique quando não houver dados."
    )
    prompt = (
        _contexto_dados_gerenciais(dados)
        + "\n\nFaça um resumo geral de todos os dados disponíveis, em até 350 palavras."
    )
    resposta = _solicitar_resposta_gemini(
        system_instruction,
        [{"role": "user", "parts": [{"text": prompt}]}],
    )
    if resposta:
        return JsonResponse({
            "analise": resposta,
            "graficos_html": graficos_html,
            "modo": "gemini"
        })

    return JsonResponse(
        {
            "analise": _gerar_resumo_executivo_local(dados),
            "graficos_html": graficos_html,
            "modo": "local",
            "aviso": (
                "O Gemini não está disponível agora; este resumo foi montado "
                "diretamente a partir dos dados registrados."
            ),
        }
    )


def _gerar_resposta_conversacional_local(pergunta, dados):
    texto_normalizado = unicodedata.normalize("NFKD", pergunta.lower())
    texto_normalizado = "".join(
        caractere
        for caractere in texto_normalizado
        if not unicodedata.combining(caractere)
    )
    p = re.sub(r"[^\w\s]", " ", texto_normalizado)
    p = " ".join(p.split())

    saudacao = next(
        (
            cumprimento
            for cumprimento in ("bom dia", "boa tarde", "boa noite", "oi", "ola", "e ai")
            if p == cumprimento or p.startswith(f"{cumprimento} ")
        ),
        "",
    )
    if saudacao:
        p = p[len(saudacao) :].strip()

    abertura = f"{saudacao.capitalize()}! " if saudacao else ""
    if p in {"", "tudo bem", "como vai", "tudo bem voce"}:
        return (
            f"{abertura}Tudo bem, obrigado por perguntar! Como posso ajudar? "
            "Posso mostrar os gráficos de avaliações, consultar equipe, analisar reclamações ou gerar um resumo completo."
        )

    if p in {"obrigado", "obrigada", "muito obrigado", "muito obrigada", "valeu"}:
        return "Por nada! Se quiser, posso consultar outro indicador ou fazer um resumo geral."

    if any(termo in p for termo in ("grafico", "graficos")):
        return (
            f"Aqui estão os gráficos detalhados das avaliações da Polo Fit! 📊\n\n"
            f"• Total de {dados['total']} avaliações registradas com nota média de {dados['media_texto']}.\n"
            f"• Elogios: {dados['elogios']} ({dados.get('percentual_elogios', 0)}%) | "
            f"Reclamações: {dados['reclamacoes']} ({dados.get('percentual_reclamacoes', 0)}%) | "
            f"Sugestões: {dados['sugestoes']} ({dados.get('percentual_sugestoes', 0)}%).\n\n"
            "Confira os gráficos visuais de sentimento, notas e áreas avaliadas logo acima."
        )

    if any(
        termo in p
        for termo in (
            "o que voce pode fazer",
            "como voce pode me ajudar",
            "quais informacoes voce tem",
            "ajuda",
        )
    ):
        return (
            "Posso ajudar você a analisar satisfação e notas, exibir gráficos das avaliações, "
            "tópicos avaliados, reclamações, sugestões, desempenho dos funcionários e enquete. "
            "Também posso montar um resumo geral de todos os dados disponíveis."
        )

    if any(
        termo in p
        for termo in ("resumo", "visao geral", "todos os dados", "tudo sobre")
    ):
        return _gerar_resumo_executivo_local(dados)

    if any(termo in p for termo in ("enquete", "aula", "aulas", "espaco", "espaço", "participa")):
        return f"""**Resultados da enquete** ({dados['total_enquetes']} resposta(s))

• Participação em aulas: {dados['participacao']}.
• Aulas favoritas: {dados['aulas_favoritas']}.
• Aulas que precisam de melhoria: {dados['aulas_melhoria']}.
• Aulas que os alunos sentem falta: {dados['aulas_faltantes']}.
• Novos espaços desejados: {dados['novos_espacos']}.
• Funcionários elogiados: {dados['elogios_colaboradores_nomes']}.
• Sugestões abertas: {'; '.join(dados['sugestoes_valor'][:3]) or 'nenhuma resposta registrada'}."""

    if any(
        termo in p
        for termo in ("professor", "funcionario", "equipe", "ranking", "quem", "instrutor", "atendente")
    ):
        return f"""**Desempenho da equipe**

{dados['ranking']}

Os números mostram avaliações associadas a cada funcionário; considere também o volume de respostas ao comparar médias."""

    if any(
        termo in p
        for termo in ("reclamacao", "problema", "critica", "queixa", "ruim", "defeito")
    ):
        comentarios = "\n".join(f'• "{texto}"' for texto in dados["comentarios"])
        return f"""**Reclamações e acompanhamento**

• Reclamações registradas: {dados['reclamacoes']}.
• {dados['status_texto']}.
• Categorias: {dados['categorias']}.
• Comentários recentes: {comentarios or 'nenhum comentário registrado'}.

Revise as avaliações pendentes no painel e atualize o status quando a equipe iniciar ou concluir o atendimento."""

    if any(termo in p for termo in ("sugestao", "melhorar", "ideia", "prioridade", "acao")):
        return f"""**Sugestões e oportunidades**

• Sugestões nas avaliações: {dados['sugestoes']}.
• Tópicos avaliados: {dados['categorias']}.
• Aulas para melhoria: {dados['aulas_melhoria']}.
• Espaços desejados: {dados['novos_espacos']}.
• Sugestões da enquete: {'; '.join(dados['sugestoes_valor'][:4]) or 'nenhuma resposta aberta registrada'}.

Priorize os temas que aparecem repetidamente e valide as ações com a equipe."""

    if any(termo in p for termo in ("satisfacao", "nota", "avaliacao", "avaliacoes", "feedback", "panorama", "desempenho")):
        return f"""**Panorama das avaliações**

• {dados['total']} avaliação(ões); nota média {dados['media_texto']}.
• Elogios: {dados['elogios']} ({dados.get('percentual_elogios', 0)}%); reclamações: {dados['reclamacoes']} ({dados.get('percentual_reclamacoes', 0)}%); sugestões: {dados['sugestoes']} ({dados.get('percentual_sugestoes', 0)}%).
• Status: {dados['status_texto']}.
• Categorias: {dados['categorias']}.
• Notas: {dados['notas']}.
• Locais: {dados['locais']}.

Se quiser, também posso detalhar os resultados da enquete ou da equipe."""

    return (
        f"{abertura}Entendi. Posso consultar gráficos das avaliações, categorias e notas, "
        "funcionários, reclamações, sugestões e enquete. Qual desses pontos você quer ver?"
    )


@csrf_exempt
@ensure_csrf_cookie
@staff_required(permission="feedback.view_avaliacao")
def ia_chat(request):
    if request.method == "GET":
        return render(request, "feedback/ia_chat.html")
    
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"erro": "A solicitação não contém JSON válido."}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({"erro": "Formato de solicitação inválido."}, status=400)

    mensagem_usuario = data.get("mensagem", "")
    if not isinstance(mensagem_usuario, str):
        return JsonResponse({"erro": "A mensagem deve ser texto."}, status=400)
    mensagem_usuario = mensagem_usuario.strip()
    if not mensagem_usuario:
        return JsonResponse({"erro": "Digite uma pergunta para continuar."}, status=400)
    if len(mensagem_usuario) > 1000:
        return JsonResponse(
            {"erro": "A mensagem deve ter no máximo 1.000 caracteres."},
            status=400,
        )

    historico = []
    historico_recebido = data.get("historico", [])
    if isinstance(historico_recebido, list):
        for item in historico_recebido[-8:]:
            if not isinstance(item, dict):
                continue
            papel = item.get("role")
            texto = item.get("content")
            if papel not in {"user", "assistant"} or not isinstance(texto, str):
                continue
            texto = texto.strip()
            if texto:
                historico.append(
                    {
                        "role": "model" if papel == "assistant" else "user",
                        "parts": [{"text": texto[:1000]}],
                    }
                )

    dados = _coletar_dados_gerenciais_ia()
    
    # Verificar se a mensagem pede gráficos, avaliações, satisfação ou métricas
    texto_norm = unicodedata.normalize("NFKD", mensagem_usuario.lower())
    texto_norm = "".join(c for c in texto_norm if not unicodedata.combining(c))
    deve_incluir_graficos = any(
        termo in texto_norm
        for termo in (
            "grafico", "graficos", "avaliacao", "avaliacoes", "nota", "notas",
            "satisfacao", "desempenho", "panorama", "resumo", "metricas", "indicador"
        )
    )
    graficos_html = _gerar_html_graficos_ia(dados) if deve_incluir_graficos else None

    system_instruction = (
        "Você é a assistente executiva da Academia Polo Fit, conversando com o "
        "gerente. Responda como em um chat natural: entenda a mensagem atual no "
        "contexto das mensagens anteriores, responda saudações e perguntas simples "
        "sem gerar relatórios desnecessários e faça uma pergunta objetiva se faltar "
        "contexto. Use português brasileiro, tom cordial e profissional. Para "
        "perguntas sobre a academia, use somente os dados fornecidos; não invente "
        "números, funcionários ou opiniões. Resuma todos os tópicos quando solicitado. "
        "Prefira respostas diretas e títulos/listas apenas quando ajudarem.\n\n"
        + _contexto_dados_gerenciais(dados)
    )
    contents = historico + [
        {"role": "user", "parts": [{"text": mensagem_usuario}]}
    ]
    resposta = _solicitar_resposta_gemini(system_instruction, contents)
    if resposta:
        return JsonResponse({
            "resposta": resposta,
            "graficos_html": graficos_html,
            "modo": "gemini"
        })

    resposta_local = _gerar_resposta_conversacional_local(mensagem_usuario, dados)
    aviso = (
        "O chat está usando respostas locais baseadas nos dados cadastrados. "
        "Para respostas generativas em conversa, configure uma chave Gemini válida."
    )
    return JsonResponse(
        {
            "resposta": resposta_local,
            "graficos_html": graficos_html,
            "modo": "local",
            "aviso": aviso
        }
    )


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect("login")

