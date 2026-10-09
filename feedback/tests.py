from django.test import TestCase, Client
from django.test import override_settings
from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.db import OperationalError
from django.core.management import call_command
import json
import os
from io import StringIO
from unittest.mock import patch
from feedback.models import (
    Avaliacao,
    Equipamento,
    Exercicio,
    Funcao,
    Funcionario,
    ItemPlanoTreino,
    PlanoTreino,
    RespostaEnquete,
)
from feedback.middleware import DatabaseErrorPageMiddleware


class FeedbackModelTests(TestCase):
    def setUp(self):
        self.funcao_professor = Funcao.objects.create(nome="Professor")
        self.funcao_instrutor = Funcao.objects.create(nome="Instrutor")
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Treinador",
            cargo="Professor de Musculação",
            ativo=True
        )
        self.funcionario.funcoes.add(self.funcao_professor, self.funcao_instrutor)

    def test_criar_funcionario(self):
        self.assertEqual(str(self.funcionario), "Carlos Treinador")
        self.assertTrue(self.funcionario.ativo)
        self.assertEqual(
            self.funcionario.funcoes_display,
            "Instrutor, Professor",
        )

    def test_criar_avaliacao(self):
        av = Avaliacao.objects.create(
            categoria="atendimento",
            categorias=["atendimento", "equipamentos"],
            nota=5,
            tipo_feedback="elogio",
            tipos_feedback=["elogio"],
            comentario="Excelente atendimento!",
            localizacao="polo1",
            funcionario=self.funcionario
        )
        self.assertEqual(av.nota, 5)
        self.assertEqual(av.status, "pendente")
        self.assertEqual(av.funcionario.nome, "Carlos Treinador")
        self.assertEqual(av.funcionarios_avaliados, [self.funcionario])
        self.assertIn("atendimento", str(av))

    def test_video_do_youtube_usa_embed_privado(self):
        exercicio = Exercicio(video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

        self.assertEqual(
            exercicio.video_embed_url,
            "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ",
        )

    def test_video_de_dominio_nao_autorizado_nao_e_embutido(self):
        exercicio = Exercicio(
            video_url="https://youtube.com.example.org/watch?v=dQw4w9WgXcQ"
        )

        self.assertEqual(exercicio.video_embed_url, "")

    def test_resolucao_automatica_data(self):
        av = Avaliacao.objects.create(
            categoria="limpeza",
            nota=4,
            tipo_feedback="sugestao",
            status="resolvida"
        )
        self.assertIsNotNone(av.data_resolucao)


class FeedbackViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="gerente_teste",
            password="senha_segura_123"
        )
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save(update_fields=["is_staff", "is_superuser"])
        self.funcionario = Funcionario.objects.create(
            nome="Mariana Instrutora",
            cargo="Instrutora de Pilates",
            ativo=True
        )
        self.funcionario.funcoes.add(
            Funcao.objects.create(
                nome="Instrutora de Pilates",
                grupo=Funcao.GRUPO_ESTAGIARIOS_PROFESSORES,
            )
        )

    def test_cadastro_publico_cria_aluno_sem_permissoes_de_equipe(self):
        response = self.client.post(
            reverse("cadastro_aluno"),
            {
                "first_name": "Ana",
                "last_name": "Aluna",
                "username": "ana_aluna",
                "password1": "TreinoSeguro#93",
                "password2": "TreinoSeguro#93",
            },
        )

        self.assertRedirects(response, reverse("meus_treinos"))
        aluno = User.objects.get(username="ana_aluna")
        self.assertEqual(aluno.get_full_name(), "Ana Aluna")
        self.assertFalse(aluno.is_staff)
        self.assertFalse(aluno.is_superuser)
        self.assertEqual(
            self.client.get(reverse("meus_treinos")).status_code,
            200,
        )

    def test_cadastro_publico_rejeita_senha_fraca(self):
        response = self.client.post(
            reverse("cadastro_aluno"),
            {
                "first_name": "Ana",
                "last_name": "Aluna",
                "username": "ana_senha_fraca",
                "password1": "123",
                "password2": "123",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="ana_senha_fraca").exists())

    def test_equipe_cria_plano_para_aluno_com_exercicio(self):
        professor = User.objects.create_user(
            username="professor_plano",
            is_staff=True,
        )
        aluno = User.objects.create_user(
            username="aluno_plano",
            first_name="Ana",
            last_name="Aluna",
        )
        equipamento = Equipamento.objects.create(nome="Esteira")
        exercicio = Exercicio.objects.create(
            nome="Caminhada",
            equipamento=equipamento,
            instrucoes="Caminhe em ritmo confortável.",
        )
        exercicio_extra = Exercicio.objects.create(
            nome="Corrida leve",
            equipamento=equipamento,
            instrucoes="Aumente o ritmo apenas conforme sua orientação.",
        )
        self.client.force_login(professor)

        form_response = self.client.get(reverse("plano_treino_novo"))
        self.assertEqual(form_response.status_code, 200)
        self.assertContains(form_response, "Ana Aluna (@aluno_plano)")
        self.assertContains(form_response, "add-exercise")
        self.assertNotContains(form_response, "gerente_teste")

        response = self.client.post(
            reverse("plano_treino_novo"),
            {
                "aluno": aluno.pk,
                "nome": "Plano inicial",
                "observacoes": "Começar com orientação do professor.",
                "ativo": "on",
                "itens-TOTAL_FORMS": "2",
                "itens-INITIAL_FORMS": "0",
                "itens-MIN_NUM_FORMS": "1",
                "itens-MAX_NUM_FORMS": "1000",
                "itens-0-exercicio": exercicio.pk,
                "itens-0-ordem": "1",
                "itens-0-series": "3",
                "itens-0-repeticoes": "15",
                "itens-0-descanso_segundos": "60",
                "itens-0-carga": "",
                "itens-0-observacoes": "",
                "itens-1-exercicio": exercicio_extra.pk,
                "itens-1-ordem": "2",
                "itens-1-series": "3",
                "itens-1-repeticoes": "12",
                "itens-1-descanso_segundos": "60",
                "itens-1-carga": "",
                "itens-1-observacoes": "",
            },
        )

        self.assertRedirects(response, reverse("gestao_treinos"))
        plano = PlanoTreino.objects.get(aluno=aluno, nome="Plano inicial")
        self.assertEqual(plano.professor, professor)
        item = ItemPlanoTreino.objects.get(plano=plano, ordem=1)
        self.assertEqual(item.exercicio, exercicio)
        self.assertEqual(item.series, 3)
        self.assertTrue(
            ItemPlanoTreino.objects.filter(
                plano=plano,
                ordem=2,
                exercicio=exercicio_extra,
            ).exists()
        )

    def test_aluno_nao_acessa_gestao_dos_planos(self):
        aluno = User.objects.create_user(username="aluno_sem_gestao")
        self.client.force_login(aluno)

        response = self.client.get(reverse("gestao_treinos"))

        self.assertEqual(response.status_code, 403)

    def test_login_redireciona_aluno_para_treinos_e_equipe_para_dashboard(self):
        aluno = User.objects.create_user(username="aluno_login", password="TreinoSeguro#93")
        resposta_aluno = self.client.post(
            reverse("login"),
            {"username": aluno.username, "password": "TreinoSeguro#93"},
        )
        self.assertRedirects(resposta_aluno, reverse("meus_treinos"))

        self.client.logout()
        funcionario = User.objects.create_user(
            username="funcionario_login",
            password="TreinoSeguro#93",
            is_staff=True,
        )
        resposta_funcionario = self.client.post(
            reverse("login"),
            {"username": funcionario.username, "password": "TreinoSeguro#93"},
        )
        self.assertRedirects(resposta_funcionario, reverse("qrcodes_treinos"))

    def test_inicio_e_avaliacao_tem_destinos_separados(self):
        inicio_response = self.client.get(reverse("inicio"))
        self.assertEqual(inicio_response.status_code, 200)
        self.assertContains(inicio_response, "Sua experiência ajuda a gente a evoluir")
        self.assertContains(inicio_response, reverse("avaliar"))
        self.assertContains(inicio_response, 'from-lime-500/20')
        self.assertContains(inicio_response, "QR Code para avaliação Polo Fit")
        self.assertContains(inicio_response, "QR Code para pesquisa Polo Fit")
        self.assertTrue(inicio_response.context["avaliar_qr"])
        self.assertTrue(inicio_response.context["enquete_qr"])
        self.assertContains(
            inicio_response,
            "https://drive.google.com/file/d/1dMbcjNqjXwljGSaJdAHkax_5Sy_12_bX/preview",
        )
        self.assertContains(
            inicio_response,
            "https://drive.google.com/file/d/1dMbcjNqjXwljGSaJdAHkax_5Sy_12_bX/view",
        )
        self.assertContains(
            inicio_response,
            "https://drive.google.com/uc?export=download&amp;id=1dMbcjNqjXwljGSaJdAHkax_5Sy_12_bX",
        )
        self.assertContains(inicio_response, "academia2.png")
        self.assertContains(inicio_response, "class=\"mb-3 aspect-video w-full rounded-2xl bg-black\"")
        self.assertContains(inicio_response, "Baixar vídeo")
        self.assertContains(inicio_response, "Abrir no Google Drive")
        self.assertContains(inicio_response, "Vídeo de apresentação da Academia Polo Fit")
        avaliacao_response = self.client.get(reverse("avaliar"))
        self.assertEqual(avaliacao_response.status_code, 200)
        self.assertContains(avaliacao_response, f'href="{reverse("inicio")}"')
        self.assertContains(avaliacao_response, 'aria-current="page"')

    def test_login_explica_que_nao_existe_credencial_padrao(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não existe login padrão “admin/admin”")
        self.assertNotContains(response, "gerente123")
        self.assertNotContains(response, "marcos123")

    @override_settings(AUTH_PASSWORD_VALIDATORS=[])
    def test_configura_duas_contas_privadas_sem_superusuario(self):
        variaveis = {
            "DASHBOARD_MANAGER_USERNAME": "gerente_configurado",
            "DASHBOARD_MANAGER_PASSWORD": "T8!qL3@vR9#pK2",
            "DASHBOARD_OWNER_USERNAME": "responsavel_configurado",
            "DASHBOARD_OWNER_PASSWORD": "X5#kM9!sQ2@vL7",
        }
        with patch.dict(os.environ, variaveis, clear=False):
            call_command("setup_dashboard_users")

        gerente = User.objects.get(username="gerente_configurado")
        self.assertTrue(gerente.is_staff)
        self.assertFalse(gerente.is_superuser)
        self.assertTrue(gerente.has_perm("feedback.view_avaliacao"))
        self.assertTrue(gerente.has_perm("feedback.change_funcionario"))
        self.assertTrue(gerente.check_password(variaveis["DASHBOARD_MANAGER_PASSWORD"]))
        self.assertTrue(
            self.client.login(
                username="gerente_configurado",
                password=variaveis["DASHBOARD_MANAGER_PASSWORD"],
            )
        )
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 200)

    def test_setup_dashboard_users_avisa_quando_faltam_variaveis(self):
        conta_legada = User.objects.create_superuser(
            username="gerente",
            email="gerente@example.com",
            password="senha_conhecida",
        )
        variaveis = {
            "DASHBOARD_MANAGER_USERNAME": "",
            "DASHBOARD_MANAGER_PASSWORD": "",
            "DASHBOARD_OWNER_USERNAME": "",
            "DASHBOARD_OWNER_PASSWORD": "",
        }
        saida_erro = StringIO()
        with patch.dict(os.environ, variaveis, clear=False):
            call_command("setup_dashboard_users", stderr=saida_erro)

        self.assertIn("não atualizadas", saida_erro.getvalue())
        conta_legada.refresh_from_db()
        self.assertFalse(conta_legada.is_active)
        self.assertFalse(conta_legada.has_usable_password())

    def test_rodape_exibe_contato_e_creditos(self):
        response = self.client.get(reverse("inicio"))
        self.assertContains(response, "Rua Antônio dos Santos, nº 62, Bairro Cenecista, Picuí - PB, CEP 58187-000")
        self.assertContains(response, "(83) 98671-9438")
        self.assertContains(response, "https://wa.me/5583986719438")
        self.assertContains(response, "https://www.instagram.com/polofitacademias/")
        self.assertContains(response, "Rua+Ant%C3%B4nio+dos+Santos")
        self.assertContains(response, "Segunda a sexta: 05h às 22h")
        self.assertContains(response, "Sábado: 11h às 19h")
        self.assertContains(response, "mensalidades")
        self.assertContains(response, "Marcos Paulo Santos Lira")
        self.assertContains(response, "Instituto Federal de Educação")

    def test_painel_executivo_tem_atalhos_de_gestao_para_superusuario(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gerenciar funcionários")
        self.assertContains(response, reverse("admin:feedback_funcionario_changelist"))
        self.assertContains(response, "Cadastrar funcionário")
        self.assertContains(response, reverse("admin:feedback_funcionario_add"))
        self.assertContains(response, reverse("configuracao_sistema"))
        self.assertContains(response, reverse("divulgacao"))

    def test_diagnostico_mostra_status_das_migracoes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("configuracao_sistema"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diagnóstico e ajuda")
        self.assertContains(response, "Estrutura do banco atualizada")

    def test_pagina_divulgacao_nao_anuncia_endereco_local_como_publico(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("divulgacao"),
            HTTP_HOST="localhost:8000",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Este endereço é local")
        self.assertContains(response, "Compartilhar pelo WhatsApp")

    def test_middleware_mostra_tela_de_ajuda_em_erro_operacional_do_banco(self):
        def view_com_banco_indisponivel(request):
            raise OperationalError("no such table: feedback_equipamento")

        middleware = DatabaseErrorPageMiddleware(view_com_banco_indisponivel)
        request = RequestFactory().get("/admin/feedback/equipamento/")

        with self.assertLogs("feedback.middleware", level="ERROR"):
            response = middleware(request)

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, "O banco ainda não está pronto", status_code=503)

    def test_admin_tem_link_de_volta_ao_painel_e_tema_da_aplicacao(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voltar ao Painel Executivo")
        self.assertContains(response, "feedback/admin.css")

    def test_equipe_inicial_cadastrada_no_admin_para_avaliacoes(self):
        nomes_esperados = {
            "Alan Araújo": "Gerente",
            "Anderson Adriel": "Funcionário",
            "Jefferson Tauin": "Proprietário",
            "Vivia Gabriella": "Funcionária",
        }

        for nome, cargo in nomes_esperados.items():
            with self.subTest(nome=nome):
                funcionario = Funcionario.objects.get(nome=nome)
                self.assertEqual(funcionario.cargo, cargo)
                self.assertEqual(
                    list(funcionario.funcoes.values_list("nome", flat=True)),
                    [cargo],
                )
                expected_group = (
                    Funcao.GRUPO_DIRECAO
                    if cargo in {"Gerente", "Proprietário"}
                    else Funcao.GRUPO_ESTAGIARIOS_PROFESSORES
                )
                self.assertEqual(
                    funcionario.funcoes.get().grupo,
                    expected_group,
                )
                self.assertTrue(funcionario.ativo)

    def test_colaboradoras_da_recepcao_ficam_no_grupo_correto(self):
        nomes_recepcao = (
            "Jaqueline Lima",
            "Jessica Karla",
            "Micheli Priscila",
        )

        for nome in nomes_recepcao:
            with self.subTest(nome=nome):
                funcionario = Funcionario.objects.get(nome=nome)
                self.assertEqual(
                    list(funcionario.funcoes.values_list("nome", flat=True)),
                    ["Recepção"],
                )
                self.assertEqual(
                    funcionario.funcoes.get().grupo,
                    Funcao.GRUPO_RECEPCAO,
                )

    def test_pagina_avaliar_get(self):
        response = self.client.get(reverse("avaliar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Polo Feedback")
        self.assertContains(response, "Mariana Instrutora")
        self.assertContains(response, "feedback/funcionarios/alan-araujo.png")
        self.assertContains(response, 'name="funcionarios_ids"', html=False)
        self.assertContains(response, "marque um ou mais funcionários")

    def test_pagina_avaliar_possui_botao_area_gerente(self):
        response = self.client.get(reverse("avaliar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Área do gerente")
        self.assertContains(response, "dashboard")

    def test_pagina_avaliar_possui_botoes_por_local(self):
        response = self.client.get(reverse("avaliar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Selecione o local")
        self.assertContains(response, "Recepção")
        self.assertContains(response, "Academia Principal")
        self.assertContains(response, "Vestiários")

    def test_pwa_manifest_and_root_scoped_service_worker(self):
        response = self.client.get(reverse("avaliar"))
        self.assertContains(response, 'rel="manifest"', html=False)
        self.assertContains(response, "pwa-install-button")

        manifest_path = finders.find("feedback/manifest.webmanifest")
        self.assertIsNotNone(manifest_path)
        with open(manifest_path, encoding="utf-8") as manifest_file:
            manifest = json.load(manifest_file)
        self.assertEqual(manifest["scope"], "/")
        self.assertEqual({icon["sizes"] for icon in manifest["icons"]}, {"192x192", "512x512"})

        worker = self.client.get(reverse("service_worker"))
        self.assertEqual(worker.status_code, 200)
        self.assertEqual(worker["Service-Worker-Allowed"], "/")
        self.assertContains(worker, 'request.method !== "GET"')

    def test_pagina_avaliar_post_valido(self):
        dados = {
            "categorias": ["atendimento", "professores"],
            "nota": "5",
            "tipos_feedback": ["elogio"],
            "comentario": "Ótima aula com a professora Mariana!",
            "localizacao": "Unidade Central",
        }
        segundo_funcionario = Funcionario.objects.create(
            nome="Ana Professora",
            cargo="",
            ativo=True,
        )
        dados["funcionarios_ids"] = [self.funcionario.pk, segundo_funcionario.pk]
        response = self.client.post(reverse("avaliar"), dados)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Muito Obrigado")
        self.assertEqual(Avaliacao.objects.count(), 1)
        av = Avaliacao.objects.first()
        self.assertEqual(av.funcionario, self.funcionario)
        self.assertCountEqual(
            av.funcionarios.all(),
            [self.funcionario, segundo_funcionario],
        )
        self.assertEqual(av.nota, 5)

    def test_pagina_avaliar_post_invalido_sem_campos_obrigatorios(self):
        dados = {
            "comentario": "Faltou marcar nota e categoria"
        }
        response = self.client.post(reverse("avaliar"), dados)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Por favor, atente-se")
        self.assertEqual(Avaliacao.objects.count(), 0)

    def test_dashboard_requer_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_dashboard_autenticado_get(self):
        self.client.login(username="gerente_teste", password="senha_segura_123")
        Avaliacao.objects.create(
            categoria="estrutura",
            categorias=["estrutura"],
            nota=5,
            tipo_feedback="elogio",
            tipos_feedback=["elogio"],
            comentario="Ambiente climatizado e agradável."
        )
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Ambiente climatizado")

    def test_dashboard_filtra_e_ranqueia_funcionario_em_avaliacoes_multiplas(self):
        segundo_funcionario = Funcionario.objects.create(
            nome="Ana Professora",
            cargo="",
            ativo=True,
        )
        avaliacao = Avaliacao.objects.create(
            categoria="professores",
            categorias=["professores"],
            nota=5,
            tipo_feedback="elogio",
            tipos_feedback=["elogio"],
            funcionario=self.funcionario,
        )
        avaliacao.funcionarios.set([self.funcionario, segundo_funcionario])
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("dashboard"),
            {"funcionario": segundo_funcionario.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_avaliacoes"], 1)
        ranking = {
            item["nome"]: item
            for item in response.context["ranking_funcionarios"]
        }
        self.assertEqual(ranking["Ana Professora"]["total"], 1)
        self.assertContains(response, "Mariana Instrutora")
        self.assertContains(response, "Ana Professora")

    def test_dashboard_chat_script_is_valid_for_suggestion_buttons(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode()
        script_start = content.index("const chatForm =")
        script_end = content.index("</script>", script_start)
        chat_script = content[script_start:script_end]

        self.assertNotIn("<script", chat_script)
        self.assertIn('document.querySelectorAll(".sugestao-chat")', chat_script)
        self.assertContains(response, "Como está a satisfação dos alunos atualmente?")

    def test_dashboard_survey_results_are_rendered_for_managers(self):
        self.client.force_login(self.user)
        for _ in range(6):
            RespostaEnquete.objects.create(
                aulas_favoritas=["Funcional"],
                aula_melhoria=["Jump", "Dança"],
                novo_espaco=["Espaço Kids", "Yoga"],
                aula_falta="Natação",
                sugestao_valor="Ampliar os horários das aulas",
                elogio_colaborador="A equipe é muito atenciosa",
            )

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.content.decode(), r"6\s+respostas coletadas")
        self.assertContains(response, "6 votos")
        self.assertRegex(response.content.decode(), r"6\s+menções")
        self.assertContains(response, "Sinal de atenção")
        self.assertContains(response, "Espaço Kids")
        self.assertIn(("Yoga", 6), response.context["espacos_ranking"])
        self.assertIn(("Dança", 6), response.context["melhorias_ranking"])
        self.assertContains(response, "Sugestão de melhoria:")
        self.assertContains(response, "Ampliar os horários das aulas")
        self.assertNotContains(response, "{{")

    @override_settings(GEMINI_API_KEY="")
    def test_ia_chat_handles_greetings_and_small_talk(self):
        self.client.force_login(self.user)

        for message, expected in [
            ("Bom dia!", "Como posso ajudar?"),
            ("Oi, tudo bem?", "Como posso ajudar?"),
            ("Bom dia, o que você precisa saber sobre o aplicativo?", "Bom dia!"),
            ("Obrigado", "Por nada!"),
            ("O que você pode fazer?", "Posso ajudar você a analisar"),
        ]:
            with self.subTest(message=message):
                response = self.client.post(
                    reverse("ia_chat"),
                    data=json.dumps({"mensagem": message}),
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(expected, response.json()["resposta"])

    def test_dashboard_atualizar_status(self):
        self.client.login(username="gerente_teste", password="senha_segura_123")
        av = Avaliacao.objects.create(
            categoria="equipamentos",
            categorias=["equipamentos"],
            nota=2,
            tipo_feedback="reclamacao",
            tipos_feedback=["reclamacao"],
            status="pendente"
        )
        response = self.client.post(reverse("dashboard"), {
            "avaliacao_id": av.pk,
            "novo_status": "resolvida"
        })
        self.assertEqual(response.status_code, 302)
        av.refresh_from_db()
        self.assertEqual(av.status, "resolvida")
        self.assertEqual(av.resolvido_por, self.user)
        self.assertIsNotNone(av.data_resolucao)

    def test_pagina_avaliar_possui_botao_dashboard_navbar(self):
        response = self.client.get(reverse("avaliar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
        self.assertNotContains(response, "{{")

    def test_gerar_qrcode_view(self):
        self.client.login(username="gerente_teste", password="senha_segura_123")
        response = self.client.get(reverse("gerar_qrcode") + "?localizacao=polo_norte")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "polo_norte")
        self.assertContains(response, "Unidade / Ponto: <span class=\"font-bold text-black\">polo_norte</span>")
        self.assertNotContains(response, "{{")
        self.assertIsNotNone(response.context["qrcode_base64"])

    def test_treino_por_qr_exige_login_e_preserva_destino(self):
        equipamento = Equipamento.objects.create(
            nome="Leg press",
            instrucoes="Ajuste o encosto antes de começar.",
        )

        response = self.client.get(
            reverse(
                "treino_equipamento",
                kwargs={"identificador_qr": equipamento.identificador_qr},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertIn(str(equipamento.identificador_qr), response.url)

    def test_aluno_ve_apenas_o_proprio_treino_do_aparelho(self):
        equipamento = Equipamento.objects.create(
            nome="Leg press",
            localizacao="Musculação",
            instrucoes="Ajuste o encosto antes de começar.",
        )
        exercicio_proprio = Exercicio.objects.create(
            nome="Leg press horizontal",
            equipamento=equipamento,
            instrucoes="Empurre a plataforma sem travar os joelhos.",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )
        exercicio_alheio = Exercicio.objects.create(
            nome="Exercício privado de outro aluno",
            equipamento=equipamento,
            instrucoes="Não deve aparecer para esta conta.",
        )
        aluno = User.objects.create_user(username="aluno_teste")
        outro_aluno = User.objects.create_user(username="outro_aluno")
        plano_proprio = PlanoTreino.objects.create(
            aluno=aluno,
            professor=self.user,
            nome="Treino A",
        )
        plano_alheio = PlanoTreino.objects.create(
            aluno=outro_aluno,
            professor=self.user,
            nome="Treino reservado",
        )
        ItemPlanoTreino.objects.create(
            plano=plano_proprio,
            exercicio=exercicio_proprio,
            ordem=1,
            series=4,
            repeticoes="12",
            descanso_segundos=90,
            carga="40 kg",
        )
        ItemPlanoTreino.objects.create(
            plano=plano_alheio,
            exercicio=exercicio_alheio,
            ordem=1,
        )
        self.client.force_login(aluno)

        home_response = self.client.get(reverse("meus_treinos"))
        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, "Treino A")
        self.assertContains(home_response, "Leg press horizontal")
        self.assertNotContains(home_response, "Treino reservado")
        self.assertNotContains(home_response, "Exercício privado de outro aluno")

        response = self.client.get(
            reverse(
                "treino_equipamento",
                kwargs={"identificador_qr": equipamento.identificador_qr},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leg press horizontal")
        self.assertContains(response, "40 kg")
        self.assertContains(response, "Abrir vídeo no YouTube")
        self.assertContains(
            response,
            "https://www.youtube-nocookie.com/embed/dQw4w9WgXcQ",
        )
        self.assertNotContains(response, "Exercício privado de outro aluno")
        self.assertNotContains(response, "Treino reservado")

    def test_qr_dos_treinos_so_e_disponivel_para_equipe(self):
        equipamento = Equipamento.objects.create(nome="Puxada alta")
        url = reverse("qrcodes_treinos")
        aluno = User.objects.create_user(username="aluno_teste")
        self.client.force_login(aluno)

        forbidden_response = self.client.get(url)
        self.assertEqual(forbidden_response.status_code, 403)

        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Puxada alta")
        self.assertContains(response, str(equipamento.identificador_qr))
        self.assertContains(response, "Imprimir QR Codes")
        self.assertContains(response, reverse("gestao_treinos"))

    def test_professor_pode_imprimir_qr_sem_ver_dashboard_gerencial(self):
        professor = User.objects.create_user(username="professor_teste", is_staff=True)
        self.client.force_login(professor)

        qrcodes_response = self.client.get(reverse("qrcodes_treinos"))
        self.assertEqual(qrcodes_response.status_code, 200)
        self.assertNotContains(qrcodes_response, 'href="/dashboard/"')
        self.assertEqual(self.client.get(reverse("dashboard")).status_code, 403)

    def test_usuario_aluno_nao_acessa_dashboard_gerencial(self):
        aluno = User.objects.create_user(username="aluno_teste")
        self.client.force_login(aluno)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 403)

    def test_enquete_get(self):
        response = self.client.get(reverse("enquete"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enquete de Satisfação")
        self.assertContains(response, "Quais aulas você MAIS gosta ou participa?")
        self.assertContains(response, "Você participa das aulas coletivas da academia?")
        self.assertContains(response, "Sobre novos espaços na academia")
        self.assertContains(response, "Quais espaços você acha que fariam MAIS diferença")
        self.assertContains(response, "Qual aula precisa de MAIS atenção ou melhorias?")
        self.assertContains(response, "Marque todas as aulas que precisam de atenção")
        self.assertContains(
            response,
            'type="checkbox" name="novo_espaco"',
            html=False,
        )
        self.assertContains(
            response,
            'type="checkbox" name="aula_melhoria"',
            html=False,
        )
        self.assertContains(response, "Pensando em agregações e melhorias")
        self.assertContains(response, "Deixe aqui um elogio para nossos colaboradores")
        self.assertContains(response, 'name="funcionarios_ids"', html=False)
        self.assertContains(response, "uma ou mais pessoas")
        self.assertContains(response, "Recepção")
        self.assertContains(response, "Time de limpeza")
        self.assertContains(response, "Estagiários e professores")
        self.assertContains(response, "Direção e coordenação")
        self.assertContains(response, "Mariana Instrutora")
        self.assertContains(response, "feedback/funcionarios/alan-araujo.png")
        self.assertContains(response, "feedback/funcionarios/jefferson-tauin.png")
        self.assertContains(response, "feedback/funcionarios/italo-kelps.png")
        self.assertContains(response, "feedback/funcionarios/thalyson-pablo.png")
        self.assertContains(response, "feedback/funcionarios/douglas-augusto.png")
        self.assertContains(response, "feedback/funcionarios/anderson-adriel.png")
        self.assertContains(response, "feedback/funcionarios/joao-matheus.png")
        self.assertNotContains(response, "{{")

    def test_enquete_post(self):
        segundo_funcionario = Funcionario.objects.create(
            nome="Ana Professora",
            cargo="",
            ativo=True,
        )
        dados = {
            "aulas_favoritas": ["Funcional", "Dança"],
            "aulas_favoritas_outra": "Zumba",
            "participa_aulas": "Sim, com frequência",
            "novo_espaco": ["Cross / Treinamento funcional avançado", "Yoga"],
            "aula_melhoria": ["Jump", "Dança"],
            "aula_falta": "Boxe",
            "sugestao_valor": "Mais esteiras no horário de pico",
            "elogio_colaborador": "Parabéns ao Carlos pelo ótimo treino!",
            "funcionarios_ids": [self.funcionario.pk, segundo_funcionario.pk],
        }
        response = self.client.post(reverse("enquete"), dados)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enquete Enviada com Sucesso")
        self.assertContains(response, "Quer avaliar sua experiência na Polo Fit?")
        self.assertContains(response, 'href="/"')
        self.assertContains(response, "Agora não")
        self.assertEqual(RespostaEnquete.objects.count(), 1)
        r = RespostaEnquete.objects.first()
        self.assertEqual(r.participa_aulas, "Sim, com frequência")
        self.assertIn("Funcional", r.aulas_favoritas)
        self.assertEqual(
            r.novo_espaco,
            ["Cross / Treinamento funcional avançado", "Yoga"],
        )
        self.assertEqual(r.aula_melhoria, ["Jump", "Dança"])
        self.assertEqual(r.aula_falta, "Boxe")
        self.assertCountEqual(
            list(r.funcionarios_elogiados.all()),
            [self.funcionario, segundo_funcionario],
        )
        self.assertCountEqual(
            Avaliacao.objects.get(comentario__startswith="[Enquete]").funcionarios.all(),
            [self.funcionario, segundo_funcionario],
        )
