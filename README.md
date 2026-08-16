# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue.

Add this store in 5tratumOS: `https://github.com/cortex-repo/cortex-5tratum-store`

## Cortex Mining Hub (`dev-0.1.0`)

First-party portal for Axe nodes, LAN miners, and 5tratumOS fleet KPIs.
The recipe pulls `ghcr.io/cortex-repo/cortex-mining-hub:dev-0.1.0` (built
from [cortex-mining](https://github.com/cortex-repo/cortex-mining)).

### Ports

| Service | URL |
|---------|-----|
| **Hub (5tratumOS app)** | `http://<node>:8790/` |

### First-run config

On install, the init container seeds `nodes.json`, `mining.json`, and
`portal.json` under the app data directory. Edit those files with RPC
passwords and miner credentials, then restart the app:

```bash
sudo nano /var/lib/5tratumos/apps/cortex-mining-hub/data/nodes.json
sudo nano /var/lib/5tratumos/apps/cortex-mining-hub/data/mining.json
```

Install the Axe node apps you want to monitor **before** this hub, so their
Docker networks exist (`5tratumos-axebch_default`, and so on). If a
standalone `cortex-mining-nodes` container is already bound to 8790, stop
it first.

Image source and publish workflow: [cortex-mining](https://github.com/cortex-repo/cortex-mining).

## Cortex Monitoring (`dev-0.0.12`)

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

Provisioned dashboards (Grafana → Cortex Monitoring folder):
- **Node Exporter Full** (1860)
- **APU Power** — RAPL package/core watts + GPU hwmon watts

**Note:** Fan Speed / Power Supply panels only show data if the host exposes
them via `/sys` (hwmon / power_supply). On AMD mini PCs such as the Minisforum
AI X1 Pro, use **APU Power** for package/core/GPU watts (RAPL + amdgpu).

## Password

- Username: `admin`
- Password: `cortex` (fixed; also written to `admin-password.txt`)

```bash
sudo cat /var/lib/5tratumos/apps/cortex-monitoring/admin-password.txt
```

Reset if an older install still has a generated password:

```bash
docker exec -it "$(docker ps --format '{{.Names}}' | grep -E 'cortex-monitoring.*grafana' | head -1)" \
  grafana cli admin reset-admin-password cortex
```

## Install

1. Add Custom Store: `https://github.com/cortex-repo/cortex-5tratum-store`
2. Install **Cortex Mining Hub** `dev-0.1.0` and/or **Cortex Monitoring** `dev-0.0.12`
3. Open the app in 5tratumOS

If upgrading Cortex Monitoring from an older build and the portal files are missing:

```bash
# uninstall in UI first for a clean copy of data/portal
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```
