# Licence and image record

Cortex Mining Hub `dev-0.1.2` is a first-party Cortex recipe. The store
ships listing metadata and Compose only. The node pulls the portal image
from GitHub Container Registry.

- **Cortex Mining Hub `dev-0.1.2`** — source-available first-party portal
  - Source: https://github.com/cortex-repo/cortex-mining
  - Image: `ghcr.io/cortex-repo/cortex-mining-hub:dev-0.1.2`
  - Base: `python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7` (PSF)
- **Icon:** original Cortex Mining artwork (`icon.png`), the same mark used
  in the hub portal.

Config JSON (`nodes.json`, `mining.json`, `portal.json`) is seeded on first
start from defaults baked in the image. Those defaults use `CHANGE_ME`
placeholders and are not credentials. Node RPC secrets are copied at
runtime from the sibling 5tratumOS app confs and are not stored in the
image.
