# NETWORK APIs

APIs in the **NETWORK** category.

## APIs in this category

- `interface_operate` — Add/Delete/Edit network interfaces
- `dns_get` — Get DNS configuration
- `dns_set` — Set DNS servers
- `static_route_get` — Get static routes
- `static_route_set` — Set static routes
- `mtu_get` — Get MTU settings
- `mtu_set` — Set MTU
- `work_mode_get` — Get work mode
- `work_mode_set` — Set work mode
- `interface_status_get` — Get interface status
- `interface_dump` — Dump all interfaces
- `ether_status_get` — Get ethernet port status
- `interface_track_get` — Get interface link tracking configuration
- `interface_track_set` — Set interface link tracking configuration (MWAN3)

## `interface_operate`

Add/Delete/Edit network interfaces.

> ⚠️ **Note**: Configuration changes made via this API **do not take effect immediately**. You must call `restart_service` with `name=network` to restart the network for the changes to be applied.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation type: add (create new), del (delete), edit (modify existing)  
(Values: add | del | edit) |
| `name` | string | Yes | Interface name (e.g., wan3, eth0) |
| `label` | string | No | Physical port label. **REQUIRED for wired WAN types** (`dhcp`/`static`/`pppoe`) — specifies which physical Ethernet port to assign as the WAN interface. Omit for `wifi_sta`, `usb`, and `modem` modes. Query existing interface labels via `interface_dump`, or view all physical ports via `ether_status_get` |
| `info` | json | No | Interface configuration JSON object (see details below) |
| `batch` | integer | No | Enable batch mode for multiple operations  
(Values: 0 | 1) |
| `batch_info` | json_array | No | Array of batch operations when batch=1 |

### Returns

> code

### Details

