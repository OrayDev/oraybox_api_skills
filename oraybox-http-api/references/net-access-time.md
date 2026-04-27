# NET_ACCESS_TIME APIs

APIs for controlling network access time scheduling.

> **Note:** These APIs are not included in the main `exec_api.lua` documentation. They exist in the `net_access_time` package which has separate implementations for OpenWrt SDK 17.01 (firmware 6.x) and 21.02 (firmware 7.x).

## APIs in this category

- `net_access_time_get` — Get network access time rules
- `net_access_time_set` — Set network access time rules

## `net_access_time_get`

Get network access time rules

### Parameters

None

### Returns

> rules[] (enabled, idx, ...)

### SDK Version Differences (17.01 vs 21.02)

`17.01` corresponds to firmware 6.x; `21.02` corresponds to firmware 7.x.

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Rule fields** | `enabled`, `idx`, `weekday`, `group_name`, `timestart`, `timestop` | `enabled`, `idx`, `ip_group`, `time_group` |
| **Time model** | Inline time definition | Group reference (`time_group`) |
| **User model** | Inline group name (`group_name`) | Group reference (`ip_group`) |

## `net_access_time_set`

Set network access time rules

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: 1=add, 2=delete, 3=modify, 4=stop(disable), 5=start(enable), 6=raise priority, 7=lower priority |
| `rules` | json_array | No | Rules array for batch operations (op=1,2,4,5) |
| `rule` | json | No | Single rule for modify/priority operations (op=3,6,7) |

### Returns

> code

### SDK Version Differences (17.01 vs 21.02)

`17.01` corresponds to firmware 6.x; `21.02` corresponds to firmware 7.x.

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Add/Modify fields** | `group_name`, `weekday`, `timestart`, `timestop`, `enabled` | `time_group`, `ip_group`, `enabled` |
| **Group validation** | `check_group_name()` + UCI existence check | Removed entirely |
| **Weekday validation** | `check_weekday()` | Removed |
| **Time validation** | `check_timestartstop()` | Removed |
| **New param validation** | — | Only `time_group` presence checked |
| **Shell injection filter** | Keys: `group_name`, `weekday`, `timestart`, `timestop` | Same keys (stale, does not cover `ip_group`/`time_group`) |
| **No-change ops** | Delete(2), Stop(4), Start(5), Raise(6), Reduce(7) | Same |

## CLI Examples

### `net_access_time_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api net_access_time_get
```

### `net_access_time_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api net_access_time_set --param op=1
```

Optional parameters:
- `--param 'rules=<json>'`
- `--param 'rule=<json>'`
