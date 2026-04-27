# DEVICE APIs

APIs in the **DEVICE** category.

## APIs in this category

- `lan_device_get` — Get LAN connected devices
- `lan_device_alias_set` — Set device alias
- `mac_control_get` — Get MAC access control
- `mac_control_set` — Set MAC access control

## `lan_device_get`

Get LAN connected devices

### Parameters

> [version=new|raw]

### Returns

> lan_devs[] (mac, ip, hostname, class(0=wire/1=wifi), alias, ssid, band(0=2.4G/1=5G), signal, tx_rate)

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

None

### Returns

> enable, policy(allow|deny), macs[]

## `mac_control_set`

Set MAC access control

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `switch` | integer | Yes | Enable MAC control: 0=off, 1=on  
(Values: 0 | 1) |
| `allow` | integer | Yes | Policy: 0=deny listed MACs, 1=allow only listed MACs  
(Values: 0 | 1) |
| `mac_addrs` | string | Yes | Pipe-separated MAC addresses (e.g., \ |
| `describe` | string | No | Pipe-separated device descriptions (matching mac_addrs order) |
| `guest_control` | integer | No | Apply to guest WiFi: 0=exclude guest, 1=include guest (default: 0)  
(Values: 0 | 1) |

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `lan_device_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api lan_device_get
```

### `lan_device_alias_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api lan_device_alias_set --param type=1 --param mac=<value>
```

Optional parameters:
- `--param alias=<value>`

### `mac_control_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mac_control_get
```

### `mac_control_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mac_control_set --param switch=1 --param allow=1 --param mac_addrs=<value>
```

Optional parameters:
- `--param describe=<value>`
- `--param guest_control=<value>`
