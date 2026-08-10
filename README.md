# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue.

## Cortex Monitoring (`dev-0.0.6`)

Installed via the 5tratumOS Custom Store. Grafana is opened directly on the
default port **3000** (portal embedding optional).

### Direct ports (LAN checks)

| Service | URL on the node |
|---------|-----------------|
| Grafana | `http://<node>:3000/` |
| VictoriaMetrics (VMUI) | `http://<node>:8428/vmui/` |
| VictoriaLogs (VMUI) | `http://<node>:9428/select/vmui/` |
| Alertmanager | `http://<node>:9093/` |
| Alloy | `http://<node>:12345/` |
| Node Exporter metrics | `http://<node>:9100/metrics` |

Quick health checks:

```bash
curl -fsS http://127.0.0.1:8428/health
curl -fsS http://127.0.0.1:9428/health
curl -fsS http://127.0.0.1:9100/metrics | head
curl -fsS http://127.0.0.1:12345/-/ready
curl -fsS http://127.0.0.1:9093/-/healthy
```

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
2. Install **Cortex Monitoring** `dev-0.0.6`
3. Login with the password methods above

If upgrading from a broken earlier build:

```bash
# uninstall in UI first
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```

Then reinstall so provisioning files are copied fresh.
