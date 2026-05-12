# DEVICE APIs

APIs in the **DEVICE** category.

## APIs in this category

- `lan_device_get` — Get LAN connected devices
- `lan_device_alias_set` — Set device alias
- `mac_control_get` — Get MAC access control
- `mac_control_set` — Set MAC access control (batch replace)
- `mac_control_set_ex` — Set MAC access control (fine-grained operations)

## `lan_device_get`

Get LAN connected devices

### Parameters

> [version=new|raw]

### Returns

Without `version` or with an unknown value:
> eth_data[], wifi_data[], wifi5g_data[], guest_wifi_data[] (mac, ip, hostname, class(0=wire/1=wifi), alias, ssid, band(0=2.4G/1=5G), signal, tx_rate)

With `version=new`:
> lan_devs[] (mac, ip, hostname, class(0=wire/1=wifi), alias, ssid, band(0=2.4G/1=5G), signal, tx_rate, rx_bytes, tx_bytes, noise, tx_40mhz, tx_short_gi, rx_short_gi, inactive, tx_mcs, hwmode)

## `lan_device_alias_set`

Set device alias

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `type` | integer | Yes | Operation: 0=add, 1=delete, 2=edit  
(Values: 0 | 1 | 2) |
| `mac` | string | Yes | Device MAC address  
(Format: AA:BB:CC:DD:EE:FF) |
| `alias` | string | No | Custom name/alias (required for add/edit, empty to clear) |

### Returns

> code

## `mac_control_get`

Get MAC access control

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tag` | integer | No | When provided (non-nil), `mac_addrs` is returned as an array of objects |

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `switch` | string | Global enable: `"0"`=off, `"1"`=on |
| `allow` | string | Policy: `"0"`=deny listed MACs, `"1"`=allow only listed MACs |
| `mac_addrs` | array | MAC address list (format depends on `tag`, see below) |
| `describe` | array | Device descriptions (parallel to `mac_addrs`) — present only when `tag` is absent |
| `enabled` | array | Per-rule enable state (parallel to `mac_addrs`) — present only when `tag` is absent |
| `guest_control` | string | Apply to guest WiFi: `"0"`=exclude, `"1"`=include |

**`mac_addrs` format:**
- Without `tag`: plain string array of MAC addresses.
- With `tag`: array of objects, each with `mac`, `describe`, and `enabled` fields.

## `mac_control_set`

Set MAC access control (replaces all existing rules).

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `switch` | string | Yes | Enable MAC control: `"0"`=off, `"1"`=on |
| `allow` | string | Yes | Policy: `"0"`=deny listed MACs, `"1"`=allow only listed MACs |
| `mac_addrs` | string | Yes | Pipe-separated MAC addresses (e.g. `AA:BB:CC:DD:EE:FF\|11:22:33:44:55:66`) |
| `describe` | string | No | Pipe-separated device descriptions (matching `mac_addrs` order) |
| `guest_control` | string | No | Apply to guest WiFi: `"0"`=exclude guest, `"1"`=include guest (default: `"0"`) |

### Returns

> code

## `mac_control_set_ex`

Fine-grained MAC access control operations (add / edit / delete / batch / import).

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `type` | integer | Yes | Operation type (see below)  
(Values: 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7) |
| `switch` | string | Yes | Global enable: `"0"`=off, `"1"`=on (required for `type=0`) |
| `allow` | string | Yes | Policy: `"0"`=deny listed, `"1"`=allow only (required for `type=0`) |
| `mac_addr` | string | No | MAC address for single-record operations (`type=1,2,3`) |
| `describe` | string | No | Device description for single-record operations |
| `enabled` | string | No | Per-rule enable state (`"0"`/`"1"`) for single-record operations |
| `macArr` | JSON string | No | JSON array for batch/import operations (`type=4,5,6,7`). Each element is an object with `mac`, `describe`, and `enabled` fields. |
| `merge` | string | No | Import mode for `type=7`: `"0"`=overwrite, `"1"`=merge (default: `"0"`) |
| `guest_control` | string | No | Apply to guest WiFi: `"0"`=exclude, `"1"`=include (default: `"0"`) |
| `not_restart_net` | integer | No | Set to `1` to skip firewall reload after change |

**`type` values:**

| Value | Operation | Required params |
|-------|-----------|-----------------|
| `0` | Global switch + policy reset | `switch`, `allow` |
| `1` | Add single MAC rule | `mac_addr`, `enabled` |
| `2` | Edit single MAC rule | `mac_addr`, `enabled`, `describe` |
| `3` | Delete single MAC rule | `mac_addr` |
| `4` | Batch delete | `macArr` (array of MAC strings) |
| `5` | Batch enable | `macArr` (array of MAC strings) |
| `6` | Batch disable | `macArr` (array of MAC strings) |
| `7` | Import from file / list | `macArr` (array of objects), `merge` |

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `lan_device_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api lan_device_get
```

### `lan_device_alias_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api lan_device_alias_set --param type=1 --param mac=<value>
```

Optional parameters:
- `--param alias=<value>`

### `mac_control_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api mac_control_get
```

### `mac_control_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api mac_control_set --param switch=1 --param allow=1 --param mac_addrs=<value>
```

Optional parameters:
- `--param describe=<value>`
- `--param guest_control=<value>`

### `mac_control_set_ex`

Add a single MAC rule:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api mac_control_set_ex --param type=1 --param mac_addr=AA:BB:CC:DD:EE:FF --param enabled=1
```

Batch disable:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api mac_control_set_ex --param type=6 --param macArr='["AA:BB:CC:DD:EE:FF","11:22:33:44:55:66"]'
```

Import with overwrite:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api mac_control_set_ex --param type=7 --param switch=1 --param allow=1 --param merge=0 --param macArr='[{"mac":"AA:BB:CC:DD:EE:FF","describe":"Phone","enabled":"1"}]'
```
