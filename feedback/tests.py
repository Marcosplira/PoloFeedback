from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
import json
from feedback.models import Funcionario, Avaliacao


class FeedbackModelTests(TestCase):
    def setUp(self):
        self.funcionario = Funcionario.objects.create(
            nome="Carlos Treinador",
            cargo="Professor de Musculação",
            ativo=True
        )

    def test_criar_funcionario(self):
        self.assertEqual(str(self.funcionario), "Carlos Treinador")
        self.assertTrue(self.funcionario.ativo)

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
        self.assertIn("atendimento", str(av))

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
        self.funcionario = Funcionario.objects.create(
            nome="Mariana Instrutora",
            cargo="Instrutora de Pilates",
            ativo=True
        )

    def test_pagina_avaliar_get(self):
        response = self.client.get(reverse("avaliar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Polo Feedback")
        self.assertContains(response, "Mariana Instrutora")

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
            "funcionario_id": self.funcionario.pk
        }
        response = self.client.post(reverse("avaliar"), dados)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Muito Obrigado")
        self.assertEqual(Avaliacao.objects.count(), 1)
        av = Avaliacao.objects.first()
        self.assertEqual(av.funcionario, self.funcionario)
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

    def test_gerar_qrcode_view(self):
        self.client.login(username="gerente_teste", password="senha_segura_123")
        response = self.client.get(reverse("gerar_qrcode") + "?localizacao=polo_norte")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "polo_norte")
        self.assertIsNotNone(response.context["qrcode_base64"])
