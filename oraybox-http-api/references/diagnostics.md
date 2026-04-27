# DIAGNOSTICS APIs

APIs in the **DIAGNOSTICS** category.

## APIs in this category

- `dump_ping` — Execute ping test
- `ping` — Simple ping test
- `dump_traceroute` — Execute traceroute
- `dump_ifconfig` — Get interface config
- `dump_route` — Get routing table
- `dump_ps` — Get process list
- `net_test` — Test network connectivity

## `dump_ping`

Execute ping test

### Parameters

> hostname=<host> [interface=<iface>] [resolution=4|6]

### Returns

> code, data

## `ping`

Simple ping test

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hostname` | string | Yes | Target host to ping |
| `interface` | string | No | Source interface for ping |

### Returns

> code, sn

## `dump_traceroute`

Execute traceroute

### Parameters

> hostname=<host> [interface=<iface>]

### Returns

> code, data

## `dump_ifconfig`

Get interface config

### Parameters

> [interface=<iface>]

### Returns

> code, data

## `dump_route`

Get routing table

### Parameters

None

### Returns

> code, data

## `dump_ps`

Get process list

### Parameters

None

### Returns

> code, data

## `net_test`

Test network connectivity

### Parameters

> [host=<host>] [count=<n>]

### Returns

> result
