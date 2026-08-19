# Licence and image record

Cortex Trading `dev-0.1.3` is a first-party Cortex recipe. The store ships
listing metadata and Compose only. The node pulls the portal+worker image
from GitHub Container Registry.

- **Cortex Trading `dev-0.1.3`** — source-available first-party agent
  - Source: https://github.com/cortex-repo/cortex-trading
  - Image: `ghcr.io/cortex-repo/cortex-trading:dev-0.1.3`
  - Base: `python:3.12.11-slim-bookworm@sha256:519591d6871b7bc437060736b9f7456b8731f1499a57e22e6c285135ae657bf7` (PSF)
- **Icon:** original Cortex mark (`icon.png`), the same artwork as the portal.
- **Gallery:** portal screenshot (`1.png`).

No eToro API keys, `APP_SECRET`, or `.env` files are stored in the image.
Bootstrap login (`admin` / `cortex`) is the documented first-run password and
must be changed in Profile. Secrets entered after install live on `APP_DATA_DIR`.
