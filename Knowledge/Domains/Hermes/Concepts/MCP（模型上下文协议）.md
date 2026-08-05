---
name: MCP（模型上下文协议）
type: connection
status: core
source: "[[Hermes教程-模块二-能力篇]]"
domain: hermes
---

# MCP（模型上下文协议）

## 类型判定
连接型 — 它把外部工具服务器和 Agent 连接起来，是 AI Agent 的「USB 接口」。

## 是什么
MCP（Model Context Protocol）是 Anthropic 发布的开放协议，标准化了 LLM 应用与外部工具/数据源之间的通信。Hermes 通过 MCP 可以接入任何兼容 MCP 的工具服务器——GitHub API、文件系统、数据库、Stripe 支付——无需为每个服务写定制集成代码。

## 输入-输出空间
**输入**：MCP Server 的配置（stdio 命令 / HTTP URL + 认证）
**输出**：MCP Server 暴露的所有工具自动注册为 Hermes tool → Agent 可以直接调用

## 正例（≥2个）
- GitHub MCP Server：在 Hermes 里 `create_issue`、`search_code`——Agent 直接操作 GitHub
- 文件系统 MCP Server：Agent 可以读写指定目录的文件
- 魔搭广场 MCP：modelscope.cn 提供的 MCP 目录，大量预配置工具

## 反例/边界（≥1个）
- stdio vs HTTP 两种传输：本地 server 用 stdio（进程通信），远程 server 用 HTTP + OAuth 2.1
- 工具白名单/黑名单：`tools.include` / `tools.exclude` 精确控制暴露哪些工具
- 不是所有 MCP Server 都能直接用——有些需要额外的 API Key（如 Stripe MCP Server 需要 Stripe API Key）
- MCP Server Mode（反向）：Hermes 也可以**作为 MCP Server**暴露给 Claude Desktop/VS Code，让别人调用 Hermes 的工具

## 详细解释
两种传输方式配置：
```yaml
mcp_servers:
  # stdio 模式 — Hermes 启动一个本地进程
  project-fs:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]

  # HTTP 模式 — 连接已运行的服务
  company_api:
    url: "https://mcp.internal.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

**MCP Server Mode 反向暴露**：在 Claude Desktop 里配置 `hermes mcp serve` → Claude 可以调用 Hermes 的所有工具（terminal、web_search、browser 等）。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| MCP Server Mode | Hermes 作为 MCP Server → Claude Desktop/VS Code 调用 Hermes 工具 |
| Nous MCP Catalog | v0.15+：hermes mcp catalog → 浏览精选 MCP Server |
| OAuth 2.1 授权 | HTTP MCP Server 支持浏览器式 OAuth → token 缓存复用 |

### 工具白名单
```yaml
mcp_servers:
  github:
    tools:
      include: [list_issues, create_issue]
      exclude: [delete_repo]
      resources: false
      prompts: false
```


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### ← 被指向
- [[Tool／Toolset（工具集）]] (depends-on) — MCP 工具注册到 toolset 供 Agent 调用
- [[Gateway（消息网关）]] (depends-on) — Gateway 可在启动时加载 MCP Server