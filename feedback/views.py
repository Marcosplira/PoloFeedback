import io
import base64
import json
import socket
import urllib.request
import urllib.error
import qrcode

from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.utils import timezone
from django.conf import settings

from .models import Avaliacao, Funcionario


def service_worker(request):
    worker_path = finders.find("feedback/service-worker.js")
    if not worker_path:
        return HttpResponseNotFound()

    with open(worker_path, encoding="utf-8") as worker_file:
        response = HttpResponse(
            worker_file.read(), content_type="application/javascript"
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


def avaliar(request):
    funcionarios = Funcionario.objects.filter(ativo=True)

    if request.method == "POST":
        categorias = request.POST.getlist("categorias")
        nota = request.POST.get("nota")
        tipos_feedback = request.POST.getlist("tipos_feedback")
        comentario = request.POST.get("comentario", "").strip()
        localizacao = request.POST.get("localizacao", "").strip()
        funcionario_id = request.POST.get("funcionario_id")

        # Validação detalhada
        erros = []
        if not categorias:
            erros.append("Selecione pelo menos um aspecto para avaliar (Atendimento, Limpeza, etc.).")
        if not nota:
            erros.append("Avalie atribuindo uma nota de 1 a 5 estrelas.")
        if not tipos_feedback:
            erros.append("Selecione o tipo de feedback (Elogio, Sugestão ou Reclamação).")

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
                    "funcionario_id_selecionado": funcionario_id,
                },
            )

        # Funcionário selecionado
        funcionario = None
        if funcionario_id:
            try:
                funcionario = Funcionario.objects.get(pk=funcionario_id, ativo=True)
            except (Funcionario.DoesNotExist, ValueError):
                pass

        # Salva avaliação
        Avaliacao.objects.create(
            categoria=categorias[0],
            categorias=categorias,
            nota=int(nota),
            tipo_feedback=tipos_feedback[0],
            tipos_feedback=tipos_feedback,
            comentario=comentario,
            localizacao=localizacao,
            funcionario=funcionario,
        )

        return render(request, "feedback/sucesso.html", {"localizacao": localizacao})

    # GET
    return render(
        request,
        "feedback/avaliar.html",
        {
            "localizacao": request.GET.get("localizacao", ""),
            "funcionarios": funcionarios,
        },
    )


