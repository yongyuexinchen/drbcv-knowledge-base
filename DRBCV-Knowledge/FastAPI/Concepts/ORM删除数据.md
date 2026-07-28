---
name: ORM删除数据
type: procedure
status: core
source: "[[28-FastAPI进阶-ORM操作数据-删除数据_原文]]"
domain: FastAPI
---

# ORM删除数据

## 类型判定
procedure — 与更新同模式：先查 → 找到则 `db.delete()` → `commit`。找不到抛 404。

## 类比 ★
### 一句话比喻
ORM 删除数据就像注销银行卡——你不能凭空说"把卡号 8888 的卡注销了"，必须先出示身份证和卡（`db.get` 查找确认这张卡存在且是你的），然后填写销户申请（`db.delete()`），最后柜员确认销毁（`db.commit()`）。如果卡号不存在——柜员会告诉你"查无此卡"。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| `db.get(Model, id)` | 出示身份证 + 银行卡——确认你要销的是这张卡 |
| `is None` → 抛 404 | 柜员查系统："先生，这个卡号不存在" |
| `db.delete(obj)` | 填写销户申请表——标记为待删除 |
| `db.commit()` | 柜员盖章确认——卡被正式注销 |

## 是什么
删除数据遵循"先查后删再提交"的黄金流程。通过路径参数拿到要删除的记录 ID → 用 `get` 查出 ORM 对象 → `db.delete()` 标记删除 → `commit` 提交。找不到则抛 HTTP 404。

## 输入-输出空间（程序型必填）
- **输入**：路径参数：要删除的记录 ID（主键）
- **输出**：成功/失败消息（通常不返回被删数据）
- **前置条件**：已注入 DB session

## 三步法
```
第一步：先查
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")

第二步：删除
    await db.delete(db_book)    # 标记为待删除

第三步：提交
    await db.commit()            # 真正从数据库删除
    return {"message": "删除成功"}
```

## 核心代码
```python
from fastapi import HTTPException

@app.delete("/books/{book_id}")
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    # ① 先查
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="查无此书")

    # ② 删除
    await db.delete(db_book)

    # ③ 提交
    await db.commit()
    return {"message": "删除图书成功"}
```

### 删除 vs 更新 —— 同模板对比
```python
# 更新模板（PUT）
db_obj = await db.get(Model, id)      # ① 查
if not db_obj: raise 404
db_obj.field = new_value              # ② 改（赋值）
await db.commit()                     # ③ 提交

# 删除模板（DELETE）
db_obj = await db.get(Model, id)      # ① 查（完全一样）
if not db_obj: raise 404
await db.delete(db_obj)               # ② 删（调 delete 方法）
await db.commit()                     # ③ 提交（完全一样）
```
两步相同的（查 + 提交），只有中间操作不同（改 vs 删）。

## 正例（≥2 个）
1. **取消收藏**：用户点"取消收藏"按钮，`DELETE /favorites/{news_id}`——查出收藏记录，`db.delete()`，提交——记录消失。
2. **后台批量删除**：管理员勾选 10 条违规评论，循环查出每条 → `db.delete()` → 一次性 `commit`——10 条在一个事务中删除，要么全删要么全不删。
3. **软删除**：不真删，而是 `obj.is_deleted = True` 然后 `commit`——数据还在，只是前端不展示。适合需要审计追溯的业务。

## 反例/边界（≥1 个）
1. **假删除（只调 delete 不调 commit）**：对象在会话中被标记删除，但数据库里还在——关掉程序再开，数据又"复活"了。
2. **删除不存在的 ID**：用户传 `book_id=99999`——`get` 返回 `None`，应该抛 404 而不是静默返回"删除成功"（误导用户）。
3. **级联删除没配置**：Book 表被 Order 表外键引用，直接 `delete(book)` 会报外键约束错误——需要先在模型类设置 `cascade="all, delete-orphan"` 或手动先删关联数据。

## 详细解释
### `db.delete()` 的内部机制
```python
await db.delete(db_book)
# SQLAlchemy 内部做的事：
# 1. 检查该对象是否在当前会话中
# 2. 标记为 'deleted' 状态
# 3. commit 时生成 DELETE SQL：
#    DELETE FROM book WHERE id = 7;
```
和更新一样，你必须删除查出来的"活对象"——新构造的 `Book(id=7)` 不在会话中，`delete` 无效。

### 为什么更新和删除都需要"先查"？
1. **保证对象存在于会话中**（SQLAlchemy 身份映射机制）
2. **验证数据存在**——不存在的 ID 提前拦截，避免无效操作
3. **提供清晰的错误信息**——用户知道是"没找到"而不是"操作失败"

## 关系
### → 指向
- [[ORM更新数据]] (同模板：先查再操作再提交)
- [[ORM查询总结]] (删除前必须查询)
- [[HTTP异常处理]] (找不到资源抛 404)

### ← 被指向
- [[ORM总结]] (增删改查四大操作之一)
