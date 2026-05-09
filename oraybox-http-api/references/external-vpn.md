# EXTERNAL VPN APIs

APIs in the **EXTERNAL VPN** category for third-party VPN tunnel management (PPTP, L2TP, IPSec).

## APIs in this category

- `pptp_get` — Get PPTP configuration list
- `pptp_set` — Add/delete/modify/enable/disable PPTP connection
- `l2tp_get` — Get L2TP configuration list
- `l2tp_set` — Add/delete/modify/enable/disable L2TP connection
- `ipsec_get` — Get IPSec configuration
- `ipsec_set` — Set IPSec configuration
- `ipsec_status_get` — Get IPSec runtime status

## `pptp_get`

Get PPTP configuration list.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `pptp` | array | List of PPTP connection entries (see Details) |

### Details

```
PPTP entry:
  {
    "iface": "pptp1",       // Interface name
    "server": "pptp.example.com",  // Server address (IP or domain)
    "user": "username",     // Username
    "pwd": "password",      // Password
    "remark": "Office",     // Remark
    "ip": "10.0.0.100",     // Assigned IP address
    "mask": "255.255.255.0", // Subnet mask
    "mtu": "1400",          // MTU
    "out_if": "wan",        // Outbound interface
    "enable": 1             // Enabled: 1=on, 0=off
  }
```

## `pptp_set`

Add, delete, modify, enable, or disable a PPTP connection.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: `1`=add, `2`=delete, `3`=modify, `4`=enable, `5`=disable |
| `iface` | string | Yes | Interface name (e.g., `pptp1`). Required for all operations |
| `server` | string | No | Server address (IP or domain). Required for `op=1` |
| `user` | string | No | Username. Required for `op=1` |
| `pwd` | string | No | Password. Required for `op=1` |
| `remark` | string | No | Remark |
| `mtu` | string | No | MTU value |
| `out_if` | string | No | Outbound interface |
| `enable` | string | No | Enable state: `1`=on, `0`=off. Used for `op=3` |

### Returns

> code

## `l2tp_get`

Get L2TP configuration list.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `l2tp` | array | List of L2TP connection entries (see Details) |

### Details

```
L2TP entry:
  {
    "iface": "l2tp1",       // Interface name
    "server": "l2tp.example.com",  // Server address (IP or domain)
    "user": "username",     // Username
    "pwd": "password",      // Password
    "remark": "Office",     // Remark
    "ip": "10.0.0.100",     // Assigned IP address
    "mask": "255.255.255.0", // Subnet mask
    "mtu": "1400",          // MTU
    "out_if": "wan",        // Outbound interface
    "enable": 1             // Enabled: 1=on, 0=off
  }
```

## `l2tp_set`

Add, delete, modify, enable, or disable an L2TP connection.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | Yes | Operation: `1`=add, `2`=delete, `3`=modify, `4`=enable, `5`=disable |
| `iface` | string | Yes | Interface name (e.g., `l2tp1`). Required for all operations |
| `server` | string | No | Server address (IP or domain). Required for `op=1` |
| `user` | string | No | Username. Required for `op=1` |
| `pwd` | string | No | Password. Required for `op=1` |
| `remark` | string | No | Remark |
| `mtu` | string | No | MTU value |
| `out_if` | string | No | Outbound interface |
| `localip` | string | No | Local IP address |
| `mask` | string | No | Local subnet mask |
| `enable` | string | No | Enable state: `1`=on, `0`=off. Used for `op=3` |

### Returns

> code

## `ipsec_get`

Get IPSec configuration.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `base` | object | Global IPSec settings |
| `crypto_proposal` | object | Crypto proposal configurations |
| `tunnel` | object | Tunnel configurations |
| `remote` | object | Remote endpoint configurations |

### Details

