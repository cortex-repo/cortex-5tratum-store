# Cortex Monitoring (`dev-0.0.15`)

5tratumOS store recipe for the Cortex Monitoring stack. The store app opens a
**Cortex-branded portal image** (not Grafana). Each tool link opens in a new
browser tab as `http://<host-ip>:<port>…`.

Portal image: `ghcr.io/cortex-repo/cortex-monitoring:dev-0.0.13`  
Source: [cortex-repo/cortex-monitoring](https://github.com/cortex-repo/cortex-monitoring)

## Ports

| Service | URL |
|---------|-----|
| **Portal (5tratumOS app)** | `http://<node>:8080/` |
| Grafana | `http://<node>:3000/` |
| VictoriaMetrics (VMUI) | `http://<node>:8428/vmui/` |
| VictoriaLogs (VMUI) | `http://<node>:9428/select/vmui/` |
| Alertmanager | `http://<node>:9093/` |
| Alloy | `http://<node>:12345/` |
| Node Exporter | `http://<node>:9100/metrics` |

## Stack notes

Node Exporter collectors enabled for Node Exporter Full: `processes`, `systemd`
(+ D-Bus), `tcpstat`, `interrupts`, `ethtool`, `hwmon`, `powersupplyclass`.

Provisioned dashboards (Grafana → Cortex Monitoring folder):
- **Node Exporter Full** (1860)
- **APU Power** — RAPL package/core watts + GPU hwmon watts
- **Axe BCH Pool Logs** — ckpool.log + sharelog explore panels

Fan Speed / Power Supply panels only show data if the host exposes them via
`/sys` (hwmon / power_supply). On AMD mini PCs such as the Minisforum AI X1 Pro,
use **APU Power** for package/core/GPU watts (RAPL + amdgpu).

## Axe BCH pool logs → VictoriaLogs

Alloy mounts `/var/lib/5tratumos/apps/axebch/data/pool/www` and tails:

| Path | Stream labels |
|------|----------------|
| `ckpool.log*` | `job=ckpool`, `log_type=ckpool`, `coin=bch` |
| `**/*.sharelog` | `job=ckpool`, `log_type=sharelog`, `coin=bch` (+ `result`, `agent` from JSON) |

New hex subfolders / `.sharelog` files are discovered every 10s. On first
discover Alloy starts at **EOF** (`tail_from_end`) so historical heavy sharelogs
are not backfilled. To re-ingest from scratch, stop the stack, clear Alloy
positions under `APP_DATA_DIR/alloy`, set `tail_from_end = false` temporarily,
and restart.

Sharelog lines are pure JSON without a `msg` field. Alloy injects `_msg`
(worker + result + diff) before push so VictoriaLogs does not show
“missing _msg field”.

### Explore (VictoriaLogs / Grafana Explore)

```
_stream:{job="ckpool"}
_stream:{job="ckpool",log_type="sharelog"}
_stream:{job="ckpool",log_type="sharelog"} | unpack_json
_stream:{job="ckpool",log_type="sharelog"} | unpack_json | result:true
_stream:{job="ckpool",log_type="sharelog"} | unpack_json | workername:="<worker>"
_stream:{job="ckpool",log_type="ckpool"}
```

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

## Upgrade / clean reinstall

```bash
# uninstall in UI first, then clear app data if config/dashboards are stale
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```

For Alloy config updates only, refresh the Custom Store version and restart the
`alloy` service so `/etc/alloy/config.alloy` is re-read (or reinstall retaining
data after copying the new `data/config/alloy.alloy`).

## Recipe layout

| Path | Purpose |
|------|---------|
| `docker-compose.yml` | Stack services (portal image + observability) |
| `5tratstore-app.yml` | Store listing metadata |
| `5tratstore-review.yml` | Review checklist |
| `data/config/` | Alloy + Alertmanager defaults |
| `data/provisioning/` | Grafana datasources/dashboards provisioning |
| `data/dashboards/` | Provisioned dashboard JSON |