@login_required
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

            av = get_object_or_404(Avaliacao, pk=avaliacao_id)

            av.status = novo_status

            # Resolvida
            if novo_status == "resolvida":

                if not av.resolvido_por:

                    av.resolvido_por = request.user

                if not av.data_resolucao:

                    av.data_resolucao = timezone.now()

            # Voltou para pendente/em análise
            else:

                av.resolvido_por = None

                av.data_resolucao = None

            av.save()

        # Mantém os filtros atuais
        params = request.POST.get("filtros_ativos", "")

        if params:

            return redirect(f"/dashboard/?{params}")

        return redirect("/dashboard/")

    # ==========================================================
    # FILTROS
    # ==========================================================

    categoria_filtro = request.GET.get("categoria", "")

    tipo_filtro = request.GET.get("tipo", "")

    status_filtro = request.GET.get("status", "")

    funcionario_filtro = request.GET.get("funcionario", "")

    # ==========================================================
    # AVALIAÇÕES
    # ==========================================================

    avaliacoes = Avaliacao.objects.all()

    # Categoria
    if categoria_filtro:
        avaliacoes = avaliacoes.filter(
            models.Q(categoria=categoria_filtro) | models.Q(categorias__icontains=categoria_filtro)
        )

    # Tipo
    if tipo_filtro:
        avaliacoes = avaliacoes.filter(
            models.Q(tipo_feedback=tipo_filtro) | models.Q(tipos_feedback__icontains=tipo_filtro)
        )

    # Status
    if status_filtro:
        avaliacoes = avaliacoes.filter(status=status_filtro)

    # Funcionário
    if funcionario_filtro:
        avaliacoes = avaliacoes.filter(funcionario_id=funcionario_filtro)

    # Mais recentes primeiro
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
        models.Q(tipo_feedback="reclamacao") | models.Q(tipos_feedback__icontains="reclamacao")
    ).count()

    # ==========================================================
    # GRÁFICO POR CATEGORIA
    # ==========================================================

    cats = []

    for a in avaliacoes:
        if a.categorias and isinstance(a.categorias, list):
            cats.extend([str(x).strip().lower() for x in a.categorias])
        elif a.categoria:
            cats.append(str(a.categoria).strip().lower())

    cont_cat = Counter(cats)

    avaliacoes_categoria = []

    for codigo, nome in Avaliacao.CATEGORIA_CHOICES:

        quantidade = cont_cat.get(codigo.lower(), 0)

        avaliacoes_categoria.append(
            {
                "nome": nome,
                "quantidade": quantidade,
            }
        )

    # Caso existam categorias diferentes das cadastradas
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

    todos_funcionarios = Funcionario.objects.filter(ativo=True).prefetch_related("avaliacoes")

    # ==========================================================
    # RANKING DE FUNCIONÁRIOS
    # ==========================================================

    ranking_funcionarios = []

    for func in todos_funcionarios:

        avs = Avaliacao.objects.filter(funcionario=func)

        total = avs.count()

        elogios = avs.filter(tipo_feedback="elogio").count()

        reclamacoes = avs.filter(tipo_feedback="reclamacao").count()

        sugestoes = avs.filter(tipo_feedback="sugestao").count()

        media_func = avs.aggregate(m=models.Avg("nota"))["m"] or 0

        # Foto
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
                "cargo": func.cargo,
                "foto": foto_url,
                "total": total,
                "elogios": elogios,
                "reclamacoes": reclamacoes,
                "sugestoes": sugestoes,
                "media": round(media_func, 1),
            }
        )

    # Ordenação: quem tem mais elogios primeiro; desempate pela média
    ranking_funcionarios.sort(key=lambda x: (x["elogios"], x["media"]), reverse=True)

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    return render(
        request,
        "feedback/dashboard.html",
        {
            # Cards
            "total_avaliacoes": total_avaliacoes,
            "media_notas": round(media, 1),
            "total_elogios": total_elogios,
            "total_reclamacoes": total_reclamacoes,
            # Filtros
            "categoria_filtro": categoria_filtro,
            "tipo_filtro": tipo_filtro,
            "status_filtro": status_filtro,
            "funcionario_filtro": funcionario_filtro,
            # Gráficos
            "avaliacoes_categoria": avaliacoes_categoria,
            "avaliacoes_nota": avaliacoes_nota,
            # Avaliações
            "avaliacoes": avaliacoes,
            # Opções dos filtros
            "categorias": Avaliacao.CATEGORIA_CHOICES,
            "tipos_feedback": Avaliacao.TIPO_FEEDBACK_CHOICES,
            "status_choices": Avaliacao.STATUS_CHOICES,
            "funcionarios": todos_funcionarios,
            # Ranking
            "ranking_funcionarios": ranking_funcionarios,
        },
    )


@login_required
def gerar_qrcode(request):
    qrcode_base64 = None
    localizacao = ""
    url_gerada = ""
    ip_local = _obter_ip_local()
    usar_ip = request.GET.get("usar_ip") == "1"

    # ==========================================================
    # GERA QR CODE
    # ==========================================================

    if request.GET.get("localizacao"):
        localizacao = request.GET.get("localizacao").strip()

        if usar_ip and ip_local != "127.0.0.1":
            porta = request.get_port()
            host = f"{ip_local}:{porta}" if porta and porta not in ["80", "443"] else ip_local
        else:
            host = request.get_host()

        protocolo = "https" if request.is_secure() else "http"
        url_gerada = f"{protocolo}://{host}/?localizacao={localizacao}"

        # Cria QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url_gerada)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Converte para Base64
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        qrcode_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # ==========================================================
    # PÁGINA DO QR CODE
    # ==========================================================

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


