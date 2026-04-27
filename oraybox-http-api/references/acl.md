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

> rules[] (type, time_group, src_ip_group, dst_ip_group, src_port, dst_port, proto, action, input, output, enabled, idx, priority)

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
ACL Rule JSON Format:
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
    
  Examples:
    Add rules:
      {"_api":"acl_set","op":"1","rules":"[{\\"src_ip_group\\":\\"lan_users\\",\\"dst_ip_group\\":\\"internet\\",\\"proto\\":\\"tcp\\",\\"action\\":\\"accept\\",\\"enabled\\":1}]"}
    
    Delete rules:
      {"_api":"acl_set","op":"2","rules":"[{\\"idx\\":1},{\\"idx\\":2}]"}
    
    Modify rule:
      {"_api":"acl_set","op":"3","rule":"{\\"idx\\":1,\\"action\\":\\"drop\\",\\"enabled\\":0}"}
```

## CLI Examples

Use the script directly from the command line:

### `acl_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api acl_get
```

### `acl_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api acl_set --param op=1
```

Optional parameters:
- `--param 'rules=<json>'`
- `--param 'rule=<json>'`
