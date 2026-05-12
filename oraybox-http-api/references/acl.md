# ACL APIs

APIs in the **ACL** category.

## APIs in this category

- `acl_get` — Get ACL (Access Control List) rules
- `acl_set` — Set ACL rules

## `acl_get`

Get ACL (Access Control List) rules

### Parameters

None

### Returns

> 17.01: `rules[]` (`type`, `weekday`, `src_grp_names`, `dst_grp_names`, `src_list`, `dst_list`, `daytime_list[]`, `traffic_type`, `support_traffic_type`)
> 21.02: `rules[]` (`type`, `time_group`, `src_ip_group`, `dst_ip_group`, `src_port`, `dst_port`, `proto`, `action`, `input`, `output`, `enabled`, `idx`, `priority`)

## `acl_set`

Set ACL rules

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: 1=add, 2=delete, 3=modify, 4=stop(disable), 5=start(enable), 6=raise priority, 7=lower priority  
(Values: 1 | 2 | 3 | 4 | 5 | 6 | 7) |
| `rules` | json_array | No | Rules array for batch operations (op=1,2,4,5) |
| `rule` | json | No | Single rule for modify/priority operations (op=3,6,7) |

### Returns

> code

### Details

```
ACL Rule JSON Format (21.02):
    {
      "class": "base",                   // Rule class (default: base)
      "src_ip_group": "<group_name>",    // Source IP group name
      "dst_ip_group": "<group_name>",    // Destination IP group name
      "src_port": "<port|range>",        // Source port (number or range like "1000-2000")
      "dst_port": "<port|range>",        // Destination port
      "time_group": "<group_name>",      // Time group name
      "proto": "all|tcp|udp|icmp|gre",   // Protocol
      "action": "accept|drop",           // Action
      "input": "<interface>",            // Input interface (e.g., wan, lan)
      "output": "<interface>",           // Output interface
      "enabled": 1,                      // Enable rule: 0=disabled, 1=enabled
      "priority": 10                     // Rule priority (higher = higher priority)
    }

  17.01 Rule JSON Format:
    {
      "class": "base",
      "src_grp_names": "group1,group2",  // Source group names
      "dst_grp_names": "group1,group2",  // Destination group names
      "src_list": "192.168.1.0/24",      // Source IP list
      "dst_list": "10.0.0.0/24",         // Destination IP list
      "weekday": "Mon,Tue,Wed,Thu,Fri",  // Weekdays
      "daytime_list": ["09:00-18:00"],   // Daytime list
      "traffic_type": "input|output|forward",  // Traffic type
      "proto": "all|tcp|udp|icmp|gre",
      "action": "accept|drop",
      "enabled": 1,
      "priority": 10
    }
    
  Examples:
    Add rules:
      {"_api":"acl_set","op":"1","rules":"[{\\"src_ip_group\\":\\"lan_users\\",\\"dst_ip_group\\":\\"internet\\",\\"proto\\":\\"tcp\\",\\"action\\":\\"accept\\",\\"enabled\\":1}]"}
    
    Delete rules:
      {"_api":"acl_set","op":"2","rules":"[{\\"idx\\":1},{\\"idx\\":2}]"}
    
    Modify rule:
      {"_api":"acl_set","op":"3","rule":"{\\"idx\\":1,\\"action\\":\\"drop\\",\\"enabled\\":0}"}
```

## SDK Version Differences (17.01 vs 21.02)

`17.01` corresponds to firmware 6.x; `21.02` corresponds to firmware 7.x.

> **Agent Guidance:** Call `sys_base_info` first and check the `ver_main` field to determine the firmware generation. `ver_main` starting with `6` means 6.x / SDK 17.01; starting with `7` means 7.x / SDK 21.02. Use the corresponding parameter format below.

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Source group** | `src_grp_names` (optional, validated) | `src_ip_group` (required) |
| **Dest group** | `dst_grp_names` (optional, validated) | `dst_ip_group` (required) |
| **Source IPs** | `src_list` (optional) | **Removed** |
| **Dest IPs** | `dst_list` (optional) | **Removed** |
| **Time** | `weekday` + `daytime_list` | `time_group` (required) |
| **Traffic type** | `traffic_type` (optional, `input`/`output`/`forward`) | **Removed** |
| **Priority change** | Calls shell scripts (`acl_raise.sh` / `acl_reduce.sh`) | Restarts firewall |
| **`acl_get` returns** | `weekday`, `src_grp_names`, `dst_grp_names`, `src_list`, `dst_list`, `daytime_list`, `traffic_type`, `support_traffic_type` | `src_ip_group`, `dst_ip_group`, `time_group` |

## CLI Examples

Use the script directly from the command line:

### `acl_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api acl_get
```

### `acl_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api acl_set --param op=1
```

Optional parameters:
- `--param 'rules=<json>'`
- `--param 'rule=<json>'`
