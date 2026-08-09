# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue.

## Cortex Monitoring (`dev-0.0.1`)

Exact runtime copy of the official GLOBAL [grafana](https://github.com/WillItMod/5tratStore-global/tree/main/grafana) recipe, rebranded as **Cortex Monitoring**.

| Field | Value |
|------|--------|
| id | `cortex-monitoring` |
| name | Cortex Monitoring |
| version | `dev-0.0.1` |
| upstream image | `grafana/grafana:13.1.0` |
| port | `33040` |

## Add this Custom Store

1. On the node, open App Store → Custom Stores → **Add store**.
2. Paste: `https://github.com/cortex-repo/cortex-5tratum-store`
3. Install **Cortex Monitoring**.
4. Sign in with Grafana admin and the OS-generated `APP_PASSWORD`.

## Clean reinstall tip

If an older Cortex Monitoring install left broken Grafana state:

```bash
# uninstall the app in the UI first, then:
sudo rm -rf /var/lib/5tratumos/apps/cortex-monitoring
```

Then install `dev-0.0.1` again from the store.
