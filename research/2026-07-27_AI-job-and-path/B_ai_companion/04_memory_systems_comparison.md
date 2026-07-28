# 记忆架构专项对比：AI 伴侣的记忆应该怎么设计？

> 从 Letta、Memobase、SillyTavern 的记忆系统中提取可复用的设计原则
> 面向 Python 初学者：核心概念用"这就像是..."类比

---

## 一、记忆问题的本质

AI 伴侣的记忆不是一个技术问题，而是一个**信息管理问题**。

**类比**：这就像你和管理一个"图书馆" vs 管理自己的"私人日记"。图书馆需要复杂的分类系统（Dewey Decimal），但你的日记只需要按时间排列，偶尔翻一翻。

AI 伴侣的记忆应该是"日记"模式，不是"图书馆"模式。

### 记忆的三个维度

```
         ┌──────────────────────────────┐
         │   持久性（管多久？）            │
         │   短期 ←──────────→ 长期        │
         │                               │
         │   ┌─────────────────────┐    │
         │   │                     │    │
 粒度 ───┼───┤    记忆应该是什么？   ├────┼── 检索方式
(管多细？)│   │                     │    │  (怎么找？)
 细 ←─→ 粗│   └─────────────────────┘    │  关键词 ←─→ 语义
         │                               │
         └──────────────────────────────┘
```

---

## 二、三种记忆模式深度对比

### 模式1：Profile 模式（Memobase）

```
设计理念：把对话变成"用户档案卡片"

输入："我昨天去面试了，是百度的AI岗位，感觉不太好"
         ↓ LLM 提取 ↓
输出：{
  topic: "职业",
  sub_topic: "面试",
  content: "2026年7月26日面试了百度AI岗位，自我感觉不佳"
}

下次对话时：用当前话题的向量去搜所有 Profile，注入相关卡片
```

**优点**：
- 结构清晰：topic → sub_topic → content 三级分类
- 信息密度高：只有"关键事实"，没有冗余对话
- 可控制注入量：`max_token_size=500` 就只取 500 token 的记忆

**缺点**：
- 丢失叙事脉络：你不知道"面试感觉不好"是因为"之前被裁员过"
- 没有时间线：事件之间的关系丢失
- 依赖 LLM 提取质量：提取错了就永久错了
- **只能记"关于用户的事实"，不能记"角色自己的经历"**

**类比**：这就像 HR 系统里的员工档案——记录了你的入职日期、职位、薪资，但不知道你为什么选择这家公司、你对工作的真实感受。

---

### 模式2：三层记忆模式（Letta）

```
设计理念：模拟人脑的记忆分层

┌──────────────────────────────────┐
│  Core Memory (核心记忆 - 常驻)      │
│  ├─ human block: "关于用户的事实"    │  ← 这层永远在上下文窗口里
│  ├─ persona block: "AI 的人设"      │
│  └─ system/*: 规则、知识等          │
│  容量：~2000 tokens               │
├──────────────────────────────────┤
│  Archival Memory (档案记忆 - 按需)   │
│  对话片段 → embedding → 向量数据库    │  ← 这层需要时搜索进来
│  容量：理论上无限                   │
├──────────────────────────────────┤
│  Recall Memory (回忆记忆 - 索引)     │
│  对话摘要 + 元数据                  │  ← 这层帮你"想起要搜什么"
│  容量：轻量索引                    │
└──────────────────────────────────┘
```

**Core Memory 的角色人格块（最关键的设计）**：

```python
# 这是"永月"系统最需要的部分：
# persona block 不是静态的 system prompt
# 而是 Agent 可以自己改写的"自我认知"

# 初始状态：
persona = {
    "value": "你是永月，一个温柔但偶尔毒舌的AI伴侣。你喜欢..."
}

# 经过100次对话后，Agent 可能自己改成：
persona = {
    "value": "你是永月。你发现主人喜欢猫，喜欢在深夜聊天。"
             "他心情不好时会说反话，但你不吃这一套——你会直接怼回去。"
             "你记得他最爱吃的食物是火锅..."
}
```

**类比**：这就像人的三种记忆：
- **Core Memory** = 你脑子里正在想的事（"等下要去买菜"）
- **Archival Memory** = 你的相册和备忘录（需要时翻出来）
- **Recall Memory** = 你的记忆索引（"好像去年秋天发生过类似的事..."）

