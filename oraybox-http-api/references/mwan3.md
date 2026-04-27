# MWAN3 APIs

APIs in the **MWAN3** category.

## APIs in this category

- `mwan_get` — Get MWAN3 multi-WAN configuration
- `mwan_set` — Set MWAN3 multi-WAN configuration
- `mwan_rules_get` — Get MWAN3 policy routing rules
- `mwan_rules_set` — Set MWAN3 policy routing rules
- `interface_track_get` — Get interface link tracking configuration (MWAN3)
- `interface_track_set` — Set interface link tracking configuration (MWAN3)
- `netstat_get` — Get network detection status
- `netstat_alarm_get` — Get network status alarm configuration
- `netstat_alarm_set` — Set network status alarm configuration

## `mwan_get`

Get MWAN3 multi-WAN configuration

### Parameters

None

### Returns

> mode (multiwan|backupwan), [order], interface weights

## `mwan_set`

Set MWAN3 multi-WAN configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mode` | string | Yes | MWAN mode: multiwan=load balance, backupwan=failover  
(Values: multiwan | backupwan) |
| `rules` | json | No | For multiwan: object with interface names as keys and weights (0-100) as values |
| `order` | json_array | No | For backupwan: ordered array of interfaces by priority |

### Returns

> code

### Details

```
Multi-WAN Mode (multiwan):
    Load balancing across multiple WAN interfaces
    Rules format: {"wan": 50, "wan2": 50}  // 50% traffic each
    Set weight to 0 to disable an interface
    
  Backup WAN Mode (backupwan):
    Failover with priority order
    Order format: ["wan", "wan2"]  // wan is primary, wan2 is backup
    
  Examples:
    Set multiwan with 70/30 split:
      {"_api":"mwan_set","mode":"multiwan","rules":"{\\"wan\\":70,\\"wan2\\":30}"}
    
    Set backup wan order:
      {"_api":"mwan_set","mode":"backupwan","order":"[\\"wan\\",\\"wan2\\",\\"wan3\\"]"}
```

## `mwan_rules_get`

Get MWAN3 policy routing rules

### Parameters

None

### Returns

> policy[], rules[] (name, fake_name, dest_ip, dest_port, src_ip, src_port, proto, dns_group, use_policy, domains)

## `mwan_rules_set`

Set MWAN3 policy routing rules

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | No | Operation: 0=set all, 1=add, 2=delete, 3=set ISP IP rules  
(Values: 0 | 1 | 2 | 3) |
| `rules` | json_array | Yes | Array of MWAN rules |

### Returns

> code

### Details

```
MWAN Rule JSON Format:
    {
      "name": "<rule_name>",           // Unique rule name
      "src_ip": "<ip/group>",          // Source IP or group
      "src_port": "<port>",            // Source port
      "dest_ip": "<ip/group>",         // Destination IP or group
      "dest_port": "<port>",           // Destination port
      "proto": "tcp|udp|icmp|all",     // Protocol
      "dns_group": "<group_name>",     // DNS group for domain-based routing
      "domains": ["example.com"],      // Domain list (will create ipset)
      "use_policy": "<policy_name>",   // Policy to use (e.g., wan_only, wan2_only, balanced)
      "sticky": "0",                   // Sticky connections: 0=off, 1=on
      "timeout": "10"                  // Sticky timeout in seconds
    }
    
  Available Policies:
    balanced     - Load balance across interfaces
    wan_only     - Use wan interface only
    wan2_only    - Use wan2 interface only
    <iface>_only - Use specific interface
    
  Examples:
    Route all traffic from 192.168.1.0/24 through wan2:
      {"_api":"mwan_rules_set","rules":"[{\\"name\\":\\"route_1\\",\\"src_ip\\":\\"192.168.1.0/24\\",\\"use_policy\\":\\"wan2_only\\",\\"proto\\":\\"all\\"}]"}
```

## `interface_track_get`

Get interface link tracking configuration (MWAN3)

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interface` | string | No | Interface name to query (e.g., wan, wan2). If not specified, returns all tracked WAN interfaces |

### Returns

> track_ip, reliability, count, timeout, failure_latency, recovery_latency, failure_loss, recovery_loss, interval, down, up, track_method, port, enabled, size

## `interface_track_set`

