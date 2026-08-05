---
name: Hook（钩子系统）
type: connection
status: core
source: "[[Hermes教程-模块三-进化篇]]"
domain: hermes
---

# Hook（钩子系统）

## 类型判定
连接型 — Hook 连接生命周期的「关键时刻」和「自定义代码」，是 Agent 的插件化拦截机制。

## 是什么
Hook 是 Hermes 的事件拦截系统。在 Agent 运行的关键时刻（工具执行前后、LLM 调用前后、会话开始/结束），自动执行用户自定义的脚本或插件代码。三种 Hook 类型：Shell Hook（任意语言脚本）、Plugin Hook（Python 插件）、Gateway Hook（消息平台专用）。

## 输入-输出空间
**输入**：事件触发 → stdin 传入 JSON payload（含 tool_name、parameters、session_id 等）
**输出**：脚本 stdout 返回 JSON 决定行为——`{"action":"allow"}` 放行 / `{"action":"block","reason":"..."}` 阻止

## 正例（≥2个）
- `pre_tool_call` 安全拦截：检测 `rm -rf /` → 返回 block → 阻止执行
- `on_session_end` 桌面通知：会话结束 → PowerShell 弹出"Session finished"提示
- `post_tool_call` token 记录：每次 web_search → 记录时间戳到日志

## 反例/边界（≥1个）
- 只有 `pre_tool_call` 能阻止执行——其他 hook 都是观察型，不能影响流程
- Shell Hook 的 command 必须是可执行文件路径（Linux 需 `chmod +x`，Windows 需指定完整路径）
- Hook 超时（默认 15s）后自动跳过，不影响 Agent 运行
- 首次运行新 hook 需要用户批准（`hooks_auto_accept: true` 可跳过）

## 详细解释
三种 Hook 对比：

| 维度 | Shell Hook | Plugin Hook | Gateway Hook |
|------|-----------|-------------|--------------|
| 语言 | 任意 | Python | Python |
| 环境 | CLI+Gateway | CLI+Gateway | Gateway only |
| 注册 | config.yaml hooks: | plugin register() | hooks/name/HOOK.yaml |

常见事件：`pre_tool_call`、`post_tool_call`、`pre_llm_call`、`post_llm_call`、`on_session_start`、`on_session_end`、`gateway:startup`、`session:start`、`agent:step`、`command:*`。

## 细节备注

### 子特性
| 特性 | 说明 |
|------|------|
| stdin JSON payload | Hook 脚本从 stdin 接收 JSON |
| hooks_auto_accept | true → 新 hook 首次无需批准 |
| 非阻塞 | 超时（默认 15s）+ 错误捕获 → 不影响 Agent |

### 三种 Hook 对比
| 维度 | Shell | Plugin | Gateway |
|------|-------|--------|---------|
| 语言 | 任意 | Python | Python |
| 环境 | CLI+Gateway | CLI+Gateway | 仅 Gateway |
| 注册 | config.yaml | register(ctx) | hooks/NAME/HOOK.yaml |


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Agent Loop（Agent 循环）]] — Hook 在循环的关键节点触发

### ← 被指向
- [[Plugin（插件系统）]] (depends-on) — Plugin Hook 是 Plugin 的一种能力