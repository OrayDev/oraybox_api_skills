# AGENTS.md — oraybox_api_skills

## Project Overview

This repository is a **Kimi skill** that provides a Python HTTP client and
comprehensive API reference for Oray router management APIs.

Routers expose management APIs via HTTP POST to `/cgi-bin/oraybox` with form
data.  Every call requires `_api` (API name) and `_pwd` (admin password).

## Technology Stack

- **Language:** Python >= 3.10
- **Dependencies:** `requests`
- **No build step required** — pure Python library

## Code Organization

```
oraybox_api_skills/
├── README.md              # Human-readable project overview
├── AGENTS.md              # This file
├── tests/                 # Unit tests
├── scripts/               # Build / packaging scripts
└── oraybox-http-api/      # Skill root (packaged and distributed)
    ├── SKILL.md           # Skill entrypoint
    ├── scripts/
    │   └── oraybox_http_api.py   # Core Python client
    └── references/               # API docs by category (19 files)
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

## Build and Test Commands

```bash
# Validate Python syntax
python3 -m py_compile oraybox-http-api/scripts/oraybox_http_api.py

# Run tests
python3 -m pytest tests/

# Package skill
./scripts/package.sh
```

## Code Style Guidelines

- Follow PEP 8.
- Use type hints for public methods.
- Docstrings use Google style.

## Security Considerations

- Password is sent in plaintext over HTTP by default.  Use HTTPS (`scheme="https"`) when possible.
- SSL verification is disabled by default (`verify_ssl=False`) because routers typically use self-signed certificates.
- Never commit real router passwords to version control.

## Deployment

Package the skill directory into a `.skill` zip archive:

```bash
zip -r oraybox-http-api.skill oraybox-http-api
```

The `.skill` file is the distributable artifact.
