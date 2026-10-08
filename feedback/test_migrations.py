from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase


class SurveyMultiSelectMigrationTests(TransactionTestCase):
    migrate_from = ("feedback", "0012_funcao_grupo")
    migrate_to = ("feedback", "0013_enquete_multiplas_escolhas")

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MigrationExecutor(connection).migrate([cls.migrate_from])
        cls.old_apps = MigrationExecutor(connection).loader.project_state(
            [cls.migrate_from]
        ).apps

    @classmethod
    def tearDownClass(cls):
        MigrationExecutor(connection).migrate(
            MigrationExecutor(connection).loader.graph.leaf_nodes()
        )
        super().tearDownClass()

    def test_previous_single_choices_are_preserved_as_lists(self):
        old_resposta = self.old_apps.get_model(
            "feedback",
            "RespostaEnquete",
        ).objects.create(
            aula_melhoria="Jump",
            novo_espaco="Yoga",
        )

        MigrationExecutor(connection).migrate([self.migrate_to])
        new_apps = MigrationExecutor(connection).loader.project_state(
            [self.migrate_to]
        ).apps
        resposta = new_apps.get_model("feedback", "RespostaEnquete").objects.get(
            pk=old_resposta.pk
        )

        self.assertEqual(resposta.aula_melhoria, ["Jump"])
        self.assertEqual(resposta.novo_espaco, ["Yoga"])