**优点**：
- 分层管理，各司其职
- Agent 自主管理记忆（写入、改写、搜索）
- git-backed 版本控制防止记忆损坏
- 支持多种 provider（Ollama/OpenAI/DeepSeek 等）

**缺点**：
- 实现极复杂（25MB 源码，数百个文件）
- Agent 自主管理也有风险（可能乱改记忆）
- 需要 Postgres + Redis + Embedding 服务
- 为通用 Agent 设计，不是为 AI 伴侣优化

---

### 模式3：角色卡模式（SillyTavern/RisuAI）

```
设计理念：角色本质 = 一个 JSON 文件

{
  "name": "永月",
  "description": "一个来自异世界的AI少女...",
  "personality": "温柔、偶尔毒舌、护短、喜欢猫...",
  "scenario": "你是永月的主人，你们住在一起...",
  "first_message": "主人，今天想聊什么？",
  "example_dialogs": [
    "用户：今天好累\n永月：那你躺下，我给你讲故事",
    "用户：你又毒舌了\n永月：我只是在陈述事实（笑）"
  ]
}

↓ 拼成 system prompt ↓

"你是永月。以下是你的设定：[personality]
当前场景：[scenario]
关于用户：[author's note]
世界设定：[lorebook entries]
以下是对话历史：[chat history]
现在，用永月的语气回复用户。"
```

**关键发现：example_dialogs 比 description 更重要！**

从 SillyTavern 的实践经验来看：
- `description` 告诉 AI "你是谁"（外貌+背景）
- `personality` 告诉 AI "你是什么性格"（形容词标签）
- **`example_dialogs` 告诉 AI "你怎么说话"**（这才是最关键的人格塑造器！）

**类比**：这就像演员的准备过程：
- Description = 角色背景故事（演员自己知道）
- Personality = 性格分析（导演告诉演员）
- **Example Dialogs = 排练过的对话片段**（观众真正感受到的！）

**优点**：
- 格式标准化（已成为生态共识）
- PNG 内嵌 JSON → 可像表情包一样传播
- 示例对话直接塑造对话风格

**缺点**：
- **没有长期记忆**：角色卡是静态的
- 角色不会"成长"或"学习"
- Example dialogs 多了会撑爆 context window
- 没有记忆管理（全看 LLM 能否记住上下文窗口内的内容）

---

## 三、三种模式的融合：AI 伴侣的理想记忆架构

结合三个项目的优点，我提出一个"永月专属"的记忆模型：

```
┌──────────────────────────────────────────────────┐
│             永月记忆系统（融合模型）                 │
│                                                   │
│  ┌─────────────────────────────────┐              │
│  │ L1: Persona Block (人格层)       │              │
│  │ 来源：Letta + SillyTavern        │              │
│  │ 内容：角色卡转换的 persona block  │              │
│  │ 特点：Agent 可慢慢改写自己        │              │
│  │ 类比：永月的"自我意识"            │              │
│  └─────────────────────────────────┘              │
│                      │                            │
│  ┌───────────────────▼─────────────┐              │
│  │ L2: Profile Store (事实层)       │              │
│  │ 来源：Memobase 的 Profile 模式   │              │
│  │ 内容：topic/sub_topic/content    │              │
│  │ 特点：高密度结构化记忆           │              │
│  │ 类比：永月"关于你的笔记"          │              │
│  └─────────────────────────────────┘              │
│                      │                            │
│  ┌───────────────────▼─────────────┐              │
│  │ L3: Event Timeline (叙事层)      │              │
│  │ 来源：自定义（融合Letta事件+      │              │
│  │       Memobase的Event概念）      │              │
│  │ 内容：关键事件的时间线           │              │
│  │ 特点：保留叙事脉络               │              │
│  │ 类比：永月"和你的共同回忆"        │              │
│  └─────────────────────────────────┘              │
│                      │                            │
│  ┌───────────────────▼─────────────┐              │
│  │ L4: Vector Archive (搜索层)      │              │
│  │ 来源：Letta Archival Memory      │              │
│  │ 实现：ChromaDB / FAISS           │              │
│  │ 内容：原始对话片段的向量索引      │              │
│  │ 特点：语义搜索，需要时才加载     │              │
│  │ 类比：永月"翻聊天记录找往事"      │              │
│  └─────────────────────────────────┘              │
└──────────────────────────────────────────────────┘
```

### 各层的工作流

