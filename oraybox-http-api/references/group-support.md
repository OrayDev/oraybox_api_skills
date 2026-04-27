# GROUP_SUPPORT APIs

APIs in the **GROUP_SUPPORT** category.

## APIs in this category

- `group_get` — Get user groups (IP/MAC/DNS/Time groups)
- `group_set` — Set user groups
- `group_reference_get` — Get group reference information
- `group_reference_set` — Delete group references from all rules

## `group_get`

Get user groups (IP/MAC/DNS/Time groups)

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `grp_type` | string | Yes | Group type to query  
(Values: ip | mac | dns | time) |

### Returns

> data[] (name, remark, id, val, use_times, [week, range_val])

### Details

```
Group Types:
    ip    - IP address groups (contains list of IP addresses)
    mac   - MAC address groups (contains list of MAC addresses)
    dns   - DNS domain groups (contains list of domains)
    time  - Time schedule groups (contains time ranges and weekdays)
    
  Response Fields:
    name       - Group name
    remark     - Group description
    id         - Unique group identifier
    val        - Group values (array of IPs/MACs/Domains/Time slots)
    use_times  - Number of rules referencing this group
    week       - For time groups: weekdays (e.g., "Mon,Tue,Wed")
    range_val  - For DNS groups: domain range values
```

## `group_set`

Set user groups

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `optype` | string | Yes | Operation type  
(Values: edit | del | load) |
| `grp_type` | string | Yes | Group type  
(Values: ip | mac | dns | time) |
| `grp_data` | json | No | Group data JSON (for edit/load) |
| `id` | string | No | Group ID (for delete) |
| `merge` | string | No | Merge mode: 1=merge with existing  
(Values: 0 | 1) |

### Returns

> code, [data]

### Details

```
Group Data JSON Format (for edit):
    {
      "id": "<group_id>",           // Group ID (empty or "0" for new group)
      "name": "<group_name>",       // Group name
      "remark": "<description>",    // Group description
      "val": ["<value1>", "<value2>"]  // Array of values
    }
    
  For DNS groups, also include:
      "range_val": ["<range1>"]     // Domain range values
    
  For Time groups, also include:
      "week": "Mon,Tue,Wed",        // Weekdays
      "val": ["09:00-18:00"]        // Time slots
```

## `group_reference_get`

Get group reference information

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `grp_type` | string | Yes | Group type  
(Values: ip | mac | dns | time) |
| `grp_index` | string | Yes | Group ID to query references for |

### Returns

> code, data[] (rule_type, count)

## `group_reference_set`

Delete group references from all rules

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cmd` | string | Yes | Command: del (delete references)  
(Values: del) |
| `grp_type` | string | Yes | Group type |
| `grp_index` | string | Yes | Group ID to remove references for |

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `group_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api group_get --param grp_type=ip
```

### `group_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api group_set --param optype=1 --param grp_type=ip
```

Optional parameters:
- `--param 'grp_data=<json>'`
- `--param id=<value>`
- `--param merge=<value>`

### `group_reference_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api group_reference_get --param grp_type=ip --param grp_index=<value>
```

### `group_reference_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api group_reference_set --param cmd=del --param grp_type=<value> --param grp_index=<value>
```