```
WAN info JSON (add/edit):
    mod=<dhcp|static|pppoe|usb|wifi_sta|modem> (required)
    
    > **Important:** For wired WAN modes (`dhcp`, `static`, `pppoe`), you MUST also provide
    > the `label` parameter to specify which physical Ethernet port becomes the WAN port.
    > The router uses `label` to look up the bound physical interface (via board.json labels).
    > If the port is a silkscreen-bound physical port (disable_vlan=true), it is removed
    > from the LAN bridge and used directly as WAN. Otherwise, a VLAN is created for it.
    > Query available labels via `interface_dump` (check the `labels` field of interfaces).
    
    ==================== DHCP ====================
    {mod:"dhcp", [dns:<ip>], [mtu:<n>], [remark:<str>], [ipv6:<0|1>], 
     [macaddr:"<mac>"], [flush_conntrack:<0|1>]}
    
    ==================== STATIC ====================
    {mod:"static", ipaddr:<ip>, netmask:<mask>, gateway:<ip>, [dns:<ip>], 
      [mtu:<n>], [remark:<str>], [ipv6:<0|1>], [macaddr:"<mac>"], [flush_conntrack:<0|1>]}
    
    ==================== PPPoE ====================
    {mod:"pppoe", username:<str>, password:<str>, [service:<str>], 
      [dns:<ip>], [mtu:<n>], [remark:<str>], [ipv6:<0|1>], [macaddr:"<mac>"], [flush_conntrack:<0|1>]}
    
    ==================== USB Tethering ====================
    {mod:"usb", [dns:<ip>], [mtu:<n>], [remark:<str>], [ipv6:<0|1>]}
    
    ==================== WiFi STA (Wireless Relay) ====================
    {
      mod:"wifi_sta",
      sta_ssid:"<WiFi_name>",          // Target WiFi SSID (required)
      sta_key:"<password>",            // Target WiFi password
      sta_encryption:"<type>",         // Encryption: none, psk, psk2, psk-mixed
      [sta_channel:"<n>"],             // Target WiFi channel (optional)
      [wifi_type:"<band>"],            // Band: 1=5G, other values=2.4G (usually 0). Auto-detect if not set
      
      // WiFi connection settings (optional)
      [sta_static:"<0|1>"],            // Use configured channel/encryption directly: 1 (use config, for hidden SSID), 0 (auto-scan, ignore config)
      
      // Static IP settings (optional, for static IP configuration)
      [ipaddr:"<ip>"],                 // Static IP address
      [netmask:"<mask>"],              // Subnet mask
      [gateway:"<ip>"],                // Gateway address
      
      // Advanced settings (optional)
      [macaddr:"<mac>"],               // Custom MAC address
      [dns:<ip>], [mtu:<n>], [remark:<str>], [ipv6:<0|1>], [flush_conntrack:<0|1>]
    }
    
    WiFi STA Notes:
      - The router will connect to target WiFi as a client
      - WiFi interface will be unavailable for AP mode during relay
      - Use wifi_scan_get API to find available networks first
      - sta_ssid, sta_key, sta_encryption correspond to target WiFi's SSID, password and encryption
      - sta_static: 1 = use sta_channel/sta_encryption from config directly (required for hidden SSID connection); 0/omit = scan and auto-detect channel/encryption (ignores config values)
      - ipaddr, netmask, gateway are for static IP configuration when DHCP is not used
    
    ==================== MODEM (Cellular/4G/5G) ====================
    {
      mod:"modem",
      modem_name:"<name>",             // Modem device name (required)
      [apn:"<apn>"],                   // APN address (auto-detect if not set)
      [pincode:"<pin>"],               // SIM card PIN code (if locked)
      [username:"<user>"],             // APN username (if required)
      [password:"<pass>"],             // APN password (if required)
      [auth_mode:"<mode>"],            // Auth: none, pap, chap
      [dns:<ip>], [mtu:<n>], [remark:<str>], [ipv6:<0|1>],
      
      // SIM card management (optional)
      [sim_master:"<n>"],              // Primary SIM slot: 0, 1, 2, 3
      [sim_mode:"<mode>"],             // SIM slot switch mode: auto, manual
      [sims_queue:"<queue>"],          // SIM slot switch order, JSON array string, e.g. "[0,1]" (0=SIM1, 1=SIM2). First element must match sim_master
      
      // Network settings (optional)
      [network_mode:"<mode>"],         // Address acquisition mode: 0 (NIC mode - get base station IP directly), 1 (Router mode - get IP from module)
      
      // Retry settings (optional)
      [retry_enable:"<0|1>"],          // Enable retry mechanism
      [max_retry_reg:"<n>"],           // Max registration retry count
      [max_retry_connect:"<n>"],       // Max connection retry count
      [max_retry_abnormal:"<n>"],      // Max abnormal retry count
      
      // Advanced settings (optional)
      [senior:"<config>"],             // Advanced modem configuration
      [flush_conntrack:"<0|1>"],       // Flush conntrack on IP change
      
      // SIM card detailed config (optional)
      [sims:"<json>"]                  // SIM detailed config, JSON object string: {"sim1":{...}, "sim2":{...}}
    }
    
    SIM object parameters (in sims):
      [pincode:"<n>"],                 // SIM PIN code (positive integer)
      [auth:"<mode>"],                 // Auth mode: none, pap, chap, both
      [modes:"<mode>"],                // Network modes: all, lte, umts, gsm, cdma, td-scdma
      [standard:"<std>"],              // Network standard: auto, 5g, 4g, 3g, 2g
      [band:"<band>"],                 // Frequency band (depends on standard, e.g., "AUTO", "B1", "B3")
      [roaming:"<0|1>"],               // Enable roaming: 0 (disable), 1 (enable)
      [delay:"<n>"],                   // Connection delay in seconds (non-negative integer)
      [plmn:"<code>"],                 // PLMN code (5-6 digits, e.g., "46000")
      [sim_sel_policy:<array>],        // SIM switch policy array: ["register_failure", "network_offline", "weak_signal", "exclude_standards"]
      [weak_signal_threshold:"<n>"],   // Weak signal threshold (-140 to -44 dBm)
      [mno_sel_enabled:"<0|1>"],       // Multi-mode SIM MNO selection enable: 0, 1
      [mno_sel:<array>],               // MNO selection array: ["cm", "cu", "ct"] (China Mobile, Unicom, Telecom)
      [exclude_standards:<array>]      // Exclude standards array: ["2g", "3g", "4g", "5g"]
    
    Modem Notes:
      - modem_name examples: "modem1", "modem2", etc.
      - apn is auto-detected for most carriers, manual setting only when needed
      - Common APNs: cmnet (China Mobile), 3gnet (China Unicom), ctnet (China Telecom)
      - Some modems require specific USB modeswitch configuration
      - sim_mode: auto (automatic switch between SIM slots), manual (manual switch only)
      - network_mode: 0 (NIC mode - directly obtain base station IP address), 1 (Router mode - obtain IP address assigned by module)
    
  LAN info JSON (add/edit):
    {ipaddr:<ip>, netmask:<mask>, [vlan:<id>], [dhcp:<0|1>], [dns:<ip>], 
     [ip_start:<ip>], [limit:<n>], [rent_time:<sec>]}
    
  Examples:
    Add DHCP WAN:
      {"op":"add","name":"wan3","label":"2","info":{"mod":"dhcp"}}
    
    Add WiFi Relay (2.4G band):
      {"op":"add","name":"wan3","info":{"mod":"wifi_sta","ssid":"TargetWiFi","password":"12345678","encryption":"psk2","band":"2.4G"}}
    
    Add 4G Modem:
      {"op":"add","name":"wan3","info":{"mod":"modem","modem_name":"usb0","apn":"cmnet"}}
    
    Edit static WAN:
      {"op":"edit","name":"wan3","info":{"mod":"static","ipaddr":"192.168.1.100","netmask":"255.255.255.0","gateway":"192.168.1.1"}}
    
  Batch example:
    batch=1&batch_info=[{"op":"add","name":"wan3","label":"2","info":{"mod":"dhcp"}}]
```

