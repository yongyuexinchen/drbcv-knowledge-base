---
title: "Docker在AI开发中的作用"
type: "概念"
category: "Learning-Path"
tags: [Docker, 容器化, 部署, 环境管理]
created: 2026-07-27
---

# Docker在AI开发中的作用

## 是什么（What）

Docker 是 AI 应用开发的"环境打包机" — 把你的应用和所有依赖（Python版本、库、系统工具）打包成一个镜像，在任何机器上都能跑。在 AI 开发中，Docker 有三个核心用途：隔离环境、一键部署、团队协作。

这就像外卖打包：你在厨房做好菜（写完代码），装进密封餐盒（Docker镜像），骑手送到任何地方打开都是一样的味道。不用担心"客人的厨房有没有辣椒"（服务器有没有同一个Python版本）。

## 为什么重要（Why）

- Docker 是学习路线优化后的**第1步**（原路线的第一步也是对的）
- 26%的深圳AI岗位JD要求 Docker，覆盖率不高但**所有部署相关的岗位都要**
- 用户正在学 Docker，方向正确，但需要压缩到1周（够用即可），不要过度深入
- Docker Compose 多容器编排比单容器更有价值 — 实际项目都是多服务（FastAPI + PostgreSQL + Redis）

## 怎么做（How）

### AI开发中的 Docker 使用场景

```bash
# 场景1：本地开发环境隔离
# Dockerfile — 定义你的开发环境
FROM python:3.11-slim
RUN pip install fastapi uvicorn langchain chromadb
COPY . /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 场景2：多服务编排
# docker-compose.yml — 同时启动 FastAPI + ChromaDB
version: '3'
services:
  api:
    build: .
    ports: ["8000:8000"]
  chromadb:
    image: chromadb/chroma
    ports: ["8001:8000"]

# 场景3：面试现场演示
# docker-compose up → 面试官浏览器打开即可体验你的项目
```

### 学习范围（1周够用）

```
必学（Day 1-2）:
  Dockerfile 编写、镜像构建、容器运行、端口映射、卷挂载

必学（Day 3-4）:
  Docker Compose 多容器编排、环境变量、网络通信

够用即可（不用深入）:
  Docker Swarm / K8s 集群（面试问到能说概念即可）
  多阶段构建、镜像优化（入行后再学）
```

## 与其他卡片的关系

- [[AI应用开发-12周学习路线图]] → Docker在第1周完成
- [[AI应用开发-必备技能清单]] → Docker在技能清单中的位置（26%覆盖率）
- [[AI应用开发-3个月求职策略]] → 简历上写Docker经验的策略

## 个人见解（留空待填）

<!-- Docker学习进度如何？卡在哪里了？对容器化的概念理解了吗？ -->

## 信息来源

- 来自研究：2026-07-27 AI-job-and-path → C_learning_path/03_gap_analysis.md + 04_optimized_roadmap.md