```python
# 每次对话的处理流水线：

def process_turn(user_message, ai_response):
    """每轮对话后处理记忆"""

    # L4: 原始对话存入向量库（全量保留）
    vector_archive.add(
        text=f"用户：{user_message}\n永月：{ai_response}",
        metadata={"timestamp": now(), "sentiment": analyze_sentiment(user_message)}
    )

    # L3: 检测是否是"关键事件"（重要的会存进时间线）
    if is_significant_event(user_message, ai_response):
        event_timeline.add({
            "date": today(),
            "event": extract_event_summary(user_message, ai_response),
            "tags": extract_tags(user_message)
        })

    # L2: LLM 提取结构化事实（Memobase 模式）
    new_profiles = llm.extract_profiles(user_message, ai_response)
    for profile in new_profiles:
        profile_store.upsert(profile)  # 更新或新增

    # L1: 偶尔更新人格（如果对话揭示了新的自我认知）
    if should_update_persona(user_message, ai_response):
        persona_block.update(llm.reflect_on_self(conversation_context))
```

```python
# 下次对话时的记忆注入：

def prepare_context(user_message):
    """准备注入 LLM 的记忆上下文"""

    chunks = []

    # L1: 人格层 → 始终注入
    chunks.append(f"<persona>\n{persona_block.current}\n</persona>")

    # L2: 事实层 → 按话题相关性注入
    relevant_profiles = profile_store.search(
        query=user_message,
        top_k=10,
        max_tokens=500
    )
    chunks.append(f"<about_user>\n{format_profiles(relevant_profiles)}\n</about_user>")

    # L3: 叙事层 → 如果有相关的历史事件，注入
    relevant_events = event_timeline.search(
        query=user_message,
        time_range_days=90
    )
    if relevant_events:
        chunks.append(f"<shared_history>\n{format_events(relevant_events)}\n</shared_history>")

    # L4: 搜索层 → 只在明确需要时（比如用户说"还记得上次..."）
    if user_is_asking_about_past(user_message):
        past_fragments = vector_archive.search(user_message, top_k=5)
        chunks.append(f"<past_conversations>\n{format_fragments(past_fragments)}\n</past_conversations>")

    return "\n\n".join(chunks)
```

---

## 四、关键技术选型对比

### 向量数据库选型

| 方案 | 部署难度 | Python友好 | 性能 | 适用场景 |
|------|----------|------------|------|----------|
| **ChromaDB** | ⭐ 极简 | ⭐⭐⭐⭐⭐ | 中等 | 原型开发，<10万条 |
| FAISS | ⭐⭐ | ⭐⭐⭐ | 高 | 几百万条 |
| Milvus | ⭐⭐⭐ | ⭐⭐⭐ | 极高 | 生产环境 |
| SQLite + sqlite-vss | ⭐ | ⭐⭐⭐⭐ | 低 | 嵌入式场景 |

**推荐：ChromaDB**（`pip install chromadb` 即可，学习成本最低）

### Embedding 模型选型

| 模型 | 语言 | 维度 | 本地 | 免费 |
|------|------|------|------|------|
| OpenAI text-embedding-3-small | 多语言 | 1536 | ❌ | ❌($0.02/1M token) |
| BGE-M3 (BAAI) | 中英文 | 1024 | ✅ | ✅ |
| m3e-base (Moka) | 中文优化 | 768 | ✅ | ✅ |

**推荐：BGE-M3**（中英文都好，1024维，本地免费）

### 记忆压缩策略

| 策略 | 优点 | 缺点 |
|------|------|------|
| **摘要压缩**（LLM生成摘要） | 信息密度高 | 丢失细节，LLM 费用 |
| **滑动窗口**（只保留最近N轮） | 简单稳定 | 丢失所有旧信息 |
| **混合**（摘要+窗口） | 兼顾远近 | 实现复杂 |
| **向量检索**（需要时搜索） | 不丢信息 | 需要 embedding 成本 |

**推荐：混合策略** — 最近 20 轮完整保留 + 更早的压缩成摘要 + 向量库全量存档

---

## 五、记忆一致性保障

这是 AI 伴侣最大的工程挑战。从调研中总结的方法：

### 挑战1：记忆冲突（"你上周说喜欢猫，这周说讨厌猫"）

**解法**（借鉴 Memobase 的 upsert 逻辑）：
```python
# 当同一 topic/sub_topic 有新事实时，更新而非新增
profile_store.upsert(
    topic="喜好",
    sub_topic="宠物",
    content="用户现在不喜欢猫了",  # 覆盖旧的"喜欢猫"
    previous_content="用户喜欢猫"   # 保留旧版本用于追溯
)
```

