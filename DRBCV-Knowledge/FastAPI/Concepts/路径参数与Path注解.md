---
name: 路径参数与Path注解
type: procedure
status: core
source:
  - "[[05-FastAPI基础入门-参数简介和路径参数_原文]]"
  - "[[06-FastAPI基础入门-路径参数_Path类型注解_原文]]"
domain: FastAPI
---

# 路径参数与Path注解

## 类型判定
procedure — 三步标准流程：URL 中用 `{参数名}` 定义 → 处理函数声明同名形参并注解类型 → Path() 添加额外校验。

## 类比 ★
### 一句话比喻
路径参数就像**快递单上的门牌号**——直接写在 URL 路径里，用来定位"唯一的那一个资源"。你要找 3 栋 502 室，`/book/3` 就是 3 栋，`/user/张三` 就是张三家，精确到户，不容含糊。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| `{id}` 占位符 | 快递单上预留的"门牌号"栏位 |
| 同名形参接收 | 快递员按门牌号敲门——URL 里的值自动传入函数 |
| Python 原生类型注解（`int`） | 门牌号必须是数字，不能写"甲单元" |
| Path() 范围限制（`ge=1, le=100`） | 小区只有 1-100 栋，101 栋不存在 → 直接退回 |
| Path() description | 门牌号旁边贴的说明标签——方便同事理解 |

## 是什么
路径参数是出现在 **URL 路径中的动态部分**，用于指向唯一的特定资源（如某本书、某个用户）。FastAPI 通过 `{参数名}` 语法在路由中定义，处理函数通过同名形参接收，配合 `Path()` 函数可添加范围、长度、描述等进阶校验。

## 输入-输出空间
- **输入**：URL 路径中的动态值（如 `/book/666` 中的 `666`）
- **输出**：处理函数中同名形参的值（自动类型转换）
- **前置条件**：`from fastapi import Path`

## 核心代码
```python
from fastapi import FastAPI, Path

app = FastAPI()

# 基础路径参数：只限制类型
@app.get("/book/{id}")
async def get_book(id: int):                    # 原生类型注解
    return {"id": id, "title": f"这是第{id}本书"}

# Path() 进阶注解：范围限制 + 描述
@app.get("/book2/{id}")
async def get_book2(
    id: int = Path(..., ge=1, le=100, description="书籍ID，取值范围1-100")
):
    return {"id": id, "title": f"这是第{id}本书"}

# 字符串路径参数：长度限制
@app.get("/author/{name}")
async def get_author(
    name: str = Path(..., min_length=2, max_length=10, description="作者姓名")
):
    return {"msg": f"这是{name}的信息"}
```

| 步骤 | 代码 | 说明 |
|------|------|------|
| ① URL 定义占位符 | `"/book/{id}"` | 大括号声明路径参数，名字自定义 |
| ② 处理函数同名形参 | `id: int` | 形参名必须与 URL 中的 `{id}` 完全一致 |
| ③ Python 原生类型注解 | `id: int` | 限制类型，FastAPI 自动做类型转换 |
| ④ Path() 进阶校验 | `id: int = Path(..., ge=1, le=100)` | `...`=必填，`ge`/`le`=范围，`min_length`/`max_length`=长度 |
| ⑤ 添加描述 | `description="..."` | 显示在 Swagger 文档中，方便联调 |

## 正例（≥2 个）
1. **查询指定图书**：`GET /book/5` → 返回 ID 为 5 的图书信息。URL 直接体现资源标识。
2. **查询用户信息**：`GET /user/zhangsan` → 返回用户名 zhangsan 的详细信息。人名作为路径参数直观易懂。
3. **新闻分类 ID 校验**：`GET /category/{id}` — 用 `Path(ge=1, le=100)` 限制分类 ID 范围，防止越界。

## 反例/边界（≥1 个）
1. **不传路径参数**：访问 `/book/` 而非 `/book/666` → 报错 `field required`，路径参数默认必填。
2. **类型不匹配**：路径参数注解为 `int`，但传入 `/book/abc` → FastAPI 返回 422 校验错误。
3. **范围越界**：`Path(ge=1, le=100)` 限制下传入 `id=101` → 报错 "less than or equal to 100"。
4. **字符串长度越界**：`min_length=2` 限制下传入单字 `"张"` → 报错 "ensure this value has at least 2 characters"。

## 详细解释
**路径参数 vs 查询参数的选择**：
- **路径参数**：指向"哪一个"——资源标识。如 `/book/5` 指第 5 本书，是 URL 结构的一部分。
- **查询参数**：描述"怎么选"——筛选条件。如 `/books?category=python` 过滤结果。

Path() 常用参数速查：
| 参数 | 含义 | 示例 |
|-----|------|------|
| `...` | 必填 | `Path(...)` |
| `gt` / `ge` | 大于 / 大于等于 | `ge=1` |
| `lt` / `le` | 小于 / 小于等于 | `le=100` |
| `min_length` / `max_length` | 最小/最大长度（字符串） | `min_length=2` |
| `description` | 参数描述（显示在文档中） | `description="书籍ID"` |

## 关系
### → 指向
- [[查询参数与Query注解]] (同级概念：路径参数 vs 查询参数)
- [[FastAPI路由]] (路径参数定义在路由的 URL 中)
- [[异常响应处理]] (校验失败时抛出 422 错误)

### ← 被指向
- [[FastAPI路由]] (路由是路径参数的宿主)
- [[响应类型]] (路径参数常用于 GET 请求返回资源)
