---
name: ORM分页查询
type: procedure
status: core
source: "[[24-FastAPI进阶-ORM操作数据-分页查询_原文]]"
domain: FastAPI
---

# ORM分页查询

## 类型判定
procedure — 核心是一个公式 + 一条 SQLAlchemy 查询语句，有明确的输入输出和计算步骤。

## 类比 ★
### 一句话比喻
分页查询就像翻一本 600 页的字典查"python"——你不会从第 1 页开始逐页翻，而是直接跳到你估算的位置。`offset` 就是你跳过的页数（前面所有页），`limit` 是你在当前页能看到的条目数。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| offset（跳过） | 翻字典时左手按住已翻过的厚度——那些页不看了 |
| limit（每页条数） | 当前页你能看到的词条数——一页 20 个词 |
| page（页码） | 你要翻到字典的第几页 |
| `(page-1) × limit` | 手指估算要跳过多少页的公式 |

## 是什么
分页查询是 ORM 中按页码和每页条数分段返回数据的技术。核心公式：**跳过的记录数 = (当前页码 - 1) × 每页条数**。SQLAlchemy 中用 `.offset(skip).limit(page_size)` 实现。

## 输入-输出空间（程序型必填）
- **输入**：
  - `page: int` — 用户要第几页（默认 1）
  - `page_size: int` — 每页显示多少条（默认 10）
- **输出**：当前页的数据列表（如 `List[Book]`）
- **前置条件**：已有数据库连接（依赖注入了 DB session）

## 核心代码
```python
@app.get("/books/")
async def get_books(page: int = 1, page_size: int = 10, db = Depends(get_db)):
    skip = (page - 1) * page_size               # ← 核心公式
    stmt = select(Book).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① 接收参数 | `page`, `page_size` | 用户指定页码和每页条数 |
| ② 计算跳过 | `skip = (page-1) × page_size` | 前面所有页的数据量 |
| ③ 构建查询 | `select(Model).offset(skip).limit(page_size)` | ORM 链式调用 |
| ④ 执行 | `await db.execute(stmt)` | 异步执行 |
| ⑤ 提取结果 | `result.scalars().all()` | 返回 ORM 对象列表 |

## 正例（≥2 个）
1. **新闻列表**：数据库有 6000 条新闻，用户请求第 3 页，每页 20 条 → `skip = (3-1)×20 = 40`，跳过前 40 条，返回第 41-60 条。
2. **用户收藏列表**：用户收藏了 150 篇文章，前端传 `page=1, page_size=15` → `skip=0`，返回前 15 条。

## 反例/边界（≥1 个）
1. **page=0 或负数**：`skip = (0-1)×10 = -10`，SQL 会报错或返回空结果——需要用 `Query(ge=1)` 限制页码 ≥1。
2. **page_size 过大**：用户传 `page_size=100000`，一次查 10 万条——内存爆炸。用 `Query(le=100)` 限制每页最多 100 条。
3. **最后一页不足**：共 23 条数据，`page_size=10`，第 3 页只有 3 条——这是正常的，不需要特殊处理。

## 详细解释
`offset` 和 `limit` 底层对应 SQL 的 `LIMIT ... OFFSET ...`：
```sql
SELECT * FROM books LIMIT 10 OFFSET 20;  -- 跳过20条，取10条
```
ORM 版本就是链式调用：`select(Book).offset(20).limit(10)`。

**为什么 skip 公式是 `(page-1) × page_size`？**
- 第 1 页：要第 1-10 条 → 跳过 0 条 → `(1-1)×10 = 0` ✓
- 第 2 页：要第 11-20 条 → 跳过 10 条 → `(2-1)×10 = 10` ✓
- 第 3 页：要第 21-30 条 → 跳过 20 条 → `(3-1)×10 = 20` ✓

## 关系
### → 指向
- [[ORM查询数据]] (分页查询是查询的子集)
- [[查询参数]] (page 和 page_size 是查询参数)
- [[ORM新增数据]] (新增后列表需要刷新分页)

### ← 被指向
- [[ORM查询总结]] (分页是五种查询模式之一)