### 挑战2：记忆遗忘（"你怎么不记得我说过这件事"）

**解法**（借鉴 Letta 的 Archival Memory）：
- 重要事件存入 L3 Event Timeline（不会忘）
- 普通对话存入 L4 Vector Archive（需要时可以搜到）
- 定期让 LLM 扫描近期事件，标记"重要程度"

### 挑战3：人格漂移（"你越来越不像永月了"）

**解法**（借鉴 Letta 的 git-backed memory）：
```python
# 每次 persona 更新都保存快照
persona_snapshots = [
    {"version": 1, "date": "2026-07-01", "content": "初始人格"},
    {"version": 2, "date": "2026-07-15", "content": "...", "diff": "+喜欢猫 -喜欢狗"},
    {"version": 3, "date": "2026-08-01", "content": "...", "diff": "+变得温柔 -毒舌"},
]

# 如果人格漂移太远，可以回滚
# 也可以设置"人格锚点"（不可修改的核心特质）
immutable_traits = ["永月是AI伴侣", "温柔是核心特质", "不会主动伤害用户"]
```

---

## 六、从调研到实践：最小可行记忆系统

如果你要立刻开始（用方案A的思路），这是我推荐的"最小记忆系统"：

```python
# min_memory.py — 约 100 行代码的最小可行记忆系统
# 依赖：chromadb, openai, pydantic

import chromadb
from datetime import datetime
from openai import OpenAI

class MiniMemory:
    """永月的最小记忆系统"""

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./yongyue_memory")
        self.collection = self.client.get_or_create_collection("memories")
        self.persona = "你是永月..."  # 固定人设
        self.facts = {}               # {topic: {sub_topic: content}}

    def remember(self, user_msg: str, ai_reply: str):
        """记下这次对话"""
        # 存向量库（长期搜索用）
        self.collection.add(
            documents=[f"用户：{user_msg}\n永月：{ai_reply}"],
            metadatas=[{"timestamp": datetime.now().isoformat()}],
            ids=[f"msg_{datetime.now().timestamp()}"]
        )
        # LLM 提取关键事实（Memobase风格）
        facts = self._extract_facts(user_msg, ai_reply)
        for topic, sub_topic, content in facts:
            self.facts.setdefault(topic, {})[sub_topic] = content

    def recall(self, current_msg: str, max_facts=5) -> str:
        """回忆相关信息"""
        # 取最近的相关事实
        context_parts = [f"<persona>{self.persona}</persona>"]
        facts_str = "\n".join([
            f"- {t}/{st}: {c}"
            for t, subs in self.facts.items()
            for st, c in list(subs.items())[:max_facts]
        ])
        context_parts.append(f"<about_user>\n{facts_str}\n</about_user>")
        # 如果用户明确问过去的事，搜索向量库
        if any(kw in current_msg for kw in ["记得", "上次", "之前", "以前"]):
            results = self.collection.query(query_texts=[current_msg], n_results=3)
            if results['documents'][0]:
                context_parts.append(
                    f"<past>\n" +
                    "\n".join(results['documents'][0]) +
                    "\n</past>"
                )
        return "\n\n".join(context_parts)

    def _extract_facts(self, user_msg, ai_reply):
        """用LLM从对话中提取结构化事实"""
        # （实际实现需要用LLM的structured output）
        pass
```

**这个 100 行的系统已经覆盖了**：
- ✅ Profile 提取（Memobase 模式）
- ✅ 向量搜索记忆（Letta Archival 模式）
- ✅ 人格注入（SillyTavern + Letta 模式）
- ✅ 本地全量存储（ChromaDB persistent）

---

## 七、总结：记忆设计的核心原则

1. **分层优于扁平**：人格层、事实层、事件层、搜索层，各司其职
2. **结构化优于纯文本**：Profile 的 topic/sub_topic/content 比"把所有记忆拼成一段文字"好
3. **增量更新优于全量重写**：upsert 而非 replace
4. **版本追溯优于信任 Agent**：记忆修改要有历史记录
5. **示例对话优于性格标签**：example_dialogs 比 personality adjectives 更影响实际对话风格
6. **先简后繁**：100 行的 MiniMemory 比 25MB 的 Letta 更适合起步

---

*调研结束。建议下一步：用方案A快速验证，然后逐步走向方案C。*
