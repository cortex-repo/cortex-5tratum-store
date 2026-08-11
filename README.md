# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue.

## Cortex Monitoring (`dev-0.0.9`)

Installed via the 5tratumOS Custom Store. The store app opens a **Python portal**
(not Grafana). Each tool link opens in a **new browser tab**.

### Ports

| Service | URL |
|---------|-----|
| **Portal (5tratumOS app)** | `http://<node>:8080/` |
| Grafana | `http://<node>:3000/` |
| VictoriaMetrics (VMUI) | `http://<node>:8428/vmui/` |
| VictoriaLogs (VMUI) | `http://<node>:9428/select/vmui/` |
| Alertmanager | `http://<node>:9093/` |
| Alloy | `http://<node>:12345/` |
| Node Exporter | `http://<node>:9100/metrics` |

Node Exporter collectors enabled for Node Exporter Full: `processes`, `systemd`
(+ D-Bus), `tcpstat`, `interrupts`, `ethtool`, `hwmon`, `powersupplyclass`.

**Note:** Fan Speed / Power Supply panels only show data if the host exposes
them via `/sys` (hwmon / power_supply).

## Password

- Username: `admin`
- Password: OS `APP_PASSWORD`, or `cortex` if unset

```bash
sudo cat /var/lib/5tratumos/apps/cortex-monitoring/admin-password.txt
```

Reset:

```bash
docker exec -it "$(docker ps --format '{{.Names}}' | grep -E 'cortex-monitoring.*grafana' | head -1)" \
  grafana cli admin reset-admin-password cortex
```

## Install

1. Add Custom Store: `https://github.com/cortex-repo/cortex-5tratum-store`
2. Install **Cortex Monitoring** `dev-0.0.9`
3. Open the app in 5tratumOS → portal → click through to tools

If upgrading from an older build and the portal files are missing:

```bash
# uninstall in UI first for a clean copy of data/portal
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```
