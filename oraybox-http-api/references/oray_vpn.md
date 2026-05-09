# ORAY VPN APIs

APIs in the **ORAY VPN** category for Oray intelligent networking (智能组网) configuration, status monitoring, and access control.

## APIs in this category

- `vpn_get` — Get VPN status, version, and member list
- `vpn_set` — Set VPN parameters
- `vpn_visitors_get` — Get VPN visitor access control list
- `vpn_visitors_set` — Set VPN visitor access control (add/edit/delete)
- `vpn_reboot_get` — Get scheduled VPN service reboot configuration
- `vpn_reboot_set` — Set scheduled VPN service reboot configuration
- `vpn_p2p_port_get` — Get fixed P2P port setting
- `vpn_p2p_port_set` — Set fixed P2P port
- `vpn_forward_get` — Get per-LAN-interface VPN forwarding status
- `vpn_forward_set` — Enable/disable VPN forwarding for a LAN interface
- `bridge_forward` — Get/set bridge layer-2 forwarding mask
- `dump_vpn_dbginfo` — Dump VPN debug information from log

## `vpn_get`

Get VPN status, version, configuration, and network member list.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filter` | json | No | Filter conditions for member list. Example: `{"dev_type":0, "is_online":1, "search_key":"", "command":["match,sn,^P"]}` |
| `page_length` | integer | No | Number of members per page |
| `page_choose` | integer | No | Page number to retrieve |
| `initiative` | integer | No | If `1` and `sn` is provided, fetches initiative data list from cloud API instead of local status |
| `sn` | string | No | Device SN, required when `initiative=1` |

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `version` | string | VPN client version |
| `connect_status` | string | Connection state: `connected`, `tryconnect`, or `disconnect` |
| `encrypt` | string | Encryption enabled: `1`=on, `0`=off |
| `natmask` | string | NAT masquerade enabled: `1`=on, `0`=off |
| `udpproxy` | string | UDP proxy (PnP) enabled: `1`=on, `0`=off |
| `mlink` | string | Smart link enabled: `1`=on, `0`=off |
| `accelerate` | string | Kernel acceleration enabled: `1`=on, `0`=off |
| `no_conflict_route` | string | Anti-172-conflict route enabled: `1`=on, `0`=off |
| `status` | object | VPN status object (see Details) |
| `members_total` | integer | Total number of members after filtering |
| `speed_total` | object | Aggregated speed statistics (see Details) |
| `page_count` | integer | Total pages when pagination is used |

### Details

```
Status object structure:
  {
    "connections": [
      {
        "ID": 5388424,       // Group/connection ID
        "type": 0,           // Group type: 0=peer, 1=hub-spoke, 2=gateway
        "name": "group_name",
        "owner_mbr_id": 123, // Self member ID in this group
        "members": [
          {
            "ID": 123,
            "name": "device_name",
            "type": 0,         // Member type: 0=normal, 1=center, 2=branch
            "ip": "172.16.1.1",       // Virtual IP
            "lan_ip": "192.168.1.1",  // Local LAN IP
            "lan_mask": "255.255.255.0",
            "connect_type": "p2p",    // "p2p", "transfer", "vpn tcp forward", ...
            "dev_type": 0,     // 0=router, 1=visitor client
            "sn": "912345678721",     // Device SN
            "nat_type": 4,     // NAT type
            "is_online": 1,
            "is_owner": 1,
            "link_diagnosis": {      // Link quality diagnosis
              "total_ping_count": 0,
              "lose_ping_count": 0
            },
            "p2p_recv_speed": 0,
            "p2p_send_speed": 0,
            "p2p_recv": 0,
            "p2p_send": 0,
            "trans_recv_speed": 0,
            "trans_send_speed": 0,
            "trans_recv": 0,
            "trans_send": 0
          }
        ]
      }
    ]
  }

Speed total object:
  {
    "trans_send": 0,
    "trans_send_speed": 0,
    "trans_recv": 0,
    "trans_recv_speed": 0,
    "p2p_send": 0,
    "p2p_send_speed": 0,
    "p2p_recv": 0,
    "p2p_recv_speed": 0
  }

Filter JSON format:
  {
    "dev_type": 0,          // Filter by device type (0=router, 1=visitor)
    "is_online": 1,         // Filter by online status
    "search_key": "name",   // Search in name, ip, or lan_ip
    "command": ["match,sn,^P"]  // Pattern match command: match,<field>,<pattern>
  }
```

## `vpn_set`

Set VPN parameters. Changes take effect after restarting the VPN service.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `encrypt` | string | No | Enable encryption: `1`=on, `0`=off |
| `udpproxy` | string | No | Enable UDP proxy (PnP): `1`=on, `0`=off |
| `natmask` | string | No | Enable NAT masquerade: `1`=on, `0`=off |
| `mlink` | string | No | Enable smart link: `1`=on, `0`=off |
| `accelerate` | string | No | Enable kernel acceleration: `1`=on, `0`=off |
| `no_conflict_route` | string | No | Enable anti-172-conflict route: `1`=on, `0`=off |

### Returns

> code

## `vpn_visitors_get`

Get VPN visitor access control configuration.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `switch` | boolean | Access control enabled: `true`=on, `false`=off |
| `action` | string | Default action: `accept` or `refuse` |
| `visitors` | array | List of visitor entries (see Details) |

### Details

```
Visitor entry:
  {
    "name": "DeviceName",   // Host name (or alias if set)
    "ip": "192.168.1.100",  // Host IP address
    "mac": "aa:bb:cc:dd:ee:ff"  // Host MAC address
  }

Action semantics:
  accept  — Members in the list are blocked; members NOT in the list are allowed
  refuse  — Members in the list are allowed; members NOT in the list are blocked
