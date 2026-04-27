# TRAFFIC_CONTROL APIs

APIs in the **TRAFFIC_CONTROL** category.

## APIs in this category

- `oraytc_get` — Get traffic control (QoS) configuration
- `oraytc_set` — Set traffic control configuration
- `group_tc_get` — Get group traffic control (QoS) configuration
- `group_tc_set` — Set group traffic control (QoS)

## `oraytc_get`

Get traffic control (QoS) configuration

### Parameters

None

### Returns

> config{base, total_shaping, shaping_list[], group_shaping[], auto_shaping, wan_shaping{}}

### Details

```
Traffic Control Configuration:
    base           - Global switch {enabled}
    total_shaping  - Overall bandwidth limit {enabled, upload, download, vpn_enabled, vpn_upload, vpn_download, ...}
    shaping_list   - Per-IP/Group shaping rules[]
    group_shaping  - Group-based shaping rules[]
    auto_shaping   - Auto-adjustment shaping settings
    wan_shaping    - Per-WAN interface shaping
```

## SDK Version Differences (17.01 vs 21.02)

`17.01` corresponds to firmware 6.x; `21.02` corresponds to firmware 7.x.

> **Agent Guidance:** Call `sys_base_info` first and check the `ver_main` field to determine the firmware generation. `ver_main` starting with `6` means 6.x / SDK 17.01; starting with `7` means 7.x / SDK 21.02. Use the corresponding parameter format below.

### `oraytc_get`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Top-level** | No `wan_shaping` | `wan_shaping` added (object keyed by WAN name) |
| **`auto_shaping`** | No `time_group` | `time_group` added |
| **`shaping_list` items** | `address`, `weekday`, `timestart`, `timestop` | `address`→`ip_group` (fallback), `weekday`/`timestart`/`timestop` **removed**, `combine_shaping` added, `time_group` added |
| **`group_shaping` items** | `enabled`, `upload`, `download`, `upload_max`, `download_max`, `weekday`, `timestart`, `timestop`, `interface`, `priority` | Only `enabled`, `upload`, `download`, `time_group`, `group_name` |

### `oraytc_set`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **New parameter** | — | `wan_shaping` (JSON object keyed by WAN name) |
| **`total_shaping`** | Supports `weekday`, `timestart`, `timestop` | `weekday`/`timestart`/`timestop` **removed**, `time_group` added |
| **`auto_shaping`** | No `time_group` | `time_group` added |
| **Validation** | Requires at least one of `base`, `total`, `shaping`, `auto_shaping` | Also accepts `wan_shaping` |

### `group_tc_get`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Return** | `{code, switch, upload, download}` (same) | Same return structure, but internally no longer reads `upload_max`, `download_max`, `interface`, `priority` |

### `group_tc_set`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **`interface`** | Written to UCI if provided | **No longer persisted** |
| **`priority`** | Written to UCI if provided | **No longer persisted** |

## `oraytc_set`

Set traffic control configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base` | json | No | Base configuration: {enabled: "0\|1"} |
| `total` | json | No | Total shaping config: {enabled, vpn_enabled, upload, download, vpn_upload, vpn_download, ...} |
| `shaping` | json_array | No | Array of shaping rules |
| `auto_shaping` | json | No | Auto shaping configuration |
| `wan_shaping` | json | No | Per-WAN shaping: {wan: {enabled, upload, download, upload_max, download_max}} *(21.02 only)* |

### Returns

> code

### Details

```
Rate Unit Note (IMPORTANT):
    TC (traffic control) uses BITS per second, not BYTES per second!
    This is different from common file transfer speed units.
    
    TC units: bps, kbps (1000 bps), mbps (1000^2 bps)
    Common units: B/s, KB/s (1024 B/s), MB/s (1024^2 B/s)
    
    Conversion:
      1 KB/s (common) = 8 kbps (tc)
      1 MB/s (common) = 8 mbps (tc)
      1000 kbps (tc) = 125 KB/s ≈ 0.125 MB/s
      10 mbps (tc) = 1.25 MB/s
    
    Examples:
      To limit download to 10 MB/s: use "80mbps" or "80000kbps"
      To limit upload to 2 MB/s: use "16mbps" or "16000kbps"
      For 100M broadband (100Mbps): use "100mbps"
  
Shaping Rule JSON Format:
    {
      "enabled": "1",              // Enable this rule
      "upload": "1000kbps",        // Upload bandwidth limit
      "download": "2000kbps",      // Download bandwidth limit
      "upload_max": "1500kbps",    // Max upload burst
      "download_max": "2500kbps",  // Max download burst
      "ip_group": "<group_name>",  // IP group name (if using groups)
      "address": "192.168.1.100",  // Single IP (alternative to ip_group)
      "remark": "Office",
      "time_group": "<group_name>",
      "priority": "1",             // Rule priority
      "interface": "wan",          // Apply to interface
      "combine_shaping": "1"       // Combine with other rules
    }
    
