---
name: 用定积分定义求 N 项和数列极限
status: unexplored
type: 程序型
source: [[Calculus]]
---

# 用定积分定义求 N 项和数列极限

## 类型判定
程序型 — 给出明确的操作步骤或解题方法

## 是什么
N 项和数列极限 $\lim_{n\to\infty} \sum_{i=1}^n \frac{1}{n} f(\frac{i}{n}) = \int_0^1 f(x) \, dx$。若 $f$ 内变量为 $a+\frac{i}{n}$，则积分区间为 $[a, a+1]$。

步骤：(1) 用求和符号整合；(2) 提出 $\frac{1}{n}$，将剩余部分凑成 $f(\frac{i}{n})$ 形式；(3) $\frac{1}{n} \to dx$，$\frac{i}{n} \to x$，求和取极限 $\to$ 积分 $\int_0^1 f(x)\,dx$。

## 输入-输出空间
- **输入**: $n$ 项和的数列极限表达式
- **输出**: 等价的一个定积分 $\int_a^b f(x) dx$
- **映射关系**: $\frac{1}{n} \to dx$，$\frac{i}{n} \to x$，$\sum \to \int$

## 正例（至少2个）
1. **场景1**: $\lim_{n\to\infty} \frac{1}{n^2}\sum_{i=1}^n \sqrt{n^2 - i^2} = \lim_{n\to\infty} \frac{1}{n}\sum_{i=1}^n \sqrt{1 - (\frac{i}{n})^2} = \int_0^1 \sqrt{1-x^2} \, dx = \frac{\pi}{4}$
2. **场景2**: $\lim_{n\to\infty} \sum_{i=1}^n \frac{n}{n^2 + i^2} = \lim_{n\to\infty} \frac{1}{n}\sum_{i=1}^n \frac{1}{1+(i/n)^2} = \int_0^1 \frac{1}{1+x^2} dx = \frac{\pi}{4}$

## 反例/边界（至少1个）
1. **常见误解/边界**: 并非所有 $n$ 项和都能转化为定积分。关键条件是能在和中提出公因子 $\frac{1}{n}$，且剩余部分能写成 $f(\frac{i}{n})$ 的形式。若变化部分 $i$ 的阶数比 $n$ 低一次（如 $\sum_{i=1}^n \frac{1}{n^2} \sin \frac{i}{n}$），求和部分不足以产生 $\frac{1}{n}$ 因子，需用夹逼准则而非定积分定义。另一边界：若 $\frac{i}{n}$ 写成 $a + \frac{k}{n}$ 形式，积分区间需要对应调整为 $[a, a+1]$ 或由起点和终点确定。

## 详细解释
若求和项中 $i$ 的变化次数比 $n$ 低一次，往往考虑夹逼准则而非定积分定义。

### 推导过程（★ 数学卡必须）
定积分定义的等分形式：将 $[0,1]$ 等分成 $n$ 份，每份长度 $\Delta x_i = \frac{1}{n}$，取右端点 $\xi_i = \frac{i}{n}$。

$$\int_0^1 f(x) dx = \lim_{n\to\infty} \sum_{i=1}^n f\left(\frac{i}{n}\right) \cdot \frac{1}{n}$$

这就是将 $n$ 项和极限转化为定积分的核心公式。

**推广到一般区间 $[a,b]$**：$\Delta x_i = \frac{b-a}{n}$，$\xi_i = a + \frac{i(b-a)}{n}$

$$\int_a^b f(x) dx = \lim_{n\to\infty} \frac{b-a}{n} \sum_{i=1}^n f\left(a + \frac{i(b-a)}{n}\right)$$

**对应关系记忆技巧**：
- $\frac{1}{n}$（或 $\frac{b-a}{n}$）$\leftrightarrow dx$
- $\frac{i}{n}$（或 $a + \frac{i(b-a)}{n}$）$\leftrightarrow x$
- $\sum_{i=1}^n \leftrightarrow \int_0^1$（或 $\int_a^b$）
- $\lim_{n\to\infty} \leftrightarrow$ 取极限即积分

