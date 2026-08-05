---
name: Plugin（插件系统）
type: system
status: core
source: "[[Hermes教程-模块三-进化篇]]"
domain: hermes
---

# Plugin（插件系统）

## 类型判定
系统型 — Plugin 是 Hermes 的可扩展架构：不改核心代码，通过 `register(ctx)` 函数添加自定义工具、Hook、命令、平台、Provider。

## 是什么
Hermes 插件系统允许用户和开发者通过独立的插件目录扩展 Agent 能力。一个插件最少只需两个文件：`plugin.yaml`（元信息）+ `__init__.py`（定义 `register(ctx)` 函数）。在 `register` 中可以注册工具、Hook、命令、会话注入、Skill、Gateway 平台、后端 Provider。

## 输入-输出空间
**输入**：`~/.hermes/plugins/<name>/` 目录 + `hermes plugins enable <name>`
**输出**：插件注册的工具出现在 toolset 中、Hook 在事件触发时执行、命令可被 `/name` 调用

## 正例（≥2个）
- `shake_window`：注册一个工具，让 Windows 前台窗口晃动——纯娱乐插件，展示最小可用插件
- `seo-checker`：注册 `check_seo` 工具，审核博客文章的 SEO 元数据质量
- 消息平台插件：接入新的消息平台（如 DingTalk）而无需修改 Hermes 核心代码

## 反例/边界（≥1个）
- 新安装插件默认不启用——必须 `hermes plugins enable <name>` 或加入 `config.yaml` 的 `plugins.enabled`
- `plugins.disabled` 是拒绝列表——同时出现在 enabled 和 disabled 时，禁用优先
- 项目插件（`.hermes/plugins/`）默认不扫描——需 `HERMES_ENABLE_PROJECT_PLUGINS=true`
- `register(ctx)` 是唯一入口——插件不能绕过注册系统直接注入

## 详细解释
插件目录结构（最小可用）：
```
~/.hermes/plugins/hello-world/
├── plugin.yaml      # name, version, description
└── __init__.py      # def register(ctx): ctx.register_tool(...)
```

插件来源：Bundled（内置）、User（~/.hermes/plugins/）、Project（.hermes/plugins/）、pip（hermes_agent.plugins entry points）。

`ctx` 可访问：`register_tool()`（注册工具）、`register_hook()`（注册 Hook）、`register_command()`（注册命令）、`llm`（v0.14+，直接调用模型）。

## 细节备注

### 四种发现来源
| 来源 | 路径 | 默认 |
|------|------|------|
| Bundled | Hermes 仓库 plugins/ | 随版本 |
| User | ~/.hermes/plugins/ | 手动 |
| Project | .hermes/plugins/ | 需环境变量 |
| pip | entry points | 自动 |

### 最小可用插件
plugin.yaml + __init__.py（def register(ctx): ...）
- 安装后默认不启用 → 须 hermes plugins enable
- ctx.llm（v0.14+）→ 插件内直接调用当前模型


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Tool／Toolset（工具集）]] — 注册的工具进入 toolset 供 Agent 调用
- [[Hook（钩子系统）]] — 注册的 Hook 在事件触发时执行

### ← 被指向
- [[Custom Provider（自定义提供商）]] — v0.13+ Provider 也可作为 Plugin 分发