Total Shaping Fields:
    enabled              - Master switch
    upload/download      - Total bandwidth limits
    vpn_enabled          - Enable VPN traffic shaping
    vpn_upload/vpn_download - VPN bandwidth limits
    remainder_upload/remainder_download - Remainder bandwidth
    time_group           - Time-based control
    
Examples:
    Enable traffic control:
      {"_api":"oraytc_set","base":"{\\"enabled\\":\\"1\\"}"}
    
    Set total shaping (100M broadband):
      {"_api":"oraytc_set","total":"{\\"enabled\\":\\"1\\",\\"upload\\":\\"20mbps\\",\\"download\\":\\"100mbps\\"}"}
    
    Set shaping rules (limit to ~1MB/s download):
      {"_api":"oraytc_set","shaping":"[{\\"enabled\\":\\"1\\",\\"upload\\":\\"1000kbps\\",\\"download\\":\\"8000kbps\\",\\"address\\":\\"192.168.1.100\\",\\"remark\\":\\"User1\\"}]"}
```

## `group_tc_get`

Get group traffic control (QoS) configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `grp_name` | string | Yes | Group name to query |

### Returns

> code, switch, upload, download

## `group_tc_set`

Set group traffic control (QoS)

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `optype` | string | Yes | Operation: 1=create, 2=edit, 3=delete  
(Values: 1 | 2 | 3) |
| `grp_name` | string | Yes | Group name |
| `switch` | string | No | Enable this group QoS  
(Values: 0 | 1) |
| `upload` | string | No | Upload rate limit (e.g., 1000kbps, 1mbps) |
| `download` | string | No | Download rate limit (e.g., 2000kbps, 2mbps) |
| `upload_max` | string | No | Max upload burst rate |
| `download_max` | string | No | Max download burst rate |
| `combine_shaping` | string | No | Combine with other shaping rules  
(Values: 0 | 1) |
| `weekday` | string | No | Weekdays (e.g., Mon,Tue,Wed,Thu,Fri) |
| `timestart` | string | No | Start time (HH:MM) |
| `timestop` | string | No | Stop time (HH:MM) |

### Returns

> code

### Details

```
Group Traffic Control:
    Apply QoS rules to entire user groups
    
Rate Unit Note (IMPORTANT):
    TC (traffic control) uses BITS per second, not BYTES per second!
    This is different from common file transfer speed units.
    
    TC units: bps, kbps (1000 bps), mbps (1000^2 bps)
    Common units: B/s, KB/s (1024 B/s), MB/s (1024^2 B/s)
    
    Conversion:
      1 KB/s (common) = 8 kbps (tc)
      1 MB/s (common) = 8 mbps (tc)
      1000 kbps (tc) = 125 KB/s ≈ 0.125 MB/s
      10 mbps (tc) = 1.25 MB/s
    
    Examples:
      To limit download to 10 MB/s: use "80mbps" or "80000kbps"
      To limit upload to 2 MB/s: use "16mbps" or "16000kbps"
      For 100M broadband (100Mbps): use "100mbps"
    
Rate Format:
    Numeric values with units: kbps, mbps (e.g., "1000kbps", "10mbps")
    
Time Format:
    timestart/timestop: "HH:MM" format (24-hour)
    weekday: Comma-separated day names (Mon,Tue,Wed,Thu,Fri,Sat,Sun)
    
Examples:
    Create group QoS (limit to ~2.5MB/s down, ~1MB/s up):
      {"_api":"group_tc_set","optype":"1","grp_name":"office_users","switch":"1","upload":"8000kbps","download":"20000kbps"}
    
    Delete group QoS:
      {"_api":"group_tc_set","optype":"3","grp_name":"office_users"}
```

## CLI Examples

Use the script directly from the command line:

### `oraytc_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api oraytc_get
```

### `oraytc_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api oraytc_set
```

Optional parameters:
- `--param 'base=<json>'`
- `--param 'total=<json>'`
- `--param 'shaping=<json_array>'`
- `--param 'auto_shaping=<json>'`
- `--param 'wan_shaping=<json>'` (21.02 only)

### `group_tc_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api group_tc_get --param grp_name=<value>
```

### `group_tc_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api group_tc_set --param optype=1 --param grp_name=<value>
```

Optional parameters:
- `--param switch=<value>`
- `--param upload=<value>`
- `--param download=<value>`
- `--param upload_max=<value>`
- `--param download_max=<value>`
- `--param combine_shaping=<value>`
- `--param weekday=<value>`
- `--param timestart=<value>`
- `--param timestop=<value>`
