# TFS APIs

APIs in the **TFS** (Traffic Flow Statistics) category.

## APIs in this category

- `tfs_one_day_get` — Get 24-hour traffic statistics for sub-devices

## `tfs_one_day_get`

Get 24-hour traffic statistics for sub-devices. Returns hourly traffic breakdown or total traffic summary per IP.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `src_ip` | string | No | IP address of the device to query. If omitted, returns statistics for all devices. |
| `total_only` | string | No | Set to `"1"` to return only total traffic per IP (no hourly breakdown). |

### Returns

#### When `total_only=1`

> code, datas[](ip, send_bytes, recv_bytes, [send_bytes_str, recv_bytes_str])

#### Normal mode (hourly breakdown)

> code, datas[](ip, traffic[](time, send_bytes, recv_bytes, [send_bytes_str, recv_bytes_str]))

### Details

```
24-Hour Traffic Flow Statistics:
    Tracks per-device upload/download traffic over the last 24 hours

  Response Fields (total_only=1):
    datas[]        - Array of total traffic per device
      ip           - Device IP address
      send_bytes   - Total upload traffic (bytes), float type
      recv_bytes   - Total download traffic (bytes), float type
      send_bytes_str - Human-readable upload string (SQLite-based implementations only)
      recv_bytes_str - Human-readable download string (SQLite-based implementations only)

  Response Fields (normal mode):
    datas[]        - Array of per-device traffic data
      ip           - Device IP address
      traffic[]    - Hourly traffic breakdown
        time       - Timestamp (HH:MM:SS format)
        send_bytes - Upload traffic for this time slot (bytes), float type
        recv_bytes - Download traffic for this time slot (bytes), float type
        send_bytes_str - Human-readable upload string (SQLite-based implementations only)
        recv_bytes_str - Human-readable download string (SQLite-based implementations only)

  Notes:
    Multicast address 239.255.255.250 is excluded from results

  Examples:
    Get total traffic for all devices:
      {"_api":"tfs_one_day_get","total_only":"1"}

    Get hourly breakdown for a specific device:
      {"_api":"tfs_one_day_get","src_ip":"192.168.1.100"}

    Get hourly breakdown for all devices:
      {"_api":"tfs_one_day_get"}

  Example Response (total_only=1):
    {
      "code": 0,
      "datas": [
        {
          "ip": "192.168.1.100",
          "send_bytes": 123456789.0,
          "recv_bytes": 987654321.0
        }
      ]
    }

  Example Response (normal mode):
    {
      "code": 0,
      "datas": [
        {
          "ip": "192.168.1.100",
          "traffic": [
            {
              "time": "12:00:00",
              "send_bytes": 1024000.0,
              "recv_bytes": 2048000.0
            }
          ]
        }
      ]
    }
```

## CLI Examples

Use the script directly from the command line:

### `tfs_one_day_get` (total only)

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api tfs_one_day_get --param total_only=1
```

### `tfs_one_day_get` (specific device)

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api tfs_one_day_get --param src_ip=192.168.1.100
```

### `tfs_one_day_get` (all devices)

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api tfs_one_day_get
```