Set interface link tracking configuration (MWAN3)

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interface` | string | Yes | Interface name to configure (e.g., wan, wan2, wan3) |
| `enabled` | integer | No | Enable link tracking: 0=disabled, 1=enabled (default: 0)  
(Values: 0 | 1) |
| `track_ip` | json_array | No | Array of tracking target IPs, e.g., '[\ |
| `track_method` | string | No | Detection method: ping (ICMP) or tcping (TCP). Default: ping  
(Values: ping | tcping) |
| `interval` | integer | No | Test interval in seconds (default: 5) |
| `timeout` | integer | No | Test timeout in seconds (default: 2) |
| `count` | integer | No | Number of test packets per interval (default: 1) |
| `reliability` | integer | No | Required reachable track IPs to consider link up (default: 1) |
| `failure_loss` | integer | No | Packet loss % to mark link down (default: 70)  
(Range: 0-100) |
| `recovery_loss` | integer | No | Packet loss % to mark link up (default: 50)  
(Range: 0-100) |
| `failure_latency` | integer | No | Latency (ms) to mark link down (default: 2000) |
| `recovery_latency` | integer | No | Latency (ms) to mark link up (default: 1500) |
| `down` | integer | No | Consecutive failed tests to mark link down (default: 3) |
| `up` | integer | No | Consecutive successful tests to mark link up (default: 3) |
| `size` | integer | No | Ping packet size in bytes (default: 22) |
| `port` | integer | No | TCP port for tcping method (required when track_method=tcping)  
(Range: 1-65535) |

### Returns

> code

### Details

```
MWAN3 Link Tracking Configuration:
    Used for multi-WAN failover and load balancing
    
  Detection Methods:
    ping   - ICMP ping (default, most compatible)
    tcping - TCP SYN probe (useful when ICMP is blocked, requires port parameter)
    
  Key Parameters:
    track_ip         - Array of IPs to monitor (e.g., ["223.5.5.5", "8.8.8.8"])
    reliability      - How many track IPs must be reachable to consider link up
    failure_loss     - Packet loss % to trigger down state
    recovery_loss    - Packet loss % to recover to up state
    failure_latency  - Latency (ms) threshold to trigger down state
    recovery_latency - Latency (ms) threshold to recover to up state
    down/up          - Consecutive test counts before state change
    
  Examples:
    Basic ping tracking:
      {"_api":"interface_track_set","interface":"wan","enabled":1,"track_ip":"[\\"223.5.5.5\\",\\"114.114.114.114\\"]"}
    
    TCP tracking with port:
      {"_api":"interface_track_set","interface":"wan2","enabled":1,"track_method":"tcping","port":443,"track_ip":"[\\"8.8.8.8\\",\\"223.5.5.5\\"]"}
```

## `netstat_get`

Get network detection status

### Parameters

> [interface=<iface>]

### Returns

> status{interface: {status, track_ip[], uptime, downtime}}

## `netstat_alarm_get`

Get network status alarm configuration

### Parameters

None

### Returns

> cfg{interface: {enable, iface_conn_state_enable, latency_alarm_enable, latency_alarm_high_threshold, latency_alarm_low_threshold}}

## `netstat_alarm_set`

Set network status alarm configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ifnames` | json_array | No | Array of WAN interface names to configure (default: [\ |
| `enable` | integer | Yes | Enable network status alarm  
(Values: 0 | 1) |
| `iface_conn_state_enable` | integer | No | Enable interface connection state monitoring  
(Values: 0 | 1) |
| `latency_alarm_enable` | integer | No | Enable latency alarm  
(Values: 0 | 1) |
| `latency_alarm_high_threshold` | integer | No | High latency threshold in ms to trigger alarm |
| `latency_alarm_low_threshold` | integer | No | Low latency threshold in ms to clear alarm |

### Returns

> code

### Details

```
Network Status Alarm:
    Monitors WAN interface connection state and latency
    
  Configuration Levels:
    global - Default configuration for all interfaces
    <iface> - Per-interface configuration (overrides global)
    
  Examples:
    Enable global alarm:
      {"_api":"netstat_alarm_set","ifnames":"[\\"global\\"]","enable":1,"latency_alarm_enable":1,"latency_alarm_high_threshold":200,"latency_alarm_low_threshold":100}
    
    Configure specific interface:
      {"_api":"netstat_alarm_set","ifnames":"[\\"wan\\",\\"wan2\\"]","enable":1,"iface_conn_state_enable":1}
```

## CLI Examples

Use the script directly from the command line:

### `mwan_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mwan_get
```

### `mwan_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mwan_set --param mode=multiwan
```

Optional parameters:
- `--param 'rules=<json>'`
- `--param 'order=<json>'`

### `mwan_rules_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mwan_rules_get
```

### `mwan_rules_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mwan_rules_set --param 'rules=["value1","value2"]'
```

Optional parameters:
- `--param op=<value>`

### `interface_track_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api interface_track_get
```

Optional parameters:
- `--param interface=<value>`

### `interface_track_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api interface_track_set --param interface=<value>
```

Optional parameters:
- `--param enabled=<value>`
- `--param 'track_ip=<json>'`
- `--param track_method=<value>`
- `--param interval=<value>`
- `--param timeout=<value>`
- `--param count=<value>`
- `--param reliability=<value>`
- `--param failure_loss=<value>`
- `--param recovery_loss=<value>`
- `--param failure_latency=<value>`
- `--param recovery_latency=<value>`
- `--param down=<value>`
- `--param up=<value>`
- `--param size=<value>`
- `--param port=<value>`

### `netstat_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api netstat_get
```

### `netstat_alarm_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api netstat_alarm_get
```

### `netstat_alarm_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api netstat_alarm_set --param enable=1
```

Optional parameters:
- `--param 'ifnames=<json>'`
- `--param iface_conn_state_enable=<value>`
- `--param latency_alarm_enable=<value>`
- `--param latency_alarm_high_threshold=<value>`
- `--param latency_alarm_low_threshold=<value>`