```
Response structure:
  {
    "base": {
      "enabled": "1"
    },
    "crypto_proposal": {
      "proposal1": {
        "encryption_algorithm": "aes128",
        "hash_algorithm": "sha256",
        "dh_group": "modp2048"
      }
    },
    "tunnel": {
      "tunnel1": {
        "mode": "route",
        "local_subnet": "192.168.1.0/24",
        "remote_subnet": "10.0.0.0/24",
        "crypto_proposal": "proposal1"
      }
    },
    "remote": {
      "remote1": {
        "gateway": "203.0.113.1",
        "pre_shared_key": "secret",
        "authentication_method": "psk",
        "local_identifier": "local-id",
        "remote_identifier": "remote-id",
        "local_id_type": "fqdn",
        "remote_id_type": "fqdn",
        "alias": "OfficeVPN",
        "crypto_proposal": "proposal1",
        "enabled": "1",
        "tunnel": "tunnel1",
        "force_crypto_proposal": "0"
      }
    }
  }
```

## `ipsec_set`

Set IPSec configuration. Supports full replace, partial modify, and delete operations.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `op` | string | No | Operation: `set`=full replace (default), `modify`=partial update, `delete`=remove sections |
| `base` | json | No | Global IPSec settings, e.g. `{"enabled":"1"}` |
| `remotes` | json | No | Remote endpoint configuration object |
| `tunnels` | json | No | Tunnel configuration object |
| `crypto_proposals` | json | No | Crypto proposal configuration object |

### Returns

> code

### Details

```
Operation modes:
  set     — Delete ALL existing crypto_proposal/tunnel/remote/ipsec configs,
            then add the provided ones. Use with complete config.
  modify  — Add or update provided sections. Existing sections with the same
            name are overwritten; new ones are added. Empty objects delete
            the named section.
  delete  — Remove named sections only. Pass arrays of section names in
            remotes/tunnels/crypto_proposals.
```

**Base fields**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `enabled` | string | No | Global IPSec switch: `1`=on, `0`=off |
| `interface` | array | No | Array of outbound interface names |

**Remote fields** (key = remote section name)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gateway` | string | Yes | Remote gateway IP or domain |
| `pre_shared_key` | string | Yes | Pre-shared key (PSK) |
| `authentication_method` | string | No | Auth method. Fixed to `"psk"` |
| `local_identifier` | string | No | Local IKE identifier |
| `remote_identifier` | string | No | Remote IKE identifier |
| `local_id_type` | string | No | Local ID type: `0`=ip, `1`=name. Used for UI display |
| `remote_id_type` | string | No | Remote ID type: `0`=ip, `1`=name. Used for UI display. When `0` and `gateway` is a domain, the domain is resolved to IP and assigned to `remote_identifier` at IPSec startup |
| `alias` | string | No | Display alias/name |
| `crypto_proposal` | string | No | Reference to a crypto proposal section name |
| `enabled` | string | No | Enable this remote: `1`=on, `0`=off |
| `tunnel` | string | No | Reference to a tunnel section name |
| `force_crypto_proposal` | string | No | Force crypto proposal: `1`=yes, `0`=no |

**Tunnel fields** (key = tunnel section name)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mode` | string | No | Tunnel mode: e.g. `route` |
| `local_subnet` | string | No | Local protected subnet (CIDR) |
| `local_nat` | string | No | Local NAT network |
| `local_sourceip` | string | No | Local source IP |
| `local_leftip` | string | No | Local left IP |
| `local_updown` | string | No | Local updown script |
| `local_firewall` | string | No | Local firewall zone |
| `remote_subnet` | string | No | Remote protected subnet (CIDR) |
| `remote_sourceip` | string | No | Remote source IP |
| `remote_updown` | string | No | Remote updown script |
| `remote_firewall` | string | No | Remote firewall zone |
| `ikelifetime` | string | No | IKE SA lifetime (e.g. `8h`) |
| `lifetime` | string | No | Child SA lifetime (e.g. `1h`) |
| `margintime` | string | No | Rekey margin time (e.g. `9m`) |
| `keyingtries` | string | No | Keying retries |
| `dpdaction` | string | No | DPD action: e.g. `restart` |
| `dpddelay` | string | No | DPD delay (e.g. `30s`) |
| `inactivity` | string | No | Inactivity timeout |
| `keyexchange` | string | No | Key exchange version: e.g. `ikev2` |
| `aggressive` | string | No | Aggressive mode |
| `reqid` | string | No | Request ID |
| `packet_marker` | string | No | Packet marker |
| `crypto_proposal` | string | No | Reference to a crypto proposal section name |
| `force_crypto_proposal` | string | No | Force crypto proposal: `1`=yes, `0`=no |
| `allow_peer_access` | string | No | Allow peer access |

