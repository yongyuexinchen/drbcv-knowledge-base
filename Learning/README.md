# 学习路线总规划

> 创建日期：2026-07-30
> 目标岗位：深圳 AI 应用开发工程师（大模型方向）
> 目标薪资：20-25K（基准）/ 25-35K（乐观）
> 核心项目：AI 伴侣系统「永月」
> 数据来源：Boss直聘 289 条深圳 AI/大模型岗位分析

---

## 一、当前水平

| 已有 | 薄弱/缺失 |
|------|----------|
| Python 基础 | 网络协议（TCP/UDP/DNS/TLS） |
| SQL + MySQL | Java/Go（42%/23% 岗位要求） |
| FastAPI 新闻模块 CRUD | Docker 容器化 |
| Git 基础 | Nginx 反向代理 |
| 黑马 V6.5 课程在读 | 记忆系统工程实践 |

---

## 二、三条线并行

```
工程线（黑马不教）        AI 线（黑马教+自研）      项目线（永月 Demo）
──────────────────       ──────────────────      ──────────────────
Git → Docker → Nginx     LangChain → Milvus       FastAPI 后端
Java Spring Boot         记忆系统（2-3套）         WebSocket 实时通信
Redis 缓存实战           Agent/Tool Calling       前端对话界面（MVP）
Go 基础（后期）          RAG 深度优化              Docker 部署上线
```

---

## 三、分阶段详细计划

### 第一阶段：打地基（第 1-3 周）

**目标：FastAPI 项目完整 + Docker 容器化 + Git 版本控制**

| 周次  | 内容                                                                     | 产出                 |
| --- | ---------------------------------------------------------------------- | ------------------ |
| 第1周 | FastAPI 用户模块（JWT + 密码哈希 + Depends 依赖注入）<br>HTTP 基础嵌入教学                 | 用户注册/登录 API        |
| 第2周 | FastAPI 收藏模块（多对多关系）<br>Git 初始化 + 首次 commit                             | 收藏功能 API           |
| 第3周 | Docker 入门：Dockerfile + docker-compose<br>把今日头条项目一键容器化（FastAPI + MySQL） | docker-compose.yml |

**HTTP 基础（嵌入第1周教学）：**
- [ ] 请求/响应模型：Method、URL、Headers、Body、Status Code
- [ ] 无状态协议：为什么每次请求是独立的
- [ ] JWT 为什么放在 Authorization Header 里
- [ ] Cookie vs Token 认证的本质区别

---

### 第二阶段：工程能力（第 4-6 周）

**目标：Nginx + Java Spring Boot + Redis 实战**

| 周次 | 内容 | 产出 |
|------|------|------|
| 第4周 | Nginx 反向代理<br>放在 FastAPI 前面，80 端口 → uvicorn 8000<br>静态文件服务 | Nginx 配置文件 |
| 第5-6周 | Java Spring Boot 入门<br>做一个「短链服务」项目：<br>- Controller/Service/Repository 三层<br>- MySQL 持久化<br>- Redis 缓存（先查 Redis → miss 再查 MySQL → 回写）<br>- 301 重定向 | 短链服务源码 |

**短链服务为什么是最好的 Java 入门项目：**
- 覆盖 Spring Boot 核心三层架构
- 天然需要 Redis 缓存（热点 URL 不能每次都查数据库）
- 短码生成算法（Base62 / 哈希冲突处理）有算法含量
- 301 重定向教你 HTTP 状态码的实际用途
- 可以做 API + 简单前端页面，简历能写两行

---

### 第三阶段：AI 核心（第 7-10 周）

**目标：LangChain + Milvus + 记忆系统调研与选型**

| 周次 | 内容 | 产出 |
|------|------|------|
| 第7周 | LangChain 入门<br>- Prompt Template<br>- Chain（顺序链/路由链）<br>- 第一个 RAG Demo（文本切分 → embedding → 检索 → 生成） | RAG Demo（命令行） |
| 第8周 | LangChain 进阶<br>- Agent + Tool Calling<br>- Memory（ConversationBuffer / Summary）<br>- 流式输出（Streaming） | Agent Demo |
| 第9周 | Milvus 向量数据库<br>- Docker 部署 Milvus<br>- Collection 设计<br>- 与 LangChain 集成<br>- 对比 Chroma（轻量方案） | 向量检索 API |
| 第10周 | 记忆系统深度调研（详见 `memory-systems/`）<br>- Mem0 完整试用<br>- Zep 完整试用<br>- Letta/MemGPT 试用<br>- 选型决策 | 记忆系统选型报告 |

**最多在记忆系统上投入 2 周深度研究，然后必须做出选型决策。**

---

### 第四阶段：永月 MVP（第 11-14 周）

**目标：AI 伴侣系统最小可用版本**

| 周次 | 内容 | 产出 |
|------|------|------|
| 第11周 | 对话引擎<br>- FastAPI WebSocket 端点<br>- LLM 流式对话<br>- System Prompt 人格设计 | 能对话的永月 |
| 第12周 | 记忆系统接入<br>- 短期记忆（当前会话）<br>- 长期记忆（跨会话）<br>- 用户画像提取 | 有记忆的永月 |
| 第13周 | Agent 能力<br>- Function Calling（天气、时间等）<br>- 主动关心（定时任务触发）<br>- 情绪系统（初版） | 能主动说话的永月 |
| 第14周 | 打包部署<br>- docker-compose（FastAPI + Milvus + Redis）<br>- Nginx + HTTPS<br>- 前端对话界面（Streamlit/Gradio MVP） | 可演示的 Demo |