## `dns_get`

Get DNS configuration

### Parameters

> [interface=<iface>] (default: lan)

### Returns

> dns, backup_dns

## `dns_set`

Set DNS servers

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dns` | string | No | Primary DNS server IP |
| `backup_dns` | string | No | Backup DNS server IP |
| `interface` | string | No | Interface to set DNS for (default: lan) |
| `no_restart_network` | integer | No | Skip network restart (legacy param)  
(Values: 0 | 1) |
| `not_restart_net` | integer | No | Skip network restart (alternative param)  
(Values: 0 | 1) |

### Returns

> code

## `static_route_get`

Get static routes

### Parameters

None

### Returns

> routes[]

## `static_route_set`

Set static routes

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | integer | Yes | Operation: 1=add, 2=edit, 3=delete  
(Values: 1 | 2 | 3) |
| `interface` | string | Yes | Interface name (e.g., wan, lan) |
| `target` | string | Yes | Target network/host IP address  
(Format: x.x.x.x) |
| `netmask` | string | No | Netmask (default: 255.255.255.255 for host route)  
(Format: x.x.x.x) |
| `gateway` | string | No | Gateway IP address  
(Format: x.x.x.x) |
| `metric` | string | No | Route metric/priority (default: 0) |

### Returns

> code

## `mtu_get`

Get MTU settings

### Parameters

None

### Returns

> mtu_wan, mtu_lan

## `mtu_set`

Set MTU

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mtu` | integer | No | MTU value (default: 1500 if empty) |
| `interface` | string | No | Interface name (default: lan) |
| `not_restart_net` | integer | No | Skip network restart  
(Values: 0 | 1) |

### Returns

> code

## `work_mode_get`

