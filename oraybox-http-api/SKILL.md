---
name: oraybox-http-api
version: 1.1.0
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
Every call requires an `_api` field (the API name) and a `_pwd` field (the router
admin password). When using the CLI, the password is read from the
`ORAYBOX_PASSWORD` environment variable by default — you do **not** need to
pass it explicitly unless the variable is not set.

> **Agent guidance:** Do **not** ask the user for the router password before
> attempting the first API call. Assume `ORAYBOX_HOST` and `ORAYBOX_PASSWORD`
> are already configured in the environment. Only if the call fails with
> `code=4` (authentication error) should you ask the user for the password.

## Requirements

- **Python**: 3.6 or newer
- **Dependencies**: No external packages — uses only the Python standard library (`urllib`, `ssl`, `json`)

## Quick Start

```bash
# host and password use environment variables
python3 scripts/oraybox_http_api.py --api sys_base_info
```

```python
from scripts.oraybox_http_api import OrayboxHttpAPI

# Password can be omitted when ORAYBOX_PASSWORD is set in the environment
client = OrayboxHttpAPI(host="192.168.1.1")

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

## Environment Variables

The client reads the following environment variables when `host` or `password` are not provided explicitly:

| Variable | Description | Explicit override |
|----------|-------------|-------------------|
| `ORAYBOX_HOST` | Router IP or hostname | `host=` argument |
| `ORAYBOX_PASSWORD` | Router admin password | `password=` argument |

This works for both Python API usage and CLI usage.

## Client Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | `$ORAYBOX_HOST` | Router IP or hostname. Falls back to `ORAYBOX_HOST` env var when omitted |
| `password` | str | `$ORAYBOX_PASSWORD` | Admin panel password. Falls back to `ORAYBOX_PASSWORD` env var when omitted |
| `timeout` | int | 30 | HTTP timeout in seconds |
| `scheme` | str | "http" | URL scheme: "http" or "https" |
| `verify_ssl` | bool | False | Verify SSL certificates |
| `use_proxy` | bool | False | Use system HTTP/HTTPS proxy |

## API Categories

API documentation is split by category in `references/`.  
Read the relevant file when you need parameter details or examples for a specific domain.

| Category | File | APIs | Description |
|----------|------|------|-------------|
| System | [system.md](references/system.md) | sys_base_info, cpu_mem_get, system_status_get, sys_time_get/set, timezone_get/set, reboot, reset, passwd, upgrade_info_get, sys_upgrade_ex | Router system info, CPU/memory, time, timezone, reboot, reset, password, firmware upgrade |
| Network | [network.md](references/network.md) | interface_operate, dns_get/set, static_route_get/set, mtu_get/set, work_mode_get/set, interface_status_get, interface_dump, ether_status_get, interface_track_get/set | WAN/LAN interface config, DNS, static routes, MTU, work mode, interface status |
| DHCP | [dhcp.md](references/dhcp.md) | dhcp_get/set, dhcp_bind_get/set, hosts_get/set | DHCP server settings, static IP bindings, host management |
| WiFi | [wifi.md](references/wifi.md) | wifi_get/set, wifi_scan_get, wifi_channels_get, wifi_disconnect_sta | WiFi settings, scan, channels, disconnect clients |
| Port Forward | [port-forward.md](references/port-forward.md) | port_map_get/add/delete, ip_bind_get/set | Port mapping, DMZ-like IP binding |
| Device | [device.md](references/device.md) | lan_device_get, lan_device_alias_set, mac_control_get/set | LAN device list, device alias, MAC access control |
| Diagnostics | [diagnostics.md](references/diagnostics.md) | dump_ping, ping, dump_traceroute, dump_ifconfig, dump_route, dump_ps, net_test | Ping, traceroute, network/interface diagnostics |
| Flowrate | [flowrate.md](references/flowrate.md) | flowrate_get, flowrate_ip_get, flowrate_wan_get | Real-time flow rate statistics |
| Service Control | [service-control.md](references/service-control.md) | restart_service | Service restart control |
| Behaviour | [behaviour.md](references/behaviour.md) | behaviour_get/set, behaviour_log_get/set/clear | Network behaviour monitoring and logging |
| ACL | [acl.md](references/acl.md) | acl_get/set | Access control list (firewall rules) |
| Group Support | [group-support.md](references/group-support.md) | group_get/set, group_reference_get/set | IP/group management and reference |
| MWAN3 | [mwan3.md](references/mwan3.md) | mwan_get/set, mwan_rules_get/set, interface_track_get/set, netstat_get, netstat_alarm_get/set | Multi-WAN load balancing and failover |
| Traffic Control | [traffic-control.md](references/traffic-control.md) | oraytc_get/set, group_tc_get/set | QoS/bandwidth shaping and rate limiting |
| DMZ | [dmz.md](references/dmz.md) | dmz_get, dmz_get_ex, dmz_set | DMZ host configuration |
| SNMP | [snmp.md](references/snmp.md) | snmp_get/set | SNMP service configuration |
| UPnP | [upnpd.md](references/upnpd.md) | upnpd_get/set | UPnP port mapping service |
| App Traffic | [app-traffic.md](references/app-traffic.md) | app_traffic_get/set, app_traffic_upload_get/set | Per-application traffic monitoring |
| TFS | [tfs.md](references/tfs.md) | tfs_one_day_get | 24-hour traffic flow statistics for sub-devices |
| USB File | [usb-file.md](references/usb-file.md) | usb_file_samba_get/get_ex/set, usb_file_format, usb_file_format_result, usb_label_set, usb_safe_remove | USB storage, Samba share, format, safe remove |
| Net Access Time | [net-access-time.md](references/net-access-time.md) | net_access_time_get/set | Time-based network access control |

## Response Format

The router returns JSON:

```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

