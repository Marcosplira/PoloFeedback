"""
URL configuration for polofeedback project.
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import reverse

from feedback.views import (
    avaliar,
    dashboard,
    configuracao_sistema,
    divulgacao,
    enquete,
    gerar_qrcode,
    inicio,
    ia_analisar,
    ia_chat,
    projeto_treino,
    cadastro_aluno,
    editar_plano_treino,
    gestao_treinos,
    meus_treinos,
    qrcodes_treinos,
    service_worker,
    treino_equipamento,
)


class LoginPoloFitView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        if self.request.user.is_staff:
            destination = (
                "dashboard"
                if self.request.user.has_perm("feedback.view_avaliacao")
                else "qrcodes_treinos"
            )
            return reverse(destination)
        return reverse("meus_treinos")


urlpatterns = [
    path("service-worker.js", service_worker, name="service_worker"),
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("avaliar/", avaliar, name="avaliar"),
    path("enquete/", enquete, name="enquete"),
    path(
        "login/",
        LoginPoloFitView.as_view(),
        name="login",
    ),
    path("cadastro/aluno/", cadastro_aluno, name="cadastro_aluno"),
    path("treinos/meus/", meus_treinos, name="meus_treinos"),
    path("treinos/gestao/", gestao_treinos, name="gestao_treinos"),
    path(
        "treinos/gestao/novo/",
        editar_plano_treino,
        name="plano_treino_novo",
    ),
    path(
        "treinos/gestao/<int:plano_id>/",
        editar_plano_treino,
        name="plano_treino_editar",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/projeto-treino/", projeto_treino, name="projeto_treino"),
    path("dashboard/configuracao/", configuracao_sistema, name="configuracao_sistema"),
    path("dashboard/divulgacao/", divulgacao, name="divulgacao"),
    path("qrcode/", gerar_qrcode, name="gerar_qrcode"),
    path("treinos/qrs/", qrcodes_treinos, name="qrcodes_treinos"),
    path(
        "treinos/aparelho/<uuid:identificador_qr>/",
        treino_equipamento,
        name="treino_equipamento",
    ),
    path("ia/analisar/", ia_analisar, name="ia_analisar"),
    path("ia/chat/", ia_chat, name="ia_chat"),
]


# Em desenvolvimento (DEBUG=True), o Django serve arquivos de mídia diretamente.
# Em produção, configure um servidor web ou storage (S3, Cloudflare R2, etc.)
# para servir os arquivos de /media/.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
