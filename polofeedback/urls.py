"""
URL configuration for polofeedback project.
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

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
    qrcodes_treinos,
    service_worker,
    treino_equipamento,
)

urlpatterns = [
    path("service-worker.js", service_worker, name="service_worker"),
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("avaliar/", avaliar, name="avaliar"),
    path("enquete/", enquete, name="enquete"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("dashboard/", dashboard, name="dashboard"),
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