Get work mode

### Parameters

None

### Returns

> mode (router|ap|bridge)

## `work_mode_set`

Set work mode

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mode` | string | Yes | Work mode: 0=router, 1=nat, 2=bridge  
(Values: 0 | 1 | 2) |
| `zone` | string | No | Firewall zone (default: wan) |

### Returns

> code

## `interface_status_get`

Get interface status

### Parameters

> [iface=<interface>]

### Returns

> status, speed, duplex

## `interface_dump`

Dump a single interface's information from ubus

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interface` | string | Yes | Interface name to query (e.g., `wan`, `lan`, `wan2`). The API calls ubus `network.interface dump`, then searches the returned array for an entry whose `.interface` field matches this value. **Omitting this parameter always returns `no_target`** |

### Returns

> code, result

### Details

```
Implementation behavior:
  1. Calls ubus "network.interface" "dump" to fetch all interfaces
  2. Iterates the interface array and matches entry.interface == args.interface
  3. On match: returns code=success, result=the matched interface object
  4. On no match (including interface=nil): returns code=no_target, result=nil

Response format:
  {
    "code": 0,
    "result": {          // single interface object, NOT an array
      "interface": "wan",
      "up": true,
      "pending": false,
      "available": true,
      "autostart": true,
      "dynamic": false,
      "uptime": 12345,
      "l3_device": "eth0.2",
      "proto": "dhcp",
      "device": "eth0.2",
      "updated": ["addresses", "routes", "data"],
      "metric": 0,
      "dns_metric": 0,
      "delegation": true,
      "ipv4-address": [{"address":"192.168.1.100","mask":24}],
      "ipv6-address": [],
      "ipv6-prefix": [],
      "ipv6-prefix-assignment": [],
      "route": [{"target":"0.0.0.0","mask":0,"nexthop":"192.168.1.1","source":"192.168.1.100/24"}],
      "dns-server": ["192.168.1.1"],
      "dns-search": [],
      "neighbors": [],
      "inactive": {"ipv4-address":[],"ipv6-address":[],"route":[],"dns-server":[],"dns-search":[],"neighbors":[]},
      "data": {}
    }
  }
```

## `ether_status_get`

Get ethernet port status

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `version` | string | No | API version: new (recommended) or old (legacy). Default: old  
(Values: new | old) |

### Returns

> ether_status{wan{}, lan{}}, ether_capability{port{speed}}

### Details

```
Ethernet Port Status Information:
    Returns detailed link status for all ethernet ports

  Response Fields:
    ether_status      - Port status grouped by interface type (wan/lan)
    ether_capability  - Hardware capability for each port (max speed)

  Port Status Object Fields:
    link   - Link state: "up" or "down"
    speed  - Current link speed (e.g., "10Mbps", "100Mbps", "1000Mbps")
    mode   - Duplex mode: "full" or "half"
    tx     - Transmitted bytes (switch-based devices only, new version)
    rx     - Received bytes (switch-based devices only, new version)

  Examples:
    Get ethernet status:
      {"_api":"ether_status_get"}

    Get with new version format:
      {"_api":"ether_status_get","version":"new"}

  Sample Response:
    {
      "ether_status": {
        "wan": {
          "WAN": {"link": "up", "speed": "1000Mbps", "mode": "full"}
        },
        "lan": {
          "LAN1": {"link": "up", "speed": "1000Mbps", "mode": "full", "tx": "123456", "rx": "789012"},
          "LAN2": {"link": "down", "speed": "", "mode": ""}
        }
      },
      "ether_capability": {
        "wan": {"speed": "1000Mbps"},
        "lan1": {"speed": "1000Mbps"},
        "lan2": {"speed": "1000Mbps"}
      }
    }
```

## `interface_track_get`

