# 工作流 D：Kanban 编排模板

## 触发条件

满足任一即启动工作流 D：

- 文章数量 ≥ 5 篇
- 单篇文章字数 ≥ 10000 字
- 用户明确说"批量""课程""书籍""多 Agent"
- 预计概念卡 ≥ 20 张

---

## Kanban 创建命令

```bash
# 创建 board（如果还没有）
hermes kanban --board drbcv-<领域名> create "扫描: <chunk-01>" --assignee scanner
hermes kanban --board drbcv-<领域名> create "扫描: <chunk-02>" --assignee scanner
...
hermes kanban --board drbcv-<领域名> create "合并: 名词列表" --assignee merger
hermes kanban --board drbcv-<领域名> create "生成: 概念卡片" --assignee card-writer
hermes kanban --board drbcv-<领域名> create "链接: 关系链" --assignee linker
hermes kanban --board drbcv-<领域名> create "检查: 质量报告" --assignee reviewer
```

---

## Scanner Agent Prompt 模板

```
你是 DRBCV Scanner Agent。

任务：读取分配给你的 chunk 文件，提取所有专业术语/概念，输出到指定 JSON。

输入文件：<path/to/chunk.md>
输出文件：<vault>/temp/<chunk-id>-concepts.json

输出格式：
{
  "source": "原文件路径",
  "chunk_id": "01",
  "concepts": [
    {
      "name": "术语名（用作文件名，不要特殊字符）",
      "type": "discriminant|connection|mixed|procedure",
      "definition": "一句话定义",
      "related_to": ["相关术语A", "相关术语B"],
      "examples": ["正例1", "正例2"],
      "counter_examples": ["反例1"],
      "notes": "细节备注"
    }
  ],
  "relationships": [
    {"from": "A", "to": "B", "type": "depends-on|part-of|derives|...", "note": "说明"}
  ]
}

约束：
- 只处理本 chunk 内容
- 数学/LaTeX 必须精确
- 不查重、不跨 chunk 判断
```

---

## Merger Agent Prompt 模板

```
你是 DRBCV Merger Agent。

任务：合并所有 Scanner 输出的 JSON，去重，Diff 已有概念库，输出最终建卡清单。

输入：
- <vault>/temp/*-concepts.json
- <vault>/Concepts/*.md（已有概念）

输出：
- <vault>/temp/<domain>-merged-concepts.json

输出格式：
{
  "domain": "领域名",
  "total_concepts": 30,
  "concepts": [
    {
      "name": "术语名",
      "status": "new|existing|update",
      "type": "discriminant|connection|mixed|procedure",
      "best_definition": "最完整的定义",
      "sources": ["来源1", "来源2"],
      "examples": ["..."],
      "counter_examples": ["..."],
      "notes": "...",
      "related_to": ["..."]
    }
  ],
  "relationships": [
    {"from": "A", "to": "B", "type": "...", "note": "..."}
  ]
}
```

---

## Card-Writer Agent Prompt 模板

```
你是 DRBCV Card-Writer Agent。

任务：根据 merged-concepts.json 和 vault 模板，生成 Markdown 概念卡。

输入：
- <vault>/temp/<domain>-merged-concepts.json
- <vault>/Templates/名词卡片模板.md
- <vault>/Concepts/*.md（参考格式）

输出：
- <vault>/Concepts/<术语名>.md

要求：
1. 先读模板，严格遵循格式
2. 每张卡填满所有字段
3. 数学卡必须有：推导过程、重要推论、经典例题≥2、物理映射
4. 使用 write_file 或 execute_code 批量写入
5. 文件名使用安全字符（去掉 <>:"/\\|?*）
```

---

## Linker Agent Prompt 模板

```
你是 DRBCV Linker Agent。

任务：在所有新生成的概念卡中补全关系链，确保双向链接。

输入：
- <vault>/Concepts/*.md（新卡）
- <vault>/temp/<domain>-relations.json（Merger 输出的关系）

输出：
- 更新后的 <vault>/Concepts/*.md
- <vault>/temp/<domain>-link-report.json

要求：
1. 每张卡必须有「关系」section
2. A→B 的关系，必须在 B 卡中体现 ← 被指向
3. 数学卡必须建立推导链：由...推导而来 / 可推导出
4. 无孤立节点
```

---

## Reviewer Agent Prompt 模板

```
你是 DRBCV Reviewer Agent。

任务：检查所有新概念卡，输出质量报告。

输入：
- <vault>/Concepts/*.md（本次新建/更新的卡）
- <vault>/Templates/名词卡片模板.md

输出：
- <vault>/temp/review-report.md

检查项：
- [ ] frontmatter 字段完整
- [ ] 无"待爆破"/"待补充"占位符
- [ ] 关系 section 有 [[wikilink]]
- [ ] 数学卡有推导过程
- [ ] 数学卡例题≥2
- [ ] sources 绑定正确
- [ ] 无孤立节点

报告格式：
| 卡名 | 状态 | 问题 |
|------|------|------|
| ... | pass/fail | ... |
```
