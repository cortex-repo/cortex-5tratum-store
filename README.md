# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue.

## Cortex Monitoring (`dev-0.0.3`)

Official GLOBAL Grafana wiring (`APP_HOST: app`, port `33012`) plus:

- VictoriaMetrics + VictoriaLogs
- Grafana Alloy + Node Exporter + Alertmanager
- VictoriaMetrics metrics/logs Grafana plugins
- Provisioned datasources
- [Node Exporter Full](https://grafana.com/grafana/dashboards/1860-node-exporter-full/) dashboard (id 1860)

## Password

- Username: `admin`
- Password: OS `APP_PASSWORD`, or `cortex` if the OS did not inject one

Find it on the node:

```bash
sudo cat /var/lib/5tratumos/apps/cortex-monitoring/admin-password.txt
# also try:
sudo grep -R APP_PASSWORD /var/lib/5tratumos/apps/cortex-monitoring -n 2>/dev/null
docker exec "$(docker ps --format '{{.Names}}' | grep -E 'cortex-monitoring.*app' | head -1)" printenv GF_SECURITY_ADMIN_PASSWORD
```

Reset if needed (does not require knowing the old password):

```bash
docker exec -it "$(docker ps --format '{{.Names}}' | grep -E 'cortex-monitoring.*app' | head -1)" \
  grafana cli admin reset-admin-password cortex
```

## Install

1. Add Custom Store: `https://github.com/cortex-repo/cortex-5tratum-store`
2. Install **Cortex Monitoring** `dev-0.0.3`
3. Login with the password methods above

If upgrading from a broken earlier build:

```bash
# uninstall in UI first
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```

Then reinstall so provisioning files are copied fresh.
