---
name: Pydantic嵌套模型与自定义校验器
type: procedure
status: core
source: "[[请求体传参_原文]] / [[请求体单个传参_原文]]"
domain: FastAPI
---

# Pydantic嵌套模型与自定义校验器

## 类型判定
procedure — 三个进阶技巧：定义嵌套 Pydantic 模型（对象里套对象）→ 写 `@field_validator` 自定义校验逻辑 → 用 `Body()` 逐个接收简单 JSON 字段（不用建模型类）。

## 类比 ★
### 一句话比喻
嵌套 Pydantic 模型就像**快递包裹里的箱中箱**——外层箱子是员工档案，打开里面还有一个地址小盒子，小盒子里又分省、市、县。FastAPI 自动把 JSON 里嵌套的对象层层拆开变成 Python 对象。自定义校验器就像**海关查验**——不是只看箱子外表，而是打开每一项检查：名字不能是"张三"（某些规则禁止）、年龄必须在 18-60 之间。Body() 单个接收则像**寄一个小件**——就两个字段，犯不着用大箱子（模型类），直接用泡沫袋（Body()）就行。

### 生活映射
| 概念世界 | 现实世界 |
|---------|---------|
| 嵌套 Pydantic 模型 | 大箱套小箱——Employee 里面套 Address，Address 里再分省/市/县 |
| `@field_validator("name")` | 海关查验员——专门检查"姓名"这一项是否符合规定 |
| `Field()` 校验（gt, min_length） | 箱子外的标签——"重量不超过 20kg" |
| `Body()` 单个接收 | 寄小件的泡沫袋——两个字段没必要拿大箱子装 |
| 模型作为响应返回 | 把收到的东西原样寄回去——客户传了什么就收到什么 |

## 是什么
**嵌套模型**：Pydantic 模型类的属性可以是另一个 Pydantic 模型类，实现 JSON 嵌套对象的自动解析。**自定义校验器**：用 `@field_validator("字段名")` 装饰器写复杂的校验逻辑（如正则匹配、断言、跨字段联动），超越 Field() 的简单范围限制。**Body() 单个传参**：当请求体 JSON 结构简单（只有几个平级字段），不想建模型类时，用 `Body()` 逐个接收。

## 核心代码

### 嵌套模型
```python
from pydantic import BaseModel, Field
from datetime import date

class Address(BaseModel):
    """地址（嵌套子模型）"""
    province: str = Field(..., description="省份")
    city: str = Field(..., description="城市")
    county: str = Field(default="", description="区县")

class Employee(BaseModel):
    """员工（父模型，包含嵌套子模型）"""
    name: str = Field(..., description="员工名字")
    age: int = Field(..., ge=18, lt=60, description="员工年龄")
    birth: date | None = Field(default=None, description="出生日期")
    address: Address | None = Field(default=None, description="员工详细地址")

@router.post("/emp")
async def create_emp(emp: Employee):    # 嵌套 JSON 自动解析
    return emp                           # 模型可直接作为响应
```

请求 JSON 示例：
```json
{
  "name": "张三",
  "age": 23,
  "birth": "2001-05-20",
  "address": {"province": "湖南省", "city": "长沙市", "county": "长沙县"}
}
```

### 自定义字段校验器
```python
import re
from pydantic import field_validator

class Employee(BaseModel):
    name: str = Field(...)
    age: int = Field(..., ge=18, lt=60)

    @field_validator("name")              # 针对 name 字段的自定义校验
    @classmethod
    def validate_name(cls, value: str) -> str:
        """名字必须以字母或下划线开头，5-15 位"""
        pattern = r"^[a-zA-Z_]\w{5,15}$"
        assert re.match(pattern, value), "名字格式不合法"
        return value
```

### Body() 单个接收（极简传参）
```python
from fastapi import Body

@router.post("/emp/simple")
async def create_emp_simple(
    name: str = Body(..., description="测试姓名"),
    age: int = Body(default=18, description="测试年龄")
):
    return {"name": name, "age": age}
```

## 正例（≥2 个）
1. **用户注册含地址**：用户信息里包含 `address: Address` 嵌套对象（省/市/区 + 详细地址），前端传一个嵌套 JSON，FastAPI 自动拆成 Python 对象。
2. **订单含商品列表**：`Order` 模型里包含 `items: list[OrderItem]`，每个 `OrderItem` 又是一个独立模型。
3. **正则校验用户名**：`@field_validator("username")` 里写正则，要求"以字母开头，只含数字字母下划线，6-16位"。
4. **简单接口不用建模型**：就一个 `keyword: str = Body(...)` 的搜索接口，不需要建 SearchRequest 类。

## 反例/边界（≥1 个）
1. **嵌套模型的必填字段缺了**：`Address` 里 `province` 是必填（`...`），但请求 JSON 的 address 里没写 province → 422 校验失败。
2. **自定义校验器未注册**：写了 `def validate_name` 但忘了加 `@field_validator("name")` 装饰器 → 校验函数永远不会被调用。
3. **Body() 与 Pydantic 模型混用**：同一个处理函数既用了 `emp: Employee`（接收整个 Body），又用了 `name: str = Body(...)`（想单独接收一个字段） → FastAPI 会把整个 Body 给 Employee，`name` 收不到。

## 详细解释
三种请求体接收方式对比：

| 方式 | 适用场景 | 复杂度 |
|------|---------|--------|
| Pydantic 模型（推荐） | 参数多、有嵌套、需要复用 | 中 |
| Pydantic 嵌套模型 | JSON 中有对象嵌套对象 | 高 |
| Body() 逐个接收 | 只有 1-3 个平级字段 | 低 |

`@field_validator` 是 Pydantic v2 的写法（v1 用 `@validator`），返回校验后的值即可。

## 关系
### → 指向
- [[请求体参数与Field注解]] (基础：BaseModel + Field() 定义单层模型)
- [[请求参数校验规则全景]] (Field() 中的 ge/le/min_length 等内置规则)

### ← 被指向
- [[用户注册]] (用户注册接口使用嵌套模型接收注册表单数据)
