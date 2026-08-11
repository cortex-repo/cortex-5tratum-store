#!/usr/bin/env python3
"""Minimal Cortex Monitoring portal for 5tratumOS app_proxy."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "0.0.0.0"
PORT = 8080

LINKS = [
    {
        "id": "grafana",
        "name": "Grafana",
        "blurb": "Dashboards, Explore, and alerts",
        "port": 3000,
        "path": "/",
    },
    {
        "id": "victoriametrics",
        "name": "VictoriaMetrics",
        "blurb": "Metrics TSDB and VMUI",
        "port": 8428,
        "path": "/vmui/",
    },
    {
        "id": "victorialogs",
        "name": "VictoriaLogs",
        "blurb": "Log store and VMUI",
        "port": 9428,
        "path": "/select/vmui/",
    },
    {
        "id": "alertmanager",
        "name": "Alertmanager",
        "blurb": "Alert routing and silences",
        "port": 9093,
        "path": "/",
    },
    {
        "id": "alloy",
        "name": "Grafana Alloy",
        "blurb": "Collector UI and status",
        "port": 12345,
        "path": "/",
    },
    {
        "id": "node-exporter",
        "name": "Node Exporter",
        "blurb": "Host metrics endpoint",
        "port": 9100,
        "path": "/metrics",
    },
]


def render_page() -> bytes:
    cards = []
    for item in LINKS:
        cards.append(
            f"""
            <a class="card" id="link-{item['id']}" href="#" target="_blank" rel="noopener noreferrer"
               data-port="{item['port']}" data-path="{item['path']}">
              <div class="name">{item['name']}</div>
              <div class="blurb">{item['blurb']}</div>
              <div class="meta">:<span class="port">{item['port']}</span>{item['path']}</div>
            </a>
            """
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Cortex Monitoring</title>
  <style>
    :root {{
      --bg0: #0e1c20;
      --bg1: #143038;
      --panel: #1a3d46;
      --text: #e7f3f1;
      --muted: #9cb5b3;
      --accent: #3ea896;
      --accent-dim: #2c7d70;
      --line: rgba(231, 243, 241, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
      color: var(--text);
      background:
        radial-gradient(1200px 600px at 10% -10%, rgba(62, 168, 150, 0.22), transparent 55%),
        radial-gradient(900px 500px at 100% 0%, rgba(20, 80, 90, 0.45), transparent 50%),
        linear-gradient(160deg, var(--bg0), var(--bg1) 55%, #10262c);
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 20px 64px;
    }}
    .brand {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-bottom: 36px;
    }}
    .eyebrow {{
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-size: 12px;
      color: var(--accent);
      font-weight: 600;
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
      background: linear-gradient(180deg, rgba(62, 168, 150, 0.08), transparent 40%), var(--panel);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 18px 18px 16px;
      transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: rgba(62, 168, 150, 0.55);
      background: linear-gradient(180deg, rgba(62, 168, 150, 0.16), transparent 45%), #1e4852;
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
      font-size: 0.82rem;
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
      <div class="eyebrow">Cortex Monitoring</div>
      <h1>Observability portal</h1>
      <p class="lede">
        Open each tool in a new tab. Links use this host&rsquo;s address automatically.
      </p>
    </div>
    <div class="grid">
      {''.join(cards)}
    </div>
    <footer>Deployed via 5tratumOS store · Cortex Monitoring</footer>
  </main>
  <script>
    (function () {{
      var host = window.location.hostname || "127.0.0.1";
      document.querySelectorAll("a.card").forEach(function (el) {{
        var port = el.getAttribute("data-port");
        var path = el.getAttribute("data-path") || "/";
        el.href = "http://" + host + ":" + port + path;
      }});
    }})();
  </script>
</body>
</html>
"""
    return html.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            body = render_page()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/healthz":
            body = b"ok\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/api/links":
            body = json.dumps(LINKS).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Cortex Monitoring portal on http://{HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
