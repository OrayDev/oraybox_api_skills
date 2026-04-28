# UPNPD APIs

APIs in the **UPNPD** category.

## APIs in this category

- `upnpd_get` — Get UPnP configuration and active port mappings
- `upnpd_set` — Set UPnP configuration

## `upnpd_get`

Get UPnP configuration and active port mappings

### Parameters

None

### Returns

> enabled, external_iface, datas[](proto, ex_port, address, in_port, name)

### Details

```
UPnP Configuration:
    Universal Plug and Play - allows LAN devices to automatically configure port forwarding
    
  Response Fields:
    enabled        - UPnP service enabled: true/false
    external_iface - External interface for UPnP (e.g., "wan")
    datas          - Array of active UPnP port mappings
      
  Port Mapping Fields (datas[]):
    proto          - Protocol: "tcp" or "udp"
    ex_port        - External port (WAN side)
    address        - Internal IP address
    in_port        - Internal port (LAN side)
    name           - Application/device name
    
  Note:
    UPnP allows LAN devices to automatically open ports on the router
    Use with caution in untrusted networks
```

## `upnpd_set`

Set UPnP configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enabled` | string | Yes | Enable UPnP: 0=off, 1=on  
(Values: 0 | 1) |
| `external_iface` | string | No | External interface (default: wan) |

### Returns

> code

### Details

```
UPnP Configuration:
    Enable/disable UPnP service and set external interface
    
  Examples:
    Enable UPnP on default WAN:
      {"_api":"upnpd_set","enabled":"1"}
    
    Enable UPnP on specific interface:
      {"_api":"upnpd_set","enabled":"1","external_iface":"wan2"}
    
    Disable UPnP:
      {"_api":"upnpd_set","enabled":"0"}
```

## CLI Examples

Use the script directly from the command line:

### `upnpd_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api upnpd_get
```

### `upnpd_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api upnpd_set --param enabled=0
```

Optional parameters:
- `--param external_iface=<value>`
