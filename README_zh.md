# Oraybox HTTP API 工具包

[English](README.md) | [中文](README_zh.md)

Oray 路由器管理 API 的 Python HTTP 客户端与参考文档。

## 概述

Oray 路由器通过 HTTP POST 到 `/cgi-bin/oraybox` 暴露管理 API。
本仓库提供了一个技能包（`oraybox-http-api/`），包含：

- 轻量 Python 封装（`OrayboxHttpAPI`），用于 HTTP API 调用。
- 按类别划分的完整 API 参考文档，便于高效检索。

## 仓库结构

```
oraybox_api_skills/
├── README.md              # 英文说明
├── README_zh.md           # 本文件（中文说明）
├── AGENTS.md              # 智能体指南
├── tests/                 # 单元测试
│   └── test_client.py
├── scripts/               # 构建 / 打包脚本
│   └── package.sh
└── oraybox-http-api/      # 技能根目录（打包分发）
    ├── SKILL.md           # 技能入口
    ├── scripts/
    │   └── oraybox_http_api.py   # 核心 Python 客户端
    └── references/               # 按类别划分的 API 文档
        ├── index.md
        ├── system.md
        ├── network.md
        ├── dhcp.md
        ├── wifi.md
        ├── port-forward.md
        ├── device.md
        ├── diagnostics.md
        ├── flowrate.md
        ├── service-control.md
        ├── behaviour.md
        ├── acl.md
        ├── group-support.md
        ├── mwan3.md
        ├── traffic-control.md
        ├── dmz.md
        ├── snmp.md
        ├── upnpd.md
        ├── app-traffic.md
        └── usb-file.md
```

## 快速开始

```python
from oraybox-http-api.scripts.oraybox_http_api import OrayboxHttpAPI

client = OrayboxHttpAPI(host="192.168.1.1", password="admin")
info = client.call("sys_base_info")
wifi = client.call("wifi_get", dev="2.4G", tag=1)
```

## 配置说明

### 环境变量

当未显式提供 `host` 或 `password` 时，客户端会读取以下环境变量：

| 变量 | 说明 | 显式覆盖 |
|------|------|----------|
| `ORAYBOX_HOST` | 路由器 IP 或主机名 | `host=` 参数 |
| `ORAYBOX_PASSWORD` | 路由器管理员密码 | `password=` 参数 |

在 shell 配置文件或当前会话中设置：

```bash
export ORAYBOX_HOST="192.168.1.1"
export ORAYBOX_PASSWORD="你的管理员密码"
```

设置后即可省略参数：

```python
client = OrayboxHttpAPI()  # 自动使用 ORAYBOX_HOST 和 ORAYBOX_PASSWORD
```

### 客户端参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `host` | str | `$ORAYBOX_HOST` | 路由器 IP 或主机名，省略时回退到 `ORAYBOX_HOST` 环境变量 |
| `password` | str | `$ORAYBOX_PASSWORD` | 管理员密码，省略时回退到 `ORAYBOX_PASSWORD` 环境变量 |
| `timeout` | int | 30 | HTTP 超时时间（秒） |
| `scheme` | str | `"http"` | URL 协议：`"http"` 或 `"https"` |
| `verify_ssl` | bool | `False` | 是否验证 SSL 证书 |
| `use_proxy` | bool | `False` | 是否使用系统 HTTP/HTTPS 代理 |

> **安全提示：** 默认使用 HTTP 明文传输密码。建议在支持时使用 HTTPS（`scheme="https"`）。SSL 验证默认关闭，因为路由器通常使用自签名证书。

## 提示词示例

在 AI 助手（如 Kimi Code）中使用该 skill 时，以下是一些典型提示词：

### 扫描路由器周围的热点

> 扫描蒲公英路由器周围的热点

Agent 会调用 `wifi_scan_get` 列出附近的无线网络：

```python
client = OrayboxHttpAPI()
result = client.call("wifi_scan_get")
# 返回: wifi_scan[] (2.4G 列表), wifi_scan_5g[] (5G 列表)
# 每项包含: mac, mode, quality, quality_max, signal, ssid, channel, encryption
```

CLI 等效命令：

```bash
python3 scripts/oraybox_http_api.py --api wifi_scan_get
```

### 查询路由器系统信息

> 查询蒲公英路由器的系统信息

调用 `sys_base_info` 获取固件版本、设备型号、运行时间等。

```bash
python3 scripts/oraybox_http_api.py --api sys_base_info
```

### 修改 WiFi 密码

> 修改蒲公英路由器的 WiFi 密码

Agent 先通过 `wifi_get` 读取当前配置，更新密码后通过 `wifi_set` 应用。

### 查看已连接的设备

> 查看蒲公英路由器上连接的设备列表

调用 `lan_device_get` 列出所有局域网客户端及其 IP、MAC 和主机名。

## 打包

构建可分发的 `.skill` 文件：

```bash
./scripts/package.sh
```

这将创建 `oraybox-http-api.skill`（技能目录的 zip 归档文件）。

## 依赖

- Python >= 3.10
- `requests`

```bash
pip install -r oraybox-http-api/requirements.txt
```

## 测试

```bash
python3 -m pytest tests/
```

## 许可

MIT
