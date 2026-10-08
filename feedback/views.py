import io
import base64
import json
import re
import socket
import unicodedata
import urllib.request
import urllib.error
import qrcode
from datetime import timedelta
from functools import wraps
from urllib.parse import quote

from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.views import redirect_to_login
from django.contrib.staticfiles import finders
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
    Funcao,
    Funcionario,
    ItemPlanoTreino,
    RespostaEnquete,
)


def staff_required(view_func=None, *, permission=None):
    def decorate(view):
        @wraps(view)
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not request.user.is_staff:
                return HttpResponseForbidden(
                    "Acesso permitido somente à equipe da academia."
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
        nota = request.POST.get("nota")
        tipos_feedback = request.POST.getlist("tipos_feedback")
        comentario = request.POST.get("comentario", "").strip()
        localizacao = request.POST.get("localizacao", "").strip()
        funcionario_ids = request.POST.getlist("funcionarios_ids")
        funcionarios_selecionados, selecao_valida = _selecionar_funcionarios(
            funcionario_ids
        )

        erros = []

        if not categorias:
            erros.append(
                "Selecione pelo menos um aspecto para avaliar "
                "(Atendimento, Limpeza, etc.)."
            )

        if not nota:
            erros.append("Avalie atribuindo uma nota de 1 a 5 estrelas.")

        if not tipos_feedback:
            erros.append(
                "Selecione o tipo de feedback " "(Elogio, Sugestão ou Reclamação)."
            )

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

        agora = timezone.now()

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
        for n in range(1, 6)
    ]

    # ==========================================================
    # FUNCIONÁRIOS
    # ==========================================================

    todos_funcionarios = (
        Funcionario.objects.filter(ativo=True)
        .prefetch_related("avaliacoes", "avaliacoes_multiplas", "funcoes")
    )

    # ==========================================================
    # RANKING DE FUNCIONÁRIOS
    # ==========================================================

    ranking_funcionarios = []

    for func in todos_funcionarios:

        avs = Avaliacao.objects.filter(
            models.Q(funcionario=func) | models.Q(funcionarios=func)
        ).distinct()

        total = avs.count()

        elogios = avs.filter(tipo_feedback="elogio").count()

        reclamacoes = avs.filter(tipo_feedback="reclamacao").count()

        sugestoes = avs.filter(tipo_feedback="sugestao").count()

        media_func = avs.aggregate(m=models.Avg("nota"))["m"] or 0

        foto_url = ""

        if func.foto:

            try:
                foto_url = func.foto.url
            except ValueError:
                foto_url = ""

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

    todas_avs = Avaliacao.objects.all()

    for nome_local, icone in LOCAIS_DEFINIDOS:

        avs_local = todas_avs.filter(localizacao=nome_local)

        total_local = avs_local.count()

        if total_local == 0:
            continue

        media_local = avs_local.aggregate(m=models.Avg("nota"))["m"] or 0

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
        },
    )


@staff_required(permission="feedback.view_avaliacao")
def configuracao_sistema(request):
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    executor = MigrationExecutor(connection)
    pendentes = executor.migration_plan(executor.loader.graph.leaf_nodes())
    return render(
        request,
        "feedback/configuracao_sistema.html",
        {
            "banco_engine": connection.settings_dict["ENGINE"],
            "migracoes_pendentes": [
                f"{migration.app_label}.{migration.name}"
                for migration, _ in pendentes
            ],
            "migracoes_ok": not pendentes,
        },
    )


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

    if request.GET.get("localizacao"):

        localizacao = request.GET.get("localizacao").strip()

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

            url_gerada = f"{protocolo}://{host}/" f"?localizacao={localizacao}"

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


