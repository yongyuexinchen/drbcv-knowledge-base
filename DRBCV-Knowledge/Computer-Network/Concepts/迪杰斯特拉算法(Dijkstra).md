---
name: 迪杰斯特拉算法(Dijkstra)
type: stub
status: core
source: "[[Dijkstra算法]]"
domain: computer-network
---

# 迪杰斯特拉算法（Dijkstra）

> **↳ 主卡片见数据结构：** `Data-Structures/Concepts/Dijkstra算法.md`

## 在计算机网络中的作用

Dijkstra 是 **链路状态路由算法（OSPF）** 的核心引擎。每台路由器收集全网 LSA 构建 LSDB（图的邻接表）后，以自己为源点运行 Dijkstra，算出到每个目的网络的最短路径。

## 连接到

- [[OSPF工作原理]] — OSPF 的步骤⑤即运行 Dijkstra
- [[距离向量vs链路状态对比]] — Dijkstra vs Bellman-Ford
- [[路由算法分类]] — 链路状态路由的数学基础

## 关系
### → 指向
- [[OSPF工作原理]]
- [[距离向量vs链路状态对比]]
- [[路由算法分类]]
