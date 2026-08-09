# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue.

## Cortex Monitoring (`dev-0.0.2`)

Official GLOBAL Grafana wiring (`APP_HOST: app`, port `33012`) plus:

- VictoriaMetrics + VictoriaLogs
- Grafana Alloy + Node Exporter + Alertmanager
- VictoriaMetrics metrics/logs Grafana plugins
- Provisioned datasources
- [Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/) dashboard (id 1860)

## Install

1. Add Custom Store: `https://github.com/cortex-repo/cortex-5tratum-store`
2. Install **Cortex Monitoring** `dev-0.0.2`
3. Login: `admin` + OS `APP_PASSWORD`

If upgrading from a broken earlier build:

```bash
# uninstall in UI first
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```

Then reinstall so provisioning files are copied fresh.
