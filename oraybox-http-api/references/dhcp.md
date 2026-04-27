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

> switch, ip_start, ip_end, rent_time, rent_users[] (mac, ip, hostname, time, alias)

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

> leases[] (mac, ip, name)

## `dhcp_bind_set`

Set DHCP static leases

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | integer | Yes | Operation: 1=add, 2=edit, 3=delete  
(Values: 1 | 2 | 3) |
| `hostname` | string | No | Device name (required for add/edit) |
| `ip` | string | No | IP address to bind (required for add/edit/delete)  
(Format: x.x.x.x) |
| `mac` | string | No | MAC address (required for add/edit/delete)  
(Format: AA:BB:CC:DD:EE:FF) |
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

> hosts[]

## `hosts_set`

Set hosts entries

### Parameters

> hosts=<json_array>

### Returns

> code