The client raises `OrayboxHttpAPIError` on HTTP failures, JSON decode errors,
or when `code != 0`.

### Common Error Codes

| Code | Meaning | When it happens |
|------|---------|-----------------|
| 0 | Success | Request completed successfully |
| 1 | Internal error | Router internal processing failure |
| 2 | API not exist | The `_api` name is not recognized by the router |
| 3 | No API specified | Missing `_api` field in the request |
| 4 | Wrong password | Admin password (`_pwd`) is incorrect or missing |
| 100 | Invalid arguments | Parameter format error, missing required param, or value out of range |

See [references/errorcode.md](references/errorcode.md) for the full error codes reference.

## CLI Usage

The script can also be run directly from the command line:

```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 \
    --api sys_base_info
```

### CLI Examples

Simple parameter:
```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 \
    --api wifi_get --param dev=2.4G --param tag=1
```

JSON parameter (shell-quoted):
```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 \
    --api interface_operate \
    --param 'op=add' \
    --param 'name=wan3' \
    --param 'info={"mod":"dhcp"}'
```

Pass password on the command line (when not using environment variables):
```bash
python3 scripts/oraybox_http_api.py \
    --host 192.168.1.1 --password admin \
    --api cpu_mem_get
```

See the individual category reference files under `references/` for per-API CLI examples.

## WiFi Configuration Notes

The `wifi_set` API has special compatibility behavior:

1. **New firmware** (`wifi_get` returns `feature` field):
   - Use `encryption` field in `ssid_list`
   - Value must be from `feature.encryptions` list (e.g., `"psk2+ccmp"`)

2. **Older firmware** (`wifi_get` without `feature` field):
   - Use deprecated `encrypt` field in `ssid_list` instead
   - Deprecated fields: `auth`, `encrypt`, `wpa3`

3. **`wifi_set` is OVERWRITING** — always call `wifi_get` first, modify, then submit.
   Missing parameters reset to defaults.

## Notes

- Complex parameters (dicts/lists) are automatically JSON-encoded before sending.
- SSL verification is disabled by default because routers typically use
  self-signed certificates.
- When using `https`, the router may redirect to `http`.
