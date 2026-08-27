# Cortex Mining Hub (`dev-0.1.9`)

First-party portal for Axe nodes, LAN miners, and 5tratumOS fleet KPIs.
The recipe pulls `ghcr.io/cortex-repo/cortex-mining-hub:dev-0.1.9` (built
from [cortex-mining](https://github.com/cortex-repo/cortex-mining)).
The store listing gallery is `1.png`–`6.png`.

## Ports

| Service | URL |
|---------|-----|
| **Hub (5tratumOS)** | `http://<node>/apps/cortex-mining-hub/` |
| Node page | `http://<node>/apps/cortex-mining-hub/nodes/bch` |
| Direct port | `http://<node>:8790/` |

## First-run config

On install, the init container seeds `nodes.json`, `mining.json`, and
`portal.json`, then copies each Axe node's `rpcuser` / `rpcpassword` /
`rpcport` from `/var/lib/5tratumos/apps/<app>/data/node/`. Use Settings →
**Scrape RPC from 5tratumOS** if a node password or RPC port changes.

Still fill 5tratumOS WebUI and miner credentials in Settings (or edit
`mining.json`):

```bash
sudo nano /var/lib/5tratumos/apps/cortex-mining-hub/data/mining.json
```

Install the Axe node apps you want to monitor **before** this hub, so their
Docker networks exist (`5tratumos-axebch_default`, and so on). If a
standalone `cortex-mining-nodes` container is already bound to 8790, stop
it first.

Image source and publish workflow: [cortex-mining](https://github.com/cortex-repo/cortex-mining).

## Known issues

**Reinstall does not work.** To pick up a new version, uninstall the app and
choose **Retain Data**, then install the latest version from the store. If that
install fails, uninstall again and **purge data**, then install the latest
version (you will need to re-enter Settings credentials).
