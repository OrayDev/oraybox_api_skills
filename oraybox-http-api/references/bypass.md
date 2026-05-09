# BYPASS APIs

APIs in the **BYPASS** category for VPN bypass route management and full bypass configuration.

## APIs in this category

- `bypass_alarm_get` — Get bypass route alarm switch state
- `bypass_alarm_set` — Set bypass route alarm switch
- `vpn_route_get` — Get VPN bypass route table (legacy)
- `vpn_route_get_ex` — Get VPN bypass route table (extended)
- `vpn_route_set` — Add/edit/delete a single VPN bypass route
- `vpn_route_set_ex` — Batch add/edit/delete VPN bypass routes (extended)
- `full_bypass_get` — Get full bypass configuration
- `full_bypass_set` — Set full bypass configuration (switch, add/edit/delete rules)

## `bypass_alarm_get`

Get bypass route alarm switch state.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `enable` | string | Alarm switch: `1`=on, `0`=off |

## `bypass_alarm_set`

Set bypass route alarm switch.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enable` | string | Yes | Alarm switch: `1`=on, `0`=off |

### Returns

> code

## `vpn_route_get`

Get VPN bypass route table (legacy interface). Returns routes whose interface is `oray_vnc`.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page_length` | integer | No | Number of routes per page |
| `page_choose` | integer | No | Page number to retrieve |

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `data` | array | Route entries (see Details) |
| `page_count` | integer | Total pages when pagination is used |

### Details

```
Route entry:
  {
    "target": "192.168.10.0",
    "netmask": "255.255.255.0",
    "gateway": "172.16.1.1",
    "metric": "1"
  }
```

## `vpn_route_get_ex`

Get VPN bypass route table (extended interface). Returns routes with backup gateway and health-check configuration.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `page_length` | integer | No | Number of routes per page |
| `page_choose` | integer | No | Page number to retrieve |

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `data` | array | Route entries (see Details) |
| `page_count` | integer | Total pages when pagination is used |

### Details

```
Route entry (extended):
  {
    "target": "192.168.10.0",
    "netmask": "255.255.255.0",
    "gateway": "172.16.1.1",
    "metric": "1",
    "backup_switch": 0,       // 0=off, 1=on
    "backup_gw_list": [],     // Array of backup gateway IPs
    "check_type": "ping",     // "ping" or "tcp"
    "check_ip": "172.16.1.1", // Health-check target IP
    "check_port": 0           // Required when check_type="tcp"
  }
```

## `vpn_route_set`

Add, edit, or delete a single VPN bypass route. Interface is fixed to `oray_vnc`.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: `1`=add, `2`=edit, `3`=delete |
| `target` | string | Yes | Target network/host IP address |
| `netmask` | string | No | Subnet mask. Empty = host route (255.255.255.255) |
| `gateway` | string | No | Gateway IP address |
| `metric` | string | No | Route metric/priority (default: 1) |

### Returns

> code

### Details

```
Notes:
  - The interface is always "oray_vnc"; do not pass it explicitly.
  - For edit (op=2), target and netmask are used to locate the existing
    route; only gateway and metric can be modified.
  - On X6/V5/G300-ARM devices, routes are also added to/removed from
    the mwan3_connected_v4 ipset.
```

## `vpn_route_set_ex`

Batch add, edit, or delete VPN bypass routes with backup gateway support.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: `1`=add, `2`=edit, `3`=delete |
| `rules` | json_array | Yes | Array of route rule objects (see Details) |

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `results` | array | Operation results per rule, each with an added `result` field (error code) |

### Details

