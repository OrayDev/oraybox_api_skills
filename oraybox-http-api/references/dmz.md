# DMZ APIs

APIs in the **DMZ** category.

## APIs in this category

- `dmz_get` — Get DMZ configuration (legacy)
- `dmz_get_ex` — Get extended DMZ configuration
- `dmz_set` — Set DMZ configuration

## `dmz_get`

Get DMZ configuration (legacy)

### Parameters

None

### Returns

> code, {wan: {ip, enable}, wan2: {ip, enable}, oray_vnc: {ip, enable}}

## `dmz_get_ex`

Get extended DMZ configuration

### Parameters

None

### Returns

> code, {wan: {ip, enable}, wan2: {ip, enable}, oray_vnc: {ip, enable}, ...}

### Details

```
DMZ Configuration:
    Exposes all ports of a LAN device to the WAN
    
  Response Fields:
    Nested per-interface objects, e.g. {wan: {ip, enable}, wan2: {ip, enable}, oray_vnc: {ip, enable}}
    Each interface key maps to an object with `ip` and `enable` fields.
```

## `dmz_set`

Set DMZ configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `wan_name` | string | No | WAN interface name (e.g., wan, wan2) or 'oray_vnc' for VPN (default: wan) |
| `dest_ip` | string | No | LAN IP address for DMZ host  
(Format: x.x.x.x) |
| `enable` | string | No | Enable DMZ (string boolean)  
(Values: true | false) |
| `enabled` | string | No | Enable DMZ (0=off, 1=on) - alternative to enable  
(Values: 0 | 1) |

### Returns

> code

### Details

```
DMZ (Demilitarized Zone):
    Forwards all external ports to a specific internal host
    
  Note:
    Use with caution - exposes the entire host to the internet
    Port forwarding rules take precedence over DMZ
    
  Examples:
    Enable DMZ for primary WAN:
      {"_api":"dmz_set","wan_name":"wan","dest_ip":"192.168.1.100","enable":"true"}
    
    Enable DMZ for secondary WAN:
      {"_api":"dmz_set","wan_name":"wan2","dest_ip":"192.168.1.101","enabled":"1"}
    
    Disable DMZ:
      {"_api":"dmz_set","wan_name":"wan","enable":"false"}
```

## CLI Examples

Use the script directly from the command line:

### `dmz_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dmz_get
```

### `dmz_get_ex`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dmz_get_ex
```

### `dmz_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dmz_set --param wan_name=<value>
```

Optional parameters:
- `--param dest_ip=<value>`
- `--param enable=<value>`
- `--param enabled=<value>`
