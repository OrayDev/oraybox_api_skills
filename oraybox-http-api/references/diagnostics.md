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

> (interface parameter is ignored; always returns full ifconfig)

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

> (host and count parameters are ignored; always pings hard-coded IPs)

### Returns

> code, sn

## CLI Examples

Use the script directly from the command line:

### `dump_ping`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dump_ping --param hostname=<value>
```

Optional parameters:
- `--param interface=<value>`
- `--param resolution=4`
- `--param resolution=6`

### `ping`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ping --param hostname=<value>
```

Optional parameters:
- `--param interface=<value>`

### `dump_traceroute`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dump_traceroute --param hostname=<value>
```

Optional parameters:
- `--param interface=<value>`

### `dump_ifconfig`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dump_ifconfig
```

### `dump_route`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dump_route
```

### `dump_ps`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api dump_ps
```

### `net_test`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api net_test
```
