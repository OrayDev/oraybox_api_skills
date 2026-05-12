# FLOWRATE APIs

APIs in the **FLOWRATE** category.

## APIs in this category

- `flowrate_get` — Get flow rate statistics
- `flowrate_ip_get` — Get flow rate by IP
- `flowrate_wan_get` — Get WAN flow rate

## `flowrate_get`

Get flow rate statistics

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dimension` | string | No | Dimension to query: "iface" or "ip" |
| `iface_list` | string | No | Interface list to query (default: "wan") |
| `ip_list` | string | No | IP list to query (when dimension="ip") |

### Returns

> code, data[] (iface, down, up)

## `flowrate_ip_get`

Get flow rate by IP

### Parameters

None

### Returns

> code, lan_data[] (ip, down, up)

## `flowrate_wan_get`

Get WAN flow rate

### Parameters

None

### Returns

> wifi_up, wifi_down, lan_up, lan_down, has_eth, has_wifi, plus dynamic per-WAN fields (<wan_name>_up, <wan_name>_down)

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
