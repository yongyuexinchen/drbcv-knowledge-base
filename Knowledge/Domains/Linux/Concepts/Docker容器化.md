---
name: Docker容器化
type: discriminant
status: core
source: "[[计算机基础篇：Linux（下）_原文]]"
domain: Linux
---

# Docker容器化

## 类型判定
这是一个概念定义——解释 Docker 是什么、它解决什么问题，以及容器、镜像、服务、Docker Compose 之间的层级关系。

## 类比 ★
### 一句话比喻
Docker 就是把你的精装房整个塞进一辆房车里——不管开到海边、山顶还是沙漠，下车就是你的家，一切和原来一模一样。Docker Compose 则是一个车队：厨房车、卫生间车、卧室车各司其职，浩浩荡荡一起出发。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| Docker 镜像（Image） | 房车的设计图纸（不可变） |
| Docker 容器（Container） | 按图纸造出来的、正在跑的房车 |
| 一个容器 | 一辆房车（装着你的厨房） |
| Docker Compose 服务（Service） | 一种类型的车（厨房车队有5辆） |
| docker-compose.yml | 车队的调度手册 |
| docker ps | 查看哪些房车正在被使用 |
| docker images | 车库里所有房车的清单（不管用没用） |
| docker run | 启动一辆新房车 |
| docker stop | 让一辆房车熄火 |
| docker rm | 把一辆房车报废处理 |

## 是什么
Docker 是一个容器化平台。它把应用程序及其所有依赖打包成一个轻量级、可移植的「容器」，可以在任何安装了 Docker 的机器上一致运行。它类似于虚拟机但更轻量——只包含运行应用所需的必要组件，不模拟完整操作系统。

## 正例（≥2 个）
1. 在自己的 Windows 电脑上开发了一个 Python Web 应用 → 用 Docker 打包成镜像 → 复制到阿里云 Linux 服务器上 `docker run`，一行命令就跑起来了，不需要重装任何依赖。
2. 一个项目需要 MySQL + Redis + Nginx + Python 后端 → 写一个 `docker-compose.yml` 定义4个服务 → `docker compose up -d`，四个容器同时启动。

## 反例/边界（≥1 个）
1. Docker 不是虚拟机。虚拟机有完整操作系统内核，启动慢、占用大。Docker 共享宿主机内核，启动秒级、体积小，但隔离性不如虚拟机——它不是用来「跑另一个操作系统」的，是用来「跑应用」的。

## 详细解释
Docker 解决了「在我电脑上能跑，到你电脑上就报错」的经典问题。根本原因：不同机器的操作系统版本、Python 版本、依赖库版本不一致。Docker 把应用和它的环境打包在一起，确保在任何地方行为一致。

核心概念层级：
- **镜像（Image）**：只读模板，如 `ubuntu:22.04`、`python:3.10`
- **容器（Container）**：镜像的运行实例，可启动、停止、删除
- **Dockerfile**：构建镜像的指令文件
- **Docker Compose**：管理多容器应用的工具，通过 YAML 文件定义所有服务
- **服务（Service）**：Compose 中的概念，一个服务可运行多个容器副本

常用指令对比：
| 指令 | 作用 |
|------|------|
| `docker ps` | 列出正在运行的容器 |
| `docker ps -a` | 列出所有容器（含已停止） |
| `docker images` | 列出所有镜像 |
| `docker run 镜像` | 创建并启动新容器 |
| `docker start/stop 容器名` | 启动/停止已有容器 |
| `docker rm 容器名` | 删除容器 |
| `docker compose up -d` | 后台启动 Compose 所有服务 |
| `docker compose down` | 停止并删除 Compose 所有服务 |

## 关系
### → 指向
- [[SSH远程登录]]
### ← 被指向
- (无)