```

## `vpn_visitors_set`

Configure VPN visitor access control. Supports enabling/disabling the feature and adding, editing, or deleting visitor entries.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `switch` | string | No | Enable access control: `1`=on, `0`=off. Required when setting base config |
| `action` | string | No | Default action: `accept` or `refuse`. Required when setting base config |
| `op` | string | No | Operation: `1`=add, `2`=edit, `3`=delete |
| `name` | string | No | Host name. Required when `op` is 1, 2, or 3 |
| `ip` | string | No | Host IP address. Required when `op` is 1, 2, or 3 |
| `mac` | string | No | Host MAC address. Required when `op` is 1, 2, or 3 |

### Returns

> code

## `vpn_reboot_get`

Get scheduled VPN service reboot configuration.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `enabled` | string | Scheduled reboot enabled: `1`=on, `0`=off |
| `hour` | string | Hour (0–23) |
| `minute` | string | Minute (0–59) |
| `day` | string | Day of month (1–31), `0` means every day. **Only present when `enabled=1`** |
| `month` | string | Month (1–12), `0` means every month. **Only present when `enabled=1`** |
| `week` | string | Week days as JSON array string, e.g. `[1,2,3,4,5,6,0]`. `0`=Sunday. **Only present when `enabled=1`** |

## `vpn_reboot_set`

Set scheduled VPN service reboot. Uses crontab to schedule `restart_service` for the VPN.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enabled` | string | Yes | Enable scheduled reboot: `1`=on, `0`=off |
| `hour` | integer | No | Hour (0–23). Required when `enabled=1` |
| `minute` | integer | No | Minute (0–59). Required when `enabled=1` |
| `day` | integer | No | Day of month (1–31), `0` means every day |
| `month` | integer | No | Month (1–12), `0` means every month |
| `week` | string | No | Week days as JSON array string, e.g. `"[1,2,3,4,5]"`. `0`=Sunday, `*` means every day |

### Returns

> code

## `vpn_p2p_port_get`

Get the configured fixed P2P port.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `p2p_port` | string | Fixed P2P port number. Empty string means random port |

## `vpn_p2p_port_set`

Set a fixed P2P port for VPN. Setting an empty value restores random port allocation.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `p2p_port` | string | No | Fixed P2P port (15111–16000). Empty or omitted for random port |

### Returns

> code

## `vpn_forward_get`

Get VPN forwarding status for LAN interfaces.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `iface` | string | No | Interface name (e.g., `lan`, `lan2`). If omitted, returns status for all LAN interfaces |

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `forward` | object | Forwarding status object. Per-interface object with `enabled` field, or single `enabled` value when `iface` is specified |

### Details

```
Response when iface is omitted:
  {
    "lan": {"enabled": "1"},
    "lan2": {"enabled": "0"}
  }

Response when iface="lan":
  {
    "enabled": "1"
  }
```

## `vpn_forward_set`

Enable or disable VPN forwarding for a specific LAN interface.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `iface` | string | Yes | Interface name (e.g., `lan`, `lan2`) |
| `enabled` | string | No | Enable VPN forwarding: `1`=on, `0`=off (default: `0`) |

### Returns

> code

## `bridge_forward`

Get or set bridge layer-2 forwarding mask. Controls whether the bridge forwards special layer-2 frames.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | string | Yes | Operation: `get` or `set` |
| `enable` | string | No | Enable forwarding: `1`=on, `0`=off. Required when `action=set` |

### Returns

When `action=get`:

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `enable` | string | Forwarding state: `1`=on, `0`=off |

When `action=set`:

> code

## `dump_vpn_dbginfo`

Dump VPN debug information from the log file. Sends USR1 signal to the running orayboxvpn process and extracts the latest debug block from `/var/log/oraybox/OrayBoxVpn.log`.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `data` | string | Debug information text block |

## CLI Examples

### `vpn_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_get
```

Optional parameters:
- `--param 'filter=<json>'`
- `--param page_length=<value>`
- `--param page_choose=<value>`

### `vpn_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_set --param encrypt=1 --param udpproxy=0
```

Optional parameters:
- `--param natmask=<value>`
- `--param mlink=<value>`
- `--param accelerate=<value>`
- `--param no_conflict_route=<value>`

### `vpn_visitors_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_visitors_get
```

### `vpn_visitors_set`

Enable access control and add a visitor:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_visitors_set --param switch=1 --param action=refuse --param op=1 --param name=Device1 --param ip=192.168.1.100 --param mac=aa:bb:cc:dd:ee:ff
```

Delete a visitor:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_visitors_set --param op=3 --param name=Device1 --param ip=192.168.1.100 --param mac=aa:bb:cc:dd:ee:ff
```

### `vpn_reboot_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_reboot_get
```

### `vpn_reboot_set`

Enable daily reboot at 03:30:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_reboot_set --param enabled=1 --param hour=3 --param minute=30 --param day=0 --param month=0 --param week='*'
```

Disable scheduled reboot:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_reboot_set --param enabled=0
```

### `vpn_p2p_port_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_p2p_port_get
```

### `vpn_p2p_port_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_p2p_port_set --param p2p_port=15111
```

To use random port:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_p2p_port_set
```

### `vpn_forward_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_forward_get
```

Optional parameters:
- `--param iface=<value>`

### `vpn_forward_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api vpn_forward_set --param iface=lan --param enabled=1
```

### `bridge_forward`

Get current state:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api bridge_forward --param action=get
```

Enable:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api bridge_forward --param action=set --param enable=1
```

### `dump_vpn_dbginfo`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dump_vpn_dbginfo
```