def _gerar_resumo_executivo_local(
    avaliacoes,
    total,
    elogios,
    reclamacoes,
    sugestoes,
    media,
    pendentes,
    resolvidas,
):

    taxa_aprovacao = (
        round(
            (elogios / total * 100),
            1,
        )
        if total > 0
        else 0
    )

    cats = []

    for a in avaliacoes:

        if a.categorias and isinstance(
            a.categorias,
            list,
        ):

            cats.extend(a.categorias)

        elif a.categoria:

            cats.append(a.categoria)

    cont_cat = Counter(cats)

    principais_cats = [
        dict(Avaliacao.CATEGORIA_CHOICES).get(
            c,
            c.capitalize(),
        )
        for c, _ in cont_cat.most_common(2)
    ]

    setores_txt = " e ".join(principais_cats) if principais_cats else "Geral"

    comentarios = [a.comentario.strip() for a in avaliacoes if a.comentario.strip()][:3]

    amostra_comentarios = ""

    if comentarios:

        amostra_comentarios = "\n\n**O que os alunos estão dizendo:**\n" + "\n".join(
            f'• *"{c}"*' for c in comentarios
        )

    return f"""**📊 Resumo Executivo: Experiência e Qualidade — Polo Fit**

**1. Diagnóstico Geral de Desempenho**
• **Nota Média Geral:** {round(media, 1)} / 5.0 ⭐
• **Índice de Satisfação:** {taxa_aprovacao}% de feedbacks positivos ({elogios} elogios em {total} avaliações).
• **Status de Resolução:** {resolvidas} demandas resolvidas e {pendentes} em acompanhamento.

**2. Pontos Fortes em Destaque**
Os alunos demonstram alta satisfação especialmente nas áreas de **{setores_txt}**.

**3. Pontos de Atenção e Oportunidades**
Foram registradas {reclamacoes} reclamação(ões) e {sugestoes} sugestão(ões) de melhoria.

**4. Recomendações Práticas para a Gerência**
1. **Reconhecimento da Equipe:** Parabenizar os colaboradores mais elogiados.
2. **Tempo de Resposta:** Manter o acompanhamento das avaliações pendentes.
3. **Melhoria Contínua:** Utilizar as sugestões dos alunos para orientar melhorias futuras.{amostra_comentarios}"""


@staff_required(permission="feedback.view_avaliacao")
def ia_analisar(request):

    ids_recentes = list(
        Avaliacao.objects.order_by("-data_criacao").values_list(
            "id",
            flat=True,
        )[:50]
    )

    if not ids_recentes:

        return JsonResponse(
            {"analise": ("Nenhuma avaliação cadastrada " "ainda para analisar.")}
        )

    avaliacoes = Avaliacao.objects.filter(id__in=ids_recentes)

    total = avaliacoes.count()

    elogios = avaliacoes.filter(
        models.Q(tipo_feedback="elogio") | models.Q(tipos_feedback__icontains="elogio")
    ).count()

    reclamacoes = avaliacoes.filter(
        models.Q(tipo_feedback="reclamacao")
        | models.Q(tipos_feedback__icontains="reclamacao")
    ).count()

    sugestoes = avaliacoes.filter(
        models.Q(tipo_feedback="sugestao")
        | models.Q(tipos_feedback__icontains="sugestao")
    ).count()

    media = avaliacoes.aggregate(m=models.Avg("nota"))["m"] or 0

    pendentes = avaliacoes.filter(status="pendente").count()

    resolvidas = avaliacoes.filter(status="resolvida").count()

    comentarios = list(
        avaliacoes.exclude(comentario="").values_list(
            "comentario",
            flat=True,
        )[:10]
    )

    comentarios_txt = (
        "\n".join(f'- "{c}"' for c in comentarios) or "Nenhum comentário registrado."
    )

    prompt = f"""Você é um consultor especialista em qualidade para a academia Polo Fit.

Gere um resumo executivo direto e profissional para o gerente com base nos dados reais:

- Total: {total} avaliações
- Nota média geral: {round(media, 1)} de 5.0
- Elogios: {elogios}
- Reclamações: {reclamacoes}
- Sugestões: {sugestoes}
- Pendentes: {pendentes}
- Resolvidas: {resolvidas}

Comentários dos alunos:
{comentarios_txt}

Apresente em português brasileiro:

1. **Pontos Fortes**
2. **Pontos de Atenção**
3. **Recomendações Práticas para a Gerência**
4. **Visão Geral**

Máximo 250 palavras."""

    api_key = getattr(
        settings,
        "GEMINI_API_KEY",
        "",
    )

    modelo_cfg = getattr(
        settings,
        "GEMINI_MODEL",
        "gemini-1.5-flash",
    )

    modelos_ativos = list(
        dict.fromkeys(
            [
                modelo_cfg,
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]
        )
    )

    if api_key:

        for modelo in modelos_ativos:

            try:

                url = (
                    "https://generativelanguage.googleapis.com/"
                    f"v1beta/models/{modelo}:generateContent"
                    f"?key={api_key}"
                )

                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": 600,
                        "temperature": 0.6,
                    },
                }

                data = json.dumps(payload).encode("utf-8")

                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )

                with urllib.request.urlopen(
                    req,
                    timeout=8,
                ) as resp:

                    result = json.loads(resp.read().decode("utf-8"))

                cands = result.get(
                    "candidates",
                    [],
                )

                if cands:

                    parts = cands[0].get("content", {}).get("parts", [])

                    if parts and parts[0].get("text"):

                        return JsonResponse({"analise": parts[0].get("text")})

            except Exception:
                continue

    analise_local = _gerar_resumo_executivo_local(
        avaliacoes=avaliacoes,
        total=total,
        elogios=elogios,
        reclamacoes=reclamacoes,
        sugestoes=sugestoes,
        media=media,
        pendentes=pendentes,
        resolvidas=resolvidas,
    )

    return JsonResponse({"analise": analise_local})


