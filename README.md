# Oraybox HTTP API Skill

Python HTTP client and reference documentation for Oray router management APIs.

## Overview

Oray routers expose management APIs via HTTP POST to `/cgi-bin/oraybox`.  
This repository packages a Kimi skill (`oraybox-http-api/`) that provides:

- A thin Python wrapper (`OrayboxHttpAPI`) for HTTP API calls.
- Complete API reference documentation split by category for efficient retrieval.

## Repository Layout

```
oraybox_api_skills/
├── README.md              # This file
├── AGENTS.md              # Agent guidelines
├── tests/                 # Unit tests
│   └── test_client.py
├── scripts/               # Build / packaging scripts
│   └── package.sh
└── oraybox-http-api/      # Skill root (packaged and distributed)
    ├── SKILL.md           # Skill entrypoint
    ├── scripts/
    │   └── oraybox_http_api.py   # Core Python client
    └── references/               # API docs by category
        ├── index.md
        ├── system.md
        ├── network.md
        ├── dhcp.md
        ├── wifi.md
        ├── port-forward.md
        ├── device.md
        ├── diagnostics.md
        ├── flowrate.md
        ├── service-control.md
        ├── behaviour.md
        ├── acl.md
        ├── group-support.md
        ├── mwan3.md
        ├── traffic-control.md
        ├── dmz.md
        ├── snmp.md
        ├── upnpd.md
        ├── app-traffic.md
        └── usb-file.md
```

## Quick Start

```python
from oraybox-http-api.scripts.oraybox_http_api import OrayboxHttpAPI

client = OrayboxHttpAPI(host="192.168.1.1", password="admin")
info = client.call("sys_base_info")
wifi = client.call("wifi_get", dev="2.4G", tag=1)
```

## Packaging

Build the distributable `.skill` file:

```bash
./scripts/package.sh
```

This creates `oraybox-http-api.skill` (a zip archive of the skill directory).

## Requirements

- Python >= 3.10
- `requests`

```bash
pip install -r oraybox-http-api/requirements.txt
```

## Testing

```bash
python3 -m pytest tests/
```

## License

MIT
