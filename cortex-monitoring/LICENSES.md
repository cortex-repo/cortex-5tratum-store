# Licence and image record

Cortex Monitoring `dev-0.0.2` starts from the 5tratStore GLOBAL Grafana recipe and
adds VictoriaMetrics stack components. Images are pulled directly from upstream.

- **Grafana 13.1.0** — AGPL-3.0-only
  - Source: https://github.com/grafana/grafana/tree/v13.1.0
  - Licence: https://github.com/grafana/grafana/blob/v13.1.0/LICENSE
  - Image: `grafana/grafana:13.1.0@sha256:121a7a9ece6dc10b969f1f96eed64b4f07dfac0d0b8abc070f7cb83bbde86f63`
  - Plugins installed at runtime: `victoriametrics-metrics-datasource`, `victoriametrics-logs-datasource`
- **VictoriaMetrics v1.148.0** — Apache-2.0
  - Image: `victoriametrics/victoria-metrics:v1.148.0@sha256:407013e902f9a0ba1d4b2d4c077c47bbaf917c893c52ff39b19efe83a654afda`
- **VictoriaLogs v1.52.0** — Apache-2.0
  - Image: `victoriametrics/victoria-logs:v1.52.0@sha256:47b820890d64c4575a2a0a46415dcd8a4fd59a0f1fcd6a377693d7aea639442e`
- **Grafana Alloy v1.11.3** — Apache-2.0
  - Image: `grafana/alloy:v1.11.3@sha256:8c7256f412feb9f5f48f9f6f9394dc97ca887f63dea9304f347970ecc1787669`
- **Node Exporter v1.9.1** — Apache-2.0
  - Image: `prom/node-exporter:v1.9.1@sha256:d00a542e409ee618a4edc67da14dd48c5da66726bbd5537ab2af9c1dfc442c8a`
- **Alertmanager v0.33.1** — Apache-2.0
  - Image: `quay.io/prometheus/alertmanager:v0.33.1@sha256:9e082985f56f4c8c9f724e18f2288c6708f472e56a5286b8863d080434ea065d`
- **Alpine 3.22.1** (init) — `alpine:3.22.1@sha256:4bcff63911fcb4448bd4fdacec207030997caf25e9bea4045fa6c8c44de311d1`
- **Dashboard:** Node Exporter Full (Grafana.com id 1860), provisioned from upstream export
  - https://grafana.com/grafana/dashboards/1860-node-exporter-full/
- Icon: official Grafana asset
  https://raw.githubusercontent.com/grafana/grafana/v13.1.0/public/img/grafana_icon.svg

Node Exporter mounts host `/proc`, `/sys`, and `/` read-only and uses `pid: host`.
Alloy mounts `/var/run/docker.sock` and runs as root to collect logs from all
Docker containers into VictoriaLogs.
