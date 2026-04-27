# DMZ APIs

APIs in the **DMZ** category.

## APIs in this category

- `dmz_get` — Get DMZ configuration (legacy)
- `dmz_get_ex` — Get extended DMZ configuration
- `dmz_set` — Set DMZ configuration

## `dmz_get`

Get DMZ configuration (legacy)

### Parameters

None

### Returns

> code, ip, enable, ip2, enable2

## `dmz_get_ex`

Get extended DMZ configuration

### Parameters

None

### Returns

> code, ip, enable, ip<N>, enable<N>, ip_oray_vnc, enable_oray_vnc

### Details

```
DMZ Configuration:
    Exposes all ports of a LAN device to the WAN
    
  Response Fields:
    ip, enable          - Primary WAN DMZ settings
    ip<N>, enable<N>    - Additional WAN interfaces (ip2, enable2, etc.)
    ip_oray_vnc         - VPN network DMZ IP
    enable_oray_vnc     - VPN network DMZ enabled
```

## `dmz_set`

Set DMZ configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `wan_name` | string | Yes | WAN interface name (e.g., wan, wan2) or 'oray_vnc' for VPN |
| `dest_ip` | string | No | LAN IP address for DMZ host  
(Format: x.x.x.x) |
| `enable` | string | No | Enable DMZ (string boolean)  
(Values: true | false) |
| `enabled` | string | No | Enable DMZ (0=off, 1=on) - alternative to enable  
(Values: 0 | 1) |

### Returns

> code

### Details

```
DMZ (Demilitarized Zone):
    Forwards all external ports to a specific internal host
    
  Note:
    Use with caution - exposes the entire host to the internet
    Port forwarding rules take precedence over DMZ
    
  Examples:
    Enable DMZ for primary WAN:
      {"_api":"dmz_set","wan_name":"wan","dest_ip":"192.168.1.100","enable":"true"}
    
    Enable DMZ for secondary WAN:
      {"_api":"dmz_set","wan_name":"wan2","dest_ip":"192.168.1.101","enabled":"1"}
    
    Disable DMZ:
      {"_api":"dmz_set","wan_name":"wan","enable":"false"}
```
