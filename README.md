# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue for Cortex apps on 5tratumOS.

**Repo:** `cortex-5tratum-store`  
**Stack in this store:** Grafana · VictoriaMetrics · VictoriaLogs · Alloy · Node Exporter · Alertmanager (bundled as **Cortex Monitoring**)

5tratumOS keeps **port 80**. The app is opened through the OS proxy into Grafana. There is no standalone nginx portal.

## Add this Custom Store

1. On the node (e.g. `192.168.0.70`), open the App Store → Custom / Community Stores → **Add store**.
2. Paste:

   ```text
   https://github.com/cortex-repo/cortex-5tratum-store
   ```

3. Install **Cortex Monitoring**.
4. Open the app and sign in to Grafana as `admin` with the generated app password.
5. Uninstall duplicate GLOBAL Grafana / VictoriaMetrics / VictoriaLogs / Prometheus apps if you do not want parallel stacks.

Optional local clone (recipe mirror only; install still goes through the store UI):

```bash
sudo mkdir -p /home/forge/cortexMonitoring
sudo git clone https://github.com/cortex-repo/cortex-5tratum-store.git /home/forge/cortexMonitoring
```

## Layout

```text
.
├── 5tratstore-store.yml      # store id/name
├── README.md
└── cortex-monitoring/
    ├── 5tratstore-app.yml
    ├── 5tratstore-review.yml # status: proposed
    ├── LICENSES.md
    ├── docker-compose.yml
    ├── icon.png
    └── data/
```

Manifests use **`5tratstore-app.yml`** (not `umbrel-app.yml`), matching 5tratStore GLOBAL.

## Persistence

Host data root is the 5tratumOS apps tree:

```text
/var/lib/5tratumos/apps/cortex-monitoring/data/
```

Compose uses `${APP_DATA_DIR}` when 5tratumOS injects it, otherwise defaults to
`/var/lib/5tratumos/apps/cortex-monitoring` (not a bare `/var/lib/...` path).

Under that `data/` directory:

- `grafana/`, `victoriametrics/`, `victorialogs/`, `alertmanager/`, `alloy/`
- `alloy.alloy`, `alertmanager.yml`, `grafana-provisioning/`, `dashboards/`

## Privileges (Node Exporter)

Read-only host mounts: `/proc`, `/sys`, `/` (as `/host/root`), plus `pid: host`. No `privileged: true`, no Docker socket. Alloy is metrics-first; log shipping to VictoriaLogs is commented in `data/alloy.alloy`.

## First start

- Datasources: VictoriaMetrics (default), VictoriaLogs, Alertmanager
- Dashboard: Host overview
- Alloy scrapes Node Exporter / VictoriaMetrics / self → remote_write to VictoriaMetrics

## GLOBAL

`5tratstore-review.yml` stays `status: proposed` until a maintainer clears rights and lifecycle tests for any GLOBAL submission.
