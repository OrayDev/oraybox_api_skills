# SYSTEM APIs

APIs in the **SYSTEM** category.

## APIs in this category

- `sys_base_info` — Get system base information
- `cpu_mem_get` — Get CPU and memory usage
- `system_status_get` — Get comprehensive system status
- `sys_time_get` — Get system time
- `sys_time_set` — Set system time
- `timezone_get` — Get timezone info
- `timezone_set` — Set timezone
- `reboot` — Reboot system
- `reset` — Factory reset
- `passwd` — Change admin password
- `upgrade_info_get` — Get firmware upgrade info
- `sys_upgrade_ex` — Upgrade firmware

## `sys_base_info`

Get system base information

### Parameters

None

### Returns

> sn, ver_main, ver_sub, ver_revision, ver_type, os_run_time, wan_if, wan_ip, wan_mask, wan_mac, wan2_if, wan2_ip, wan2_mask, wan2_mac, public_ip, conn_devs_count, machine, machine_display, wan_mode, wan2_mode, wan_gw, wan2_gw

## `cpu_mem_get`

Get CPU and memory usage

### Parameters

None

### Returns

> used_cpu(%), total_ram(KB), used_ram(KB), total_flash, used_flash, cpu_info, percent

## `system_status_get`

Get comprehensive system status

### Parameters

> [querys=<json_array>] (e.g., [base,runtime,network,wwan])

### Returns

> status.base, status.runtime, status.network[], status.wwan[]

## `sys_time_get`

Get system time

### Parameters

None

### Returns

> date (YYYY-MM-DD HH:MM:SS)

## `sys_time_set`

Set system time

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `time` | string | Yes | System time to set  
(Format: YYYY.MM.DD-HH:MM:SS) |

### Returns

> code

## `timezone_get`

Get timezone info

### Parameters

None

### Returns

> zonename (e.g., Asia/Shanghai), timezone (e.g., CST-8), ntp_list[], ntp_enabled

## `timezone_set`

Set timezone

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `zonename` | string | No | IANA timezone name  
(Example: Asia/Shanghai) |
| `timezone` | string | No | Timezone offset (e.g., CST-8, GMT0)  
(Example: CST-8) |
| `ntp_list` | json_array | No | Array of NTP server addresses |
| `ntp_enabled` | integer | No | Enable NTP synchronization: 0=off, 1=on  
(Values: 0 | 1) |

### Returns

> code

## `reboot`

Reboot system

### Parameters

None

### Returns

> code

## `reset`

Factory reset

### Parameters

None

### Returns

> code

## `passwd`

Change admin password

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `old_pwd` | string | Yes | Current admin password |
| `new_pwd` | string | Yes | New admin password (min 6 characters) |

### Returns

> code

## `upgrade_info_get`

Get firmware upgrade info

### Parameters

> [versiontype=<type>] [versionno=<ver>]

### Returns

| Name | Type | Description |
|------|------|-------------|
| `data` | string | Upgrade info JSON string. If empty or not present, the firmware is already up to date |

## `sys_upgrade_ex`

Upgrade firmware

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | string | Yes | Firmware download URL, from upgrade_info_get response |
| `md5` | string | Yes | MD5 checksum of firmware, from upgrade_info_get response |
| `file_name` | string | No | Local filename for downloaded firmware (default: oraybox_firmware.bin) |
| `use_https` | integer | No | Use HTTPS without cert verification: 0=no, 1=yes  
(Values: 0 | 1) |
| `reset` | integer | No | Factory reset after upgrade: 0=no, 1=yes  
(Values: 0 | 1) |

### Returns

> code

## CLI Examples

Use the script directly from the command line:

### `sys_base_info`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api sys_base_info
```

### `cpu_mem_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api cpu_mem_get
```

### `system_status_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api system_status_get
```

### `sys_time_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api sys_time_get
```

### `sys_time_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api sys_time_set --param time=<value>
```

### `timezone_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api timezone_get
```

### `timezone_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api timezone_set
```

Optional parameters:
- `--param zonename=<value>`
- `--param timezone=<value>`
- `--param 'ntp_list=<json>'`
- `--param ntp_enabled=<value>`

### `reboot`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api reboot
```

### `reset`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api reset
```

### `passwd`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api passwd --param old_pwd=<value> --param new_pwd=<value>
```

### `upgrade_info_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api upgrade_info_get
```

### `sys_upgrade_ex`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api sys_upgrade_ex --param url=<value> --param md5=<value>
```

Optional parameters:
- `--param file_name=<value>`
- `--param use_https=<value>`
- `--param reset=<value>`