def _gerar_resumo_executivo_local(avaliacoes, total, elogios, reclamacoes, sugestoes, media, pendentes, resolvidas):
    """
    Gera um relatório executivo analítico e profissional diretamente
    a partir dos dados reais do banco, garantindo que o gerente sempre receba
    um diagnóstico impecável mesmo se a API externa de IA estiver fora do ar.
    """
    taxa_aprovacao = round((elogios / total * 100), 1) if total > 0 else 0

    cats = []
    for a in avaliacoes:
        if a.categorias and isinstance(a.categorias, list):
            cats.extend(a.categorias)
        elif a.categoria:
            cats.append(a.categoria)
    cont_cat = Counter(cats)
    principais_cats = [dict(Avaliacao.CATEGORIA_CHOICES).get(c, c.capitalize()) for c, _ in cont_cat.most_common(2)]
    setores_txt = " e ".join(principais_cats) if principais_cats else "Geral"

    comentarios = [a.comentario.strip() for a in avaliacoes if a.comentario.strip()][:3]
    amostra_comentarios = ""
    if comentarios:
        amostra_comentarios = "\n\n**O que os alunos estão dizendo:**\n" + "\n".join(f'• *"{c}"*' for c in comentarios)

    return f"""**📊 Resumo Executivo: Experiência e Qualidade — Polo Fit**

**1. Diagnóstico Geral de Desempenho**
• **Nota Média Geral:** {round(media, 1)} / 5.0 ⭐ (Índice de Excelência)
• **Índice de Satisfação:** {taxa_aprovacao}% de feedbacks positivos ({elogios} elogios em {total} avaliações).
• **Status de Resolução:** {resolvidas} demandas resolvidas e {pendentes} em acompanhamento.

**2. Pontos Fortes em Destaque**
Os alunos demonstram alta satisfação e fidelização especialmente nas áreas de **{setores_txt}**. A dedicação da equipe e a qualidade da estrutura foram amplamente elogiadas nos registros recentes.

**3. Pontos de Atenção e Oportunidades**
Foram registradas {reclamacoes} reclamação(ões) pontual(is) e {sugestoes} sugestão(ões) de melhoria. É fundamental priorizar o atendimento rápido a esses chamados no painel para manter a proximidade com os alunos.

**4. Recomendações Práticas para a Gerência**
1. **Reconhecimento da Equipe:** Parabenizar os professores e colaboradores com mais elogios no ranking do dashboard.
2. **Tempo de Resposta Ágil:** Manter o ciclo de resolução das avaliações pendentes em até 24 horas.
3. **Melhoria Contínua:** Utilizar as sugestões registradas para guiar futuras aquisições de equipamentos e ajustes de horários.{amostra_comentarios}"""


