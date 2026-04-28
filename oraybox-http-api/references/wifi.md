# WIFI APIs

APIs in the **WIFI** category.

## APIs in this category

- `wifi_get` — Get WiFi configuration
- `wifi_set` — Set WiFi configuration
- `wifi_scan_get` — Scan WiFi networks
- `wifi_channels_get` — Get available channels
- `wifi_disconnect_sta` — Disconnect WiFi client

## `wifi_get`

Get WiFi configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dev` | string | No | WiFi device/band to query (default: both)  
(Values: 2.4G | 5G) |
| `tag` | string | No | Version tag: not specified or 0=old version, 1=new version (recommend: always use 1)  
(Values: 0 | 1) |

### Returns

> switch, level(1-3), htmode, channel, country, ssid, pattern(0=single/1=multi), hidden, pwd, encryption, isolation, sta_isolation, maxassoc, ssid_list[] (multi-SSID mode)

## `wifi_set`

Set WiFi configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dev` | string | Yes | WiFi device/band to configure  
(Values: 2.4G | 5G) |
| `switch` | integer | Yes | WiFi switch: 0=off, 1=on  
(Values: 0 | 1) |
| `htmode` | string | Yes | HT mode (e.g., HT20, HT40, VHT40, VHT80) |
| `channel` | integer | Yes | WiFi channel number (0 or auto for auto-selection) |
| `level` | integer | Yes | Signal strength level: 1=low, 2=medium, 3=high  
(Values: 1 | 2 | 3) |
| `pattern` | integer | Yes | SSID mode: 0=single SSID, 1=multi-SSID  
(Values: 0 | 1) |
| `country` | string | Yes | Country code for regulatory domain (e.g., CN, US, JP) |
| `ssid_list` | json_array | Yes | SSID configuration list. Each element is a dict with ssid/pwd/encryption/hidden/isolation/sta_isolation/maxassoc/ft/vlanid/shaping_switch/upload/download/ramode/auth_server/auth_port/auth_secret/nasid. **Important:** `encryption` value must be chosen from `feature.encryptions` returned by `wifi_get`. For older firmware without `feature`, use `encrypt` instead (deprecated). |
| `batch_set` | json | No | Batch configure multiple bands (e.g., {\ |
| `is_restart_wifi` | integer | No | Restart WiFi after set: 0=no, 1=yes (default: delayed restart)  
(Values: 0 | 1) |
| `not_restart_net` | integer | No | Skip network restart during batch operations  
(Values: 0 | 1) |

### Returns

> code

### Details

```
IMPORTANT USAGE NOTES:
    1. This interface is OVERWRITING - unspecified parameters will be reset to defaults or deleted
    2. You MUST first call wifi_get to get current config, modify based on it, then submit
    3. Each dev(2.4G | 5G) supports up to 4 SSIDs in ssid_list
    4. To delete an SSID, set the corresponding object in ssid_list to an empty object {}

  ssid_list Parameter Description:
    ssid_list is a JSON array used to configure one or more SSIDs. Each element in the array
    represents an SSID configuration. Up to 4 SSIDs can be configured per band (2.4G or 5G).

  ssid_list JSON Array Format:
    [
      {
        "ssid": "WiFi-Name",           // SSID name (required)
        "pwd": "password",             // Password (8-63 chars for WPA, empty for open network)
        "encryption": "psk2+ccmp",     // Encryption type. MUST match one of feature.encryptions from wifi_get
        "hidden": 0,                   // SSID hidden: 0=visible (default), 1=hidden
        "isolation": 0,                // AP/Bridge isolation: 0=off (default), 1=on
        "sta_isolation": 0,            // STA isolation: 0=off (default), 1=on (same BSSID clients cannot communicate)
        "maxassoc": 32,                // Maximum number of associated clients (optional)
        "switch": 1,                   // SSID switch: 0=off, 1=on (default: 1)
        "ft": 0,                       // Fast BSS Transition (802.11r): 0=off, 1=on
        "vlanid": 100,                 // VLAN ID (optional)
        "shaping_switch": 0,           // Traffic shaping: 0=off, 1=on
        "upload": 1024,                // Upload limit in kbps (when shaping on)
        "download": 2048,              // Download limit in kbps (when shaping on)
        "auth_server": "10.0.0.1",     // RADIUS server IP (for WPA2-EAP)
        "auth_port": 1812,             // RADIUS server port
        "auth_secret": "secret123",    // RADIUS shared secret
        "nasid": "nas01"               // NAS Identifier (optional)
      }
    ]

  Field Descriptions:
    - ssid:           WiFi network name (1-32 characters, required)
    - pwd:            WiFi password (8-63 characters for WPA, required when encryption is not "none")
    - encryption:     Encryption type. **Must be chosen from `feature.encryptions`** returned by `wifi_get`.
                      Common values: "none", "psk+ccmp", "psk2+ccmp", "psk-mixed+ccmp".
                      The exact supported values depend on the hardware/driver.
                      **Note:** `auth`, `encrypt`, `wpa3` fields in ssid_list are deprecated.
                      Use `encryption` directly for new code.
    - hidden:         Whether to hide SSID broadcast: 0=visible (default), 1=hidden
    - isolation:      AP/Bridge isolation (br_isolate_mode): 0=off (default), 1=on
                      Isolates clients at bridge level
    - sta_isolation:  STA isolation (isolated): 0=off (default), 1=on
                      Isolates clients under the same BSSID (same SSID)
                      Note: This is different from standard OpenWrt isolate field,
                      as mt_dbdc.sh driver reads 'isolated' field specifically
    - maxassoc:       Maximum number of clients allowed to connect (optional)
    - switch:         SSID switch: 0=off, 1=on (default: 1)
    - ft:             Fast BSS Transition (802.11r): 0=off (default), 1=on
    - vlanid:         VLAN ID for this SSID (optional, requires VLAN support)
    - shaping_switch: Traffic shaping switch: 0=off (default), 1=on
    - upload:         Upload speed limit in kbps (required when shaping_switch=1)
    - download:       Download speed limit in kbps (required when shaping_switch=1)
    - tcmode:         Traffic control mode (optional, e.g., "htb")
    - ramode:         RADIUS authentication mode (required for WPA2-EAP)
    - auth_server:    RADIUS server IP address (required for WPA2-EAP)
    - auth_port:      RADIUS server port (default: 1812, required for WPA2-EAP)
    - auth_secret:    RADIUS shared secret (required for WPA2-EAP)
    - nasid:          NAS Identifier for RADIUS (optional for WPA2-EAP)

  > **Agent Guidance:** Call `sys_base_info` first and check the `ver_main` field to determine the firmware generation. `ver_main` starting with `6` means 6.x / SDK 17.01 (no `feature` field in `wifi_get`); starting with `7` means 7.x / SDK 21.02 (`feature` field present). Use the corresponding parameter format below.

  Compatibility Notes:
    1. If `wifi_get` response contains `feature` field, use `encryption` in ssid_list.
    2. If `wifi_get` response does NOT contain `feature` field (older firmware),
       use deprecated `encrypt` field in ssid_list instead.
    3. `auth`, `encrypt`, `wpa3` fields are deprecated and may be removed in future.

  Example - Set 2.4G with single SSID (new firmware with feature):
    {"_api":"wifi_set","dev":"2.4G","switch":1,"htmode":"HT40","channel":0,"level":3,"pattern":0,"country":"CN","ssid_list":"[{\"ssid\":\"MyWiFi\",\"pwd\":\"12345678\",\"encryption\":\"psk2+ccmp\"}]"}

  Example - Set 2.4G with single SSID (older firmware without feature):
    {"_api":"wifi_set","dev":"2.4G","switch":1,"htmode":"HT40","channel":0,"level":3,"pattern":0,"country":"CN","ssid_list":"[{\"ssid\":\"MyWiFi\",\"pwd\":\"12345678\",\"encrypt\":\"psk2+ccmp\"}]"}

  Example - Set 5G with multiple SSIDs:
    {"_api":"wifi_set","dev":"5G","switch":1,"htmode":"VHT80","channel":0,"level":3,"pattern":1,"country":"CN","ssid_list":"[{\"ssid\":\"MainWiFi\",\"pwd\":\"password1\",\"encryption\":\"psk2+ccmp\"},{\"ssid\":\"GuestWiFi\",\"pwd\":\"password2\",\"encryption\":\"psk2+ccmp\",\"isolation\":1}]"}

  Example - Delete the 2nd SSID (set to empty object):
    {"_api":"wifi_set","dev":"5G","switch":1,"htmode":"VHT80","channel":0,"level":3,"pattern":1,"country":"CN","ssid_list":"[{\"ssid\":\"MainWiFi\",\"pwd\":\"password1\",\"encryption\":\"psk2+ccmp\"},{},{\"ssid\":\"GuestWiFi\",\"pwd\":\"password3\",\"encryption\":\"psk2+ccmp\"}]"}
```

## `wifi_scan_get`

Scan WiFi networks

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dev` | string | No | WiFi band to scan (default: current band)  
(Values: 2.4G | 5G) |

### Returns

> networks[] (ssid, signal, encryption, channel)

## `wifi_channels_get`

Get available channels

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `dev` | string | Yes | WiFi band to query channels for  
(Values: 2.4G | 5G) |

### Returns

> channels[]

## `wifi_disconnect_sta`

Disconnect WiFi client

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mac` | string | Yes | MAC address of the client to disconnect  
(Format: AA:BB:CC:DD:EE:FF) |
| `dev` | string | No | WiFi band where the client is connected  
(Values: 2.4G | 5G) |

### Returns

> code

## SDK Version Differences for `wifi_timer` (17.01 vs 21.02)

`17.01` corresponds to firmware 6.x; `21.02` corresponds to firmware 7.x.

> **Agent Guidance:** Call `sys_base_info` first and check the `ver_main` field to determine the firmware generation. `ver_main` starting with `6` means 6.x / SDK 17.01; starting with `7` means 7.x / SDK 21.02. Use the corresponding parameter format below.

> **Note:** `wifi_timer` APIs (`wifi_timer_get`, `wifi_timer_set`) are not listed in the main API docs but exist in the `wifi_timer` package with version-specific implementations.

### `wifi_timer_get`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Returns** | `enable`, `ssidlist`, **`rules`** (array of `{id, weeks, start, ends, ssids}`) | `enable`, `ssidlist`, **`time_id`**, **`apply`** |
| **SSID item fields** | `iface`, `ssid`, `band` | `iface`, `ssid`, `band`, **`apply`** (`"1"` if time_group assigned) |
| **Data source** | `timer_rule` list per iface | `time_group` per iface |

### `wifi_timer_set`

| Aspect | 17.01 (Firmware 6.x) | 21.02 (Firmware 7.x) |
|--------|----------------------|----------------------|
| **Key params** | `enable`, `weeks`, `start`, `ends`, `action` (`add`/`modify`/`del`/`reset`), `id` | `enable`, `weeks`, `time_id`, `reload` |
| **Removed** | `action`, `start`, `ends`, `id` | — |
| **New** | — | `time_id` (references `group_time` config), `reload` (`"1"` to re-apply) |
| **Time model** | Inline `start`/`ends`/`weeks` | Indirect via `group_time` (from `group_support` package) |
| **Cross-day** | Not supported (`start` ≤ `ends`) | Supported (splits into two rules internally) |
| **Rule ID** | `os.time()` timestamp | `group_time.id` |

## CLI Examples

Use the script directly from the command line:

### `wifi_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api wifi_get
```

Optional parameters:
- `--param dev=<value>`
- `--param tag=<value>`

### `wifi_set`

**New firmware (with `feature` in wifi_get response):**
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 \
  --api wifi_set --param dev=2.4G --param switch=1 --param htmode=HT40 \
  --param channel=0 --param level=3 --param pattern=0 --param country=CN \
  --param 'ssid_list=[{"ssid":"MyWiFi","pwd":"12345678","encryption":"psk2+ccmp"}]'
```

**Older firmware (without `feature`):**
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 \
  --api wifi_set --param dev=2.4G --param switch=1 --param htmode=HT40 \
  --param channel=0 --param level=3 --param pattern=0 --param country=CN \
  --param 'ssid_list=[{"ssid":"MyWiFi","pwd":"12345678","encrypt":"psk2+ccmp"}]'
```

Optional parameters:
- `--param 'batch_set=<json>'`
- `--param is_restart_wifi=<value>`
- `--param not_restart_net=<value>`

### `wifi_scan_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api wifi_scan_get
```

Optional parameters:
- `--param dev=<value>`

### `wifi_channels_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api wifi_channels_get --param dev=2.4G
```

### `wifi_disconnect_sta`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api wifi_disconnect_sta --param mac=<value>
```

Optional parameters:
- `--param dev=<value>`
