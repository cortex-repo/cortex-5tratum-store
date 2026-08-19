# Cortex Trading (`dev-0.1.2`)

First-party eToro agent portal + strategy worker. The recipe pulls
`ghcr.io/cortex-repo/cortex-trading:dev-0.1.2` (built from
[cortex-trading](https://github.com/cortex-repo/cortex-trading)).

**No eToro keys are in the image.** After install, sign in and paste keys in
Profile, then create a **new** eToro Agent and set Config → Agent URL.

## Ports

| Service | URL |
|---------|-----|
| **Portal (5tratumOS)** | `http://<node>/apps/cortex-trading/` |
| Direct port | `http://<node>:8787/` |

## First-run config

1. Open the portal. Login: `admin` / `cortex` (change this in Profile).
2. Profile: eToro public key + Demo/LIVE read and Agent trade private keys.
3. Config: Agent URL of the **new** copy (not an existing live book unless you intend to reuse it).
4. Default is Demo. LIVE stays blocked until you arm `LIVE_ARMED` in Profile.
5. Start the loop from the dashboard. The worker ticks on the shared data volume.

Data lives under `/var/lib/5tratumos/apps/cortex-trading/data/` (ledger, ops,
`runtime_config.json`). Uninstall → **Retain Data** keeps keys and history.

If a standalone `cortex-trading` compose stack is already bound to 8787, stop
it first.

## Known issues

**Reinstall does not work.** Uninstall the app first and choose **Retain Data**,
then install the latest version. If that install fails, uninstall again and
**purge data**, then install the latest version (you will need to re-enter
Profile keys).
