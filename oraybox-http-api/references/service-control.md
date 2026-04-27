# SERVICE_CONTROL APIs

APIs in the **SERVICE_CONTROL** category.

## APIs in this category

- `restart_service` — Restart a service or network component

## `restart_service`

Restart a service or network component.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `name` | string | Yes | Service or component name to restart (see supported values below) |
| `reason` | string | No | Restart reason. Used by `orayboxvpn` (`join_group`/`leave_group`) and `network` (`reload`) |
| `res` | string | No | Interface name for `iface` mode (default: `lan`, use `all` for all interfaces) |

### Supported Service Names

| Name | Description | Parameters |
|------|-------------|------------|
| `orayboxsl` | Restart OrayBox smart link service | — |
| `orayboxvpn` | Restart OrayBox VPN service | `reason=join_group` / `reason=leave_group` |
| `orayboxsn` | Restart OrayBox SN (serial number) service | — |
| `orayboxph` | Restart OrayBox PH (D DNS) service | — |
| `network` | Restart network service | `reason=reload` (reload only) |
| `uhttpd` | Restart uhttpd web server | — |
| `wifi` | Restart WiFi radios | — |
| `mwan3` | Restart MWAN3 multi-WAN service | — |
| `lan_ether` | Disconnect all LAN wired devices (down/up Ethernet ports) | — |
| `lan_wireless` | Disconnect all LAN wireless devices (kick all WiFi stations) | — |
| `lan` | Disconnect all LAN devices (wired + wireless) | — |
| `ether` | Down/up all Ethernet ports (WAN + LAN) | — |
| `iface` | Restart a specific network interface | `res=<iface_name>` (default: `lan`, `all` = all interfaces) |
| `firewall` | Reload firewall rules | — |
| `conntrack` | Flush conntrack connection tracking table | — |

### Returns

> code

### Details

```
Service Restart Behaviours:

  orayboxsl
    Calls oraybox.util.restart_orayboxsl()

  orayboxvpn
    reason=join_group   -> restart with bypass route sync
    reason=leave_group  -> stop the service
    (other)             -> normal restart

  orayboxsn
    Restarts SN service, then waits for SN to be ready.
    Clears luci cache after restart.

  network
    reason=reload      -> /etc/init.d/network reload + mwan3 reload
    (other)            -> full network restart

  lan_ether
    Down/up all LAN-side Ethernet ports to force reconnection
    of wired sub-devices.

  lan_wireless
    Sends DisConnectAllSta=2 on all enabled AP-mode WiFi interfaces
    to kick all wireless stations.

  lan
    Combines lan_ether + lan_wireless.

  ether
    Combines WAN Ethernet down/up + LAN Ethernet down/up.

  iface
    res=<iface> -> ifup <iface>
    res=all     -> restart entire network

  conntrack
    Runs "conntrack -D" after a 3-second delay.
```

### Examples

Restart WiFi:
  {"_api":"restart_service","name":"wifi"}

Reload firewall:
  {"_api":"restart_service","name":"firewall"}

Restart a specific interface:
  {"_api":"restart_service","name":"iface","res":"wan"}

Kick all WiFi clients:
  {"_api":"restart_service","name":"lan_wireless"}

Restart VPN with group join:
  {"_api":"restart_service","name":"orayboxvpn","reason":"join_group"}

Reload network config only:
  {"_api":"restart_service","name":"network","reason":"reload"}

Flush connection tracking:
  {"_api":"restart_service","name":"conntrack"}

## CLI Examples

### `restart_service`

Restart WiFi:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api restart_service --param name=wifi
```

Reload firewall:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api restart_service --param name=firewall
```

Restart WAN interface:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api restart_service --param name=iface --param res=wan
```

Kick all wireless clients:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --password admin --api restart_service --param name=lan_wireless
```

Optional parameters:
- `--param reason=<value>`
- `--param res=<value>`
