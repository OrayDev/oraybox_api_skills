# APP_TRAFFIC APIs

APIs in the **APP_TRAFFIC** category.

## APIs in this category

- `app_traffic_get` — Get application traffic statistics
- `app_traffic_set` — Enable/disable application traffic monitoring
- `app_traffic_upload_get` — Get traffic data upload configuration
- `app_traffic_upload_set` — Set traffic data upload configuration

## `app_traffic_get`

Get application traffic statistics

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dev` | string | Yes | Device IP address or 'all' for all devices |
| `time` | string | Yes | Time range: 24h=last 24 hours, 7d=last 7 days, 1m=last 30 days  
(Values: 24h | 7d | 1m) |

### Returns

> code, data{all, app[](name, up, down, total)}, enable

### Details

```
Application Traffic Statistics:
    Tracks traffic usage per application/protocol
    
  Response Fields:
    enable         - Feature enabled: 0=off, 1=on
    data.all       - Total traffic across all apps (bytes)
    data.app[]     - Array of application traffic data
      name         - Application name (e.g., "HTTP", "HTTPS", "BitTorrent")
      up           - Upload traffic (bytes)
      down         - Download traffic (bytes)
      total        - Total traffic (bytes)
    
  Note:
    Data is sorted by total traffic in descending order
    Requires app_traffic feature to be enabled
    Uses SQLite database for historical data storage
    
  Examples:
    Get all devices traffic for last 24 hours:
      {"_api":"app_traffic_get","dev":"all","time":"24h"}
    
    Get specific device 7-day traffic:
      {"_api":"app_traffic_get","dev":"192.168.1.100","time":"7d"}
    
    Get monthly traffic report:
      {"_api":"app_traffic_get","dev":"all","time":"1m"}
```

## `app_traffic_set`

Enable/disable application traffic monitoring

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enable` | string | Yes | Enable app traffic monitoring: 0=off, 1=on  
(Values: 0 | 1) |

### Returns

> code

### Details

```
Application Traffic Monitoring:
    Controls the application-level traffic monitoring feature
    
  Note:
    Enabling this feature disables flow offloading for accurate per-app tracking
    This may impact routing performance on high-speed connections
    
  Examples:
    Enable monitoring:
      {"_api":"app_traffic_set","enable":"1"}
    
    Disable monitoring:
      {"_api":"app_traffic_set","enable":"0"}
```

## `app_traffic_upload_get`

Get traffic data upload configuration

### Parameters

None

### Returns

> code, enabled, frequency

### Details

```
Traffic Upload Configuration:
    Controls automatic uploading of traffic statistics
    
  Response Fields:
    enabled    - Upload enabled: 0=off, 1=on
    frequency  - Upload frequency: "hour" or "day"
```

## `app_traffic_upload_set`

Set traffic data upload configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enabled` | string | Yes | Enable traffic data upload  
(Values: 0 | 1) |
| `frequency` | string | No | Upload frequency (default: hour)  
(Values: hour | day) |

### Returns

> code

### Details

```
Traffic Data Upload:
    Configure automatic upload of traffic statistics via cron job
    
  Examples:
    Enable hourly upload:
      {"_api":"app_traffic_upload_set","enabled":"1","frequency":"hour"}
    
    Enable daily upload:
      {"_api":"app_traffic_upload_set","enabled":"1","frequency":"day"}
    
    Disable upload:
      {"_api":"app_traffic_upload_set","enabled":"0"}
```

## CLI Examples

Use the script directly from the command line:

### `app_traffic_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api app_traffic_get --param dev=<value> --param time=24h
```

### `app_traffic_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api app_traffic_set --param enable=0
```

### `app_traffic_upload_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api app_traffic_upload_get
```

### `app_traffic_upload_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api app_traffic_upload_set --param enabled=0
```

Optional parameters:
- `--param frequency=<value>`
