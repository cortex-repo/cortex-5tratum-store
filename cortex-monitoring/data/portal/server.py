#!/usr/bin/env python3
"""Minimal Cortex Monitoring portal for 5tratumOS app_proxy."""

from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 8080
ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"

# Keep in sync with 5tratstore-app.yml and docker-compose image tags.
CORTEX_VERSION = "dev-0.0.10"

LINKS = [
    {
        "id": "grafana",
        "name": "Grafana",
        "blurb": "Dashboards, Explore, and alerts",
        "port": 3000,
        "path": "/",
        "version": "13.1.0",
        "icon": "/static/icons/grafana.svg",
    },
    {
        "id": "victoriametrics",
        "name": "VictoriaMetrics",
        "blurb": "Metrics TSDB and VMUI",
        "port": 8428,
        "path": "/vmui/",
        "version": "v1.148.0",
        "icon": "/static/icons/victoriametrics.svg",
    },
    {
        "id": "victorialogs",
        "name": "VictoriaLogs",
        "blurb": "Log store and VMUI",
        "port": 9428,
        "path": "/select/vmui/",
        "version": "v1.52.0",
        "icon": "/static/icons/victorialogs.svg",
    },
    {
        "id": "alertmanager",
        "name": "Alertmanager",
        "blurb": "Alert routing and silences",
        "port": 9093,
        "path": "/",
        "version": "v0.33.1",
        "icon": "/static/icons/alertmanager.svg",
    },
    {
        "id": "alloy",
        "name": "Grafana Alloy",
        "blurb": "Collector UI and status",
        "port": 12345,
        "path": "/",
        "version": "v1.11.3",
        "icon": "/static/icons/alloy.svg",
    },
    {
        "id": "node-exporter",
        "name": "Node Exporter",
        "blurb": "Host metrics endpoint",
        "port": 9100,
        "path": "/metrics",
        "version": "v1.9.1",
        "icon": "/static/icons/node-exporter.svg",
    },
]