```
Rule object (for add/edit):
  {
    "target": "192.168.88.33",          // Required
    "netmask": "255.255.255.255",       // Optional
    "gateway": "172.41.251.114",        // Optional
    "interface": "oray_vnc",            // Optional, defaults to "oray_vnc"
    "check_type": "tcp",                // "ping" or "tcp", default: "ping"
    "check_ip": "192.168.88.33",        // Health-check target IP
    "check_port": 80,                   // Required when check_type="tcp"
    "backup_switch": 1,                 // 0=off, 1=on
    "backup_gw_list": ["172.41.251.114"] // Array of backup gateway IPs
  }

Rule object (for delete):
  {
    "target": "192.168.88.33",
    "netmask": "255.255.255.255"
  }

Example response:
  {
    "code": 0,
    "results": [
      {
        "target": "192.168.88.33",
        "netmask": "255.255.255.255",
        "gateway": "172.41.251.114",
        "result": 0
      }
    ]
  }
```

## `full_bypass_get`

Get full bypass configuration.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `enabled` | boolean | Full bypass global switch: `true`=on, `false`=off |
| `bypasses` | array | List of bypass rules (see Details) |

### Details

```
Bypass rule entry:
  {
    "src": "192.168.1.100",   // Source IP address (LAN device IP)
    "gate": "172.16.1.1",     // Gateway virtual IP (must be a router member)
    "enabled": true           // Rule enabled: true=on, false=off
  }
```

## `full_bypass_set`

Configure full bypass. Supports global switch and add/edit/delete rules.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: `0`=global switch, `1`=add rule, `2`=edit rule, `3`=delete rule |
| `enabled` | string | No | Enable switch: `1`=on, `0`=off. Required for `op=0`, `op=1`, `op=2` |
| `src` | string | No | Source IP address (LAN device IP). Required for `op=1`, `op=2`, `op=3` |
| `gate` | string | No | Gateway virtual IP (router member virtual IP). Required for `op=1`, `op=2` |

### Returns

> code

### Details

```
Operation notes:
  op=0  — Set global enabled switch only (needs: enabled)
  op=1  — Add a bypass rule (needs: src, gate, enabled)
  op=2  — Edit a bypass rule (needs: src, gate, enabled). src is the key
  op=3  — Delete a bypass rule (needs: src)
```

## CLI Examples

### `bypass_alarm_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api bypass_alarm_get
```

### `bypass_alarm_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api bypass_alarm_set --param enable=1
```

### `vpn_route_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_get
```

Optional parameters:
- `--param page_length=<value>`
- `--param page_choose=<value>`

### `vpn_route_get_ex`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_get_ex
```

Optional parameters:
- `--param page_length=<value>`
- `--param page_choose=<value>`

### `vpn_route_set`

Add a bypass route:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_set --param op=1 --param target=192.168.10.0 --param netmask=255.255.255.0 --param gateway=172.16.1.1
```

Edit a bypass route:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_set --param op=2 --param target=192.168.10.0 --param netmask=255.255.255.0 --param gateway=172.16.1.2
```

Delete a bypass route:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_set --param op=3 --param target=192.168.10.0 --param netmask=255.255.255.0
```

### `vpn_route_set_ex`

Batch add bypass routes:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_set_ex --param op=1 --param 'rules=[{"target":"192.168.10.0","netmask":"255.255.255.0","gateway":"172.16.1.1","backup_switch":1,"backup_gw_list":["172.16.1.2"]}]'
```

Batch delete bypass routes:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_route_set_ex --param op=3 --param 'rules=[{"target":"192.168.10.0","netmask":"255.255.255.0"}]'
```

### `full_bypass_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api full_bypass_get
```

### `full_bypass_set`

Enable/disable full bypass globally:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api full_bypass_set --param op=0 --param enabled=1
```

Add a full bypass rule:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api full_bypass_set --param op=1 --param src=192.168.1.100 --param gate=172.16.1.1 --param enabled=1
```

Edit a full bypass rule:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api full_bypass_set --param op=2 --param src=192.168.1.100 --param gate=172.16.1.2 --param enabled=1
```

Delete a full bypass rule:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api full_bypass_set --param op=3 --param src=192.168.1.100
```
