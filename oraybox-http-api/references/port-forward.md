# PORT_FORWARD APIs

APIs in the **PORT_FORWARD** category.

## APIs in this category

- `port_map_get` — Get port mapping rules
- `port_map_add` — Add port mapping rule
- `port_map_delete` — Delete port mapping rule
- `ip_bind_get` — Get IP-MAC binding
- `ip_bind_set` — Set IP-MAC binding

## `port_map_get`

Get port mapping rules

### Parameters

> [page_length=<n>] [page_choose=<n>]

### Returns

> data[](enabled, hostname, wan_name, src_port, dest_ip, dest_port, proto), page_count

## `port_map_add`

Add port mapping rule

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hostname` | string | Yes | Rule name/description |
| `proto` | string | Yes | Protocol(s) to forward  
(Values: tcp | udp | tcp udp) |
| `dest_ip` | string | Yes | Destination IP address (internal host)  
(Format: x.x.x.x) |
| `dest_port` | integer | Yes | Destination port number  
(Range: 1-65535) |
| `src_port` | integer | No | External/WAN port (defaults to dest_port if not specified)  
(Range: 1-65535) |
| `wan_name` | string | No | WAN interface name to apply rule on (default: wan) |
| `enabled` | integer | No | Enable this rule: 0=disabled, 1=enabled (default: 1 if not specified)  
(Values: 0 | 1) |
| `map_list` | json_array | No | Batch port mappings for multiple rules |
| `not_restart_net` | integer | No | Skip firewall restart: 0=restart, 1=skip  
(Values: 0 | 1) |

### Returns

> code

## `port_map_delete`

Delete port mapping rule

### Parameters

> dest_ip=<ip> dest_port=<port> proto=<tcp|udp|tcp udp> [wan_name=<wan>] [hostname=<name>] [src_port=<port>] [map_list=<json>] [not_restart_net=<0|1>]

### Returns

> code

## `ip_bind_get`

Get IP-MAC binding

### Parameters

None

### Returns

> arp_list[] (host, grp_name, dev, attribute), dhcp_sync_switch

## `ip_bind_set`

Set IP-MAC binding

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | integer | Yes | Operation: 1=add, 2=delete, 3=modify  
(Values: 1 | 2 | 3) |
| `host` | string | No | Device name |
| `ip` | string | No | IP address to bind  
(Format: x.x.x.x) |
| `mac` | string | No | MAC address  
(Format: AA:BB:CC:DD:EE:FF) |
| `dev` | string | No | Device/interface |
| `attribute` | string | No | Attribute flag |
| `grp_name` | string | No | Group name |
| `old_ip` | string | No | Old IP address (for modify)  
(Format: x.x.x.x) |
| `old_mac` | string | No | Old MAC address (for modify)  
(Format: AA:BB:CC:DD:EE:FF) |
| `old_dev` | string | No | Old device/interface (for modify) |
| `dhcp_sync_switch` | integer | No | Enable DHCP sync with static leases  
(Values: 0 | 1) |
| `batch` | json_array | No | Batch operations (JSON array) |

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `port_map_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api port_map_get
```

### `port_map_add`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api port_map_add --param hostname=<value> --param proto=tcp --param dest_ip=<value> --param dest_port=1
```

Optional parameters:
- `--param src_port=<value>`
- `--param wan_name=<value>`
- `--param enabled=<value>`
- `--param 'map_list=<json>'`
- `--param not_restart_net=<value>`

### `port_map_delete`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api port_map_delete --param dest_ip=<value> --param dest_port=<value> --param proto=tcp
```

Optional parameters:
- `--param wan_name=<value>`
- `--param hostname=<value>`
- `--param src_port=<value>`
- `--param 'map_list=<json>'`
- `--param not_restart_net=<value>`

### `ip_bind_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ip_bind_get
```

### `ip_bind_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ip_bind_set --param op=1
```

Optional parameters:
- `--param host=<value>`
- `--param ip=<value>`
- `--param mac=<value>`
- `--param dev=<value>`
- `--param attribute=<value>`
- `--param grp_name=<value>`
- `--param old_ip=<value>`
- `--param old_mac=<value>`
- `--param old_dev=<value>`
- `--param dhcp_sync_switch=<value>`
- `--param 'batch=<json>'`
