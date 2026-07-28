---
name: Headless Mode（无头模式）
type: system
status: core
source: "[[Hermes-Grok-集成方案-全量审核]]"
domain: grok-build
---

# Headless Mode（无头模式）

## 类型判定
系统型 — Headless 模式是 Grok 的非交互运行方式，**是 Hermes 集成 Grok 的唯一接口面**。

## 是什么
Headless 模式通过 `grok -p "任务"` 非交互地执行编码任务，完成后输出 JSON 结果。不需要 TUI、不需要人工审批（配 `--yolo` 后），适合脚本、CI 和 Hermes 自动调度。

## 输入-输出空间
- **输入**：CLI 参数（`-p` 任务、`-m` 模型、`--cwd` 工作目录、`--yolo` 自动批准、`--output-format json`）
- **输出**：JSON 对象（`text`、`stopReason`、`sessionId`、`usage`）或 `streaming-json`（NDJSON 事件流）

## 正例（≥2个）
1. **Hermes 集成**：`grok -m deepseek-v4 -p "写 RAG demo" --yolo --output-format json --cwd E:/project`
2. **CI/CD**：`grok -p "修复 CI 报错" --yolo --cwd $GITHUB_WORKSPACE`
3. **续接**：`grok -p "测试失败，修复" --resume <session_id>` —— 加载历史上下文

## 反例/边界（≥1个）
- Headless 下首次运行需要 OAuth 认证——但用 `-m` 选自定义模型（DeepSeek）+ API Key 认证可跳过
- `--max-turns` 是 headless-only 旗标，TUI 里无效
- `--output-format json` 输出单 JSON 对象；`streaming-json` 输出 NDJSON 事件流（v0.2 支持）

## 详细解释
核心旗标（Hermes 集成必用）：
```bash
grok \
  -m deepseek-v4 \                      # 选 DeepSeek 省钱
  -p "任务描述" \                        # 自然语言任务
  --output-format json \                # JSON 输出供 adapter 解析
  --yolo \                              # 自动批准工具调用
  --cwd /absolute/path \                # 工作目录（Win 用 E:/x 格式）
  --max-turns 30 \                      # 限深防死循环
  --allow "Bash(git*)" \               # 权限规则
  --deny "Bash(rm -rf*)"                # 禁止危险操作
```

## 细节备注

### 结果 JSON 核心字段
| 字段 | 含义 |
|------|------|
| `text` | Grok 最终回复全文 |
| `stopReason` | `EndTurn`=正常结束，`max_turns_reached`=被截断 |
| `sessionId` | UUID，续接凭证 |
| `num_turns` | 走了几轮工具循环 |
| `usage` | token 消耗（input/output/total） |

### 安全三层
| 层 | 旗标 | 效果 |
|----|------|------|
| 工具白名单 | `--tools "a,b"` | 只给这些工具 |
| 权限规则 | `--allow/--deny` | glob 匹配，deny 优先 |
| 沙箱 | `--sandbox <profile>` | 文件系统/网络隔离 |

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### 依赖 (depends-on)
- [[Custom Models（自定义模型）]] — `-m` 选模型
- [[Goal Orchestration（目标编排）]] — Headless 内部跑同样的编排流水线

### ← 被指向
- [[Hermes-Grok Integration（Hermes-Grok 集成）]] — Adapter 通过本模式调用 Grok