def _gerar_resposta_conversacional_local(
    pergunta,
    total,
    media,
    elogios,
    reclamacoes,
    sugestoes,
    pendentes,
    resolvidas,
    ranking_txt,
    comentarios,
):

    p = unicodedata.normalize("NFKD", pergunta.lower())
    p = "".join(caractere for caractere in p if not unicodedata.combining(caractere))
    p = re.sub(r"[^\w\s]", " ", p)
    p = " ".join(p.split())

    saudacao = next(
        (
            cumprimento
            for cumprimento in (
                "bom dia",
                "boa tarde",
                "boa noite",
                "oi",
                "ola",
                "e ai",
            )
            if p == cumprimento or p.startswith(f"{cumprimento} ")
        ),
        "",
    )
    if saudacao:
        p = p[len(saudacao) :].strip()

    if p in {"", "tudo bem", "como vai", "tudo bem voce"}:
        return (
            f"{saudacao.capitalize() + '! ' if saudacao else 'Olá! '}"
            "Bom ter você por aqui. Como posso ajudar? "
            "Posso consultar a satisfação dos alunos, reclamações, sugestões "
            "ou avaliações da equipe."
        )

    if p in {
        "obrigado",
        "obrigada",
        "muito obrigado",
        "muito obrigada",
        "valeu",
    }:
        return (
            "Por nada! Estou à disposição para ajudar com os dados e as "
            "decisões de gestão da Polo Fit."
        )

    if any(
        termo in p
        for termo in [
            "o que voce pode fazer",
            "como voce pode me ajudar",
            "como pode me ajudar",
            "quais informacoes voce tem",
            "ajuda",
        ]
    ):
        return (
            "Posso ajudar você a analisar os indicadores da academia: satisfação "
            "e notas dos alunos, elogios, reclamações pendentes, sugestões, "
            "preferências da enquete e avaliações dos colaboradores. "
            "O que gostaria de consultar?"
        )

    if any(
        k in p
        for k in [
            "professor",
            "professores",
            "funcionario",
            "funcionarios",
            "equipe",
            "ranking",
            "quem",
            "instrutor",
            "atendente",
        ]
    ):

        return f"""**🏆 Análise da Equipe e Professores — Polo Fit**

Com base nas avaliações recentes dos alunos:

{ranking_txt}

**Recomendação para a Gerência:**
Considere reconhecer os colaboradores com maior número de elogios e acompanhar
as notas médias junto ao volume de avaliações de cada pessoa."""

    if any(
        k in p
        for k in [
            "reclamacao",
            "reclamacoes",
            "reclamação",
            "reclamações",
            "problema",
            "critica",
            "queixa",
            "ruim",
            "defeito",
        ]
    ):

        coments_rec = [
            c
            for c in comentarios
            if any(
                w in c.lower()
                for w in [
                    "quebrado",
                    "demora",
                    "ar",
                    "limpeza",
                    "espera",
                    "ruim",
                ]
            )
        ]

        amostra = (
            "\n*Comentários relacionados:* "
            + "; ".join(f'"{c}"' for c in coments_rec[:2])
            if coments_rec
            else ""
        )

        return f"""**⚠️ Panorama de Reclamações e Pontos Críticos**

• **Total de Reclamações:** {reclamacoes}
• **Demandas Pendentes:** {pendentes}
• **Demandas Resolvidas:** {resolvidas}.{amostra}

**Plano de Ação Recomendado:**

1. Verifique os chamados com status **Pendente**.
2. Altere para **Em Análise** quando a equipe iniciar a tratativa.
3. Registre a resolução diretamente no painel."""

    if any(
        k in p
        for k in [
            "sugestao",
            "sugestoes",
            "sugestão",
            "sugestões",
            "melhorar",
            "ideia",
            "plano",
            "acao",
            "ação",
        ]
    ):

        return f"""**💡 Ideias e Recomendações Estratégicas — Polo Fit**

Com base nas **{sugestoes} sugestões** e na nota média de **{round(media, 1)}/5.0**:

1. Avaliar melhorias nos horários de maior movimento.
2. Reforçar a manutenção preventiva dos equipamentos.
3. Manter os QR Codes visíveis para ampliar os feedbacks.
4. Compartilhar os elogios nas reuniões com a equipe."""

    if any(
        termo in p
        for termo in [
            "satisfacao",
            "satisfacao dos alunos",
            "nota",
            "notas",
            "resumo",
            "visao geral",
            "panorama",
            "desempenho",
            "avaliacao",
            "avaliacoes",
        ]
    ):
        return f"""**📋 Panorama de Feedbacks — Polo Fit**

• **Volume Total:** {total} avaliações.
• **Nota Média:** {round(media, 1)} / 5.0 ⭐
• **Elogios:** {elogios} 👍
• **Sugestões:** {sugestoes} 💡
• **Reclamações:** {reclamacoes} ⚠️
• **Resolvidas:** {resolvidas}
• **Pendentes:** {pendentes}

**Leitura para a gestão:** acompanhe as demandas pendentes e compare a nota média
com a evolução dos próximos períodos para identificar tendências."""

    abertura = f"{saudacao.capitalize()}! " if saudacao else ""
    return (
        f"{abertura}Claro, posso conversar com você e ajudar com as informações da Polo Fit. "
        "Para manter as recomendações baseadas em dados reais, posso analisar "
        "satisfação, avaliações, reclamações, sugestões, equipe e resultados da "
        "enquete. Qual desses assuntos você gostaria de explorar?"
    )


