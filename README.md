# Oraybox HTTP API Skill

[English](README.md) | [中文](README_zh.md)

Python HTTP client and reference documentation for Oray router management APIs.

## Overview

Oray routers expose management APIs via HTTP POST to `/cgi-bin/oraybox`.  
This repository packages a skill (`oraybox-http-api/`) that provides:

- A thin Python wrapper (`OrayboxHttpAPI`) for HTTP API calls.
- Complete API reference documentation split by category for efficient retrieval.

## Repository Layout

```
oraybox_api_skills/
├── README.md              # This file (English)
├── README_zh.md           # 中文版
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

## Configuration

### Environment Variables

The client reads the following environment variables when `host` or `password` are not provided explicitly:

| Variable | Description | Explicit override |
|----------|-------------|-------------------|
| `ORAYBOX_HOST` | Router IP or hostname | `host=` argument |
| `ORAYBOX_PASSWORD` | Router admin password | `password=` argument |

Set them in your shell profile or session:

```bash
export ORAYBOX_HOST="192.168.1.1"
export ORAYBOX_PASSWORD="your_admin_password"
```

Once set, omit the parameters:

```python
client = OrayboxHttpAPI()  # uses ORAYBOX_HOST and ORAYBOX_PASSWORD
```

### Client Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | `$ORAYBOX_HOST` | Router IP or hostname. Falls back to `ORAYBOX_HOST` env var when omitted |
| `password` | str | `$ORAYBOX_PASSWORD` | Admin panel password. Falls back to `ORAYBOX_PASSWORD` env var when omitted |
| `timeout` | int | 30 | HTTP timeout in seconds |
| `scheme` | str | `"http"` | URL scheme: `"http"` or `"https"` |
| `verify_ssl` | bool | `False` | Verify SSL certificates |
| `use_proxy` | bool | `False` | Use system HTTP/HTTPS proxy |

> **Security:** Password is sent in plaintext over HTTP by default. Use HTTPS (`scheme="https"`) when possible. SSL verification is disabled by default because routers typically use self-signed certificates.

## Prompt Examples

When using this skill in an AI agent (e.g., Kimi Code), here are typical prompts:

### Scan WiFi hotspots around the router

> 扫描蒲公英路由器周围的热点

The agent will call `wifi_scan_get` to list nearby wireless networks:

```python
client = OrayboxHttpAPI()
result = client.call("wifi_scan_get")
# Returns: wifi_scan[] (2.4G list), wifi_scan_5g[] (5G list)
# Each item: mac, mode, quality, quality_max, signal, ssid, channel, encryption
```

CLI equivalent:

```bash
python3 scripts/oraybox_http_api.py --api wifi_scan_get
```

### Get router system info

> 查询蒲公英路由器的系统信息

Calls `sys_base_info` for firmware version, device model, uptime, etc.

```bash
python3 scripts/oraybox_http_api.py --api sys_base_info
```

### Modify WiFi password

> 修改蒲公英路由器的 WiFi 密码

The agent reads current config via `wifi_get`, updates the password, and applies it via `wifi_set`.

### Check connected devices

> 查看蒲公英路由器上连接的设备列表

Calls `lan_device_get` to list all LAN clients with their IP, MAC, and hostname.

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