def _strip_host_port(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("["):
        end = value.find("]")
        return value[1:end] if end != -1 else value
    # host:port — avoid splitting IPv6 without brackets
    if value.count(":") == 1:
        return value.split(":", 1)[0]
    return value


def resolve_public_host(headers: dict[str, str] | None = None) -> str:
    """Prefer an explicit LAN IP, then proxy/request host."""
    for key in ("HOST_IP", "DEVICE_HOST_IP", "DEVICE_IP", "LAN_IP"):
        env = os.environ.get(key, "").strip()
        if env:
            return _strip_host_port(env)

    headers = headers or {}
    for key in ("X-Forwarded-Host", "Host"):
        raw = headers.get(key, "")
        if not raw:
            continue
        candidate = _strip_host_port(raw.split(",")[0])
        if candidate and candidate.lower() not in {"localhost", "127.0.0.1", "::1"}:
            return candidate

    host = _strip_host_port((headers or {}).get("Host", ""))
    return host or "127.0.0.1"


def tool_url(host: str, port: int, path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    return f"http://{host}:{port}{path}"


def render_page(host: str) -> bytes:
    cards = []
    for item in LINKS:
        url = tool_url(host, item["port"], item["path"])
        cards.append(
            f"""
            <a class="card" id="link-{item['id']}" href="{url}" target="_blank" rel="noopener noreferrer"
               data-port="{item['port']}" data-path="{item['path']}">
              <div class="card-top">
                <img class="icon" src="{item['icon']}" alt="" width="40" height="40" />
                <span class="version">{item['version']}</span>
              </div>
              <div class="name">{item['name']}</div>
              <div class="blurb">{item['blurb']}</div>
              <div class="meta">{url}</div>
            </a>
            """
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="dark" />
  <title>Cortex Monitoring</title>
  <style>
    :root {{
      --bg0: #05070a;
      --bg1: #0a0f14;
      --panel: #121820;
      --panel-hover: #18212c;
      --text: #e8eef4;
      --muted: #8b98a8;
      --accent: #3dd6c6;
      --accent-dim: #1f8f84;
      --line: rgba(232, 238, 244, 0.08);
      --chip: rgba(61, 214, 198, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "IBM Plex Sans", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(900px 480px at 8% -8%, rgba(61, 214, 198, 0.12), transparent 55%),
        radial-gradient(700px 420px at 100% 0%, rgba(40, 70, 110, 0.22), transparent 50%),
        linear-gradient(165deg, var(--bg0), var(--bg1) 50%, #070b10);
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 20px 64px;
    }}
    .brand {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 36px;
    }}
    .brand-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px 14px;
    }}
    .eyebrow {{
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-size: 12px;
      color: var(--accent);
      font-weight: 600;
    }}
    .app-version {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: var(--chip);
      color: var(--accent);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.78rem;
      letter-spacing: 0.02em;
    }}
    h1 {{
      margin: 0;
      font-size: clamp(2rem, 4vw, 3rem);
      font-weight: 650;
      letter-spacing: -0.03em;
    }}
    .lede {{
      margin: 0;
      max-width: 42rem;
      color: var(--muted);
      line-height: 1.55;
      font-size: 1.05rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
    }}
    .card {{
      display: block;
      text-decoration: none;
      color: inherit;
      background: linear-gradient(180deg, rgba(61, 214, 198, 0.05), transparent 42%), var(--panel);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 18px 18px 16px;
      transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: rgba(61, 214, 198, 0.4);
      background: linear-gradient(180deg, rgba(61, 214, 198, 0.1), transparent 45%), var(--panel-hover);
    }}
    .card-top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 14px;
    }}
    .icon {{
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: #0a0e13;
      border: 1px solid var(--line);
      object-fit: contain;
      padding: 4px;
    }}
    .version {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.75rem;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 3px 9px;
      white-space: nowrap;
    }}
    .name {{
      font-size: 1.15rem;
      font-weight: 650;
      margin-bottom: 6px;
    }}
    .blurb {{
      color: var(--muted);
      font-size: 0.95rem;
      line-height: 1.4;
      min-height: 2.6em;
    }}
    .meta {{
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.78rem;
      color: var(--accent);
      word-break: break-all;
    }}
    .lede code {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: 0.92em;
      color: var(--accent);
    }}
    footer {{
      margin-top: 28px;
      color: var(--muted);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <main>
    <div class="brand">
      <div class="brand-row">
        <div class="eyebrow">Cortex Monitoring</div>
        <span class="app-version">{CORTEX_VERSION}</span>
      </div>
      <h1>Observability portal</h1>
      <p class="lede">
        Open each tool in a new tab. Links use
        <code>http://&lt;host-ip&gt;:&lt;port&gt;</code> for this machine.
      </p>
    </div>
    <div class="grid">
      {''.join(cards)}
    </div>
    <footer>Deployed via 5tratumOS store · Cortex Monitoring {CORTEX_VERSION}</footer>
  </main>
  <script>
    (function () {{
      var fallback = {json.dumps(host)};
      var host = window.location.hostname || fallback || "127.0.0.1";
      if (!host || host === "localhost" || host === "127.0.0.1") {{
        host = fallback || host;
      }}
      document.querySelectorAll("a.card").forEach(function (el) {{
        var port = el.getAttribute("data-port");
        var path = el.getAttribute("data-path") || "/";
        var url = "http://" + host + ":" + port + path;
        el.href = url;
        var meta = el.querySelector(".meta");
        if (meta) meta.textContent = url;
      }});
    }})();
  </script>
</body>
</html>
"""
    return html.encode("utf-8")


def _safe_static(path: str) -> Path | None:
    if not path.startswith("/static/"):
        return None
    rel = path[len("/static/") :]
    if not rel or ".." in rel.split("/"):
        return None
    candidate = (STATIC / rel).resolve()
    try:
        candidate.relative_to(STATIC.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return candidate


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]

        if path in ("/", "/index.html"):
            host = resolve_public_host({k: v for k, v in self.headers.items()})
            body = render_page(host)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/healthz":
            body = b"ok\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == "/api/links":
            host = resolve_public_host({k: v for k, v in self.headers.items()})
            links = [
                {
                    **item,
                    "url": tool_url(host, item["port"], item["path"]),
                }
                for item in LINKS
            ]
            payload = {"cortex_version": CORTEX_VERSION, "host": host, "links": links}
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        static_file = _safe_static(path)
        if static_file is not None:
            data = static_file.read_bytes()
            ctype, _ = mimetypes.guess_type(str(static_file))
            if static_file.suffix == ".svg":
                ctype = "image/svg+xml"
            self.send_response(200)
            self.send_header("Content-Type", ctype or "application/octet-stream")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(data)
            return

        self.send_response(404)
        self.end_headers()


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Cortex Monitoring portal {CORTEX_VERSION} on http://{HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