@staff_required(permission="feedback.view_avaliacao")
def ia_chat(request):
    """
    Endpoint conversacional interativo com a IA sobre as avaliações dos alunos.
    """

    if request.method != "POST":

        return JsonResponse(
            {"erro": "Método não permitido"},
            status=405,
        )

    try:

        data = json.loads(request.body.decode("utf-8"))

        mensagem_usuario = data.get(
            "mensagem",
            "",
        ).strip()

    except Exception:

        mensagem_usuario = request.POST.get(
            "mensagem",
            "",
        ).strip()

    if not mensagem_usuario:

        return JsonResponse(
            {"resposta": ("Por favor, digite uma " "pergunta para a IA.")}
        )

    # ==========================================================
    # AVALIAÇÕES
    # ==========================================================
    #
    # IMPORTANTE:
    # Não fazemos [:100] aqui.
    # Primeiro aplicamos filtros como exclude().
    # Depois limitamos os comentários.
    #

    avaliacoes = Avaliacao.objects.all().order_by("-data_criacao")

    total = avaliacoes.count()

    elogios = avaliacoes.filter(
        models.Q(tipo_feedback="elogio") | models.Q(tipos_feedback__icontains="elogio")
    ).count()

    reclamacoes = avaliacoes.filter(
        models.Q(tipo_feedback="reclamacao")
        | models.Q(tipos_feedback__icontains="reclamacao")
    ).count()

    sugestoes = avaliacoes.filter(
        models.Q(tipo_feedback="sugestao")
        | models.Q(tipos_feedback__icontains="sugestao")
    ).count()

    media = avaliacoes.aggregate(m=models.Avg("nota"))["m"] or 0

    pendentes = avaliacoes.filter(status="pendente").count()

    resolvidas = avaliacoes.filter(status="resolvida").count()

    # ==========================================================
    # RANKING
    # ==========================================================

    ranking = []

    for f in Funcionario.objects.filter(ativo=True):

        f_avs = Avaliacao.objects.filter(
            models.Q(funcionario=f) | models.Q(funcionarios=f)
        ).distinct()

        f_el = f_avs.filter(
            models.Q(tipo_feedback="elogio")
            | models.Q(tipos_feedback__icontains="elogio")
        ).count()

        f_rec = f_avs.filter(
            models.Q(tipo_feedback="reclamacao")
            | models.Q(tipos_feedback__icontains="reclamacao")
        ).count()

        f_med = f_avs.aggregate(m=models.Avg("nota"))["m"] or 0

        ranking.append(
            f"{f.nome} "
            f"({f.funcoes_display or 'Instrutor'}): "
            f"{f_el} elogios, "
            f"{f_rec} reclamações, "
            f"nota média {round(f_med, 1)}"
        )

    ranking_txt = "\n".join(ranking) or "Nenhum funcionário cadastrado."

    # ==========================================================
    # COMENTÁRIOS
    # ==========================================================
    #
    # Primeiro filtramos comentários vazios.
    # Só depois aplicamos [:15].
    #

    comentarios = list(
        avaliacoes.exclude(comentario="").values_list(
            "comentario",
            flat=True,
        )[:15]
    )

    comentarios_txt = (
        "\n".join(f'- "{c}"' for c in comentarios) or "Nenhum comentário registrado."
    )

    # ==========================================================
    # PROMPT DA IA
    # ==========================================================

    prompt = f"""Você é o Consultor Executivo de Inteligência Artificial da Academia Polo Fit.

Você está conversando diretamente com o gerente da academia para auxiliá-lo a tomar decisões operacionais e estratégicas.

BASE DE DADOS EM TEMPO REAL DA POLO FIT:

- Total de avaliações: {total}
- Nota média geral: {round(media, 1)} de 5.0
- Elogios: {elogios}
- Reclamações: {reclamacoes}
- Sugestões: {sugestoes}
- Pendentes de resolução: {pendentes}
- Resolvidas: {resolvidas}

DESEMPENHO DOS COLABORADORES:
{ranking_txt}

COMENTÁRIOS REAIS DOS ALUNOS:
{comentarios_txt}

PERGUNTA DO GERENTE:
"{mensagem_usuario}"

Responda em português brasileiro com tom cordial, natural e profissional.
Converse como um assistente: cumprimente de volta saudações, responda agradecimentos
e perguntas simples sem apresentar um relatório desnecessário. Para perguntas sobre
a academia, use os dados abaixo; quando faltar contexto, faça uma pergunta objetiva.

Seja:
- profissional;
- cordial;
- objetivo;
- executivo;
- baseado nos dados disponíveis;
- orientado a resultados.

Organize a resposta para facilitar a leitura.

Use títulos curtos e marcadores quando forem úteis.

Não invente dados que não estejam disponíveis.

Máximo de 200 palavras."""

    # ==========================================================
    # GEMINI
    # ==========================================================

    api_key = getattr(
        settings,
        "GEMINI_API_KEY",
        "",
    )

    modelo_cfg = getattr(
        settings,
        "GEMINI_MODEL",
        "gemini-1.5-flash",
    )

    modelos_ativos = list(
        dict.fromkeys(
            [
                modelo_cfg,
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]
        )
    )

    if api_key:

        for modelo in modelos_ativos:

            try:

                url = (
                    "https://generativelanguage.googleapis.com/"
                    f"v1beta/models/{modelo}:generateContent"
                    f"?key={api_key}"
                )

                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": 500,
                        "temperature": 0.6,
                    },
                }

                data = json.dumps(payload).encode("utf-8")

                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )

                with urllib.request.urlopen(
                    req,
                    timeout=5,
                ) as resp:

                    result = json.loads(resp.read().decode("utf-8"))

                cands = result.get(
                    "candidates",
                    [],
                )

                if cands:

                    parts = cands[0].get("content", {}).get("parts", [])

                    if parts and parts[0].get("text"):

                        return JsonResponse({"resposta": parts[0].get("text")})

            except Exception:
                continue

    # ==========================================================
    # FALLBACK LOCAL
    # ==========================================================

    resposta_local = _gerar_resposta_conversacional_local(
        pergunta=mensagem_usuario,
        total=total,
        media=media,
        elogios=elogios,
        reclamacoes=reclamacoes,
        sugestoes=sugestoes,
        pendentes=pendentes,
        resolvidas=resolvidas,
        ranking_txt=ranking_txt,
        comentarios=comentarios,
    )

    return JsonResponse({"resposta": resposta_local})
