import logging

from django.db import OperationalError
from django.shortcuts import render


logger = logging.getLogger(__name__)


class DatabaseErrorPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except OperationalError:
            logger.exception(
                "Falha de banco de dados ao atender %s %s",
                request.method,
                request.path,
            )
            return render(
                request,
                "feedback/erro_banco.html",
                status=503,
            )
