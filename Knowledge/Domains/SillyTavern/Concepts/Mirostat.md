---
name: Mirostat
type: connection
status: unexplored
source: [[知乎-酒馆EP05-预设指南]]
---

# ⬜ Mirostat

## 类型判定
**连接型** — 输入目标复杂度→自适应调整Temperature→保持输出复杂度稳定

## 是什么
自适应Temperature算法。不同于固定Temperature值，Mirostat根据目标"困惑度"（Perplexity）动态调整每一步的Temperature，自动保持输出复杂度在目标区间。

## 输入-输出空间
- **输入**: 目标困惑度（通常2-5）
- **输出**: 每一步动态调整的Temperature值
- **映射关系**: 实际复杂度偏离目标→自动调整Temperature

## 正例
1. **场景A**: 固定Temperature=0.9→有些轮太保守有些轮太发散。Mirostat目标=3.5→每轮自动调整，输出复杂度始终稳定。
2. **场景B**: 创意写作→设Mirostat目标=5（高复杂度），Mirostat自动维持高创意输出。

## 反例/边界
1. **常见误解**: Mirostat不是"替代Temperature"——是在Temperature基础上的自适应层。可以和手动Temperature共存。
2. **边界**: Mirostat是进阶功能，新手先掌握固定Temperature调参。理解采样原理后再用Mirostat事半功倍。

## 详细解释
Mirostat由Basu等人在2021年提出。核心创新：不再手动设Temperature，而是设"想要的输出复杂度"，算法自动维持。优势：避免手动调参的"试错循环"，长对话中保持输出质量稳定。酒馆中作为高级采样选项。


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系

### ← 被指向
- [[预设参数(Preset)]] (进阶功能)
- [[Temperature(温度)]] (自适应替代)
