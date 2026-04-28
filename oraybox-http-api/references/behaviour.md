# BEHAVIOUR APIs

APIs in the **BEHAVIOUR** category.

## APIs in this category

- `behaviour_get` — Get behaviour management rules
- `behaviour_set` — Set behaviour management rules and user groups
- `behaviour_log_get` — Get HTTP behaviour logs
- `behaviour_log_set` — Enable/disable HTTP log recording
- `behaviour_log_clear` — Clear HTTP behaviour logs

## `behaviour_get`

Get behaviour management rules

### Parameters

None

### Returns

> rules[] (type, ip_group, mac_group, dns_group, time_group)

## `behaviour_set`

Set behaviour management rules and user groups

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `optype` | string | Yes | Operation type: 1=create user group, 2=edit user group, 3=delete user group, 4=edit rules  
(Values: 1 | 2 | 3 | 4) |
| `grp_name` | string | No | Group name (required for optype 1-3) |
| `addr_list` | json_array | No | Address list for user group (required for optype 1-2) |
| `rules` | json_array | No | Behaviour rules JSON array (required for optype 4) |
| `merge` | string | No | Merge mode for user group edit: 1=merge existing, 0=replace  
(Values: 0 | 1) |

### Returns

> code

### Details

```
Behaviour Management Rules:
    Controls network access behaviour based on user groups, time groups, and DNS groups
    
  Rule JSON Format:
    {
      "list_type": "white" or "black",        // White list or black list
      "ip_group": "<group_name>",        // IP group name
      "mac_group": "<group_name>",       // MAC group name (optional)
      "dns_group": "<group_name>",       // DNS group name
      "time_group": "<group_name>"       // Time group name
    }
    
  Examples:
    Create user group:
      {"_api":"behaviour_set","optype":"1","grp_name":"office_users","addr_list":"[\"192.168.1.10\",\"192.168.1.11\"]"}
    
    Edit rules:
      {"_api":"behaviour_set","optype":"4","rules":"[{\\"list_type\\":\\"white\\",\\"ip_group\\":\\"office_users\\",\\"dns_group\\":\\"work_sites\\",\\"time_group\\":\\"work_hours\\"}]"}
```

## SDK Version Differences (17.01 vs 21.02)

`17.01` corresponds to firmware 6.x; `21.02` corresponds to firmware 7.x.

> **Agent Guidance:** Call `sys_base_info` first and check the `ver_main` field to determine the firmware generation. `ver_main` starting with `6` means 6.x / SDK 17.01; starting with `7` means 7.x / SDK 21.02. Use the corresponding parameter format below.

### `behaviour_get`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Top-level** | Returns `user_groups` + `rules` | `user_groups` **removed** |
| **Rule fields** | `weekday`, `address_list`, `user_groups`, `daytime_list[]` | `ip_group`, `mac_group`, `dns_group`, `time_group` |

### `behaviour_set`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Rule fields** | `grp_names`, `visit_list`, `weekday`, `timestart`, `timestop`, `daytime_list` | `ip_group`, `mac_group`, `dns_group`, `time_group`, `list_type` |
| **Validation** | Validates `grp_names`, `visit_list`, `weekday`, `daytime_list` | Validates `ip_group`, `dns_group`, `time_group` |
| **Post-commit** | Restarts behaviour service | Restarts firewall (`restart_firewall(false)`) |
| **User group ops** | Restarts behaviour service on success | Returns success without restarting behaviour |

### `behaviour_log_get`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Log file missing** | Returns `no_target` error | Returns `success` with empty log data |

### `behaviour_log_set`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Side effects** | Restarts behaviour service | Also controls firewall `flow_offloading`: disables when enabling logs, re-enables when disabling logs (if `app_traffic` is also off) |

## `behaviour_log_get`

Get HTTP behaviour logs

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `search` | string | No | Search keyword for filtering logs |
| `time_start` | integer | No | Start timestamp for filtering |
| `time_stop` | integer | No | Stop timestamp for filtering |
| `page_record_count` | integer | No | Records per page (default: 10) |
| `page_seq` | integer | No | Page number (default: 1) |

### Returns

> http_enabled, http_log_file_size, http_log_file_max_size, http_log_total_page_count, http_log[]

## `behaviour_log_set`

Enable/disable HTTP log recording

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `http_enabled` | string | Yes | HTTP log recording: 0=off, 1=on  
(Values: 0 | 1) |

### Returns

> code

## `behaviour_log_clear`

Clear HTTP behaviour logs

### Parameters

None

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `behaviour_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api behaviour_get
```

### `behaviour_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api behaviour_set --param optype=1
```

Optional parameters:
- `--param grp_name=<value>`
- `--param 'addr_list=<json>'`
- `--param 'rules=<json>'`
- `--param merge=<value>`

### `behaviour_log_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api behaviour_log_get
```

Optional parameters:
- `--param search=<value>`
- `--param time_start=<value>`
- `--param time_stop=<value>`
- `--param page_record_count=<value>`
- `--param page_seq=<value>`

### `behaviour_log_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api behaviour_log_set --param http_enabled=1
```

### `behaviour_log_clear`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api behaviour_log_clear
```