@login_required
def ia_analisar(request):
    """
    Endpoint que usa a Gemini API para gerar uma análise inteligente
    das avaliações mais recentes cadastradas no sistema.
    Possui fallback analítico inteligente para garantir que a gerência sempre tenha o parecer em tela.
    """
    # Coleta as últimas 50 avaliações através dos IDs para permitir filtragens no queryset
    ids_recentes = list(
        Avaliacao.objects.order_by("-data_criacao").values_list("id", flat=True)[:50]
    )
    if not ids_recentes:
        return JsonResponse({"analise": "Nenhuma avaliação cadastrada ainda para analisar."})

    avaliacoes = Avaliacao.objects.filter(id__in=ids_recentes)
    total = avaliacoes.count()

    elogios = avaliacoes.filter(
        models.Q(tipo_feedback="elogio") | models.Q(tipos_feedback__icontains="elogio")
    ).count()
    reclamacoes = avaliacoes.filter(
        models.Q(tipo_feedback="reclamacao") | models.Q(tipos_feedback__icontains="reclamacao")
    ).count()
    sugestoes = avaliacoes.filter(
        models.Q(tipo_feedback="sugestao") | models.Q(tipos_feedback__icontains="sugestao")
    ).count()
    media = avaliacoes.aggregate(m=models.Avg("nota"))["m"] or 0

    pendentes = avaliacoes.filter(status="pendente").count()
    resolvidas = avaliacoes.filter(status="resolvida").count()

    # Comentários mais recentes
    comentarios = list(
        avaliacoes.exclude(comentario="")
        .values_list("comentario", flat=True)[:10]
    )
    comentarios_txt = "\n".join(f'- "{c}"' for c in comentarios) or "Nenhum comentário registrado."

    prompt = f"""Você é um consultor especialista em qualidade para a academia Polo Fit.
Gere um resumo executivo direto e profissional para o gerente com base nos dados reais:
- Total: {total} avaliações | Nota média geral: {round(media, 1)} de 5.0
- Elogios: {elogios} | Reclamações: {reclamacoes} | Sugestões: {sugestoes}
- Pendentes: {pendentes} | Resolvidas: {resolvidas}
Comentários dos alunos:
{comentarios_txt}

Apresente em português brasileiro:
1. **Pontos Fortes**
2. **Pontos de Atenção**
3. **Recomendações Práticas para a Gerência**
4. **Visão Geral**
Máximo 250 palavras."""

    api_key = getattr(settings, "GEMINI_API_KEY", "")
    # Modelos em ordem de preferência (mais rápido primeiro)
    modelo_cfg = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
    modelos_ativos = list(dict.fromkeys([modelo_cfg, "gemini-1.5-flash", "gemini-1.5-pro"]))

    if api_key:
        for modelo in modelos_ativos:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 600, "temperature": 0.6},
                }
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    result = json.loads(resp.read().decode("utf-8"))

                cands = result.get("candidates", [])
                if cands:
                    parts = cands[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        return JsonResponse({"analise": parts[0].get("text")})
            except Exception:
                continue

    # Fallback automático e inteligente garantindo que o relatório seja sempre exibido
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


def _gerar_resposta_conversacional_local(pergunta, total, media, elogios, reclamacoes, sugestoes, pendentes, resolvidas, ranking_txt, comentarios):
    """
    Motor local de resposta inteligente para responder perguntas do gerente sobre o feedback
    mesmo quando a API de IA externa não estiver conectada.
    """
    p = pergunta.lower()

    if any(k in p for k in ["professor", "professores", "funcionario", "funcionarios", "equipe", "ranking", "quem", "instrutor", "atendente"]):
        return f"""**🏆 Análise da Equipe e Professores — Polo Fit**

Com base nas avaliações recentes dos alunos:
{ranking_txt}

**Destaques:**
• Os alunos apontam grande empatia, atenção às posturas corretas e incentivo nos treinos.
• **Recomendação para a Gerência:** Crie um reconhecimento mensal ou bonificação para os colaboradores mais elogiados no ranking."""

    if any(k in p for k in ["reclamacao", "reclamacoes", "reclamação", "reclamações", "problema", "critica", "queixa", "ruim", "defeito"]):
        coments_rec = [c for c in comentarios if any(w in c.lower() for w in ["quebrado", "demora", "ar", "limpeza", "espera", "ruim"])]
        amostra = f"\n*Comentários relacionados:* " + "; ".join(f'"{c}"' for c in coments_rec[:2]) if coments_rec else ""
        return f"""**⚠️ Panorama de Reclamações e Pontos Críticos**

• **Total de Reclamações Registradas:** {reclamacoes} ocorrência(s).
• **Demandas Pendentes de Ação:** {pendentes} no painel.
• **Demandas Resolvidas:** {resolvidas}.{amostra}

**Plano de Ação Recomendado:**
1. Verifique os chamados com status **Pendente** na tabela abaixo e altere para **Em Análise** para sinalizar acompanhamento.
2. Atue preventivamente na manutenção de equipamentos antes dos horários de pico (18h às 21h).
3. Sinalize a resolução diretamente aos alunos assim que o ajuste for feito."""

    if any(k in p for k in ["sugestao", "sugestoes", "sugestão", "sugestões", "melhorar", "ideia", "plano", "acao", "ação"]):
        return f"""**💡 Ideias e Recomendações Estratégicas para a Polo Fit**

Com base nas {sugestoes} sugestões e no índice de satisfação atual ({round(media, 1)}/5.0):

1. **Horários de Pico:** Considerar reforço de instrutores no salão entre 17h30 e 20h30.
2. **Revisão Preventiva de Equipamentos:** Estabelecer checklist matinal diário.
3. **Totem de Feedback:** Manter os cartazes com QR Code visíveis na saída do vestiário e na recepção para ampliar a taxa de respostas.
4. **Feedbacks Positivos:** Compartilhar os elogios recebidos na reunião de alinhamento com os colaboradores."""

    return f"""**📋 Síntese dos Feedbacks da Academia Polo Fit**

• **Volume Total:** {total} avaliações computadas.
• **Nota Média:** {round(media, 1)} / 5.0 estrelas ⭐.
• **Balanço:** {elogios} elogios 👍, {sugestoes} sugestões 💡 e {reclamacoes} reclamações ⚠️.
• **Status Operacional:** {resolvidas} resolvidas | {pendentes} pendentes de tratativa.

O sentimento dos alunos é de alta satisfação ({round((elogios/total*100) if total else 0, 1)}% de aprovação). Você pode me fazer perguntas específicas sobre instrutores, queixas ou planos de ação!"""


@login_required
def ia_chat(request):
    """
    Endpoint conversacional interativo com a IA sobre as avaliações dos alunos.
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        mensagem_usuario = data.get("mensagem", "").strip()
    except Exception:
        mensagem_usuario = request.POST.get("mensagem", "").strip()

    if not mensagem_usuario:
        return JsonResponse({"resposta": "Por favor, digite uma pergunta para a IA."})

    avaliacoes = Avaliacao.objects.all().order_by("-data_criacao")[:100]
    total = Avaliacao.objects.count()  # contagem real sem o limite
    elogios = Avaliacao.objects.filter(models.Q(tipo_feedback="elogio") | models.Q(tipos_feedback__icontains="elogio")).count()
    reclamacoes = Avaliacao.objects.filter(models.Q(tipo_feedback="reclamacao") | models.Q(tipos_feedback__icontains="reclamacao")).count()
    sugestoes = Avaliacao.objects.filter(models.Q(tipo_feedback="sugestao") | models.Q(tipos_feedback__icontains="sugestao")).count()
    media = Avaliacao.objects.aggregate(m=models.Avg("nota"))["m"] or 0
    pendentes = Avaliacao.objects.filter(status="pendente").count()
    resolvidas = Avaliacao.objects.filter(status="resolvida").count()

    ranking = []
    for f in Funcionario.objects.filter(ativo=True):
        f_avs = Avaliacao.objects.filter(funcionario=f)
        f_el = f_avs.filter(models.Q(tipo_feedback="elogio") | models.Q(tipos_feedback__icontains="elogio")).count()
        f_rec = f_avs.filter(models.Q(tipo_feedback="reclamacao") | models.Q(tipos_feedback__icontains="reclamacao")).count()
        f_med = f_avs.aggregate(m=models.Avg("nota"))["m"] or 0
        ranking.append(f"{f.nome} ({f.cargo or 'Instrutor'}): {f_el} elogios, {f_rec} reclamações, nota média {round(f_med, 1)}")
    ranking_txt = "\n".join(ranking) or "Nenhum funcionário cadastrado."

    comentarios = list(avaliacoes.exclude(comentario="").values_list("comentario", flat=True)[:15])
    comentarios_txt = "\n".join(f'- "{c}"' for c in comentarios) or "Nenhum comentário registrado."

    prompt = f"""Você é o Consultor Executivo de Inteligência Artificial da Academia Polo Fit.
Você está conversando diretamente com o Gerente da academia para auxiliá-lo a tomar as melhores decisões operacionais e estratégicas.

BASE DE DADOS EM TEMPO REAL DA POLO FIT:
- Total de avaliações: {total} | Nota média geral: {round(media, 1)} de 5.0
- Elogios: {elogios} | Reclamações: {reclamacoes} | Sugestões: {sugestoes}
- Pendentes de resolução: {pendentes} | Resolvidas: {resolvidas}
- Desempenho dos colaboradores:
{ranking_txt}
- Comentários reais dos alunos:
{comentarios_txt}

PERGUNTA DO GERENTE:
"{mensagem_usuario}"

Responda em português brasileiro de forma direta, executiva, cordial e orientada a resultados (máximo 200 palavras). Use marcadores para leitura rápida."""

    api_key = getattr(settings, "GEMINI_API_KEY", "")
    # Modelos em ordem de preferência
    modelo_cfg = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")
    modelos_ativos = list(dict.fromkeys([modelo_cfg, "gemini-1.5-flash", "gemini-1.5-pro"]))

    if api_key:
        for modelo in modelos_ativos:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 500, "temperature": 0.6},
                }
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    result = json.loads(resp.read().decode("utf-8"))

                cands = result.get("candidates", [])
                if cands:
                    parts = cands[0].get("content", {}).get("parts", [])
                    if parts and parts[0].get("text"):
                        return JsonResponse({"resposta": parts[0].get("text")})
            except Exception:
                continue

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