### 重要推论（★ 数学卡必须）
1. **识别标志**：极限中含有 $\sum_{i=1}^n$ 且 $i$ 与 $n$ 的幂次相同（如 $\frac{i}{n}$、$\frac{i^2}{n^2}$），是使用此方法的标志。
2. **三步走流程**：
   - **提**：从和中提取 $\frac{1}{n}$ 因子
   - **凑**：将剩余部分凑成 $f(\frac{i}{n})$ 形式
   - **化**：转化为定积分 $\int_0^1 f(x) dx$ 并计算
3. **区间推广**：若凑出 $f(a+\frac{i(b-a)}{n})$ 的形式，积分区间为 $[a,b]$，积分前还要乘上 $(b-a)$。
4. **与夹逼准则的分工**：若 $i$ 的次数低于 $n$，和式整体量级太小，无法凑出 $\frac{1}{n}$，改用夹逼准则。

## 经典例题（★ 至少2题，含完整解答）
**例题1**
**题目**：$\lim_{n\to\infty} \frac{1}{n^2}\sum_{i=1}^n \sqrt{n^2 - i^2}$

**解**：提取因子 $\frac{1}{n}$：

$$\lim_{n\to\infty} \frac{1}{n^2}\sum_{i=1}^n \sqrt{n^2 - i^2} = \lim_{n\to\infty} \frac{1}{n} \sum_{i=1}^n \sqrt{\frac{n^2-i^2}{n^2}}$$

$$= \lim_{n\to\infty} \frac{1}{n} \sum_{i=1}^n \sqrt{1 - \left(\frac{i}{n}\right)^2}$$

识别：$\frac{1}{n} \to dx$，$\frac{i}{n} \to x$，故极限等于：

$$\int_0^1 \sqrt{1-x^2} \, dx$$

这是单位圆第一象限的面积，等于 $\frac{\pi}{4}$。

（也可用三角换元验证：令 $x = \sin t$）

**例题2**
**题目**：$\lim_{n\to\infty} \sum_{i=1}^n \frac{n}{n^2 + i^2}$

**解**：提取 $\frac{1}{n}$：

$$\lim_{n\to\infty} \sum_{i=1}^n \frac{n}{n^2 + i^2} = \lim_{n\to\infty} \frac{1}{n} \sum_{i=1}^n \frac{n^2}{n^2 + i^2}$$

$$= \lim_{n\to\infty} \frac{1}{n} \sum_{i=1}^n \frac{1}{1 + (\frac{i}{n})^2}$$

识别：$f(x) = \frac{1}{1+x^2}$，$\int_0^1 f(x)dx = \int_0^1 \frac{1}{1+x^2} dx$

$$= [\arctan x]_0^1 = \frac{\pi}{4}$$

## 类比

### 一句话比喻
用定积分定义求极限就像慢放电影——把连续过程（积分）拆成一帧一帧的离散画面（求和），当帧数趋近无穷时，离散画面重新变成连续的影片。

### 物理映射
| 数学对象 | 物理类比 |
|---------|---------|
| $\frac{1}{n}$ | 每帧的时间间隔 |
| $\frac{i}{n}$ | 第 $i$ 个采样的时间点 |
| $f(\frac{i}{n})$ | 该时刻的瞬时采样值 |
| $\sum f(\frac{i}{n})\frac{1}{n}$ | 离散采样的累积量 |
| $\int_0^1 f(x)dx$ | 连续过程的精确总量 |


## 个人见解
（留空，自行填写学习心得、记忆技巧、踩坑记录等）

## 关系（★ 必须用 [[wikilink]] 双向链接）

### 由...推导而来（依赖）
- [[黎曼和]] (N 项和的极限就是黎曼和的极限)
- [[定积分的定义]] (定积分定义中取等分分割的特例)
- [[数列极限（ε-N定义）]] (N 项和极限的严格定义基础)

### 可推导出
- [[夹逼准则]] (有些 N 项和极限不适用积分定义，需用夹逼准则)

### 属于 / 组成 / 应用
- [[Calculus]] (微积分体系)
