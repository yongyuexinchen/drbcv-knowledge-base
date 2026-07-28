---
name: KMP算法的优化_nextval
type: procedure
status: core
source: "[[037 4.2.3_KMP算法的进一步优化_原文]]"
domain: 数据结构
---

# KMP 算法的优化 —— nextval 数组

## 类型判定
程序型 — 对 KMP 算法中 next 数组的进一步优化。`derives` [[KMP算法]]，将必然失败的跳转短路掉，进一步提升匹配效率。KMP 主算法逻辑不变，仅将 `next` 替换为 `nextval`。

## 是什么
在 KMP 算法中，当 `T[j]` 失配时，`j = next[j]`。但如果 `T[next[j]] == T[j]`，则下一次匹配**注定失败**——因为主串该位置的字符已经确定 ≠ `T[j]`，自然也不等于相同的 `T[next[j]]`。nextval 数组就是把这个「注定失败」的跳转直接短路，让 `j` 一次性跳到最终有效的位置。

## 输入-输出空间
- **输入**：模式串 T 的 next 数组
- **输出**：优化后的 nextval 数组
- **前置条件**：已按手算法求出 next 数组

## 正例（≥2 个）
1. **T="AAAAB", next=[0,1,2,3,4] → nextval=[0,0,0,0,4]**：当 j=4（'A'）失配时，next[4]=3 而 T[3] 也是 'A' → 必然再失配 → 直接 nextval[4]=nextval[3]=0，跳过所有连续的 A
2. **T="ABAABC", next=[0,1,1,2,3,4]**：nextval[3]=0（T[3]=A, T[1]=A 相同 → 短路），nextval[5]=1（T[5]=B, T[2]=B 相同 → 短路），nextval[6]=4（T[6]=C, T[4]=A 不同 → 保持）

## 反例/边界（≥1 个）
1. **T="ABCDEF"**：没有任何重复字符 → 每个 `T[next[j]] ≠ T[j]` → nextval 与 next 完全相同，优化无效（但也没坏处）
2. **nextval[1] 固定为 0**：与 next[1]=0 一致，没有进一步优化的空间

## 详细解释

### 为什么 next 有冗余？
回顾 KMP 失配处理：`S.ch[i]` 已经 ≠ `T[j]`（因为失配了）。
如果 `T[j] == T[next[j]]`，那么 `S.ch[i]` 也必然 ≠ `T[next[j]]` → 这次匹配**注定失败**。

所以与其 `j → next[j] → 发现又失败 → next[next[j]]`（两步），不如直接 `j → next[next[j]]`（一步）。

### nextval 手算方法

**两步法**：
1. 先用手算法求出 next 数组
2. 按公式求 nextval：
   - `nextval[1] = 0`（固定）
   - 对 $j \ge 2$：
     - 若 `T[j] == T[next[j]]` → `nextval[j] = nextval[next[j]]`（短路！）
     - 若 `T[j] != T[next[j]]` → `nextval[j] = next[j]`（保持原值）

### 手算示例

#### 示例 1：T = "ABABAA"
```
j:       1  2  3  4  5  6
T:       A  B  A  B  A  A
next:    0  1  1  2  3  4
```

| j | T[j] | next[j] | T[next[j]] | 相等? | nextval[j] |
|---|------|---------|-----------|-------|------------|
| 1 | A | 0 | — | — | **0**（固定） |
| 2 | B | 1 | A | ≠ | **1** |
| 3 | A | 1 | A | = | nextval[1] = **0** |
| 4 | B | 2 | B | = | nextval[2] = **1** |
| 5 | A | 3 | A | = | nextval[3] = **0** |
| 6 | A | 4 | B | ≠ | **4** |

**结果**：`nextval = [0, 1, 0, 1, 0, 4]`

#### 示例 2：T = "AAAAB"
```
j:       1  2  3  4  5
T:       A  A  A  A  B
next:    0  1  2  3  4
```

| j | T[j] | next[j] | T[next[j]] | 相等? | nextval[j] |
|---|------|---------|-----------|-------|------------|
| 1 | A | 0 | — | — | **0** |
| 2 | A | 1 | A | = | nextval[1] = **0** |
| 3 | A | 2 | A | = | nextval[2] = **0** |
| 4 | A | 3 | A | = | nextval[3] = **0** |
| 5 | B | 4 | A | ≠ | **4** |

**结果**：`nextval = [0, 0, 0, 0, 4]`

### 性能对比：next vs nextval

用 `T="AAAAB"` 匹配 `S="AAAAAAAAB"`：

**用 next = [0,1,2,3,4]**：
```
j=4 失配 → next[4]=3 → 失配（因为 S.ch[i]≠'A'）
          → next[3]=2 → 失配
          → next[2]=1 → 失配
          → next[1]=0 → i++,j++
```
共 4 次无效跳转。

**用 nextval = [0,0,0,0,4]**：
```
j=4 失配 → nextval[4]=0 → i++,j++
```
一步到位！跳过 3 次必定失败的对比。

### KMP 使用 nextval 的代码
**与原来完全相同**，只需把 `next` 数组参数换成 `nextval`：
```c
int Index_KMP(SString S, SString T, int nextval[]) {
    int i = 1, j = 1;
    while (i <= S.length && j <= T.length) {
        if (j == 0 || S.ch[i] == T.ch[j]) {
            i++; j++;
        } else {
            j = nextval[j];  // 唯一变化：用 nextval 替代 next
        }
    }
    if (j > T.length) return i - T.length;
    else return 0;
}
```

## 类比

### 一句话比喻
**nextval 优化就像快递路线规划——next 数组说「先去 A 站→再去 B 站→再去 C 站」，但 nextval 看了一眼发现「A 站 B 站都没你要的包裹，直接去 C 站！」——把中间的注定白跑一趟的站点全短路掉。**

### 生活映射
| 代码世界 | 快递配送现场 |
|---|---|
| next 数组 | 快递公司的默认配送路线：「按顺序去 1→2→3→4 号柜」 |
| nextval 数组 | 老司机的优化路线：「2 号柜和 3 号柜都没你的包裹，直接去 4 号」 |
| `T[j] == T[next[j]]` | 「这个快递柜和上一个装的是一模一样的东西——这站白跑，跳过！」 |
| `T[j] != T[next[j]]` | 「这个柜子装的东西不一样，有可能有你的包裹，还是去看看吧」 |
| nextval[1]=0 | 起点站——没有任何前置可跳过 |
| 短路 | 「我知道去了也白去，干脆省点油」 |

## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系
### → 指向
（无直接后继——这是 KMP 算法的终点优化形态）

### ← 被指向
- [[KMP算法]] (nextval 是 next 的优化版本)
- [[串]] (串的 Index 操作的终极实现)