Get interface link tracking configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interface` | string | No | Interface name to query (e.g., wan, wan2). If not specified, returns all tracked WAN interfaces |

### Returns

> track_ip[], reliability, count, timeout, failure_latency, recovery_latency, failure_loss, recovery_loss, interval, down, up, track_method, port, enabled, size

## `interface_track_set`

Set interface link tracking configuration (MWAN3)

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `interface` | string | Yes | Interface name to configure (e.g., wan, wan2, wan3). Must exist in network and mwan3 config |
| `enabled` | integer | No | Enable link tracking: 0=disabled, 1=enabled (default: 0)  
(Values: 0 | 1) |
| `track_ip` | json_array | No | Array of tracking target IPs (JSON string), e.g., '[\ |
| `track_method` | string | No | Detection method: ping (ICMP) or tcping (TCP). Default: ping  
(Values: ping | tcping) |
| `interval` | integer | No | Test interval in seconds (default: system default) |
| `timeout` | integer | No | Test timeout in seconds (default: system default) |
| `count` | integer | No | Number of test packets per interval (default: system default) |
| `reliability` | integer | No | Required number of reachable track IPs to consider link up (default: system default) |
| `failure_loss` | integer | No | Packet loss percentage threshold to mark link down  
(Range: 0-100) |
| `recovery_loss` | integer | No | Packet loss percentage threshold to mark link up  
(Range: 0-100) |
| `failure_latency` | integer | No | Latency threshold in ms to mark link down |
| `recovery_latency` | integer | No | Latency threshold in ms to mark link up |
| `down` | integer | No | Number of consecutive failed tests to mark link down |
| `up` | integer | No | Number of consecutive successful tests to mark link up |
| `size` | integer | No | Ping packet size in bytes (default: system default) |
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
      {"_api":"interface_track_set","interface":"wan","enabled":1,"track_ip":"[\"223.5.5.5\",\"114.114.114.114\"]"}
    
    TCP tracking with port:
      {"_api":"interface_track_set","interface":"wan2","enabled":1,"track_method":"tcping","port":443,"track_ip":"[\"8.8.8.8\",\"223.5.5.5\"]"}
    
    With quality thresholds:
      {"_api":"interface_track_set","interface":"wan3","enabled":1,"track_ip":"[\"223.5.5.5\"]","failure_loss":50,"recovery_loss":10,"down":3,"up":2}
    
    Get tracking status:
      {"_api":"interface_track_get","interface":"wan"}
    
    Get all tracked interfaces:
      {"_api":"interface_track_get"}
    
    Disable tracking:
      {"_api":"interface_track_set","interface":"wan","enabled":0}
```

## CLI Examples

Use the script directly from the command line:

### `interface_operate`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api interface_operate --param op=add --param name=<value>
```

Optional parameters:
- `--param label=<value>`
- `--param 'info=<json>'`
- `--param batch=<value>`
- `--param 'batch_info=<json>'`

### `dns_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api dns_get
```

### `dns_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api dns_set
```

Optional parameters:
- `--param dns=<value>`
- `--param backup_dns=<value>`
- `--param interface=<value>`
- `--param no_restart_network=<value>`
- `--param not_restart_net=<value>`

### `static_route_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api static_route_get
```

### `static_route_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api static_route_set --param op=1 --param interface=<value> --param target=<value>
```

Optional parameters:
- `--param netmask=<value>`
- `--param gateway=<value>`
- `--param metric=<value>`

### `mtu_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mtu_get
```

### `mtu_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api mtu_set
```

Optional parameters:
- `--param mtu=<value>`
- `--param interface=<value>`
- `--param not_restart_net=<value>`

### `work_mode_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api work_mode_get
```

### `work_mode_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api work_mode_set --param mode=0
```

Optional parameters:
- `--param zone=<value>`

### `interface_status_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api interface_status_get
```

### `interface_dump`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api interface_dump
```

### `ether_status_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api ether_status_get
```

Optional parameters:
- `--param version=<value>`

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
