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
    enquete,
    gerar_qrcode,
    ia_analisar,
    ia_chat,
    service_worker,
)

urlpatterns = [
    path("service-worker.js", service_worker, name="service_worker"),
    path("admin/", admin.site.urls),
    path("", avaliar, name="inicio"),
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
    path("qrcode/", gerar_qrcode, name="gerar_qrcode"),
    path("ia/analisar/", ia_analisar, name="ia_analisar"),
    path("ia/chat/", ia_chat, name="ia_chat"),
]


# Em desenvolvimento (DEBUG=True), o Django serve arquivos de mídia diretamente.
# Em produção, configure um servidor web ou storage (S3, Cloudflare R2, etc.)
# para servir os arquivos de /media/.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
