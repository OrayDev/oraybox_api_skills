---
name: oraybox-http-api
description: >
  Python HTTP client for Oray router management APIs. Use when you need to
  interact with an Oray router via its HTTP API endpoint (/cgi-bin/oraybox).
  Covers system info, network config, WiFi, DHCP, port forwarding, traffic
  control, diagnostics, and more. Typical triggers: "call router api",
  "get router status", "configure router wifi", "oraybox api http".
---

# Oraybox HTTP API

## Overview

Oray routers expose management APIs via HTTP POST to `/cgi-bin/oraybox`.
Every call requires two form fields:

- `_api` — the API name (e.g., `sys_base_info`, `wifi_get`)
- `_pwd` — the router admin panel password

Additional parameters are API-specific.

## Quick Start

```python
from scripts.oraybox_http_api import OrayboxHttpAPI

client = OrayboxHttpAPI(host="192.168.1.1", password="admin")

# Single API call
info = client.call("sys_base_info")

# With parameters
wifi = client.call("wifi_get", dev="2.4G", tag=1)

# Batch calls
results = client.call_batch([
    {"api": "sys_base_info"},
    {"api": "cpu_mem_get"},
])
```

## Client Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | required | Router IP or hostname |
| `password` | str | required | Admin panel password |
| `timeout` | int | 30 | HTTP timeout in seconds |
| `scheme` | str | "http" | URL scheme: "http" or "https" |
| `verify_ssl` | bool | False | Verify SSL certificates |

## API Categories

API documentation is split by category in `references/`.  
Read the relevant file when you need parameter details or examples for a specific domain.

| Category | File | APIs |
|----------|------|------|
| System | [system.md](references/system.md) | sys_base_info, cpu_mem_get, system_status_get, sys_time_get/set, timezone_get/set, reboot, reset, passwd, upgrade_info_get, sys_upgrade_ex |
| Network | [network.md](references/network.md) | interface_operate, dns_get/set, static_route_get/set, mtu_get/set, work_mode_get/set, interface_status_get, interface_dump, ether_status_get, interface_track_get/set |
| DHCP | [dhcp.md](references/dhcp.md) | dhcp_get/set, dhcp_bind_get/set, hosts_get/set |
| WiFi | [wifi.md](references/wifi.md) | wifi_get/set, wifi_scan_get, wifi_channels_get, wifi_disconnect_sta |
| Port Forward | [port-forward.md](references/port-forward.md) | port_map_get/add/delete, ip_bind_get/set |
| Device | [device.md](references/device.md) | lan_device_get, lan_device_alias_set, mac_control_get/set |
| Diagnostics | [diagnostics.md](references/diagnostics.md) | dump_ping, ping, dump_traceroute, dump_ifconfig, dump_route, dump_ps, net_test |
| Flowrate | [flowrate.md](references/flowrate.md) | flowrate_get, flowrate_ip_get, flowrate_wan_get |
| Service Control | [service-control.md](references/service-control.md) | restart_service |
| Behaviour | [behaviour.md](references/behaviour.md) | behaviour_get/set, behaviour_log_get/set/clear |
| ACL | [acl.md](references/acl.md) | acl_get/set |
| Group Support | [group-support.md](references/group-support.md) | group_get/set, group_reference_get/set |
| MWAN3 | [mwan3.md](references/mwan3.md) | mwan_get/set, mwan_rules_get/set, interface_track_get/set, netstat_get, netstat_alarm_get/set |
| Traffic Control | [traffic-control.md](references/traffic-control.md) | oraytc_get/set, group_tc_get/set |
| DMZ | [dmz.md](references/dmz.md) | dmz_get, dmz_get_ex, dmz_set |
| SNMP | [snmp.md](references/snmp.md) | snmp_get/set |
| UPnP | [upnpd.md](references/upnpd.md) | upnpd_get/set |
| App Traffic | [app-traffic.md](references/app-traffic.md) | app_traffic_get/set, app_traffic_upload_get/set |
| USB File | [usb-file.md](references/usb-file.md) | usb_file_samba_get/get_ex/set, usb_file_format, usb_file_format_result, usb_label_set, usb_safe_remove |

See [references/index.md](references/index.md) for the full error codes reference.

## Response Format

The router returns JSON:

```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

- `code=0` — success
- `code≠0` — error (see error codes in references/index.md)

The client raises `OrayboxHttpAPIError` on HTTP failures, JSON decode errors,
or when `code != 0`.

## CLI Usage

The script can also be run directly from the command line:

```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 \
    --password admin \
    --api sys_base_info
```

### CLI Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--host` | yes | — | Router IP address or hostname |
| `--password` | yes | — | Admin panel password |
| `--api` | yes | — | API name to call |
| `--param` | no | — | API parameter as `key=value`. Can be used multiple times. For JSON values, wrap the whole argument in quotes. |
| `--timeout` | no | 30 | HTTP timeout in seconds |
| `--https` | no | false | Use HTTPS instead of HTTP |

### CLI Examples

Simple parameter:
```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 --password admin \
    --api wifi_get --param dev=2.4G --param tag=1
```

JSON parameter (shell-quoted):
```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 --password admin \
    --api interface_operate \
    --param 'op=add' \
    --param 'name=wan3' \
    --param 'info={"mod":"dhcp"}'
```

HTTPS with custom timeout:
```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 --password admin --https --timeout 60 \
    --api cpu_mem_get
```

See [references/index.md](references/index.md) for per-API CLI examples.

## Notes

- Complex parameters (dicts/lists) are automatically JSON-encoded before sending.
- SSL verification is disabled by default because routers typically use
  self-signed certificates.
- When using `https`, the router may redirect to `http`.