---

### 第五阶段：面试冲刺（第 15-16 周）

**目标：项目打磨 + 面试话术 + 投递**

| 周次 | 内容 |
|------|------|
| 第15周 | 3 个黑马明星项目 + 永月项目：技术选型 → 踩坑 → 优化 → 效果<br>RAG/Agent 面试高频问题准备<br>LeetCode 简单题刷 30 道（Python） |
| 第16周 | 开始投递（88 条匹配岗位）<br>模拟面试<br>边面边补短板 |

---

## 四、记忆系统专项（核心重点）⚠️ 已修正

> 详见 `memory-systems/RESEARCH.md`（初版 + ChatGPT 审计修正版）
>
> **教训**：初版存在严重版本混用（Letta V1 vs Agent SDK、Mem0 V2 vs V3）、LangChain API 过时、过度拔高工具能力等问题。经 ChatGPT 审计后修正。

### 核心思路转变

> **不是"先调研再选一个"，而是"先手写再看工具替你做了什么"。**

```
❌ 旧思路：调研 → 选 Letta → 按 Letta 的方式做
✅ 新思路：手写最小闭环 → 用 LangGraph 标准化 → 对照 Mem0/Letta → 实测选型
```

### 五步学习路径

```
第 1 步（第 10 周前半）
  手写最小记忆闭环：FastAPI + PostgreSQL
  四个核心对象：
    agent_identity     永月是谁
    user_profile       用户是谁
    relationship_state 关系状态
    memory_event       事件时间线
  手写流程：对话 → LLM 提取 → 分类 → 存储 → 检索 → 注入 Prompt

第 2 步（第 10 周后半）
  LangGraph 持久化（非老式 Memory 类！）
  学习：LangGraph State / Checkpointer / Store / Thread ID
  用 LangGraph 替代手写 PostgreSQL 操作

第 3 步（第 11 周）
  Mem0 V3 对照实验
  接入 Mem0，对比它能替代手写流程中的哪些部分
  重点观察：agent_id 维度隔离是否够用

第 4 步（第 12 周，独立试验）
  Letta Agent SDK 独立试验（不进主项目）
  注意：新版 SDK 是 TypeScript，可能需要额外学习
  重点研究：MemFS / Dreaming / 人格连续性

第 5 步（第 12 周末）
  统一测评
  同一组测试对话 → 分别跑手写 / Mem0 / Letta
  用实际数据做最终选型，不绑定某个框架
```

### AI 伴侣人格六层模型（你的设计责任，工具帮不了）

```
L1  Identity          我是谁，核心价值不可变
L2  Human Profile     我对用户的长期认识
L3  Relationship      我们是什么关系，处于什么阶段
L4  Episodic Memory   我们共同经历过什么
L5  Semantic Memory   从事件中归纳的稳定认识
L6  Reflection        从不污染核心人格的自我更新
```

**没有任何框架替你定义 L1。那是永月的灵魂，只能你来设计。**

---

## 五、不学清单（省时间）

| 不学 | 理由 |
|------|------|
| C++ | 应用开发岗几乎不要求（算法岗才要） |
| TensorFlow | PyTorch 是主流 |
| 前端框架（Vue/React） | AI 岗极少要求，前端用现成工具（Streamlit/Gradio） |
| 知识图谱 | 289 条中只有 1 条提到 |
| JSP/Servlet | Java 后端早已不这么写 |
| 微服务全套（Spring Cloud） | 刚开始不需要，Spring Boot 单服务够用 |

---

## 六、检查清单

### 面试前必须具备

**基础：**
- [ ] 能独立用 Git 做版本控制（commit/push/branch/PR）
- [ ] 能写 Dockerfile + docker-compose
- [ ] 理解 HTTP 协议（Method/Header/Status Code/Cookie）
- [ ] 能配 Nginx 反向代理
- [ ] 能写 Java Spring Boot 基础 CRUD

**AI：**
- [ ] 能用 LangChain 搭建 RAG 系统
- [ ] 能用 LoRA/QLoRA 微调模型（黑马教）
- [ ] 能搭建 Agent + Tool Calling
- [ ] 能部署 Milvus/Chroma 向量数据库
- [ ] 能讲清楚 2-3 套记忆系统的原理和取舍

**项目：**
- [ ] 今日头条项目能 docker-compose 一键启动
- [ ] 短链服务（Java + Redis）可演示
- [ ] 永月 MVP 能对话 + 有记忆 + 可部署
- [ ] 3 个黑马项目能讲清楚技术选型

---

## 七、每日时间建议

```
每天 6-8 小时（全职学习）：

上午 3h  → 黑马课程（跟大纲走，不要跳）
下午 2h  → 本规划的补课内容（工程线）
下午 2h  → 永月项目开发（项目线）
晚上 1h  → 复习 + Git commit + 写当日学习笔记

周日半天 → 周复盘 + 计划下周
```

---

*本规划是活的——每完成一个阶段复盘调整。不追求完美执行，追求持续向前。*
