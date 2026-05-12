# DHCP APIs

APIs in the **DHCP** category.

## APIs in this category

- `dhcp_get` — Get DHCP configuration
- `dhcp_set` — Set DHCP configuration
- `dhcp_bind_get` — Get DHCP static leases
- `dhcp_bind_set` — Set DHCP static leases
- `hosts_get` — Get hosts entries
- `hosts_set` — Set hosts entries

## `dhcp_get`

Get DHCP configuration

### Parameters

> [interface=<iface>] [remove_bind_users=<0|1>] (default: lan)

### Returns

> switch, ip_start, ip_end, rent_time, rent_users[] (mac, ip, name, time, alias)

## `dhcp_set`

Set DHCP configuration

### Parameters

> [op=<add|del|edit>] [interface=<iface>] switch=<0|1> [ip_start=<ip|offset>] [ip_end=<ip>] [limit=<n>] [rent_time=<sec>] [dhcp_option=<json>]

### Returns

> code

## `dhcp_bind_get`

Get DHCP static leases

### Parameters

None

### Returns

> code, data[] (mac, ip, name), arp_sync_switch

## `dhcp_bind_set`

Set DHCP static leases

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | integer | Yes | Operation: 1=add, 2=edit, 3=delete  
(Values: 1 | 2 | 3) |
| `ip` | string | Yes | IP address to bind  
(Format: x.x.x.x) |
| `mac` | string | Yes | MAC address  
(Format: AA:BB:CC:DD:EE:FF) |
| `hostname` | string | No | Device name (required for add/edit) |
| `new_hostname` | string | No | New device name (required for edit) |
| `new_ip` | string | No | New IP address (required for edit)  
(Format: x.x.x.x) |
| `new_mac` | string | No | New MAC address (required for edit)  
(Format: AA:BB:CC:DD:EE:FF) |
| `arp_sync_switch` | integer | No | Enable ARP binding sync with static leases  
(Values: 0 | 1) |

### Returns

> code

## `hosts_get`

Get hosts entries

### Parameters

None

### Returns

> hosts_data[]

## `hosts_set`

Set hosts entries

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hosts_data` | string | Yes | Hosts entries as JSON array string |
| `type` | string | No | Operation: `"0"` = append/replace, other = delete |

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `dhcp_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dhcp_get
```

### `dhcp_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dhcp_set --param switch=1
```

Optional parameters:
- `--param op=<value>`
- `--param interface=<value>`
- `--param ip_start=<value>`
- `--param ip_end=<value>`
- `--param limit=<value>`
- `--param rent_time=<value>`
- `--param 'dhcp_option=<json>'`

### `dhcp_bind_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dhcp_bind_get
```

### `dhcp_bind_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dhcp_bind_set --param op=1
```

Optional parameters:
- `--param hostname=<value>`
- `--param ip=<value>`
- `--param mac=<value>`
- `--param new_hostname=<value>`
- `--param new_ip=<value>`
- `--param new_mac=<value>`
- `--param arp_sync_switch=<value>`

### `hosts_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api hosts_get
```

### `hosts_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api hosts_set --param 'hosts_data=<json_array>'
```
