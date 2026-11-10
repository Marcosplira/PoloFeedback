"""Read-only availability checks for the public Polo Feedback pages."""

import json
import os
import re
import sys
import time
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen


MAX_RESPONSE_BYTES = 2 * 1024 * 1024
TIMEOUT_SECONDS = 20
CHECKS = (
    ("/", ("Sua experiência ajuda a gente a evoluir",)),
    (
        "/avaliar/",
        ("Sobre o que você quer opinar?", "Qual aula coletiva você quer avaliar?"),
    ),
    ("/enquete/", ("Ajude a escolher as próximas aulas",)),
    ("/login/", ("Bem-vindo de volta",)),
    ("/service-worker.js", ("addEventListener", "fetch")),
)


def _base_url(value):
    parts = urlsplit(value)
    if (
        parts.scheme != "https"
        or not parts.netloc
        or parts.path not in ("", "/")
        or parts.username
        or parts.password
        or parts.query
        or parts.fragment
    ):
        raise ValueError("SITE_URL deve ser uma origem HTTPS sem credenciais ou caminho.")
    return f"{parts.scheme}://{parts.netloc}"


def _fetch(base_url, path):
    url = urljoin(f"{base_url}/", path.lstrip("/"))
    request = Request(url, headers={"User-Agent": "PoloFeedback-Monitor/1.0"})
    with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        final_url = urlsplit(response.geturl())
        expected_origin = urlsplit(base_url)
        if final_url.scheme != "https" or final_url.netloc != expected_origin.netloc:
            raise ValueError("redirecionamento para origem diferente ou sem HTTPS")
        if not 200 <= response.status < 300:
            raise ValueError(f"HTTP {response.status}")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("resposta excedeu o limite de 2 MiB")
    return body.decode("utf-8", errors="replace")


def _check(base_url, path, expected):
    started = time.monotonic()
    try:
        content = _fetch(base_url, path)
        if path.endswith(".webmanifest"):
            manifest = json.loads(content)
            if manifest.get("scope") != "/" or manifest.get("start_url") != "/":
                raise ValueError("manifest sem scope/start_url esperados")
        else:
            plain_text = re.sub(r"<[^>]*>", " ", content)
            plain_text = re.sub(r"\s+", " ", plain_text)
            missing = [marker for marker in expected if marker not in plain_text]
            if missing:
                raise ValueError("marcadores ausentes: " + ", ".join(missing))
        elapsed = time.monotonic() - started
        print(f"OK   {path} ({elapsed:.2f}s)")
        return True
    except (OSError, URLError, TimeoutError, ValueError, json.JSONDecodeError) as error:
        elapsed = time.monotonic() - started
        print(f"ERRO {path} ({elapsed:.2f}s): {error}")
        return False


def main():
    site_url = os.environ.get(
        "SITE_URL",
        "https://polofeedback.pythonanywhere.com",
    )
    try:
        base_url = _base_url(site_url)
    except ValueError as error:
        print(f"ERRO SITE_URL: {error}", file=sys.stderr)
        return 2

    checks = [
        *CHECKS,
        (
            "/static/feedback/manifest.webmanifest",
            (),
        ),
    ]
    results = [_check(base_url, path, expected) for path, expected in checks]
    passed = sum(results)
    print(f"Resultado: {passed}/{len(results)} verificações passaram.")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
