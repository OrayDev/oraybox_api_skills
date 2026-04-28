# SNMP APIs

APIs in the **SNMP** category.

## APIs in this category

- `snmp_get` — Get SNMP configuration
- `snmp_set` — Set SNMP configuration

## `snmp_get`

Get SNMP configuration

### Parameters

None

### Returns

> info{enabled, port, version, syslocation, syscontact, sysname, [v2c_fields], [v3_fields], frequency, upload}

### Details

```
SNMP Configuration:
    Simple Network Management Protocol settings for device monitoring
    
  Response Fields:
    enabled        - SNMP service enabled: 0=off, 1=on
    port           - SNMP service port (default: 161)
    version        - SNMP version: "v2c" or "v3"
    syslocation    - System location description
    syscontact     - System contact information
    sysname        - System name
    
  v2c Specific Fields:
    community      - Community string (public/private)
    source         - Allowed source IP/network
    access         - Access level: "ro" (read-only) or "rw" (read-write)
    
  v3 Specific Fields:
    username       - SNMPv3 username
    access         - Access level: "ro" or "rw"
    security       - Security level: "noauthnopriv", "authnopriv", "authpriv"
    authtype       - Auth type (for authnopriv/authpriv): "MD5" or "SHA"
    authpass       - Auth password (for authnopriv/authpriv)
    privproto      - Privacy protocol (for authpriv): "DES" or "AES"
    privpass       - Privacy password (for authpriv)
    
  Other Fields:
    frequency      - Data upload frequency in seconds
    upload         - Enable SNMP data upload: 0=off, 1=on
```

## `snmp_set`

Set SNMP configuration

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `info` | json | Yes | SNMP configuration JSON object |

### Returns

> code

### Details

```
SNMP Configuration JSON Format:
  
  Common Fields (all versions):
    {
      "enabled": 1,              // Enable SNMP: 0=off, 1=on
      "port": 161,               // SNMP service port (1-65535)
      "version": "v2c",          // SNMP version: "v2c" or "v3"
      "syslocation": "Office",   // System location
      "syscontact": "admin@example.com",
      "sysname": "Router-01",    // System name
      "frequency": 300,          // Upload frequency in seconds
      "upload": 1                // Enable data upload: 0=off, 1=on
    }
    
  SNMPv2c Specific Fields:
    {
      "version": "v2c",
      "community": "public",     // Community string
      "source": "192.168.1.0/24", // Allowed source (optional)
      "access": "ro"             // Access: "ro"=read-only, "rw"=read-write
    }
    
  SNMPv3 Specific Fields:
    {
      "version": "v3",
      "username": "snmpuser",
      "access": "ro",            // "ro" or "rw"
      "security": "authpriv",    // "noauthnopriv", "authnopriv", "authpriv"
      
      // For authnopriv and authpriv:
      "authtype": "SHA",         // "MD5" or "SHA"
      "authpass": "authpassword",
      
      // For authpriv only:
      "privproto": "AES",        // "DES" or "AES"
      "privpass": "privpassword"
    }
    
  Security Levels:
    noauthnopriv - No authentication, no privacy (username only)
    authnopriv   - Authentication only (username + auth password)
    authpriv     - Authentication + privacy (username + auth + encryption)
    
  Examples:
    Enable SNMPv2c:
      {"_api":"snmp_set","info":"{\\"enabled\\":1,\\"port\\":161,\\"version\\":\\"v2c\\",\\"community\\":\\"public\\",\\"access\\":\\"ro\\",\\"syslocation\\":\\"Office\\"}"}
    
    Enable SNMPv3 with auth only:
      {"_api":"snmp_set","info":"{\\"enabled\\":1,\\"port\\":161,\\"version\\":\\"v3\\",\\"username\\":\\"admin\\",\\"security\\":\\"authnopriv\\",\\"authtype\\":\\"SHA\\",\\"authpass\\":\\"secret123\\"}"}
    
    Enable SNMPv3 with auth and privacy:
      {"_api":"snmp_set","info":"{\\"enabled\\":1,\\"port\\":161,\\"version\\":\\"v3\\",\\"username\\":\\"admin\\",\\"security\\":\\"authpriv\\",\\"authtype\\":\\"SHA\\",\\"authpass\\":\\"secret123\\",\\"privproto\\":\\"AES\\",\\"privpass\\":\\"priv456\\"}"}
    
    Disable SNMP:
      {"_api":"snmp_set","info":"{\\"enabled\\":0}"}
```

## CLI Examples

Use the script directly from the command line:

### `snmp_get`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api snmp_get
```

### `snmp_set`

```bash
python3 scripts/oraybox_http_api.py --host 192.168.1.1 --api snmp_set --param 'info={"key":"value"}'
```
