# Oraybox API Reference Index

Complete reference for all Oray router management APIs accessible via HTTP POST to `/cgi-bin/oraybox`.

Every request must include the form fields `_api` (API name) and `_pwd` (admin password).

## Categories

- [SYSTEM](system.md)
- [NETWORK](network.md)
- [DHCP](dhcp.md)
- [WIFI](wifi.md)
- [PORT_FORWARD](port-forward.md)
- [DEVICE](device.md)
- [DIAGNOSTICS](diagnostics.md)
- [FLOWRATE](flowrate.md)
- [SERVICE_CONTROL](service-control.md)
- [BEHAVIOUR](behaviour.md)
- [ACL](acl.md)
- [GROUP_SUPPORT](group-support.md)
- [MWAN3](mwan3.md)
- [TRAFFIC_CONTROL](traffic-control.md)
- [DMZ](dmz.md)
- [SNMP](snmp.md)
- [UPNPD](upnpd.md)
- [APP_TRAFFIC](app-traffic.md)
- [USB_FILE](usb-file.md)

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Internal error |
| 2 | API not exist |
| 3 | No API specified |
| 4 | Wrong password |
| 5 | Max retry exceeded |
| 6 | In disable time |
| 7 | Invalid address |
| 999 | Unknown error |
| 100 | Invalid arguments |
| 101 | Permission denied |
| 102 | UCI operation failed |
| 103 | Not implemented |
| 104 | Device not exist |
| 105 | Network unreachable |
| 106 | Target not exist |
| 107 | Target repeat/conflict |
| 108 | MD5 checksum error |
| 109 | MAC address format error |
| 110 | Download failed |
| 111 | Resource in use |
| 113 | Config wrong |
| 114 | Operation forbidden |
| 115 | Server connect failed |
| 116 | Invalid/cipher file |
| 117 | IP conflict (LAN/WAN) |
| 118 | Already bound Oray account |
| 119 | Bind account failed |
| 120 | Bridge forward failed |
| 130 | Encrypt/Decrypt failed |
| 301 | USB partition not found |
| 302 | File system not supported |


## CLI Usage

The Python script can be run directly as a CLI tool:

```bash
python3 scripts/oraybox_http_api.py     --host 192.168.1.1     --password admin     --api sys_base_info
```

### Global CLI Flags

| Flag | Required | Description |
|------|----------|-------------|
| `--host` | yes | Router IP or hostname |
| `--password` | yes | Admin password |
| `--api` | yes | API name |
| `--param` | no | Parameter as `key=value` (repeatable) |
| `--timeout` | no | HTTP timeout (default: 30) |
| `--https` | no | Use HTTPS |

For per-API CLI examples, see the individual category reference files.
