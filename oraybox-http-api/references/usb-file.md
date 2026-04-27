# USB_FILE APIs

APIs in the **USB_FILE** category.

## APIs in this category

- `usb_file_samba_get` — Get USB file sharing (Samba) status - legacy
- `usb_file_samba_get_ex` — Get USB file sharing (Samba) status - extended
- `usb_file_samba_set` — Configure USB file sharing (Samba)
- `usb_file_format` — Format USB partition
- `usb_file_format_result` — Get USB format operation result
- `usb_label_set` — Set USB partition label
- `usb_safe_remove` — Safely remove USB device

## `usb_file_samba_get`

Get USB file sharing (Samba) status - legacy

### Parameters

None

### Returns

> has_usb_disk, total_space, use_space, free_space, use_percent, file_system, share_enabled, user_name, wan_share_enable

### Details

```
USB File Sharing Status (Legacy):
    Returns basic information about USB storage and Samba share
    
  Response Fields:
    has_usb_disk     - USB disk detected: true/false
    total_space      - Total capacity (human readable)
    use_space        - Used space (human readable)
    free_space       - Free space (human readable)
    use_percent      - Usage percentage
    file_system      - File system type (NTFS, vfat, exfat, etc.)
    share_enabled    - Samba share enabled: true/false
    user_name        - Access username (empty if guest access)
    wan_share_enable - WAN access enabled: "0" or "1"
```

## `usb_file_samba_get_ex`

Get USB file sharing (Samba) status - extended

### Parameters

None

### Returns

> has_usb_disk, partitions[](device, label, total_space, use_space, free_space, use_percent, file_system), share_enabled, user_name, wan_share_enable

### Details

```
USB File Sharing Status (Extended):
    Returns detailed information about USB partitions and Samba share
    
  Response Fields:
    has_usb_disk     - USB disk detected: true/false
    partitions[]     - Array of partition information
      device         - Device path (e.g., /dev/sda1)
      label          - Partition label
      total_space    - Total capacity
      use_space      - Used space
      free_space     - Free space
      use_percent    - Usage percentage
      file_system    - File system type
    share_enabled    - Samba share enabled: true/false
    user_name        - Access username
    wan_share_enable - WAN access enabled: "0" or "1"
```

## `usb_file_samba_set`

Configure USB file sharing (Samba)

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `share_enabled` | string | Yes | Enable Samba share: 0/false=off, 1/true=on |
| `user_name` | string | No | Access username (empty for guest access) |
| `user_pwd` | string | No | Access password (required if user_name set) |
| `wan_share_enable` | string | No | Allow WAN access: 0=off, 1=on |

### Returns

> code

### Details

```
USB File Sharing Configuration:
    Configure Samba (SMB) file sharing for USB storage
    
  Security Notes:
    - Guest access: Leave user_name empty
    - Authenticated access: Set user_name and user_pwd
    - WAN access allows external networks to access shares (use with caution)
    - Valid username characters: alphanumeric, underscore, hyphen
    
  Supported File Systems:
    NTFS, exFAT, FAT32(vfat), ext2/3/4
    
  Examples:
    Enable guest sharing (LAN only):
      {"_api":"usb_file_samba_set","share_enabled":"1"}
    
    Enable with authentication:
      {"_api":"usb_file_samba_set","share_enabled":"1","user_name":"admin","user_pwd":"secret123"}
    
    Enable with WAN access:
      {"_api":"usb_file_samba_set","share_enabled":"1","user_name":"admin","user_pwd":"secret123","wan_share_enable":"1"}
    
    Disable sharing:
      {"_api":"usb_file_samba_set","share_enabled":"0"}
```

## `usb_file_format`

Format USB partition

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `device` | string | Yes | Device path to format (e.g., /dev/sda1) |

### Returns

> code

### Details

```
Format USB Partition:
    Formats a USB storage partition (default: exFAT, vfat for X5)
    
  WARNING:
    All data on the partition will be permanently lost!
    
  File System:
    Default format is exFAT (vfat for X5/X5PRO models)
    
  Examples:
    Format first partition:
      {"_api":"usb_file_format","device":"/dev/sda1"}
```

## `usb_file_format_result`

Get USB format operation result

### Parameters

None

### Returns

> code, result

### Details

```
Format Operation Result:
    Check the status of the last format operation
    
  Response Fields:
    result   - Operation result: "success" or "failed"
```

## `usb_label_set`

Set USB partition label

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `device` | string | Yes | Device path (e.g., /dev/sda1) |
| `label` | string | No | New partition label (empty to clear) |

### Returns

> code

### Details

```
Set Partition Label:
    Changes the volume label of a USB partition
    
  Supported File Systems:
    exFAT, FAT32(vfat), ext2/3/4, NTFS
    
  Note:
    For exFAT, the partition will be temporarily unmounted during label change
    Lowercase labels on vfat/exfat may not be visible in Windows
    
  Examples:
    Set label:
      {"_api":"usb_label_set","device":"/dev/sda1","label":"MyUSB"}
    
    Clear label:
      {"_api":"usb_label_set","device":"/dev/sda1","label":""}
```

## `usb_safe_remove`

Safely remove USB device

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `force` | integer | No | Force unmount even if busy: 0=normal, 1=force  
(Values: 0 | 1) |

### Returns

> code, mount_points

### Details

```
Safely Remove USB Device:
    Unmounts USB storage devices safely to prevent data corruption
    
  Response Fields:
    mount_points   - Array of unmounted mount points
    
  Note:
    Always use safe removal before physically disconnecting USB storage
    Force option may cause data loss if files are being written
    
  Examples:
    Normal removal:
      {"_api":"usb_safe_remove"}
    
    Force removal:
      {"_api":"usb_safe_remove","force":1}
```
