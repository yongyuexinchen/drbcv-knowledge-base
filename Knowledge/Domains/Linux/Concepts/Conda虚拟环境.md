---
name: Conda虚拟环境
type: discriminant
status: core
source: "[[计算机基础篇Linux（中）_原文]]"
domain: Linux
---

# Conda虚拟环境

## 类型判定
这是一个概念定义——解释什么是虚拟环境、为什么项目需要独立环境，以及 Conda 如何创建和管理这些隔离空间。

## 类比 ★
### 一句话比喻
你的房子是个大平层，`conda create` 就是在里面用隔板搭出一个独立厨房——你在厨房里炸鱼、炒菜、油烟满天飞，卧室和客厅完全不受影响。每个项目都有自己的「专用厨房」。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 操作系统 | 你的整栋房子 |
| conda 虚拟环境 | 用隔板隔出的独立房间（厨房/书房/健身房） |
| conda create -n 名字 | 请工人隔出一个新房间并挂上门牌 |
| conda activate 名字 | 推门进入这个房间 |
| conda deactivate | 退出房间回到客厅 |
| pip install（在环境内） | 往这个房间里添置锅碗瓢盆 |
| python 版本 | 房间的装修档次（毛坯/简装/精装） |
| 环境隔离 | 厨房的油烟不会飘进卧室 |

## 是什么
Conda 是一个虚拟环境管理工具。它允许在同一台机器上创建多个相互隔离的 Python 运行环境，每个环境有独立的 Python 版本和第三方包。不同项目使用不同环境，互不干扰。

## 正例（≥2 个）
1. 项目A需要 Python 3.8 + TensorFlow 1.x → `conda create -n projA python=3.8`；项目B需要 Python 3.10 + PyTorch 2.0 → `conda create -n projB python=3.10`。两个环境完全隔离。
2. 用 `conda activate myenv` 激活环境后，终端提示符出现 `(myenv)` 前缀，此时执行的 `pip install` 和 `python` 都只影响这个环境。

## 反例/边界（≥1 个）
1. 不在虚拟环境中直接 `pip install` 会把包装到系统全局——A项目和B项目的依赖互相覆盖。就像在客厅里炒菜，整栋房子都是油烟味，最后谁都住不了。

## 详细解释
Python 项目依赖地狱：项目A需要 `numpy==1.19`，项目B需要 `numpy==1.24`——全局只能装一个版本。虚拟环境通过在每个环境里维护独立的 `site-packages` 目录解决了这个问题。

Conda 的核心操作流程：
1. `conda create -n 环境名 python=版本` —— 创建环境
2. `conda activate 环境名` —— 激活（进入）
3. `pip install 包名` —— 在激活的环境内安装依赖
4. `conda deactivate` —— 退出环境

`base` 是 Conda 自带的默认环境，一般不建议在 base 里直接安装项目依赖。

在 AI 项目部署中（如 AutoDL），虚拟环境几乎必用——不同模型框架需要不同版本的 CUDA、PyTorch，隔离是唯一解。

## 关系
### → 指向
- [[Git克隆]]
### ← 被指向
- (无)
