# Cortex 5tratum Store

Custom [5tratStore](https://github.com/WillItMod/5tratStore-global)-format catalogue
for Cortex apps.

Add this store in 5tratumOS: `https://github.com/cortex-repo/cortex-5tratum-store`

This repository publishes **store recipes only**: per-app `docker-compose.yml`,
`5tratstore-*.yml`, icons, config/provisioning assets, and a README. Application
source and container images live in their own repos and are pulled from GHCR.

## Apps

| App | Version | Summary | Image / source |
|-----|---------|---------|----------------|
| [Cortex Mining Hub](./cortex-mining-hub/) | `dev-0.1.8` | Fleet portal for Axe nodes, LAN miners, and 5tratumOS KPIs | `ghcr.io/cortex-repo/cortex-mining-hub` · [cortex-mining](https://github.com/cortex-repo/cortex-mining) |
| [Cortex Trading](./cortex-trading/) | `dev-0.1.11` | eToro Demo/LIVE agent with RiskGate and ops dashboard | `ghcr.io/cortex-repo/cortex-trading` · [cortex-trading](https://github.com/cortex-repo/cortex-trading) |
| [Cortex Monitoring](./cortex-monitoring/) | `dev-0.0.13` | Observability stack portal (Grafana, VictoriaMetrics/Logs, Alloy, …) | `ghcr.io/cortex-repo/cortex-monitoring` · [cortex-monitoring](https://github.com/cortex-repo/cortex-monitoring) |

## Install

1. Add Custom Store: `https://github.com/cortex-repo/cortex-5tratum-store`
2. Install the app(s) you need from the store catalogue
3. Open each app’s README in this repo for ports, passwords, and upgrade notes

## Known issues

**Reinstall does not work.** Uninstall the app first and choose **Retain Data**,
then install the latest version. If that install fails, uninstall again and
**purge data**, then install the latest version.