**Crypto proposal fields** (key = proposal section name)

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `encryption_algorithm` | string | No | Encryption algorithm: e.g. `aes128` |
| `hash_algorithm` | string | No | Hash algorithm: e.g. `sha256` |
| `dh_group` | string | No | DH group: e.g. `modp2048` |

**Delete example** (pass arrays of names):
```json
{"remotes": ["remote1"], "tunnels": ["tunnel1"]}
```

## `ipsec_status_get`

Get IPSec runtime connection status by parsing `ipsec statusall` output.

### Parameters

None

### Returns

| Name | Type | Description |
|------|------|-------------|
| `code` | integer | Error code |
| `data` | array | List of active IPSec connection status objects (see Details) |

### Details

```
Status object:
  {
    "left": {
      "conn_name": "my_tunnel",
      "tunnel": "10.168.1.1",      // Local tunnel endpoint IP
      "ike": "f5bd7c5a6e354c63_i*", // IKE SPI (local)
      "secproto": "ESP",             // Security protocol
      "secproto_left": "c0d26842_i", // ESP SPI (local inbound)
      "channel": "10.168.6.0/24"     // Local protected subnet
    },
    "right": {
      "conn_name": "my_tunnel",
      "tunnel": "10.168.1.215",      // Remote tunnel endpoint IP
      "ike": "d2e37b1756d843ab_r",   // IKE SPI (remote)
      "secproto": "ESP",             // Security protocol
      "secproto_right": "c8653471_o", // ESP SPI (remote outbound)
      "channel": "10.168.2.0/24"     // Remote protected subnet
    }
  }
```

## CLI Examples

### `pptp_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api pptp_get
```

### `pptp_set`

Add a PPTP connection:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api pptp_set --param op=1 --param iface=pptp1 --param server=pptp.example.com --param user=admin --param pwd=secret
```

Delete a PPTP connection:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api pptp_set --param op=2 --param iface=pptp1
```

Modify a PPTP connection:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api pptp_set --param op=3 --param iface=pptp1 --param server=new.example.com
```

### `l2tp_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api l2tp_get
```

### `l2tp_set`

Add an L2TP connection:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api l2tp_set --param op=1 --param iface=l2tp1 --param server=l2tp.example.com --param user=admin --param pwd=secret
```

Delete an L2TP connection:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api l2tp_set --param op=2 --param iface=l2tp1
```

Modify an L2TP connection:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api l2tp_set --param op=3 --param iface=l2tp1 --param server=new.example.com --param localip=10.0.0.100 --param mask=255.255.255.0
```

### `ipsec_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ipsec_get
```

### `ipsec_set`

Full replace IPSec config:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ipsec_set --param 'base={"enabled":"1"}' --param 'remotes={"remote1":{"gateway":"203.0.113.1","pre_shared_key":"secret","authentication_method":"psk","enabled":"1","tunnel":"tunnel1"}}' --param 'tunnels={"tunnel1":{"mode":"route","local_subnet":"192.168.1.0/24","remote_subnet":"10.0.0.0/24"}}' --param 'crypto_proposals={"proposal1":{"encryption_algorithm":"aes128","hash_algorithm":"sha256","dh_group":"modp2048"}}'
```

Delete sections:
```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ipsec_set --param op=delete --param 'remotes=["remote1"]' --param 'tunnels=["tunnel1"]'
```

### `ipsec_status_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api ipsec_status_get
```
