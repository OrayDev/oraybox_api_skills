# FLOWRATE APIs

APIs in the **FLOWRATE** category.

## APIs in this category

- `flowrate_get` — Get flow rate statistics
- `flowrate_ip_get` — Get flow rate by IP
- `flowrate_wan_get` — Get WAN flow rate

## `flowrate_get`

Get flow rate statistics

### Parameters

None

### Returns

> rates[]

## `flowrate_ip_get`

Get flow rate by IP

### Parameters

> ip=<ip>

### Returns

> rate

## `flowrate_wan_get`

Get WAN flow rate

### Parameters

None

### Returns

> upload, download

## CLI Examples

Use the script directly from the command line:

### `flowrate_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api flowrate_get
```

### `flowrate_ip_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api flowrate_ip_get
```

### `flowrate_wan_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api flowrate_wan_get
```
