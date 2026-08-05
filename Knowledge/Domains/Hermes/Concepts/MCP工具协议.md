---
name: MCP工具协议
type: discriminant
status: core
source: "[[工具扩展与 MCP 配置_原文]]"
domain: Hermes
---

# MCP工具协议

## 类型判定
Model Context Protocol——一种标准化的工具接口协议，使不同 Agent 框架能通用地调用同一套外部工具，支持本地和远程两种部署方式。

## 类比 ★
### 一句话比喻
就像 USB 接口标准——不管你是 Windows 还是 Mac，只要设备有 USB 接口就能即插即用。MCP 就是 AI 工具的"USB 标准"，一个工具开发好，所有支持 MCP 的 Agent 都能直接调用。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| MCP 协议 | USB 接口标准 |
| MCP 工具 | USB 设备（U盘、键盘、鼠标） |
| 本地 MCP（Stdio） | 直接插电脑的 USB 设备 |
| 远程 MCP（HTTP/SSE） | 网络打印机（通过 IP 地址连接） |
| configure.yaml 配置 | 设备管理器（配置驱动和连接） |
| Hermes 内置工具 | 电脑自带键盘触摸板 |

## 是什么
MCP（Model Context Protocol，模型上下文协议）是 Anthropic 提出的工具接口标准，允许不同 AI Agent 产品和框架通用地调用同一套工具。在 Hermes 中，MCP 工具分两类：**本地 MCP**（通过 Stdio 模式直接在本地执行命令，如 NPX 拉取的 File System 工具）和**远程 MCP**（通过 HTTP/SSE 连接远程服务器上的工具服务，如魔搭社区的 12306 查询工具）。所有 MCP 工具在 `~/.hermes/configure.yaml` 文件中统一配置。

## 正例（≥2 个）
1. **本地 File System MCP**：配置 NPX 命令 → 下载 Anthropic 的 File System 工具 → Hermes 获得文件树状展示、目录结构总结、文件内容读取等 14 个工具 → 用户说"以树状图展示张三目录"→ Agent 调用 MCP 工具执行。
2. **远程 12306 MCP**：在魔搭社区部署 12306 查询工具 → 获取 HTTP URL → 配置到 configure.yaml → Hermes 重启后能查火车票 → 用户问"北京到天津高铁有哪些"→ 调用远程 MCP 返回实时票务信息。

## 反例/边界（≥1 个）
1. **内置工具（非 MCP）**：Hermes 自带的浏览器操作工具、文件操作工具等是框架内置的，不通过 MCP 协议调用——它们不需要额外配置，但也不能跨框架复用。
2. **工具描述不清晰**：MCP 工具名称或描述写得不清楚 → Agent 无法在对话中正确识别何时应该调用 → 工具虽已配置但形同虚设。

## 详细解释
MCP 工具配置方式（configure.yaml）：
```yaml
mcp_servers:
  # 本地 MCP
  file_system:
    command: npx
    args: ["-y", "@anthropic/mcp-filesystem", "/path"]
  # 远程 MCP
  12306:
    url: https://your-deployed-mcp-server.com/mcp
    headers: {}  # 如有鉴权需求在此配置
    voice_safe: true
    timeout: 120
    client_timeout: 30
```

关键参数：
- **timeout**：工具调用的超时时间（秒）
- **client_timeout**：初始化连接工具的超时时间（秒）
- **voice_safe**：是否允许语音模式下调用该工具

安装 MCP 工具的前置步骤：
1. 确保 Node.js 环境（本地 MCP 工具通常基于 NPX）
2. 安装 UV（`pip install uv`）
3. 进入 Hermes 的 Python 虚拟环境：`~/.local/share/hermes/hermes-agent/`
4. 激活环境后安装依赖（`uv pip install mcp` 等）
5. 配置 configure.yaml → 重启 Hermes

注意事项：配置 MCP 后有时启动显示红色 fail 状态，但实际功能可能正常——已知偶发问题，重启多次或忽略状态直接用即可。

## 关系
### → 指向
- [[Hermes Agent框架]]
- [[Skill工作流封装]]
### ← 被指向
- [[Hermes Agent框架]]
