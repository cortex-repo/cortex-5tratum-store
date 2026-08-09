# Licence and image record

Copied from the 5tratStore GLOBAL Grafana recipe and rebranded as Cortex Monitoring
for Custom Store testing. Runtime artifacts are unchanged upstream images.

- Upstream: Grafana 13.1.0 — GNU Affero General Public License v3.0
  - Source: https://github.com/grafana/grafana/tree/v13.1.0
  - Licence: https://github.com/grafana/grafana/blob/v13.1.0/LICENSE
  - Notice: https://github.com/grafana/grafana/blob/v13.1.0/NOTICE.md
- Container: official `grafana/grafana:13.1.0`
  - Multi-architecture index digest: `sha256:121a7a9ece6dc10b969f1f96eed64b4f07dfac0d0b8abc070f7cb83bbde86f63`
  - Image documentation: https://grafana.com/docs/grafana/v13.1/setup-grafana/installation/docker/
- Initialisation helper: Alpine Linux `alpine:3.22.1`
  - Multi-architecture index digest: `sha256:4bcff63911fcb4448bd4fdacec207030997caf25e9bea4045fa6c8c44de311d1`
  - Licence information: https://www.alpinelinux.org/about/
- The icon is loaded directly from the official Grafana project asset:
  https://raw.githubusercontent.com/grafana/grafana/v13.1.0/public/img/grafana_icon.svg

The recipe runs an unmodified official upstream image. Corresponding source is
available from the exact tagged source link above.
